from collections import defaultdict
import random
import math
import pickle
import os

class AgentWalker():
    """
    AgentWalker class, learns through the use of a Q-table,
    the best next move he could apply.
    """
    def __init__(self, x, y, color, name, width, height, grid_size, exploration_rate, discount_factor, learning_rate):
        # classic attributes of the agent
        self.x = x
        self.y = y
        self.color = color
        self.positions = []
        self.name = name
        self.width = width
        self.height = height
        self.hit_boundary = False

        # managing agents Q table
        self.grid_size = grid_size
        self.q_table = defaultdict(lambda: defaultdict(lambda: 0))
        self.exploration_rate = exploration_rate
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate

        # possible movements of agents
        self.actions = [(0, -1), (1, 0), (0, 1), (-1, 0), 
                         (1, -1), (1, 1), (-1, 1), (-1, -1)]
        
        # rewards history
        self.current_reward = 0
        self.rewards_history = []
        self.steps_history = []

    def check_boundaries(self, WIDTH, HEIGHT):
        """
        Check if agent is between the boundaries of the map, if not clamps the agent back in the possible space.
        Also returns a bool, if boundaries are hit we compute a penalty for the agent.
        """

        hit_boundary = False

        if self.x < 0:
            self.x = 0
            hit_boundary = True
        if self.x > WIDTH:
            self.x = WIDTH - self.width
            hit_boundary = True
        if self.y < 0:
            self.y = 0
            hit_boundary = True
        if self.y > HEIGHT:
            self.y = HEIGHT - self.height
            hit_boundary = True
        
        return hit_boundary

    def get_state(self, target_agent):
        """
        # Current implementation uses:
        # - Distance (discretized)
        # - Direction (discretized to 8 directions)
        # - Relative position to boundaries
        # - Agent's current velocity or previous action
        # - Distance from center of the grid
        """

        x_grid = int(self.x / 10)
        y_grid = int(self.y / 10)
        target_x_grid = int(target_agent.x / 10)
        target_y_grid = int(target_agent.y / 10)
        
        relative_x = target_x_grid - x_grid
        relative_y = target_y_grid - y_grid
        
        # Add boundary proximity information
        boundary_x = min(x_grid, int(self.grid_size[0]/10) - x_grid) / int(self.grid_size[0]/10)
        boundary_y = min(y_grid, int(self.grid_size[1]/10) - y_grid) / int(self.grid_size[1]/10)
        
        distance = (relative_x**2 + relative_y**2)**0.5
        
        angle = math.atan2(relative_y, relative_x)
        angle_deg = (math.degrees(angle) + 360) % 360
        direction = int((angle_deg + 22.5) / 45) % 8
        
        # Discretize more finely for closer distances
        if distance < 5:
            distance_bucket = int(distance)
        elif distance < 20:
            distance_bucket = 5 + int((distance - 5) / 3)
        else:
            distance_bucket = 10 + int((distance - 20) / 10)
        
        return (distance_bucket, direction, int(boundary_x * 5), int(boundary_y * 5))

    def choose_action(self, state):
        """
        Choose an action between exploration and exploitation
        """
        # EXPLORATION: random movement to update q table
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(self.actions)
        
        # EXPLOITATION: choose best option from q table
        state_actions = self.q_table[state]
        if not state_actions: # if this state was never reached just return a random movement
            return random.choice(self.actions) 

        # Choose best action, with slight randomness to prevent getting stuck
        best_actions = [
            action for action, value in state_actions.items() 
            if value == max(state_actions.values())
        ]

        return random.choice(best_actions) if best_actions else random.choice(self.actions)

    def move(self, action):
        """
        Move the agent after choosing the action.
        """
        dx, dy = action

        self.x += (dx * self.width)
        self.y += (dy * self.height)

        hit_boundary = self.check_boundaries(self.grid_size[0], self.grid_size[1])
        self.hit_boundary = hit_boundary

        self.positions.append([self.x, self.y])
        if len(self.positions) > 100:
            self.positions.pop(0) 


    def update_q_table(self, state, action, reward, next_state):
        # Q-learning formula
        current_q = self.q_table[state][action]
        best_next_q = max(self.q_table[next_state].values()) if self.q_table[next_state] else 0
        
        # Update Q-value
        self.q_table[state][action] = current_q + self.learning_rate * (
            reward + self.discount_factor * best_next_q - current_q
        )

    
    def decay_exploration(self, exploration_decay):
        """
        Decay exploration after some iterations such that exploitation is used more.
        """
        self.exploration_rate = max(0.1, self.exploration_rate * exploration_decay)

    def get_agent_attributes(self):
        """
        Returns position and color of walker, used mainly to draw the walker at each iteration.
        """
        return [self.positions, self.color, self.width, self.height]
    
    def get_boundary_hit(self):
        """
        Returns whether the agent has hit a boundary during the last movement.
        """
        return self.hit_boundary
    
    def save_q_table(self, episode_number):
        
        # Create a directory for saving if it doesn't exist
        os.makedirs("q_tables", exist_ok=True)
        
        # Convert defaultdict with lambdas to regular dict
        q_dict = {}
        for state, actions in self.q_table.items():
            q_dict[state] = dict(actions)
        
        # Save to file
        filename = f"q_tables/{self.name}_episode_{episode_number}.pkl"
        with open(filename, 'wb') as f:
            pickle.dump(q_dict, f)
        
        print(f"Q-table saved for {self.name} at episode {episode_number}")

    def load_q_table(self, episode_number):
        filename = f"q_tables/{self.name}_episode_{episode_number}.pkl"
        
        try:
            with open(filename, 'rb') as f:
                loaded_q = pickle.load(f)
                
                # Convert loaded dict back to our defaultdict structure
                self.q_table = defaultdict(lambda: defaultdict(lambda: 0))
                for state, actions in loaded_q.items():
                    for action, value in actions.items():
                        self.q_table[state][action] = value
            print(f"Q-table loaded for {self.name} from {filename}")
            return True
        except FileNotFoundError:
            print(f"No Q-table found at {filename}")
            return False
        
    def update_reward_history(self, reward, steps):
        self.steps_history.append(steps)
        self.rewards_history.append(reward)

    def update_reward(self, reward):
        self.current_reward = reward