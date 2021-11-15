"""Minesweeper v2.0
ⓒ 2021 Kyeongjin Mun, Seungwon Lee All Rights Reserved.
"""


import os
import sys
# import time  # Deprecated now

# Scheduled to change using __init__.py if possible
from object.board import Board
from object.board import adj_loc


class Agent:
    """A class which is responsible for whole game management such as level selection, displaying board, user input,
    main sequence, results, etc., that is almost all about this game.
    """

    def __init__(self):
        self.level_info = {1: 'Beginner', 2: 'Intermediate', 3: 'Expert'}
        self.board_info = {'Beginner': (9, 9, 10), 'Intermediate': (16, 16, 40), 'Expert': (16, 30, 99)}
        self.time = 0  # Temporary
        self.click = 0
    
    def select_level(self):
        while True:
            try:
                level = int(input("Select game level. 1. Beginner 2. Intermediate 3. Expert: "))
                if 1 <= level <= 3:
                    return level
                else:
                    raise
            except:
                os.system('clear')
                print("Wrong input. Please try again.\n")

    def generate_board(self):
        height, width, n_bomb = self.board_info[self.level]
        self.board = Board(height, width, n_bomb)

    def display_board(self):
        print(("Remaining Flags: %d" % self.board.remain_flag).ljust(20), "Time: %d\n" % self.time)
        for row in range(self.height):
            for col in range(self.width):
                cur = self.board.block_list[row][col]
                print(cur.mark, end=' ')
                # print("*", end=' ') if cur.has_bomb else print(cur.n_adj_bomb, end=' ')  # For debug
            print()
        print()
    
    def command(self):
        while True:
            try:
                self.display_board()
                print("Row: 0 ~ %d Column: 0 ~ %d Action: 1. left click 2. right click 3. both" % (self.height - 1, self.width - 1))
                row, col, act = map(int, input("Enter your input such as 'row column action': ").split())
                if 0 <= row < self.height and 0 <= col < self.width and 1 <= act <= 3:
                    self.click += 1
                    return row, col, act
                else:
                    raise
            except:
                os.system('clear')
                print("Wrong input. Please try again.\n")
    
    def count_adj_flag(self, row, col):
        adj_flag = 0
        for adj_r, adj_c in adj_loc(row, col, self.height, self.width):
            if self.board.block_list[adj_r][adj_c].flaged:
                adj_flag += 1
        return adj_flag

    def left_click(self, row, col):
        cur = self.board.block_list[row][col]
        if cur.has_bomb:
            self.game_over()
        else:
            if self.remain_block == 0:
                self.victory()

            # Left click algorithm (core algorithm)
            if not cur.opened:
                cur.opened = True
                self.board.remain_block -= 1
            pass  # Recursion; not completed.

    def right_click(self, row, col):
        cur = self.board.block_list[row][col]
        cur.flaged = not cur.flaged

        if cur.flaged:
            self.board.remain_flag -= 1
            cur.mark = 'F'
        else:
            self.board.remain_flag += 1
            cur.mark = cur.adj_n_bomb if cur.opened else '.'
    
    def chord(self, row, col):
        # 지뢰 위치 잘못 표시했을때 게임 오버는 아직 구현 안함
        for adj_r, adj_c in adj_loc(row, col, self.height, self.width):
            self.left_click(adj_r, adj_c)
    
    def game_over(self):
        os.system('clear')
        print("GAME OVER\n")
        print(("Remaining Flags: %d" % self.board.remain_flag).ljust(20), "Time: %d\n" % self.time)

        for row in range(self.height):
            for col in range(self.width):
                cur = self.board.block_list[row][col]
                print("*", end=' ') if cur.has_bomb else print(cur.mark, end=' ')
            print()
        print()
        
        print("Time: %f" % self.time)
        print("Clicks: %d\n" % self.click)

        sys.exit(0)
    
    def victory(self):
        os.system('clear')
        print("VICTORY!!\n")
        print(("Remaining Flags: %d" % self.board.remain_flag).ljust(20), "Time: %d\n" % self.time)
        print(self.board.remain_flag.ljust(20), self.time)

        for row in range(self.height):
            for col in range(self.width):
                cur = self.block_list[row][col]
                print(cur.mark, end=' ')
            print()
        print()
        
        print("Time: %f" % self.time)
        print("Clicks: %d\n" % self.click)

        sys.exit(0)

    def main(self):
        """Main sequence of playing minesweeper2."""
        os.system('clear')
        
        # Only 0-index is used for both backend and user input.
        while True:
            row, col, act = self.command()
            if act == 1:
                self.left_click(row, col)
            elif act == 2:
                self.right_click(row, col)
            else:
                self.count_flag(row, col)
                cur = self.board.block_list[row][col]
                
                if not cur.opened:
                    # Closed block chord exception.
                    os.system('clear')
                    print("You can chord opened block only. Please try again.\n")
                    continue
                
                if not self.count_adj_flag(row, col) == cur.n_adj_bomb:
                    # Flag num and block num mismatch exception.
                    os.system('clear')
                    print("You can only chord when the number of flags matches the block number. Please try again.\n")
                    continue
                
                self.chord(row, col)
            
            os.system('clear')

    def run(self):
        print("Minesweeper v2.0\nⓒ  2021 Kyeongjin Mun, Seungwon Lee All Rights Reserved.\n")
        level = self.select_level()
        self.level = self.level_info[level]
        self.generate_board()
        self.main()


if __name__=='__main__':
    agent = Agent()
    agent.run()
