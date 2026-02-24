import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random
import pickle
import os
import time
import datetime

class QNetwork(nn.Module):
    def __init__(self, state_size, action_size, hidden_size=64):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, action_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class QNetworkAgent:
    def __init__(self, state_size, action_size, learning_rate=0.001, discount_factor=0.9,
                 exploration_rate=1.0, exploration_decay=0.995, exploration_min=0.01,
                 batch_size=32, memory_size=10000, target_update_freq=10):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.exploration_min = exploration_min
        self.batch_size = batch_size
        self.target_update_freq = target_update_freq

        # Neural networks
        self.q_network = QNetwork(state_size, action_size)
        self.target_network = QNetwork(state_size, action_size)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=learning_rate)

        # Experience replay
        self.memory = deque(maxlen=memory_size)

        # Training metrics
        self.step_count = 0
        self.training_count = 0

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def choose_action(self, state):
        print(f'--- Q-network ---')
        if np.random.uniform(0, 1) < self.exploration_rate:
            print(f'random action, epsilon = {self.exploration_rate}')
            return np.random.randint(self.action_size)
        else:
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state).unsqueeze(0)
                q_values = self.q_network(state_tensor)
                action = np.argmax(q_values.numpy())
                print(f'action with max Q value (Q-values: {q_values.numpy()[0]}), epsilon = {self.exploration_rate}')
                return action

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        # Sample batch from memory
        batch = random.sample(self.memory, self.batch_size)
        states = torch.FloatTensor(np.array([e[0] for e in batch]))
        actions = torch.LongTensor(np.array([e[1] for e in batch]))
        rewards = torch.FloatTensor(np.array([e[2] for e in batch]))
        next_states = torch.FloatTensor(np.array([e[3] for e in batch]))
        dones = torch.FloatTensor(np.array([e[4] for e in batch]))

        # Current Q values
        current_q_values = self.q_network(states).gather(1, actions.unsqueeze(1))

        # Target Q values
        with torch.no_grad():
            next_q_values = self.target_network(next_states).max(1)[0]
            target_q_values = rewards + (1 - dones) * self.discount_factor * next_q_values

        # Compute loss
        loss = nn.MSELoss()(current_q_values.squeeze(), target_q_values)

        # Optimize
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.training_count += 1
        if self.training_count % 100 == 0:
            print(f'Training step {self.training_count}, Loss: {loss.item():.4f}')

        # Update target network
        if self.training_count % self.target_update_freq == 0:
            self.target_network.load_state_dict(self.q_network.state_dict())

    def learn(self, state, action, reward, next_state, done):
        self.remember(state, action, reward, next_state, done)
        self.replay()

    def update_exploration_rate(self):
        new_exploration_rate = max(self.exploration_min, self.exploration_rate * self.exploration_decay)
        self.exploration_rate = new_exploration_rate

    def save_model(self, filename=None):
        base_dir = './models/'
        os.makedirs(base_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'{timestamp}_q_network_snake.pkl' if filename is None else filename
        model_path = os.path.join(base_dir, filename)

        torch.save({
            'q_network_state_dict': self.q_network.state_dict(),
            'target_network_state_dict': self.target_network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'exploration_rate': self.exploration_rate
        }, model_path)
        print(f"save model into file {model_path}")

    def load_model(self, filename='q_network_snake.pth'):
        if os.path.exists(filename):
            checkpoint = torch.load(filename)
            self.q_network.load_state_dict(checkpoint['q_network_state_dict'])
            self.target_network.load_state_dict(checkpoint['target_network_state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            self.exploration_rate = checkpoint['exploration_rate']
            print(f"load model from file {filename}")
            return True
        else:
            print("not find model file, now start training")
            return False