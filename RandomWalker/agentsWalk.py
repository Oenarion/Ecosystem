import pygame
import random
import graphical_components as gc
import agentWalker
import options as opt
import time
import numpy as np
from collections import defaultdict
import agents_utils as au

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


def update_screen(screen, agents, episode_count, loading_circle):
    """
    Render all the components on the screen.
    """
    for agent in agents:
        pos, color, width, height = agent.get_agent_attributes()
        x, y = pos[-1]
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, color, rect)

    # Display episode count and exploration rates
    font = pygame.font.Font(None, 20)
    episode_text = font.render(f"Episode: {episode_count}", True, (255, 255, 255))
    screen.blit(episode_text, (10, HEIGHT - 20))
    loading_circle.draw(screen)



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
    episode_resets = 0
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
        au.choose_agent_action_reward(agents)
            
    
        if decay_timer == 50:
            # Decay exploration rate
            for agent in agents:
                if episode_count <= 50:
                    agent.decay_exploration(EXPLORATION_DECAY)
                else:
                    agent.decay_exploration(EXPLORATION_DECAY, no_minimum = True)
            decay_timer = 0
        

        if episode_count % 15 == 0 and episode_count > 0:
            for agent in agents:
                agent.partial_reset_q_table()
        
        decay_timer += 1
        episode_steps += 1
        # Check if agents have found each other
        distance = np.sqrt((agent_one.x - agent_two.x)**2 + (agent_one.y - agent_two.y)**2)
        # if more then 100s pass reset timer and go to next episode
        # simplifying the problem, agents found each other when they are in neighbourhood cells not in the same one
        episode_steps, episode_count, episode_resets, start_time = au.reset_episode(distance, agents, agent_one, agent_two, start_time, WIDTH, HEIGHT)

        # AFTER 100 EPISODES STOP GOING INTO EXPLORATION MODE
        if episode_resets > 15 and random.random() < 0.005 and episode_count < 100:
            print(f"GOING INTO EXPLORATION MODE AGAIN, EXPLORATION RATE: {EXPLORATION_RATE}")
            for agent in agents:
                if random.random() < 0.5:
                    agent.update_exploration_rate(EXPLORATION_RATE)
            episode_resets = 0

        if loading_circle.is_loading and time.time() - loading_circle.start_time >= loading_circle.duration:
            running = False

        # Render all components
        update_screen(screen, agents, episode_count, loading_circle)
        
        # Update display
        pygame.display.update()
        clock.tick(10)


if __name__ == "__main__":
    main()
    pygame.quit()