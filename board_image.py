class BoardImage:
    def __init__(self):
        """ Board images is image of game boards. Cells of board can take values: 'empty', 'ship_area', 
        False - mean that there placed ship's unflooded deck, True - mean that there placed ship's flooded deck
        """
        self.board = [['empty'] * 10 for _ in range(10)]

    def are_free_board_cells(self, ship):
        for [y, x] in ship.decks:
            if self.board[x][y] != 'empty':
                return False
        return True

    def add_ship_image(self, ship):
        for [y, x] in ship.ship_area:
            self.board[x][y] = 'ship_area'
        for [y, x] in ship.decks:
            self.board[x][y] = False

    def add_flooded_ship_image(self, ship):
        for [y, x] in ship.ship_area:
            self.board[x][y] = 'ship_area'
        for [y, x] in ship.decks:
            self.board[x][y] = True

    def get_empty_cells(self):
        return [[y, x] for x in range(10) for y in range(10) if self.board[x][y] == 'empty']

    def check_win(self):
        decks = [self.board[x][y] for x in range(10) for y in range(10)
                 if self.board[x][y] is False or self.board[x][y] is True]
        if all(decks):
            return True
        return False
