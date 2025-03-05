from collections import defaultdict
import random

class AgentWalker():
    """
    Walker class, performs either:
    - random walk, choosing a random step from -1 to 1.
    - random walk with perlin noise, with a given starting noise and step.
    """
    def __init__(self, x, y, color, name, width, height, grid_size, exploration_rate, discount_factor, learning_rate):
        self.x = x
        self.y = y
        self.color = color
        self.positions = []
        self.name = name
        self.width = width
        self.height = height
        # managing agents Q table
        self.grid_size = grid_size
        self.q_table = defaultdict(lambda: defaultdict(lambda: 0))
        self.exploration_rate = exploration_rate
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        # possible movements of agents
        self.actions = [(0, -1), (1, 0), (0, 1), (-1, 0), 
                         (1, -1), (1, 1), (-1, 1), (-1, -1)]

    def check_boundaries(self, WIDTH, HEIGHT):
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH:
            self.x = WIDTH - self.width
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT:
            self.y = HEIGHT - self.height

    def get_state(self, target_agent):
        """
        Get current state, based on the other's agent position
        """

        x_grid = int(self.x / 10)
        y_grid = int(self.y / 10)
        target_x_grid = int(target_agent.x / 10)
        target_y_grid = int(target_agent.y / 10)

        relative_x = target_x_grid - x_grid
        relative_y = target_y_grid - y_grid
        
        # Add distance as part of the state
        distance = ((self.x - target_agent.x)**2 + (self.y - target_agent.y)**2)**0.5
    
        return (relative_x, relative_y, int(distance/10))

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

        self.check_boundaries(self.grid_size[0], self.grid_size[1])
        
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
        self.exploration_rate *= exploration_decay

    def get_agent_attributes(self):
        """
        Returns position and color of walker, used mainly to draw the walker at each iteration.
        """
        return [self.positions, self.color, self.width, self.height]