import pygame
import random
import graphical_components as gc
import agentWalker
import options as opt
import time
import numpy as np
from collections import defaultdict

# General parameters
WIDTH = 640
HEIGHT = 420
AGENT_WIDTH = 10
AGENT_HEIGHT = 10
MAX_WALKERS = 50

# Q-learning parameters
LEARNING_RATE = 0.2 
DISCOUNT_FACTOR = 0.9 
EXPLORATION_RATE = 0.8  
EXPLORATION_DECAY = 0.95 


def update_screen(screen, agents):
    """
    Updates the positions of agents in the screen
    """
    for agent in agents:
        pos, color, width, height = agent.get_agent_attributes()
        x, y = pos[-1]
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, color, rect)

def calculate_reward(agent, target_agent):
    """
    Computes the reward for an agent w.r.t. a target agent
    """
    distance = ((agent.x - target_agent.x)**2 + (agent.y - target_agent.y)**2)**0.5
    
    # Base reward inversely proportional to distance
    reward = 100 * np.exp(-distance/100)
    
    # More pronounced bonus for getting close
    if distance < 20:
        reward += 50
    if distance < 10:
        reward += 100
    if distance < 5:
        reward += 200
    
    # Stronger penalty for boundary hits
    if agent.get_boundary_hit():
        reward -= 50
    
    # Add penalty for staying in the same position
    if len(agent.positions) > 1 and agent.positions[-1] == agent.positions[-2]:
        reward -= 5
    
    # Add small reward for moving toward the target
    if len(agent.positions) > 1:
        old_distance = ((agent.positions[-2][0] - target_agent.x)**2 + 
                         (agent.positions[-2][1] - target_agent.y)**2)**0.5
        if distance < old_distance:
            reward += 10
    
    return reward


def main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    agent_one_color = (0, 255, 0)  # Green
    agent_two_color = (255, 0, 0)  # Red
    background_color = (0, 0, 0)  # Black

    screen.fill(background_color)

    # Create two agents
    agent_one = agentWalker.AgentWalker(50, 50, agent_one_color, "Agent 1", AGENT_WIDTH, AGENT_HEIGHT, (WIDTH, HEIGHT), EXPLORATION_RATE, DISCOUNT_FACTOR, LEARNING_RATE)
    agent_two = agentWalker.AgentWalker(WIDTH - 50, HEIGHT - 50, agent_two_color, "Agent 2", AGENT_WIDTH, AGENT_HEIGHT, (WIDTH, HEIGHT), EXPLORATION_RATE, DISCOUNT_FACTOR, LEARNING_RATE)
    agents = [agent_one, agent_two]

    episode_count = 0
    max_episodes = 1000

    loading_circle = gc.LoadingCircle(10, 10)  # Top-left corner
    
    # Font for instructions
    esc_pressed = False
    running = True

    decay_timer = 0

    pygame.display.set_caption("Agents Walk Simulation")
    episode_steps = 0
    start_time = time.time()
    while running and episode_count < max_episodes:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # Quit simulation
            
        keys = pygame.key.get_pressed()
        
        # ESC key handling
        if keys[pygame.K_ESCAPE]:
            if not esc_pressed:
                # First time pressing ESC
                loading_circle.start_loading()
                esc_pressed = True
        else:
            # Reset if ESC is released
            loading_circle.stop_loading()
            esc_pressed = False

        # Handle events
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 25))  # Alpha value of 25 for trail effect
        screen.blit(s, (0, 0))
        
        # For each agent, choose action and update
        for i, agent in enumerate(agents):
            target_agent = agents[1 - i]  # The other agent
            
            # Get current state
            current_state = agent.get_state(target_agent)
            
            # Choose and perform action
            action = agent.choose_action(current_state)
            agent.move(action)
            
            # Get new state and reward
            next_state = agent.get_state(target_agent)
            reward = calculate_reward(agent, target_agent)
            agent.update_reward(reward)
            
            # Update Q-table
            agent.update_q_table(current_state, action, reward, next_state)
            
        if decay_timer == 50:
            # Decay exploration rate
            for agent in agents:
                agent.decay_exploration(EXPLORATION_DECAY)
            decay_timer = 0
        
        decay_timer += 1
        episode_steps += 1
        # Check if agents have found each other
        distance = np.sqrt((agent_one.x - agent_two.x)**2 + (agent_one.y - agent_two.y)**2)
        # if more then 100s pass reset timer and go to next episode
        if distance < 10 or time.time() - start_time > 100:
            print(f"End of episode {episode_count}, current exploration rate: {agent_one.exploration_rate}, time elapsed: {time.time() - start_time}")
            # Instead of completely random positions, consider placing them at opposite corners
            # or at specific distances to encourage learning different scenarios
            if episode_count % 4 == 0:
                # Place at opposite corners
                agent_one.x, agent_one.y = 50, 50
                agent_two.x, agent_two.y = WIDTH-50, HEIGHT-50
            elif episode_count % 4 == 1:
                # Place at same side but far apart
                agent_one.x, agent_one.y = 50, 50
                agent_two.x, agent_two.y = WIDTH-50, 50
            elif episode_count % 4 == 2:
                # Random but with minimum distance
                while True:
                    agent_one.x, agent_one.y = random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)
                    agent_two.x, agent_two.y = random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)
                    if np.sqrt((agent_one.x - agent_two.x)**2 + (agent_one.y - agent_two.y)**2) > WIDTH/2:
                        break
            else:
                # Completely random
                agent_one.x, agent_one.y = random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)
                agent_two.x, agent_two.y = random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)

            if (episode_count % 20) == 0:
                for agent in agents:
                    agent.save_q_table(episode_count)

            for agent in agents:
                agent.update_reward_history(agent.current_reward, episode_steps)
                print(f"AGENT CURRENT REWARD {agent.current_reward}, EPISODE STEPS: {episode_steps}")
            episode_steps = 0
            episode_count += 1
            
            start_time = time.time()
        
        # Render agents
        update_screen(screen, agents)
        
        # Display episode count and exploration rates
        font = pygame.font.Font(None, 20)
        episode_text = font.render(f"Episode: {episode_count}", True, (255, 255, 255))
        screen.blit(episode_text, (10, HEIGHT - 20))
        
        # exp_rate_1 = font.render(f"Agent 1 Exploration: {agent_one.exploration_rate:.4f}", True, (255, 255, 255))
        # exp_rate_2 = font.render(f"Agent 2 Exploration: {agent_two.exploration_rate:.4f}", True, (255, 255, 255))
        # screen.blit(exp_rate_1, (10, HEIGHT - 45))
        # screen.blit(exp_rate_2, (10, HEIGHT - 20))

        loading_circle.draw(screen)

        if loading_circle.is_loading and time.time() - loading_circle.start_time >= loading_circle.duration:
            running = False
        

        # Update display
        pygame.display.update()
        clock.tick(10)


if __name__ == "__main__":
    main()
    pygame.quit()