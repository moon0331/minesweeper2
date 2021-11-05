from random import randint
# from package.board.board import Block

from block import Block

'''board definition'''

def adj_loc(x, y, maxval):
    adj_loc = [
        (x-1, y-1), (x-1, y),   (x-1, y+1),
        (x,   y-1),             (x,   y+1),
        (x+1, y-1), (x+1, y),   (x+1, y+1)
    ]

    for x, y in adj_loc:
        if 0<=x<maxval and 0<=y<maxval:
            yield x, y

class Board:
    def __init__(self, size=9, n_bomb = 10):
        '''
        초급: 9×9 넓이의 지뢰밭에 10개의 지뢰
        중급: 16×16 넓이의 지뢰밭에 40개의 지뢰
        고급: 30×16 넓이의 지뢰밭에 99개의 지뢰
        '''
        self.size = size
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
            x = randint(0, self.size-1)
            y = randint(0, self.size-1)
            self.bomb_loc.add((x, y))


    def _generate(self):
        size = self.size
        self.board = [[Block((row, col)) for col in range(size)] for row in range(size)]
        for r, c in self.bomb_loc:
            self.board[r][c]._set_bomb()


    def _calculate_bomb_distance(self):
        size = self.size
        bomb_distance = [[0 for _ in range(size)] for _ in range(size)]
        for r, c in self.bomb_loc:
            for adj_r, adj_c in adj_loc(r, c, size):
                bomb_distance[adj_r][adj_c] += 1

        for r in range(size):
            for c in range(size):
                self.board[r][c].n_adj_bomb = bomb_distance[r][c]

    def select(self, loc): # 테스트 필요
        size = self.size
        stack = [loc]
        while stack:
            r, c = stack.pop()
            if self.board[r][c].click():
                print('Game END!')
                # exit(1)
            else:
                for adj_r, adj_c in adj_loc(r, c, size):
                    if not self.board[r][c].selected:
                        self.select((adj_r, adj_c))

    def print_board(self, raw = False, flatten=False, add_bomb_loc=False):
        for line in self.board:
            print(" | ".join([str(x) for x in line]))

if __name__ == '__main__':
    Board(4,3).print_board()