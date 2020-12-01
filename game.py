import curses
import board_image
from ship import Ship, UnknownShip
from screen import Screen
import random


class Game(Screen):
    def __init__(self, stdscr, file_name, unknown_ships, computer_board, player_board, player_board_image):
        super().__init__(stdscr, file_name)
        self.flooded_deck_char, self.aim_char, self.miss_char, self.deck_char = '□', '+', '*', '■'
        self.unknown_ships = unknown_ships
        self.computer_board = computer_board
        self.player_board = player_board
        self.player_board_image = player_board_image
        self.unknown_ship = UnknownShip(unknown_ships, player_board_image)
        self.player_aim_coordinate_y, self.player_aim_coordinate_x = 0, 0

    def print_ship_background(self, ship_background):
        for [y, x, char] in ship_background:
            self.stdscr.addch(y, x, char)
            self.stdscr.refresh()

    def print_ship(self, ship, is_blink):
        for [y_pos, x_pos] in ship.decks:
            y = self.player_board_start_y + y_pos * self.step_y
            x = self.player_board_start_x + x_pos * self.step_x
            self.stdscr.addch(y, x, self.deck_char, curses.A_BLINK if is_blink else 0)
            self.stdscr.refresh()

    def get_ship_background(self, ship):
        ship_background = []
        for [y_pos, x_pos] in ship.decks:
            y = self.player_board_start_y + y_pos * self.step_y
            x = self.player_board_start_x + x_pos * self.step_x
            ship_background.append([y, x, chr(self.stdscr.inch(y, x))])
            self.stdscr.refresh()
        return ship_background

    def place_player_ship(self, decks_number):
        curses.curs_set(0)
        y_pos = x_pos = 0
        is_gorizontal = True
        while True:
            ship = Ship(decks_number, y_pos, x_pos, is_gorizontal)
            ship_background = self.get_ship_background(ship)
            self.print_ship(ship, True)
            ch_input = self.stdscr.getch()
            if ch_input == curses.KEY_UP:
                self.print_ship_background(ship_background)
                y_pos = max(0, y_pos - 1)
            elif ch_input == curses.KEY_DOWN:
                self.print_ship_background(ship_background)
                if is_gorizontal:
                    y_pos = min(9, y_pos + 1)
                else:
                    y_pos = min(10 - decks_number, y_pos + 1)
            elif ch_input == curses.KEY_LEFT:
                self.print_ship_background(ship_background)
                x_pos = max(0, x_pos - 1)
            elif ch_input == curses.KEY_RIGHT:
                self.print_ship_background(ship_background)
                if is_gorizontal:
                    x_pos = min(10 - decks_number, x_pos + 1)
                else:
                    x_pos = min(9, x_pos + 1)
            elif ch_input == ord('d') or ch_input == ord('D'):
                self.print_ship_background(ship_background)
                is_gorizontal = not is_gorizontal
                y_pos = x_pos = 0
            elif ch_input == ord('q') or ch_input == ord('Q'):
                return True, False
            elif ch_input == ord('r') or ch_input == ord('R'):
                return False, True
            elif ch_input == ord(' '):
                if self.player_board.are_free_board_cells(ship):
                    self.player_board.add_ship_image(ship)
                    self.print_ship(ship, False)
                else:
                    self.print_ship_background(ship_background)
                    y_pos = x_pos = 0
                    continue
                return False, False

    def place_player_ships(self):
        self.print_message("Place your ships.")
        for decks_number in self.unknown_ships:
            is_break, is_restart = self.place_player_ship(decks_number)
            if is_break or is_restart: 
                return is_break, is_restart
        return False, False

    def get_ship_possible_parameters(self, board_image, decks_number):
        possible_parameters = []
        empty_cells = board_image.get_empty_cells()
        for is_gorizontal in (True, False):
            for [y, x] in empty_cells:
                ship = Ship(decks_number, y, x, is_gorizontal)
                if board_image.are_free_board_cells(ship):
                    if [ship.y, ship.x, is_gorizontal] not in possible_parameters:
                        possible_parameters.append([ship.y, ship.x, is_gorizontal])
        return possible_parameters

    def random_place_ship(self, board_image, decks_number):
        possible_parameters = self.get_ship_possible_parameters(board_image, decks_number)
        [y, x, is_gorizontal] = random.choice(possible_parameters)
        ship = Ship(decks_number, y, x, is_gorizontal)
        board_image.add_ship_image(ship)

    def place_computer_ships(self):
        for decks_number in self.unknown_ships:
            self.random_place_ship(self.computer_board, decks_number)

    def print_aim_background(self, aim_background):
        self.stdscr.addch(*aim_background)
        self.stdscr.refresh()

    def print_char_at_computer_board(self, y_pos, x_pos, char):
            y = self.computer_board_start_y + y_pos * self.step_y
            x = self.computer_board_start_x + x_pos * self.step_x
            self.stdscr.addch(y, x, char)
            self.stdscr.refresh()

    def get_aim_background_from_computer_board(self, y_pos, x_pos):
        y = self.computer_board_start_y + y_pos * self.step_y
        x = self.computer_board_start_x + x_pos * self.step_x
        return [y, x, chr(self.stdscr.inch(y, x))]

    def player_move(self):
        self.print_message("Player move now.")
        y_pos, x_pos = self.player_aim_coordinate_y, self.player_aim_coordinate_x
        while True:
            aim_background = self.get_aim_background_from_computer_board(y_pos, x_pos)
            self.print_char_at_computer_board(y_pos, x_pos, self.aim_char)
            ch_input = self.stdscr.getch()
            if ch_input == curses.KEY_UP:
                self.print_aim_background(aim_background)
                y_pos = max(0, y_pos - 1)
            elif ch_input == curses.KEY_DOWN:
                self.print_aim_background(aim_background)
                y_pos = min(9, y_pos + 1)
            elif ch_input == curses.KEY_LEFT:
                self.print_aim_background(aim_background)
                x_pos = max(0, x_pos - 1)
            elif ch_input == curses.KEY_RIGHT:
                self.print_aim_background(aim_background)
                x_pos = min(9, x_pos + 1)
            elif ch_input == ord('q') or ch_input == ord('Q'):
                return True, False
            elif ch_input == ord('r') or ch_input == ord('R'):
                return False, True
            elif ch_input == ord(' '):
                self.player_aim_coordinate_y, self.player_aim_coordinate_x = y_pos, x_pos
                if not self.computer_board.board[x_pos][y_pos]:
                    self.computer_board.board[x_pos][y_pos] = not self.computer_board.board[x_pos][y_pos]
                    self.print_char_at_computer_board(y_pos, x_pos, self.flooded_deck_char)
                    if self.computer_board.check_win():
                        is_break, is_restart = self.win_action(False)
                        return is_break, is_restart
                    continue
                else:
                    self.print_char_at_computer_board(y_pos, x_pos, self.miss_char)
                    return False, False

    def win_action(self, computer_turn):
        self.print_message(" ")
        winner = "COMPUTER" if computer_turn else "PLAYER"
        self.print_winner(winner)
        while True:
            ch_input = self.stdscr.getch()
            if ch_input == ord('q') or ch_input == ord('Q'):
                return True, False
            elif ch_input == ord('r') or ch_input == ord('R'):
                return False, True

    def print_char_at_player_board(self, y_pos, x_pos, char):
            y = self.player_board_start_y + y_pos * self.step_y
            x = self.player_board_start_x + x_pos * self.step_x
            self.stdscr.addch(y, x, char)
            self.stdscr.refresh()

    def choise_computer_shoot_coordinate(self):
        if self.unknown_ship.possible_ship_area:
            possible_decks = self.unknown_ship.possible_ship_area
        else:
            possible_decks = []
            unknown_ships_set = set(self.unknown_ships)
            empty_cells = self.player_board_image.get_empty_cells()
            for decks_number in unknown_ships_set:
                for is_gorizontal in (True, False):
                    for [y, x] in empty_cells:
                        ship = Ship(decks_number, y, x, is_gorizontal)
                        if self.player_board_image.are_free_board_cells(ship):
                            if [y, x] not in possible_decks:
                                possible_decks.append([y, x])
        return random.choice(possible_decks)

    def check_unknown_ship(self):
        if not self.unknown_ship.is_unknown:
            self.unknown_ships = self.unknown_ship.unknown_ships
            self.player_board_image = self.unknown_ship.image_board
            self.unknown_ship = UnknownShip(self.unknown_ships, self.player_board_image)

    def computer_move(self):
        self.print_message("Computer move now.")
        while True:
            curses.napms(1000)
            [y, x] = self.choise_computer_shoot_coordinate()
            if not self.player_board.board[x][y]:
                self.player_board.board[x][y] = not self.player_board.board[x][y]
                self.check_unknown_ship()
                self.unknown_ship.flood_deck(y, x)
                self.print_char_at_player_board(y, x, self.flooded_deck_char)
                if self.player_board.check_win():
                    is_break, is_restart = self.win_action(True)
                    return is_break, is_restart
                continue
            else:
                self.player_board_image.board[x][y] = 'ship_area'
                self.unknown_ship.update_ship_when_miss(y, x)
                self.print_char_at_player_board(y, x, self.miss_char)
                return False, False


def computer_ship_place_test():
    computer_own_board = board_image.BoardImage()
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    screen = Screen(stdscr, ".\screen_layout.txt")
    game = Game(screen)
    for decks_number in [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
        game.random_place_ship(computer_own_board, decks_number)
    for i in range(10):
        print('\n')
        for j in range(10):
            print('{:>10}'.format(computer_own_board.board[j][i]), end=" ")


def player_ship_place_test():
    while True:
        player_own_board = board_image.BoardImage()
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        screen = Screen(stdscr, ".\screen_layout.txt")
        screen.print_screen_layout()
        game = Game(screen)
        for decks_number in [1, 2, 3, 4]:
            is_break, is_restart = game.place_player_ship(player_own_board, decks_number)
            if is_break or is_restart: break
        if is_break: break
        if is_restart: continue
        break
    curses.endwin()
    for i in range(10):
        print('\n')
        for j in range(10):
            print('{:>10}'.format(player_own_board.board[j][i]), end=" ")


def player_turn_test():
    computer_own_board = board_image.BoardImage()
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    game = Game(stdscr, ".\screen_layout.txt")
    game.print_screen_layout()
    for decks_number in [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
        game.random_place_ship(computer_own_board, decks_number)
    game.take_player_turn(computer_own_board)
    for i in range(10):
        print('\n')
        for j in range(10):
            print('{:>10}'.format(computer_own_board.board[j][i]), end=" ")


def computer_turn_test():
    player_board = board_image.BoardImage()
    player_board_image = board_image.BoardImage()
    unknown_ships = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(True)
    game = Game(stdscr, ".\screen_layout.txt", unknown_ships, player_board_image)
    game.print_screen_layout()
    for decks_number in unknown_ships:
        game.random_place_ship(player_board, decks_number)
    game.take_computer_turn(player_board)
    print(unknown_ships)
    for i in range(10):
        print('\n')
        for j in range(10):
            print('{:>10}'.format(player_board_image.board[j][i]), end=" ")
    for i in range(10):
        print('\n')
        for j in range(10):
            print('{:>10}'.format(player_board.board[j][i]), end=" ")


if __name__ == '__main__':
    # computer_ship_place_test()
    # player_ship_place_test()
    # player_turn_test()
    computer_turn_test()

