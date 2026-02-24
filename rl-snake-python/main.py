from snakegame import SnakeGame
import numpy as np
import time
import matplotlib.pyplot as plt
from collections import deque
import datetime


def train_snake_ai(total_episodes=1000, model_path=None, enable_gui=False, engine=None):
    env = SnakeGame(width=10, height=10, enable_gui=enable_gui) # create environment
    action_size = 3  # [STRAIGHT, RIGHT, LEFT]
    if engine == 'qtable':
        from qtableagent import QTableAgent
        agent = QTableAgent(action_size) # create q-table agent
    elif engine == 'qnetwork':
        from qnetworkagent import QNetworkAgent
        state_size = 11
        agent = QNetworkAgent(state_size, action_size)
    else:
        print("engine must be 'qtable' or 'qnetwork'")
        return
    if model_path is not None:
        agent.load_model()
    scores, mean_scores, total_rewards, exploration_rates = [], [], [], []
    recent_scores = deque(maxlen=100)
    for episode in range(total_episodes):
        progress = round(episode / total_episodes * 100)
        print(f"\n{'■'*progress}{'□'*(100-progress)} {episode}-th episode\n")
        state = env.reset()
        total_reward, step, done = 0, 0, False
        while not done:
            action = agent.choose_action(state) # choose action
            next_state, reward, done = env.step(action) # exectue one step
            # if reward > 0:
            #     time.sleep(0.5)
            print(f'{step}-th step, state {state}, next_state {next_state}, reward {reward}, done {done}')
            agent.learn(state, action, reward, next_state, done) # learn
            state = next_state
            total_reward += reward
            step += 1
            # time.sleep(0.2)
        agent.update_exploration_rate()
        scores.append(env.score)
        recent_scores.append(env.score)
        mean_score = np.mean(recent_scores)
        mean_scores.append(mean_score)
        total_rewards.append(total_reward)
        exploration_rates.append(agent.exploration_rate)
        if episode % 1000 == 0:
            print(f"Episode {episode}: Score = {env.score}, Mean Score = {mean_score:.2f}, Exploration Rate = {agent.exploration_rate:.3f}")
        if episode % 1000 == 0 and episode > 0:
            agent.save_model()
    agent.save_model()
    plot_training_results(scores, mean_scores, total_rewards, exploration_rates)
    return agent, env
   
def test_snake_ai(episodes, model_path:str, enable_gui=True, engine=None):
    env = SnakeGame(width=10, height=10, enable_gui=enable_gui)
    if engine == 'qtable':
        from qtableagent import QTableAgent
        agent = QTableAgent(action_size=3) # create q-table agent
    elif engine == 'qnetwork':
        from qnetworkagent import QNetworkAgent
        agent = QNetworkAgent(state_size=11, action_size=3)
    else:
        print("engine must be 'qtable' or 'qnetwork'")
        return
    if not agent.load_model(filename=model_path):
        print("please train model first")
        return
    print("testing snake AI...")
    test_scores = []
    for episode in range(episodes):
        state, done, total_reward = env.reset(), False, 0
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            state = next_state
            total_reward += reward
            if enable_gui:
                time.sleep(0.1)
        test_scores.append(env.score)
        print(f"round {episode + 1}: score = {env.score}")
    print(f"mean score: {np.mean(test_scores):.2f}\nmax score: {np.max(test_scores)}\nmin score: {np.min(test_scores)}")
    return test_scores

def plot_training_results(scores, mean_scores, total_rewards, exploration_rates):
    plt.figure(figsize=(15, 10))
    plt.subplot(2, 2, 1)
    plt.plot(scores, alpha=0.5, label='Score per episode')
    plt.plot(mean_scores, label='Average score')
    plt.xlabel('Training Episodes')
    plt.ylabel('Score')
    plt.title('Snake AI Training Score')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 2, 2)
    plt.plot(total_rewards, alpha=0.5, color='orange')
    plt.xlabel('Training Episodes')
    plt.ylabel('Total Reward')
    plt.title('Total Reward per Episode')
    plt.grid(True)
    
    plt.subplot(2, 2, 3)
    plt.plot(exploration_rates, color='red')
    plt.xlabel('Training Episodes')
    plt.ylabel('Exploration Rate')
    plt.title('Exploration Rate Decay')
    plt.grid(True)
    
    plt.subplot(2, 2, 4)
    plt.hist(scores, bins=40, alpha=0.7, color='green')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.title('Score Distribution')
    plt.grid(True)
    
    plt.tight_layout()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f'models/{timestamp}_training_results.png'
    plt.savefig(filename)
    print(f'save picture of traning results into file {filename}')
    plt.show()
 
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['train', 'test'], default='train', help='train or test')
    parser.add_argument('--episodes', type=int, default=1000, help='epsodoes (recommend: 1000-5000)')
    parser.add_argument('--gui', choices=[0, 1], type=int, default=0,help='enable GUI')
    parser.add_argument('--model', type=str, default=None, help='model path')
    parser.add_argument('--engine', choices=['qtable', 'qnetwork'], type=str, default='qtable', help='training way: qtable or qnetwork')
    args = parser.parse_args()
    enable_gui = True if args.gui == 1 else False
    model_path = args.model

    if args.mode == 'train':
        agent, env = train_snake_ai(total_episodes=args.episodes, model_path=model_path, enable_gui=enable_gui, engine=args.engine)
    elif args.mode == 'test':
        if args.model is not None:
            test_snake_ai(episodes=args.episodes, model_path=model_path, enable_gui=enable_gui, engine=args.engine)
        else:
            print('model path can not be empty')
    else:
        print("invalid mode")