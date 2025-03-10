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

        # track recent actions
        self.recent_actions = []
        self.max_recent_actions = 10 
        self.repetition_threshold = 3

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
    
    def detect_repetitive_pattern(self):
        """
        Detect if the agent is stuck in a repetitive pattern of actions.
        Returns True if a pattern is detected, False otherwise.
        """
        if len(self.recent_actions) < 4:
            return False
        
        # Check for simple back-and-forth patterns (e.g., up-down-up-down)
        # These would be opposite actions like (0,1) and (0,-1) or (1,0) and (-1,0)
        for i in range(len(self.recent_actions) - 3):
            # Simple oscillation between two actions
            a1, a2 = self.recent_actions[i], self.recent_actions[i+1]
            a3, a4 = self.recent_actions[i+2], self.recent_actions[i+3]
            
            # Check if a1 == a3 and a2 == a4 (repeating pair)
            if a1 == a3 and a2 == a4:
                # Check if they're opposites (like up-down)
                if (a1[0] == -a2[0] and a1[1] == -a2[1]) or (a1[0] == -a2[0] or a1[1] == -a2[1]):
                    return True
        
        # Check for longer patterns (e.g., up-right-down-left repeated)
        # Simplest approach: check if last 4 actions repeat the previous 4
        if len(self.recent_actions) >= 8:
            pattern1 = tuple(self.recent_actions[-8:-4])
            pattern2 = tuple(self.recent_actions[-4:])
            if pattern1 == pattern2:
                return True
        
        # Check if agent is just repeating the same action
        if len(self.recent_actions) >= 4:
            last_actions = self.recent_actions[-4:]
            if last_actions.count(last_actions[0]) == len(last_actions):
                return True
                
        return False


    def choose_action(self, state):
        """
        Choose an action between exploration and exploitation
        """
        # EXPLORATION: random movement to update q table
        if random.uniform(0, 1) < self.exploration_rate:
            action = random.choice(self.actions)
            self.recent_actions.append(action)
            if len(self.recent_actions) > self.max_recent_actions:
                self.recent_actions.pop(0)
            return random.choice(self.actions)
        
        # EXPLOITATION: choose best option from q table
        state_actions = self.q_table[state]
        if not state_actions: # if this state was never reached just return a random movement
            action = random.choice(self.actions)
            self.recent_actions.append(action)
            if len(self.recent_actions) > self.max_recent_actions:
                self.recent_actions.pop(0)
            return random.choice(self.actions) 

        if self.detect_repetitive_pattern() and random.random() < 0.5:  # 50% chance to break pattern
            # Choose random action to break pattern
            action = random.choice(self.actions)
            #print(f"{self.name} breaking out of action loop with random action {action}")
        else:
            # Choose best action normally
            best_actions = [
                action for action, value in state_actions.items() 
                if value == max(state_actions.values())
            ]
            action = random.choice(best_actions) if best_actions else random.choice(self.actions)
        
        # Record this action
        self.recent_actions.append(action)
        if len(self.recent_actions) > self.max_recent_actions:
            self.recent_actions.pop(0)
        
        return action

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
        """
        Updates the values of the q_table.

        Args:
            - state (tuple) : current state of the agent.
            - action (tuple) : current action of the agent.
            - reward (float) : reward received by the agent for it's actions.
            - next_state (tuple): next state of the agent.
        """

        # Q-learning formula
        current_q = self.q_table[state][action]
        best_next_q = max(self.q_table[next_state].values()) if self.q_table[next_state] else 0
        
        # Update Q-value
        self.q_table[state][action] = current_q + self.learning_rate * (
            reward + self.discount_factor * best_next_q - current_q
        )

    
    def decay_exploration(self, exploration_decay, no_minimum = False):
        """
        Decay exploration after some iterations such that exploitation is used more.
        
        Args:
            - exploration_decay (float) : ratio of the decay of the exploration parameter
            - no_minimum (boolean) : if set to True, exploration rate has no minimum value anymore and can
                                     basically reach 0, used after many episodes to avoid still exploring
        """
        if no_minimum:
            self.exploration_rate = self.exploration_rate * exploration_decay
        else:
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
        """
        Saves the q_table with the respective episode it was saved at.

        Args:
            - episode_number (int) : number of episode to save the q_table at.
        """
        # Create a directory for saving if it doesn't exist        
        filepath = os.path.dirname(os.path.abspath(__file__))
        os.makedirs(f"{filepath}\\q_tables", exist_ok=True)
        
        # Convert defaultdict with lambdas to regular dict
        q_dict = {}
        for state, actions in self.q_table.items():
            q_dict[state] = dict(actions)
        
        # Save to file
        filename = f"{filepath}/q_tables/{self.name}_episode_{episode_number}.pkl"
        with open(filename, 'wb') as f:
            pickle.dump(q_dict, f)
        
        print(f"Q-table saved for {self.name} at episode {episode_number}")


    def load_q_table(self, episode_number):
        """
        Loads previously saved q_tables.

        Args:
            - episode_number (int) : number of episode that we want to retrieve.
        """

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
        """
        Updates the reward history, just for debug reasons.

        Args:
            - reward (float) : current reward of the episode.
            - steps (int) : steps done by the agent in the episode.
        """
        self.steps_history.append(steps)
        self.rewards_history.append(reward)


    def update_reward(self, reward):
        """
        Updates the current reward.
        """
        self.current_reward = reward

    def partial_reset_q_table(self):
        """
        Reset Q-values that have negative values to zero to encourage re-exploration.
        """
        for state in self.q_table:
            for action in self.q_table[state]:
                if self.q_table[state][action] < 0:
                    self.q_table[state][action] = 0

    def update_exploration_rate(self, exploration_rate):
        """
        Updates the exploration rate.
        """
        self.exploration_rate = exploration_rate