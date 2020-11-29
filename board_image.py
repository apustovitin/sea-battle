class BoardImage:
    def __init__(self):
        """ Board images is image of game boards. own_board is board of player or computer. Player or computer places
        own ships after start at own_board. Cells of own_board can take values: 'empty', 'ship_area', False - mean that
        there placed ship's unflooded deck, True - mean that there placed ship's flooded deck
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

    def get_empty_cells(self):
        return [[y, x] for x in range(10) for y in range(10) if self.board[x][y] == 'empty']

    def check_win(self):
        decks = [self.board[x][y] for x in range(10) for y in range(10)
                 if self.board[x][y] is False or self.board[x][y] is True]
        if all(decks): return True
        return False

    def count_enemy_deck_near_floded(self, y, x, y_next, x_next):
        """recursive count of floded decks by computer in image of player board after flood deck
        if coordianates inside board and if cell is flooded enemy deck than count +1
        """
        if 0 > x_next > 9 or 0 > y_next > 9 or self.board[x_next][y_next] is not True:
            return [0, [y_next, x_next]]
        return [1 + self.count_enemy_deck_near_floded(y_next, x_next, y_next * 2 - y, x_next * 2 - x)[0], 
                self.count_enemy_deck_near_floded(y_next, x_next, y_next * 2 - y, x_next * 2 - x)[1]]

    def flood_enemy_deck(self, y, x, available_enemy_ships):
        enemy_ship_deck_min_number = 1
        self.board[x][y] = True
        # diagonal cells around enemy deck are enemy ship area
        diagonal_cells_around_deck = [[y - 1, x - 1], [y - 1, x + 1], [y + 1, x - 1], [y + 1, x + 1]]
        for [y_pos, x_pos] in diagonal_cells_around_deck:
            if 0 <= x_pos <= 9 and 0 <= y_pos <= 9: # if coordianates inside board
                self.board[x_pos][y_pos] = 'ship_area'
        # linear cells around enemy deck are possibble enemy ship area if there are not other deck of this ship
        linear_cells_around_deck = [[y - 1, x], [y + 1, x], [y, x - 1], [y, x + 1]]
        cell_before_first_deck_y, cell_before_first_deck_x = None, None
        for [y_pos, x_pos] in linear_cells_around_deck:
            if 0 <= x_pos <= 9 and 0 <= y_pos <= 9 and self.board[x_pos][y_pos] is True:
                # if coordianates inside board and if cell is flooded enemy deck
                enemy_ship_deck_min_number += self.count_enemy_deck_near_floded(y, x, y_pos, x_pos)[0]
                cell_before_first_deck_y = self.count_enemy_deck_near_floded(y, x, y_pos, x_pos)[1][0]
                cell_before_first_deck_x = self.count_enemy_deck_near_floded(y, x, y_pos, x_pos)[1][1]
        max_decks_number = max(available_enemy_ships)
        if max_decks_number == enemy_ship_deck_min_number:
            available_enemy_ships.pop(available_enemy_ships.index(max_decks_number))
            if not (cell_before_first_deck_y is None) and not (cell_before_first_deck_x is None):
                if 0 <= cell_before_first_deck_y <= 9 and 0 <= cell_before_first_deck_x <= 9:
                    self.board[cell_before_first_deck_x][cell_before_first_deck_y] = 'ship_area'
            for [y_pos, x_pos] in linear_cells_around_deck:
                if 0 <= x_pos <= 9 and 0 <= y_pos <= 9 and self.board[x_pos][y_pos] == 'empty':
                    # if coordianates inside board and if cell is unknown
                    self.board[x_pos][y_pos] = 'ship_area'
        else:
            for [y_pos, x_pos] in linear_cells_around_deck:
                if 0 <= x_pos <= 9 and 0 <= y_pos <= 9 and self.board[x_pos][y_pos] == 'empty':
                    # if coordianates inside board and if cell is unknown
                    self.board[x_pos][y_pos] = 'possible'
        return available_enemy_ships
    
    def refresh_available_enemy_ships(self, last_possible_cell, available_enemy_ships):
        for x in range(10):
            for y in range(10):
                if self.board[x][y] is True:
                    left_top_x = max (0, x - 1)
                    right_bottom_x = min(10, x + 2)
                    left_top_y = max (0, y - 1)
                    right_bottom_y = min(10, y + 2)
                    around_cells = [[y_pos, x_pos] for x_pos in range(left_top_x, right_bottom_x) 
                                    for y_pos in range(left_top_y, right_bottom_y) if x_pos != x and y_pos != y]
                    
        


if __name__ == '__main__':
    # available_enemy_ships = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    available_enemy_ships = [1, 4]
    board = BoardImage()
    for [y, x] in [[3, 3]]:
        board.flood_enemy_deck(y, x, available_enemy_ships)
    print(available_enemy_ships)
    for i in range(10):
        print('\n')
        for j in range(10):
            print('{:>10}'.format(board.board[j][i]), end=" ")