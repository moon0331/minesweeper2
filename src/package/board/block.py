'''block definition'''

class Block:
    def __init__(self, has_bomb=False, n_adj_bomb=0):
        self.has_bomb = has_bomb
        self.n_adj_bomb = n_adj_bomb
        self.image = self._generate_image(has_bomb)

    def _set_atrribute(self, n_adj_bomb=0):
        if self.has_bomb:
            self._set_bomb()
        else:
            self._set_n_adj_bomb(n_adj_bomb)

    def _generate_image(self):
        if self.has_bomb:
            image = None # get bomb image file
        return image