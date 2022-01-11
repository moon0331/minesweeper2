class Block:
    def __init__(self, loc, has_bomb=False):
        self.loc = loc
        self.has_bomb = has_bomb
        self.n_adj_bomb = 0
        self.selected = False

        self.opened = False
        self.flaged = False
        self.mark = '■'

    def _set_bomb(self):
        self.has_bomb = True