from random import randint
from object.block import Block


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