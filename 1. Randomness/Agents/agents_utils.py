import numpy as np
import random
import time

SAVE_EPISODES = 50

def calculate_reward(agent, target_agent):
    """
    Computes reward for each agent:

    Args:
        - agent (AgentWalker) : current agent
        - target_agent (AgentWalker) : target agent which is connected to the main agent

    The reward function is computed as follows:
        - first the distance between the two targets is computed sqrt((x_1^2 - x_2^2) + (y_1^2 - y_2^2)) 
        - max reward is set to 100, the base reward of the agent is computed by taking the max * e^(-distance/100),
          so higher distance, lower reward.
        - an additional reward is added if the agent is in the proximity of the other one.
        - an additional reward is added if the movement of the agent led him closer to the other agent.
        - negative reward if the agent hits the wall.
        - negative reward if the agent repeats steps.

    The final reward is computed as a sum between all the rewards listed before.
    """

    distance = ((agent.x - target_agent.x)**2 + (agent.y - target_agent.y)**2)**0.5
    
    # More balanced base reward with consistent magnitude
    # Cap the maximum reward to 100 for finding each other
    max_reward = 100
    base_reward = max_reward * np.exp(-distance/100)
    
    # Create tiered distance rewards that are consistent for both agents
    if distance <= 20:
        proximity_reward = 50
    elif distance < 30:
        proximity_reward = 30
    elif distance < 50:
        proximity_reward = 15
    else:
        proximity_reward = 0
    
    # Calculate movement reward (reward moving toward target)
    movement_reward = 0
    if len(agent.positions) > 1:
        old_pos = agent.positions[-2]
        old_distance = ((old_pos[0] - target_agent.x)**2 + (old_pos[1] - target_agent.y)**2)**0.5
        # Reward or penalize based on whether agent is moving closer or farther
        distance_delta = old_distance - distance
        # Scale based on current distance (more important when closer)
        movement_reward = 20 * distance_delta / (distance + 1)  # Add 1 to avoid division by zero
    
    # Standardized boundary penalty
    boundary_penalty = -30 if agent.get_boundary_hit() else 0
    
    # Repetition penalty
    repetition_penalty = -20 if agent.detect_repetitive_pattern() else 0
    
    # Sum all components
    total_reward = base_reward + proximity_reward + movement_reward + boundary_penalty + repetition_penalty
    
    # Print detailed reward components occasionally for debugging
    if random.random() < 0.005:  # Only print 0.5% of the time to avoid flooding console
        print(f"{agent.name} reward components: base={base_reward:.1f}, proximity={proximity_reward}, " 
              f"movement={movement_reward:.1f}, boundary={boundary_penalty}, repetition={repetition_penalty}")
    
    return total_reward

def choose_agent_action_reward(agents):
    """
    Takes the agent's state, performs an action and computes the reward.

    Args:
        - agents (array) : array with all the agents.

    """
    for i, agent in enumerate(agents):
        target_agent = agents[1 - i]  # The other agent
                
        # Get current state
        current_state = agent.get_state(target_agent)
        
        # Choose and perform action
        action = agent.choose_action(current_state)
        agent.move(action)
        

    for i, agent in enumerate(agents):
        target_agent = agents[1 - i]
        # Get new state and reward
        next_state = agent.get_state(target_agent)
        reward = calculate_reward(agent, target_agent)
        agent.update_reward(reward)
        
        # Update Q-table
        agent.update_q_table(current_state, action, reward, next_state)

def reset_episode(distance, agents, agent_one, agent_two, start_time, episode_steps, episode_count, episode_resets, WIDTH, HEIGHT):
    """
    Checks if the condition for ending the episode is met, which is agents in neighboorhoud cells
    or timeout (more than 100s passed).

    Args:
        - distance (float) : distance between the two agents.
        - agents (array) : array with all the agents.
        - agent_one (AgentWalker) : first agent.
        - agent_two (AgentWalker) : second agent.
        - start_time (int) : the starting second of the episode.
        - WIDTH (int) : width of the map.
        - HEIGHT (int) : height of the map.

    If one of the condition is met to end the episode, four things can happen:
        - agents are placed at opposite corners
        - agents are placed at the same size but far part
        - agents are placed randomly with a minimum distance
        - agents are placed completely random

    After this, the q_table might get saved to be used in other simulations.
    Finally, counters are incremented or resetted.

    Returns:
        - episode_steps (int) : how many steps the agents have taken.
        - episode_count (int) : current number of episodes.
        - episode_reset (int) : used to reset the exploration_rate. 
        - start_time (int) : resetted start timer.
    """
    if distance <= 10 or time.time() - start_time > 100:
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

        if (episode_count % SAVE_EPISODES) == 0:
            for agent in agents:
                agent.save_q_table(episode_count)

        for agent in agents:
            agent.update_reward_history(agent.current_reward, episode_steps)
            avg_reward = agent.current_reward / episode_steps if episode_steps > 0 else 0
            print(f"{agent.name} AVG REWARD {avg_reward}, EPISODE STEPS: {episode_steps}")

        episode_steps = 0
        episode_count += 1
        episode_resets += 1
        
        start_time = time.time()

        return episode_steps, episode_count, episode_resets, start_time
    else:
        # Return the current values without changes
        return episode_steps, episode_count, episode_resets, start_time