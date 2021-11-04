'''block definition'''

class Block:
    def __init__(self, has_bomb=False, ):
        self.has_bomb = has_bomb
        self.

    def _set_atrribute(self, n_adj_bomb=0):
        if self.has_bomb:
            self._set_bomb()
        else:
            self._set_n_adj_bomb(n_adj_bomb)

