from random import randint
from board.block import Block

'''board definition'''

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
    # Divide size into height and width
    def __init__(self, height, width, n_bomb):
        '''
        초급: 9×9 넓이의 지뢰밭에 10개의 지뢰
        중급: 16×16 넓이의 지뢰밭에 40개의 지뢰
        고급: 30×16 넓이의 지뢰밭에 99개의 지뢰
        '''

        self.height = height
        self.width = width
        self.n_bomb = n_bomb
        self.remain_bomb = n_bomb # log

        self.bomb_loc = set()
        self.board = None
        
        self._randomize_bomb() # 지뢰 위치 랜덤 결정
        self._generate() # 보드 생성

        self._calculate_bomb_distance() # 지뢰 개수 세어 저장
    

    def _randomize_bomb(self):
        self.bomb_loc = set()
        while len(self.bomb_loc) < self.n_bomb:
            x = randint(0, self.height - 1)
            y = randint(0, self.width - 1)

            self.bomb_loc.add((x, y))


    def _generate(self):
        height, width = self.height, self.width
        self.board = [[Block((row, col)) for col in range(width)] for row in range(height)]
        for r, c in self.bomb_loc:
            self.board[r][c]._set_bomb()


    def _calculate_bomb_distance(self):
        height, width = self.height, self.width
        bomb_distance = [[0 for _ in range(width)] for _ in range(height)]
        for r, c in self.bomb_loc:
            for adj_r, adj_c in adj_loc(r, c, height, width):
                bomb_distance[adj_r][adj_c] += 1

        for r in range(height):
            for c in range(width):
                self.board[r][c].n_adj_bomb = bomb_distance[r][c]

    def select(self, loc): # 테스트 필요
        height, width = self.height, self.width
        stack = [loc]
        while stack:
            r, c = stack.pop()
            if self.board[r][c].click():
                print('Game END!')
                # exit(1)
            else:
                for adj_r, adj_c in adj_loc(r, c, height, width):
                    if not self.board[r][c].selected:
                        self.select((adj_r, adj_c))

    def print_board(self, raw = False, flatten=False, add_bomb_loc=False):
        for line in self.board:
            print(" | ".join([str(x) for x in line]))

if __name__ == '__main__':
    Board(4, 4, 3).print_board()