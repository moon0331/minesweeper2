"""
Minesweeper 2 RL Simulator
ā 2021 Kyeongjin Mun, Seungwon Lee, Jeonghan Lim. All Rights Reserved.
"""

import os

from models.torch.torch_dqn import ReplayMemory
from models.torch.torch_dqn import TorchDQNAgent


def main():
    os.system('clear')
    print("Minesweeper 2 RL Simulator\n\nā  2021 Kyeongjin Mun, Seungwon Lee, Jeonghan Lim All Rights Reserved.\n")
    torch_dqn_agent = TorchDQNAgent()
    torch_dqn_agent.run()


if __name__ == '__main__':
    main()