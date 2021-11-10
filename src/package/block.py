'''block definition'''

class Block:
    def __init__(self, loc, has_bomb=False):
        self.loc = loc
        self.has_bomb = has_bomb
        self.n_adj_bomb = 0
        self.selected = False

        self.image = ''
        self._generate_image(has_bomb)

    def click(self):
        if not self.selected:
            self.selected = True

        if self.has_bomb:
            return True # 폭탄 있음 -> 후처리 필요
        else:
            return False # 폭탄 없음 -> 연쇄 폭발 구현 필요

    def _set_bomb(self):
        self.has_bomb = True

    def _generate_image(self, has_bomb):
        if self.has_bomb:
            self.image = 'Bomb.png' # get bomb image file
        else:
            self.image = ''

    def _loc(self):
        return f'({self.loc[0]},{self.loc[1]})'

    def __repr__(self):
        loc = f'({self.loc[0]},{self.loc[1]})'
        if self.has_bomb:
            return f'B'
        else:
            if self.selected:
                return f'{self.n_adj_bomb}'
            else:
                return f'-'

if __name__ == '__main__':
    print(Block((13,2)))
    print(Block((12,3, True)))