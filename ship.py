import board_image


class Ship:
    def __init__(self, decks_number, y, x, is_gorizontal=True):
        self.decks_number = decks_number
        self.is_gorizontal = is_gorizontal
        if is_gorizontal and x > (10 - decks_number):  # condition for ship is placed outside of board
            self.x = 10 - decks_number
            self.y = y
        elif not is_gorizontal and y > (10 - decks_number):  # condition for ship is placed outside of board
            self.y = 10 - decks_number
            self.x = x
        else:
            self.x = x
            self.y = y
        self.decks = self.build_ship_decks()
        self.ship_area = self.get_ship_area()

    def build_ship_decks(self):
        decks = []
        if self.is_gorizontal:
            for deck_number in range(self.decks_number):
                # deck stucture is [coordinates at board]
                decks.append([self.y, self.x + deck_number])
        else:
            for deck_number in range(self.decks_number):
                # deck structure is [coordinates at board]
                decks.append([self.y + deck_number, self.x])
        return decks

    def get_ship_area(self):
        # ship area is cells at board where only this ship can placed
        ship_area_left_top_y = max(0, self.decks[0][0] - 1)
        ship_area_right_bottom_y = min(10, self.decks[-1][0] + 2)
        ship_area_left_top_x = max(0, self.decks[0][1] - 1)
        ship_area_right_bottom_x = min(10, self.decks[-1][1] + 2)
        ship_area = [[y, x] for y in range(ship_area_left_top_y, ship_area_right_bottom_y) 
                     for x in range(ship_area_left_top_x, ship_area_right_bottom_x)]
        return ship_area


class UnknownShip:
    def __init__(self, unknown_ships, image_board):
        self.decks = []
        self.is_unknown = True
        self.ship_area = []
        self.possible_ship_area = []
        self.unknown_ships = unknown_ships
        self.image_board = image_board

    def check_unknown(self):
        if self.decks and not self.possible_ship_area and self.is_unknown:
            self.image_board.add_flooded_ship_image(self)
            self.unknown_ships.pop(self.unknown_ships.index(len(self.decks)))
            self.is_unknown = False

    def check_other_ship_area(self, y_pos, x_pos):
        if self.image_board.board[x_pos][y_pos] == 'ship_area':
            return True
        return False

    def update_possible_ship_area(self, y, x):
        if [y, x] in self.decks and len(self.decks) > 1 and [y, x] in self.possible_ship_area:
            self.possible_ship_area.pop(self.possible_ship_area.index([y, x]))
        # linear cells around enemy deck
        linear_cells_around_deck = [[y - 1, x], [y + 1, x], [y, x - 1], [y, x + 1]]
        for [y_pos, x_pos] in linear_cells_around_deck:
            # if coordinates inside board and not in ship area and not decks
            if 0 <= x_pos <= 9 and 0 <= y_pos <= 9 and [y_pos, x_pos] not in self.ship_area \
                    and [y_pos, x_pos] not in self.decks and self.check_other_ship_area(y_pos, x_pos):
                self.ship_area.append([y_pos, x_pos])
            if 0 <= x_pos <= 9 and 0 <= y_pos <= 9 and [y_pos, x_pos] not in self.ship_area \
                    and [y_pos, x_pos] not in self.decks and not self.check_other_ship_area(y_pos, x_pos):
                self.possible_ship_area.append([y_pos, x_pos])

    def update_ship_area(self, y, x):
        # diagonal cells around enemy deck are enemy ship area
        diagonal_cells_around_deck = [[y - 1, x - 1], [y - 1, x + 1], [y + 1, x - 1], [y + 1, x + 1]]
        for [y_pos, x_pos] in diagonal_cells_around_deck:
            if 0 <= x_pos <= 9 and 0 <= y_pos <= 9:  # if coordinates inside board
                self.ship_area.append([y_pos, x_pos])
                if [y_pos, x_pos] in self.possible_ship_area:
                    self.possible_ship_area.pop(self.possible_ship_area.index([y_pos, x_pos]))
                    self.check_unknown()

    def change_possible_ship_area(self, y, x):
        self.ship_area.append([y, x])
        self.possible_ship_area.pop(self.possible_ship_area.index([y, x]))
        self.check_unknown()

    def remove_possible_ship_area(self):
        self.decks = sorted(self.decks)
        for [y, x] in self.possible_ship_area:
            self.ship_area.append([y, x])
        self.possible_ship_area = []
        self.check_unknown()

    def flood_deck(self, y, x):
        self.decks.append([y, x])
        self.update_ship_area(y, x)
        self.update_possible_ship_area(y, x)
        self.check_unknown()
        # if there are not ships longer than current
        if self.is_unknown and max(self.unknown_ships) == len(self.decks):
            self.remove_possible_ship_area()

    def update_ship_when_miss(self, y, x):
        if [y, x] in self.possible_ship_area:
            self.change_possible_ship_area(y, x)


def test_ship():
    for i in range(0, 10):
        print(f'Ship start at {i}, {i}')
        for deck_number in range(1, 5):
            ship_cur = Ship(deck_number, i, i, deck_number % 2)
            print(f'decks_number: {ship_cur.decks_number}, y: {ship_cur.y}, x: {ship_cur.x},\
            is_gorizontal: {ship_cur.is_gorizontal}, decks: {ship_cur.decks}, ship_area: {ship_cur.ship_area}')


def test_unknown_ship():
    unknown_ships = [1, 2, 3]
    image_board = board_image.BoardImage()
    unknown_ship = UnknownShip(unknown_ships, image_board)
    image_board.board[1][0] = 'ship_area'
    image_board.board[1][2] = 'ship_area'
    image_board.board[0][1] = 'ship_area'
    image_board.board[2][1] = 'ship_area'
    for [y, x] in [[1, 1]]:
        unknown_ship.flood_deck(y, x)
        print(unknown_ships)
        print(f'decks: {unknown_ship.decks}')
        print(f'ship_area: {unknown_ship.ship_area}')
        print(f'possible_ship_area: {unknown_ship.possible_ship_area}')
        print(f'is_unknown: {unknown_ship.is_unknown}')
    for i in range(10):
        print('\n')
        for j in range(10):
            print('{:>10}'.format(image_board.board[j][i]), end=" ")


if __name__ == '__main__':
    test_unknown_ship()
