from random import randint
from package.board.board import Block

'''board definition'''

class Board:
    def __init__(self, size=9, n_bomb = 10):
        '''
        초급: 9×9 넓이의 지뢰밭에 10개의 지뢰
        중급: 16×16 넓이의 지뢰밭에 40개의 지뢰
        고급: 30×16 넓이의 지뢰밭에 99개의 지뢰
        '''
        self.board_size = size
        self.n_bomb = n_bomb
        self.remain_bomb = n_bomb # log
        
        self.bomb_loc = self._randomize_bomb() # 지뢰 위치 랜덤 결정
        self.board = self._generate() # 보드 생성
        self._calculate_bomb_distance() # 지뢰 개수 세어 저장
    
    def _randomize_bomb(self):
        rnd_loc = {}
        while len(rnd_loc) < self.n_bomb:
            x = randint(0, self.size-1)
            y = randint(0, self.size-1)
            rnd_loc.add((x, y))


    def _generate(self):
        pass

    def _calculate_bomb_distance(self):
        pass

    def print_board(self, law = False, flatten=False, add_bomb_loc=False):
        for line in self.board:
            print(" ".join(line))
