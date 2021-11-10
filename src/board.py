from random import randint, seed
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

def cnt_b(board_string):
    return "".join(board_string).count('b')

class Board:
    def __init__(self, size=9, n_bomb = 10, seed=None, board_string=None):
        '''
        초급: 9×9 넓이의 지뢰밭에 10개의 지뢰
        중급: 16×16 넓이의 지뢰밭에 40개의 지뢰
        고급: 30×16 넓이의 지뢰밭에 99개의 지뢰
        '''
        if board_string:
            rsize, csize = len(board_string), len(board_string[0])
            size = rsize
            if rsize != csize:
                raise Exception('# of row != # of column')

        self.size = size
        self.n_bomb = cnt_b(board_string) if board_string else n_bomb
        self.remain_bomb = n_bomb # 실제 남은 폭탄 개수
        self.selected_bomb = 0 # 유저가 선택한 폭탄 개수            
        
        self.bomb_loc = set()
        self.board = None
        
        self._set_bomb(seed, board_string) # 지뢰 위치 랜덤 결정
        self._generate() # 보드 생성

        self._calculate_bomb_distance() # 지뢰 개수 세어 저장

    
    def _set_bomb(self, seed_number, board_string=None):
        self.bomb_loc = set()
        if board_string:
            for x in range(self.size):
                for y in range(self.size):
                    if board_string[x][y] == 'b':
                        self.bomb_loc.add((x, y))
        else:
            self._randomize_bomb(seed_number)


    def _randomize_bomb(self, seed_number):
        seed(seed_number)
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


    def right_click(self, loc):
        r, c = loc
        if self.board[r][c].has_bomb():
            self.remain_bomb -= 1
        self.selected_bomb += 1

    def select(self, loc): # 테스트 필요
        size = self.size
        stack = [loc]
        while stack:
            r, c = stack.pop()
            # print(r,c)
            if self.board[r][c].click():
                print('Game END!')
                # exit(1)
            else:
                # 주위 폭탄 수 체크하는 부분 추가하기
                # 연쇄폭발 부분은 아래에 
                if not self.board[r][c].n_adj_bomb:
                    for adj_r, adj_c in adj_loc(r, c, size):
                        # adj_block = self.board[adj_r][adj_c]
                        if not self.board[adj_r][adj_c].selected:
                            stack.append((adj_r, adj_c))


    def print_board(self, raw = False, flatten=False, add_bomb_loc=False):
        for line in self.board:
            print(" ".join([str(x) for x in line]))
            # print(" ".join([x._loc()+str(x) for x in line]))


    def print_bomb_loc(self):
        print(self.bomb_loc)


    def is_end_success(self):
        return self.selected_bomb == self.n_bomb and self.remain_bomb == 0

if __name__ == '__main__':
    b = ['----b', 'bbbb-', 'bb--b', '----b', '-----']
    b = Board(board_string=b)
    b.print_board()
    b.print_bomb_loc()

    main_board = Board(9,10,seed=12345)
    main_board.print_board()
    main_board.print_bomb_loc()
    main_board.select(list(map(int, input().split())))
    main_board.print_board()