"""Minesweeper2 Agent Test"""

import os
import sys
from collections import deque
from random import randint


def adj_loc(x, y, xmax, ymax):
    adj_loc = [
        (x-1, y-1), (x-1, y),   (x-1, y+1),
        (x,   y-1),             (x,   y+1),
        (x+1, y-1), (x+1, y),   (x+1, y+1)
    ]

    for x, y in adj_loc:
        if 0<=x<xmax and 0<=y<ymax:
            yield x, y


class Board:
    """Board definition"""

    # Divide size into height and width
    def __init__(self, height, width, n_bomb):
        self.height = height
        self.width = width
        self.n_bomb = n_bomb

        self.bomb_loc = set()
        self.blocks = None
        self.init_loc = None

        self.miss_block = None

        self.remain_flag = n_bomb  # Remaining flag value starts from n_bomb, which can be less than 0.
        self.remain_block = height * width - n_bomb # If this value goes to 0, user wins.
        
        self._generate() # 보드 생성

    def randomize_bomb(self):
        self.bomb_loc = set()
        while len(self.bomb_loc) < self.n_bomb:
            x = randint(0, self.height - 1)
            y = randint(0, self.width - 1)
            if (x, y) != self.init_loc:
                self.bomb_loc.add((x, y))
        
        for r, c in self.bomb_loc:
            self.blocks[r][c]._set_bomb()

    def _generate(self):
        height, width = self.height, self.width
        self.blocks = [[Block((row, col)) for col in range(width)] for row in range(height)]

    def calculate_bomb_distance(self):
        height, width = self.height, self.width
        bomb_distance = [[0 for _ in range(width)] for _ in range(height)]
        for r, c in self.bomb_loc:
            for adj_r, adj_c in adj_loc(r, c, height, width):
                bomb_distance[adj_r][adj_c] += 1

        for r in range(height):
            for c in range(width):
                self.blocks[r][c].n_adj_bomb = bomb_distance[r][c]

    def display_board(self):
        print(' ', end=' ')
        for i in range(self.width):
            print("%d" % i, end=' ')
        print()

        for row in range(self.height):
            print("%d" % row, end=' ')
            for col in range(self.width):
                cur = self.blocks[row][col]
                print(cur.mark, end=' ')
            print()
        print()

    def display_board_game_over(self):
        print(' ', end=' ')
        for i in range(self.width):
            print("%d" % i, end=' ')
        print()

        for row in range(self.height):
            print("%d" % row, end=' ')
            for col in range(self.width):
                cur = self.blocks[row][col]
                if cur.flaged:
                    print("▶", end=' ') if cur.has_bomb else print("X", end=' ')
                else:
                    if cur == self.miss_block:
                        print("!", end=' ')
                    else:
                        print("*", end=' ') if cur.has_bomb else print(cur.mark, end=' ')
            print()
        print()

    def display_board_victory(self):
        print(' ', end=' ')
        for i in range(self.width):
            print("%d" % i, end=' ')
        print()

        for row in range(self.height):
            print("%d" % row, end=' ')
            for col in range(self.width):
                cur = self.blocks[row][col]
                print("▶", end=' ') if cur.has_bomb else print(cur.mark, end=' ')
            print()
        print()


class Block:
    """Block definition"""

    def __init__(self, loc, has_bomb=False):
        self.loc = loc
        self.has_bomb = has_bomb
        self.n_adj_bomb = 0
        self.selected = False

        self.opened = False
        self.flaged = False
        self.mark = '■'

    def _set_bomb(self):
        self.has_bomb = True


class Minesweeper2Agent(Board):
    """A class which is responsible for whole game management such as level selection, displaying board, user input,
    main sequence, results, etc., that is almost all about this game.
    """

    def __init__(self, level=1):
        self.level = level
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
        super(Minesweeper2Agent, self).__init__(height, width, n_bomb)
    
    def command(self):
        while True:
            print(("Remaining Flags: %d" % self.remain_flag).ljust(20), "Time: %d\n" % self.time)
            self.display_board()
            print("Row: 0 ~ %d Column: 0 ~ %d Action: 1. left click 2. right click 3. chord" % (self.height - 1, self.width - 1))
            try:
                row, col, act = map(int, input("Enter your input such as 'row column action': ").split())
                if 0 <= row < self.height and 0 <= col < self.width and 1 <= act <= 3:
                    self.click += 1
                    return row, col, act
                else:
                    raise
            except:
                os.system('clear')
                print("Wrong input.\n")
    
    def count_adj_flag(self, row, col):
        adj_flag = 0
        for adj_r, adj_c in adj_loc(row, col, self.height, self.width):
            if self.blocks[adj_r][adj_c].flaged:
                adj_flag += 1
        return adj_flag

    def left_click(self, row, col):
        cur = self.blocks[row][col]
        if cur.has_bomb:
            self.miss_block = cur
            self.game_over()
        
        else:
            q = deque([(row, col)])
            vis = [[0] * self.width for _ in range(self.height)]
            vis[row][col] = 1

            while q:
                r, c = q.popleft()
                cur = self.blocks[r][c]
                
                if not cur.opened:
                    cur.opened = True
                    cur.mark = '%d' % cur.n_adj_bomb if cur.n_adj_bomb else '□'
                    self.remain_block -= 1
                
                if not self.blocks[r][c].n_adj_bomb:
                    for adj_r, adj_c in adj_loc(r, c, self.height, self.width):
                        if not vis[adj_r][adj_c]:
                            q.append((adj_r, adj_c))
                            vis[adj_r][adj_c] = 1

    def right_click(self, row, col):
        cur = self.blocks[row][col]
        cur.flaged = not cur.flaged

        if cur.flaged:
            self.remain_flag -= 1
            cur.mark = '▶'
        else:
            self.remain_flag += 1
            cur.mark = '■'
    
    def chord(self, row, col):
        for adj_r, adj_c in adj_loc(row, col, self.height, self.width):
            cur = self.blocks[adj_r][adj_c]
            if cur.has_bomb != cur.flaged:
                self.miss_block = cur
                self.game_over()

        for adj_r, adj_c in adj_loc(row, col, self.height, self.width):
            cur = self.blocks[adj_r][adj_c]
            if not cur.flaged and not cur.opened:
                self.left_click(adj_r, adj_c)
    
    def game_over(self):
        os.system('clear')
        print("GAME OVER\n")
        print(("Remaining Flags: %d" % self.remain_flag).ljust(20), "Time: %d\n" % self.time)
        
        self.display_board_game_over()
        
        print("Time: %f" % self.time)
        print("Clicks: %d\n" % self.click)

        sys.exit(0)  # Force termination
    
    def victory(self):
        os.system('clear')
        print("VICTORY!!\n")
        print(("Remaining Flags: %d" % 0).ljust(20), "Time: %d\n" % self.time)

        self.display_board_victory()
        
        print("Time: %f" % self.time)
        print("Clicks: %d\n" % self.click)

    def run(self):
        """Main sequence of playing Minesweeper 2."""
        os.system('clear')
        print("Minesweeper 2.0\n\nⓒ  2021 Kyeongjin Mun, Seungwon Lee All Rights Reserved.\n")
        self.level = self.select_level()
        self.generate_board()
        os.system('clear')
        
        # Only 0-index is used for both backend and user input.
        while self.remain_block:
            row, col, act = self.command()
            cur = self.blocks[row][col]
            
            # To avoid first trial game over.
            if not self.init_loc:
                self.init_loc = (row, col)
                self.randomize_bomb()
                self.calculate_bomb_distance()
            
            if act == 1:
                # Opended block left click exception.
                if cur.opened:
                    os.system('clear')
                    print("You can left click closed block only.\n")
                    continue
                    
                # Flaged block left click exception.
                if cur.flaged:
                    os.system('clear')
                    print("You can left click non-flaged block only.\n")
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
                if self.count_adj_flag(row, col) != cur.n_adj_bomb:
                    os.system('clear')
                    print("You can only chord when the number of flags matches the block number.\n")
                    continue
                
                self.chord(row, col)
            
            os.system('clear')
        
        self.victory()


if __name__ == '__main__':
    minesweeper2_agent = Minesweeper2Agent()
    minesweeper2_agent.run()