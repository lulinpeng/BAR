import numpy as np
import pickle
import os
import time
import datetime

class QTableAgent:
    def __init__(self, action_size, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995, exploration_min=0.01):
        self.action_size = action_size
        self.learning_rate = learning_rate  # α
        self.discount_factor = discount_factor  # γ
        self.exploration_rate = exploration_rate  # ε
        self.exploration_decay = exploration_decay
        self.exploration_min = exploration_min
        self.state_hit_count, self.state_query_count = 0, 0
        self.q_table = {}
        self.visited_states = set()
    
    def get_state_key(self, state):
        return '-'.join([str(int(s)) for s in state])
    
    def get_q_values(self, state):
        self.state_query_count += 1
        state_key = self.get_state_key(state)
        if state_key not in self.q_table:
            print(f'new state {state_key}')
            self.q_table[state_key] = np.zeros(self.action_size)
            self.visited_states.add(state_key)
        else:
            self.state_hit_count += 1
            print(f'state hit:  {round(self.state_hit_count/self.state_query_count * 100)}%, {self.state_hit_count}/{self.state_query_count}')
        return self.q_table[state_key]
    
    def choose_action(self, state):
        print(f'--- Q table: {len(self.q_table)} * {self.action_size} ---')
        if np.random.uniform(0, 1) < self.exploration_rate:
            print(f'random action, epsilon = {self.exploration_rate}')
            return np.random.randint(self.action_size)
        else:
            print(f'action with max Q value, epsilon = {self.exploration_rate}')
            q_values = self.get_q_values(state)
            return np.argmax(q_values)
    
    def learn(self, state, action, reward, next_state, done):
        y_hat = self.get_q_values(state)[action]
        if done:
            y = reward
        else:
            next_q_values = self.get_q_values(next_state)
            max_next_q = np.max(next_q_values)
            y = reward + self.discount_factor * max_next_q
        # Q-learning update
        new_y_hat = (1 - self.learning_rate) * y_hat + self.learning_rate * y
        state_key = self.get_state_key(state)
        self.q_table[state_key][action] = new_y_hat
        print(f'Update: Q_table[{state_key}][{action}]: {round(y_hat, 3)} -> {round(new_y_hat, 3)}')
        return
    
    def update_exploration_rate(self):
        new_exploration_rate = max(self.exploration_min, self.exploration_rate * self.exploration_decay)
        print(f'update exploration rate {self.exploration_rate} -> {new_exploration_rate}')
        self.exploration_rate = new_exploration_rate
        return
    
    def save_model(self, filename=None):
        base_dir = './models/'
        os.makedirs(base_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'{timestamp}_q_table_snake.pkl' if filename is None else filename
        model_path = os.path.join(base_dir, filename)
        with open(model_path, 'wb') as f:
            pickle.dump({'q_table': self.q_table, 'exploration_rate': self.exploration_rate, 'visited_states': list(self.visited_states)}, f)
        print(f"save model into file {model_path}")
        return
    
    def load_model(self, filename='q_table_snake.pkl'):
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                self.q_table = data['q_table']
                self.exploration_rate = data['exploration_rate']
                self.visited_states = set(data['visited_states'])
            print(f"load model from file {filename}")
            return True
        else:
            print("not find model file, now start training")
            return False