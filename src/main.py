"""Minesweeper 2 RL Simulator
ⓒ 2021 Kyeongjin Mun, Seungwon Lee. All Rights Reserved.
"""

import os
import sys
import random
from collections import deque

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from game.agent import Agent
from models.torch.dqn import QNet

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


def train():
    pass

def main():
    os.system('clear')
    print("Minesweeper 2 RL Simulator\n\nⓒ  2021 Kyeongjin Mun, Seungwon Lee All Rights Reserved.\n")
    agent = Agent()
    agent.run()


if __name__ == '__main__':
    main()