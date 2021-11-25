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


def train():
    pass

def main():
    os.system('clear')
    print("Minesweeper 2 RL Simulator\n\nⓒ  2021 Kyeongjin Mun, Seungwon Lee All Rights Reserved.\n")
    agent = Agent()
    agent.run()


if __name__ == '__main__':
    main()