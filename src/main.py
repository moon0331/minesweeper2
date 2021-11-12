"""Minesweeper v2.0
ⓒ 2021 Kyeongjin Mun, Seungwon Lee All Rights Reserved.
"""

# Maybe it will be changed using __init__.py
import sys
import time

from board.board import Board


class GameManager:
    """A class which is responsible for level selection, displaying board, user input, main sequence, results, etc.,
    that is almost all about this game.
    """

    def __init__(self):
        self.level_info = {1: 'Beginner', 2: 'Intermediate', 3: 'Expert'}
        self.board_info = {'Beginner': (9, 9, 10), 'Intermediate': (16, 16, 40), 'Expert': (16, 30, 99)}
        self.status = 'Playing'
        
        # Temporary
        self.timer = 0
        self.elapsed_time = 0
        self.clicks = 0
    
    def display_board(self, board, block_table, height, width):
        print(("Remaining Flags: %d" % board.remain_flag).ljust(20), "Time: %d" % self.timer)
        print()
        for row in range(height):
            for col in range(width):
                block = block_table[row][col]
                # print(block.mark, end=' ')
                print("*", end=' ') if block.has_bomb else print(block.n_adj_bomb, end=' ')  # For debug
            print()
        print()

    def select_level(self):
        while True:
            try:
                level = int(input("Select game level. 1. Beginner 2. Intermediate 3. Expert: "))
                if 1 <= level <= 3:
                    return level
                else:
                    raise
            except:
                print("Please try again.\n")
    
    def generate_board(self, level):
        height, width, n_bomb = self.board_info[level]
        self.board = Board(height, width, n_bomb)
    
    def user_input(self, board, block_table, height, width):
        while True:
            try:
                self.display_board(board, block_table, height, width)
                print("Row: 1 ~ %d Column: 1 ~ %d Action: 1. left click 2. right click 3. both" % (height, width))
                row, col, act = map(int, input("Enter your input such as 'row column action': ").split())
                if 1 <= row <= height and 1 <= col <= width and 1 <= act <= 3:
                    return row, col, act
                else:
                    raise
            except:
                print("Please try again.\n")

    def left_click(self, board, block_table, row, col):
        block = block_table[row][col]
        if block.has_bomb:
            return 'Game Over'
        else:
            # left_click algorithm
            pass

            if self.remain_block == 0:
                return 'Victory'

    def right_click(self, board, block_table, row, col):
        block = block_table[row][col]
        block.flaged = not block.flaged

        if block.flaged:
            board.remain_flag -= 1
            block.mark = 'F'
        else:
            board.remain_flag += 1
            block.mark = block.adj_n_bomb if block.opened else '.'
        
        return 'Playing'
    
    def chord(self, board, block_table, row, col):
        pass
    
    def game_over(self, board, block_table, height, width):
        print("GAME OVER\n")
        print(board.remain_flag.ljust(20), self.timer)

        for row in range(height):
            for col in range(width):
                block = block_table[row][col]
                print("*", end=' ') if block.has_bomb else print(block.mark, end=' ')
            print()
        
        print("Elapsed Time: %f" % self.elapsed_time)
        print("Clicks: %d" % self.clicks)

        sys.exit(0)
    
    def victory(self, board, block_table, height, width):
        print("YOU WIN!\n")
        print(board.remain_flag.ljust(20), self.timer)

        for row in range(height):
            for col in range(width):
                block = block_table[row][col]
                print(block.mark, end=' ')
            print()
        
        print("Elapsed Time: %f" % self.elapsed_time)
        print("Clicks: %d" % self.clicks)

        sys.exit(0)

    def main(self, board, height, width):
        """Main sequence of playing minesweeper2."""
        height, width = board.height, board.width

        # User input: 1-index, back-end: 0-index
        while self.status == 'Playing':
            row, col, act = self.user_input(board, board.block_table, height, width)
            if act == 1:
                self.status = self.left_click(board, board.block_table, row - 1, col - 1)
            elif act == 2:
                self.status = self.right_click(board, board.block_table, row - 1, col - 1)
            else:
                if not board.block_table[row - 1][col - 1].opened:
                    #  Closed block chord exception.
                    print("You can chord the opened block only. Please try again.\n")
                    continue
                self.status = self.chord(row - 1, col - 1)
        
        # Game end
        self.victory(board, board.block_table, height, width) if self.status == 'Victory' else \
        self.game_over(board, board.block_table, height, width)

    def run(self):
        print("Minesweeper v2.0\nⓒ  2021 Kyeongjin Mun, Seungwon Lee All Rights Reserved.\n")
        level = self.select_level()
        self.level = self.level_info[level]
        self.generate_board(self.level)
        height, width = self.board.height, self.board.width
        self.main(self.board, height, width)


if __name__=='__main__':
    game_manager = GameManager()
    game_manager.run()
