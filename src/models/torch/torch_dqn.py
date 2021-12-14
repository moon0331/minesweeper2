import os
import sys
import random
from collections import deque

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from game.minesweeper2_agent import Minesweeper2Agent

# Hyperparameters
LEARNING_RATE = 0.0005
GAMMA = 0.98
BUFFER_SIZE = 50000
BATCH_SIZE = 32


class ReplayBuffer:

    def __init__(self):
        self.buffer = deque(maxlen=BUFFER_SIZE)
    
    def put(self, transition):
        self.buffer.append(transition)
    
    def sample(self, n):
        mini_batch = random.sample(self.buffer, n)
        states = []
        actions = []
        rewards = []
        next_states = []
        done_masks = []

        for transition in mini_batch:
            state, action, reward, next_state, done_mask = transition
            states.append(state)
            actions.append(action)
            rewards.append(reward)
            next_states.append(next_state)
            done_masks.append(done_mask)
        
        return torch.tensor(states, dtype=torch.float), torch.tensor(actions), torch.tensor(rewards), \
                torch.tensor(next_states, dtype=torch.float), torch.tensor(done_masks)
    
    def size(self):
        return len(self.buffer)


class QNet(nn.Module):

    def __init__(self, action_size):
        super(QNet, self).__init__()
        self.fc1 = nn.Linear(4, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)
        self.action_size = action_size

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
    def sample_action(self, obs, epsilon):
        out = self.forward(obs)
        prob = random.random()
        if prob < epsilon:
            return random.randint(0, self.action_size - 1)
        else:
            return out.argmax().item()


def train():
    pass