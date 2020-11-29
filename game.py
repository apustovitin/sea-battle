import importlib
import curses
import board_image
from ship import Ship
from screen import Screen
import time
import random


class Game(Screen):
    def __init__(self, stdscr, file_name):
        super().__init__(stdscr, file_name)
        self.flooded_deck, self.aim_char, self.miss_char, self.deck_char = '□', '+', '*', '■'
        # self.is_break, self.is_restart  = self.place_player_ship(decks_number, self.deck_char)

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

    def place_player_ship(self, board_image, decks_number):
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
                if board_image.are_free_board_cells(ship):
                    board_image.add_ship_image(ship)
                    self.print_ship(ship, False)
                else:
                    self.print_ship_background(ship_background)
                    y_pos = x_pos = 0
                    continue
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

    def take_player_turn(self, computer_board):
        curses.curs_set(0)
        y_pos = x_pos = 0
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
                if not computer_board.board[x_pos][y_pos]:
                    computer_board.board[x_pos][y_pos] = not computer_board.board[x_pos][y_pos]
                    self.print_char_at_computer_board(y_pos, x_pos, self.flooded_deck)
                    if computer_board.check_win():
                        return self.win_action(False)
                    continue
                else:
                    self.print_char_at_computer_board(y_pos, x_pos, self.miss_char)
                    continue
                return False, False

    def win_action(self, computer_turn):
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

    def get_possible_deck_location(self, player_board_image, available_enemy_ships):
        possible_decks = [[y, x] for x in range(10) for y in range(10) if player_board_image.board[x][y] == 'possible']
        if not possible_decks:
            possible_decks = []
            available_enemy_ships_set = set(available_enemy_ships)
            empty_cells = player_board_image.get_empty_cells()
            for decks_number in available_enemy_ships_set:
                for is_gorizontal in (True, False):
                    for [y, x] in empty_cells:
                        ship = Ship(decks_number, y, x, is_gorizontal)
                        if player_board_image.are_free_board_cells(ship):
                            if [y, x] not in possible_decks:
                                possible_decks.append([y, x])
        return possible_decks

    def choise_computer_shoot_coordinate(self, player_board_image, available_enemy_ships):
        possible_cells = self.get_possible_deck_location(player_board_image, available_enemy_ships)
        last_possible_cell = None
        if len(possible_cells) == 1: last_possible_cell = possible_cells[0]
        return [random.choice(possible_cells), last_possible_cell]

    def take_computer_turn(self, player_board, player_board_image, available_enemy_ships):
        is_break = True
        while is_break:
            [y, x] = self.choise_computer_shoot_coordinate(player_board_image, available_enemy_ships)[0]
            last_possible_cell = self.choise_computer_shoot_coordinate(player_board_image, available_enemy_ships)[1]
            if not player_board.board[x][y]:
                player_board.board[x][y] = not player_board.board[x][y]
                player_board_image.flood_enemy_deck(y, x, available_enemy_ships)
                self.print_char_at_player_board(y, x, self.flooded_deck)
                if player_board.check_win():
                    return self.win_action(True)
            else:
                player_board_image.board[x][y] = 'ship_area'
                if last_possible_cell:
                    player_board_image.refresh_available_enemy_ships(last_possible_cell, available_enemy_ships)
                self.print_char_at_player_board(y, x, self.miss_char)
            while True:
                ch_input = self.stdscr.getch()
                if ch_input == ord('q') or ch_input == ord('Q'):
                    is_break = False
                    break
                elif ch_input == ord(' '):
                    break



def computer_ship_place_test():
    importlib.reload(board_image)
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
        importlib.reload(board_image)
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
    importlib.reload(board_image)
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
    importlib.reload(board_image)
    player_board = board_image.BoardImage()
    player_board_image = board_image.BoardImage()
    available_enemy_ships = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    game = Game(stdscr, ".\screen_layout.txt")
    game.print_screen_layout()
    for decks_number in available_enemy_ships:
        game.random_place_ship(player_board, decks_number)
    game.take_computer_turn(player_board, player_board_image, available_enemy_ships)
    print(available_enemy_ships)
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

