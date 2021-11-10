"""Minesweeper v2.0
ⓒ 2021 Kyeongjin Mun, Seungwon Lee All Rights Reserved.
"""

# Maybe it will be changed using __init__.py
from board.board import Board


class GameManager:
    """A class which is responsible for level selection, displaying board, user input, main sequence, results, etc.,
    that is almost all about this game.
    """

    def __init__(self):
        self.game_level_info = {1: 'Beginner', 2: 'Intermediate', 3: 'Expert'}
        self.board_info = {'Beginner': (9, 9, 10), 'Intermediate': (16, 16, 40), 'Expert': (16, 30, 99)}

        game_level = self.select_level()
        self.game_level = self.game_level_info[game_level]
    
    def display_board(self):
        game_board = self.game_board
        print("Remaining flags: %d" % game_board.remain_flag)
        
        height, width = game_board.height, game_board.width
        block_table = game_board.block_table
        
        print()
        for row in range(height):
            for col in range(width):
                block = block_table[row][col]
                print(block.mark, end=' ')
            print()
        print()

    def select_level(self):
        while True:
            try:
                game_level = int(input("Select game mode. 1. Beginner 2. Intermediate 3. Expert: "))
                if 1 <= game_level <= 3:
                    return game_level
                else:
                    raise
            except:
                print("Please try again.\n")
    
    def generate_board(self):
        board_info = self.board_info[self.game_level]
        height, width, n_bomb = board_info
        self.game_board = Board(height, width, n_bomb)
    
    def user_input(self, height, width):
        while True:
            try:
                self.display_board()
                print("Row: 1 ~ %d Column: 1 ~ %d Action: 1. left click 2. right click 3. both" % (height, width))
                row, col, act = map(int, input("Enter your input such as 'row column action': ").split())
                if 1 <= row <= height and 1 <= col <= width and 1 <= act <= 3:
                    return row, col, act
                else:
                    raise
            except:
                print("Please try again.\n")

    # These three action functions can be moved to another class if click algorithms get longer.

    # Left click algorithms not understood yet.
    def left_click(self, row, col):
        pass

    def right_click(self, row, col):
        row, col = row - 1, col - 1  # 0-index

        game_board = self.game_board
        block_table = game_board.block_table
        block = block_table[row][col]
        
        block.flaged = not block.flaged
        if block.flaged:
            game_board.remain_flag -= 1
            block.mark = 'F'
        else:
            game_board.remain_flag += 1
            block.mark = block.n_adj_n_bomb if block.opened else '.'
    
    # This can be implemented after understanding left click algorithms.
    def chord(self, row, col):
        pass
    
    def main(self):
        """Main sequence of playing minesweeper2."""
        self.result = None  # Maybe variable name will be changed.
        game_board = self.game_board
        height, width = game_board.height, game_board.width

        while self.result is None:
            row, col, act = self.user_input(height, width)
            if act == 1:
                self.left_click(row, col)
            elif act == 2:
                self.right_click(row, col)
            else:
                self.chord(row, col)

    def run(self):
        print("Minesweeper v2.0\nⓒ  2021 Kyeongjin Mun, Seungwon Lee All Rights Reserved.\n")
        self.generate_board()
        self.main()


if __name__=='__main__':
    game_manager = GameManager()
    game_manager.run()
