class Ship:
    def __init__(self, decks_number, y, x, is_gorizontal=True):
        self.decks_number = decks_number
        self.is_gorizontal = is_gorizontal
        if is_gorizontal and x > (10 - decks_number): # condition for ship is placed outside of board
            self.x = 10 - decks_number
            self.y = y
        elif not is_gorizontal and y > (10 - decks_number): # condition for ship is placed outside of board
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


if __name__ == '__main__':
    for i in range(0,10):
        print(f'Ship start at {i}, {i}')
        for deck_number in range(1,5):
            ship_cur = Ship(deck_number, i, i, deck_number % 2)
            print(f'decks_number: {ship_cur.decks_number}, y: {ship_cur.y}, x: {ship_cur.x},\
            is_gorizontal: {ship_cur.is_gorizontal}, decks: {ship_cur.decks}, ship_area: {ship_cur.ship_area}')
