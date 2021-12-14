"""Minesweeper 2 RL Simulator
ⓒ 2021 Kyeongjin Mun, Seungwon Lee. All Rights Reserved.
"""

import os

from game.minesweeper2_agent import Minesweeper2Agent


def main():
    os.system('clear')
    print("Minesweeper 2 RL Simulator\n\nⓒ  2021 Kyeongjin Mun, Seungwon Lee All Rights Reserved.\n")
    minesweeper2_agent = Minesweeper2Agent()
    minesweeper2_agent.run()


if __name__ == '__main__':
    main()