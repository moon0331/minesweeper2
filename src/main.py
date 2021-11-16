"""MINESWEEPER 2
ⓒ 2021 Kyeongjin Mun, Seungwon Lee All Rights Reserved.
"""


import os
import sys
import time
from collections import deque

# Scheduled to change using __init__.py if possible
from object.board import Board
from object.board import adj_loc


class Agent(Board):
    """A class which is responsible for whole game management such as level selection, displaying board, user input,
    main sequence, results, etc., that is almost all about this game.
    """

    def __init__(self):
        self.board_info = {1: (9, 9, 10), 2: (16, 16, 40), 3: (16, 30, 99)}
        self.time = 0
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
                print("Wrong input.\n")

    def generate_board(self):
        height, width, n_bomb = self.board_info[self.level]
        self.board = Board(height, width, n_bomb)

    def display_board(self):
        print(("Remaining Flags: %d" % self.board.remain_flag).ljust(20), "Time: %d\n" % self.time)
        for row in range(self.board.height):
            for col in range(self.board.width):
                cur = self.board.block_list[row][col]
                print(cur.mark, end=' ')
            print()
        print()
    
    def command(self):
        while True:
            self.display_board()
            print("Row: 0 ~ %d Column: 0 ~ %d Action: 1. left click 2. right click 3. chord" % (self.board.height - 1, self.board.width - 1))
            try:
                row, col, act = map(int, input("Enter your input such as 'row column action': ").split())
                if 0 <= row < self.board.height and 0 <= col < self.board.width and 1 <= act <= 3:
                    self.click += 1
                    return row, col, act
                else:
                    raise
            except:
                os.system('clear')
                print("Wrong input.\n")
    
    def count_adj_flag(self, row, col):
        adj_flag = 0
        for adj_r, adj_c in adj_loc(row, col, self.board.height, self.board.width):
            if self.board.block_list[adj_r][adj_c].flaged:
                adj_flag += 1
        return adj_flag

    def left_click(self, row, col):
        cur = self.board.block_list[row][col]
        
        if cur.has_bomb:
            self.board.miss_block = self.board.block_list[row][col]
            self.game_over()
        
        else:
            q = deque([(row, col)])
            vis = [[0] * self.board.width for _ in range(self.board.height)]
            vis[row][col] = 1

            while q:
                r, c = q.popleft()
                cur = self.board.block_list[r][c]
                
                if not cur.opened:
                    cur.opened = True
                    cur.mark = '%d' % cur.n_adj_bomb if cur.n_adj_bomb else '□'
                    self.board.remain_block -= 1
                
                if self.board.block_list[r][c].n_adj_bomb == 0:
                    for adj_r, adj_c in adj_loc(r, c, self.board.height, self.board.width):
                        if not vis[adj_r][adj_c]:
                            q.append((adj_r, adj_c))
                            vis[adj_r][adj_c] = 1

    def right_click(self, row, col):
        cur = self.board.block_list[row][col]
        cur.flaged = not cur.flaged

        if cur.flaged:
            self.board.remain_flag -= 1
            cur.mark = '▶'
        else:
            self.board.remain_flag += 1
            cur.mark = '■'
    
    def chord(self, row, col):
        for adj_r, adj_c in adj_loc(row, col, self.board.height, self.board.width):
            cur = self.board.block_list[adj_r][adj_c]
            if cur.has_bomb != cur.flaged:
                self.board.miss_block = cur
                self.game_over()

        for adj_r, adj_c in adj_loc(row, col, self.board.height, self.board.width):
            cur = self.board.block_list[adj_r][adj_c]
            if not cur.flaged and not cur.opened:
                self.left_click(adj_r, adj_c)
    
    def game_over(self):
        os.system('clear')
        print("GAME OVER\n")
        print(("Remaining Flags: %d" % self.board.remain_flag).ljust(20), "Time: %d\n" % self.time)

        for row in range(self.board.height):
            for col in range(self.board.width):
                cur = self.board.block_list[row][col]
                if cur.flaged:
                    print("▶", end=' ') if cur.has_bomb else print("▷", end=' ')
                else:
                    if cur == self.board.miss_block:
                        print("X", end=' ')
                    else:
                        print("*", end=' ') if cur.has_bomb else print(cur.mark, end=' ')
            print()
        print()
        
        print("Time: %f" % self.time)
        print("Clicks: %d\n" % self.click)

        sys.exit(0)
    
    def victory(self):
        os.system('clear')
        print("VICTORY!!\n")
        print(("Remaining Flags: %d" % 0).ljust(20), "Time: %d\n" % self.time)

        for row in range(self.board.height):
            for col in range(self.board.width):
                cur = self.board.block_list[row][col]
                print("▶", end=' ') if cur.has_bomb else print(cur.mark, end=' ')
            print()
        print()
        
        print("Time: %f" % self.time)
        print("Clicks: %d\n" % self.click)

        sys.exit(0)

    def main(self):
        """Main sequence of playing Minesweeper 2."""
        os.system('clear')
        
        # Only 0-index is used for both backend and user input.
        while self.board.remain_block:
            row, col, act = self.command()
            cur = self.board.block_list[row][col]
            if act == 1:
                # Opended block left click exception.
                if cur.opened:
                    os.system('clear')
                    print("You can left click closed block only.\n")
                    continue
                self.left_click(row, col)
            elif act == 2:
                # Opened block right click exception.
                if cur.opened:
                    os.system('clear')
                    print("You can right click closed block only.\n")
                    continue
                self.right_click(row, col)
            else:
                # Closed block chord exception.
                if not cur.opened:
                    os.system('clear')
                    print("You can chord opened block only.\n")
                    continue
                
                # Flag num and block num mismatch exception.
                if not self.count_adj_flag(row, col) == cur.n_adj_bomb:
                    os.system('clear')
                    print("You can only chord when the number of flags matches the block number.\n")
                    continue
                
                self.chord(row, col)
            
            os.system('clear')
        
        self.victory()

    def run(self):
        os.system('clear')
        print("MINESWEEPER 2\n\nⓒ  2021 Kyeongjin Mun, Seungwon Lee All Rights Reserved.\n")
        self.level = self.select_level()
        self.generate_board()
        self.main()


if __name__=='__main__':
    agent = Agent()
    agent.run()
