"""Minesweeper v2.0
ⓒ 2021 Kyeongjin Mun, Seungwon Lee All Rights Reserved.
"""

# Maybe it will be changed using __init__.py
from board.board import Board


class GameManager:

    def __init__(self):
        self.game_level_info = {1: 'Beginner', 2: 'Intermediate', 3: 'Expert'}
        self.board_info = {'Beginner': (9, 9, 10), 'Intermediate': (16, 16, 40), 'Expert': (16, 30, 99)}
    
    def display_board(self, game_board):
        height, width = game_board.height, game_board.width
        board = game_board.board
        
        print()
        for row in range(height):
            for col in range(width):
                has_bomb = board[row][col].has_bomb
                n_adj_bomb = board[row][col].n_adj_bomb
                mark = '*' if has_bomb else n_adj_bomb
                print(mark, end=' ')
            print()
        print()

    def select_level(self):
        while True:
            try:
                level = int(input("Select game mode. 1. Beginner 2. Intermediate 3. Expert: "))
                if 1 <= level <= 3:
                    return level
                else:
                    raise
            except:
                print("Please try again.\n")
    
    def generate_board(self):
        board_info = self.board_info[self.game_level]
        height, width, bomb = board_info
        self.game_board = Board(height, width, bomb)
    
    # Move to next situation by user input(row col act)
    def progress(self):
        pass

    def main(self):
        self.result = None  # Maybe variable name will be changed
        while self.result is None:
            self.display_board(self.game_board)
            # It will be divided into function
            while True:
                try:
                    row, col, act = map(int, input("Enter your action like 'row column action': ").split())
                    break
                except:
                    print("Please try again.\n")
            self.progress(row, col, act)

    def run(self):
        print("Minesweeper v2.0\nⓒ  2021 Kyeongjin Mun, Seungwon Lee All Rights Reserved.\n")
        
        level = self.select_level()

        self.game_level = self.game_level_info[level]
        self.generate_board()
        self.main()


if __name__=='__main__':
    game_manager = GameManager()
    game_manager.run()
