from random import randint
# from package.board.board import Block

from block import Block

'''board definition'''

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
            for adj_r in range(r-1, r+2):
                for adj_c in range(c-1, c+2):
                    if not (r == adj_r == adj_c) and 0<=adj_r<size and 0<=adj_c<size:
                        bomb_distance[adj_r][adj_c] += 1

        for r in range(size):
            for c in range(size):
                self.board[r][c].n_adj_bomb = bomb_distance[r][c]


    def print_board(self, raw = False, flatten=False, add_bomb_loc=False):
        for line in self.board:
            print(" | ".join([str(x) for x in line]))

if __name__ == '__main__':
    Board(4,3).print_board()