'''block definition'''

class Block:
    def __init__(self, loc, has_bomb=False, n_adj_bomb=0):
        self.loc = loc
        self.has_bomb = has_bomb
        self.n_adj_bomb = n_adj_bomb
        self.image = self._generate_image(has_bomb)

    def _set_atrribute(self, n_adj_bomb=0):
        if self.has_bomb:
            self._set_bomb()
        else:
            self._set_n_adj_bomb(n_adj_bomb)

    def _set_bomb(self):
        self.has_bomb = True

    def _generate_image(self, has_bomb):
        if self.has_bomb:
            image = 'Bomb.png' # get bomb image file
        else:
            image = ''
        return image

    def __repr__(self):
        if self.has_bomb:
            return f'[({self.loc[0]},{self.loc[1]}), BOMB, {self.n_adj_bomb}]'
        else:
            return f'[({self.loc[0]},{self.loc[1]}), ----, {self.n_adj_bomb}]'