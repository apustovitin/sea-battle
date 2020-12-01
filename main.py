import curses
import board_image
from game import Game
import random


def moves_loop(game):
    if random.choice([False, True]):
        is_break, is_restart = game.computer_move()
        if is_break or is_restart:
            return is_break, is_restart
    while True:
        is_break, is_restart = game.player_move()
        if is_break or is_restart:
            return is_break, is_restart
        is_break, is_restart = game.computer_move()
        if is_break or is_restart:
            return is_break, is_restart


def game_loop(stdscr):
    unknown_ships = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    while True:
        stdscr.clear()
        computer_board = board_image.BoardImage()
        player_board = board_image.BoardImage()
        player_board_image = board_image.BoardImage()
        game = Game(stdscr, ".\screen_layout.txt", unknown_ships, computer_board, player_board, player_board_image)
        game.place_computer_ships()
        game.print_screen_layout()
        is_break, is_restart = game.place_player_ships()
        if is_break:
            break
        if is_restart:
            continue
        is_break, is_restart = moves_loop(game)
        if is_break:
            break
        if is_restart:
            continue


def main():
    stdscr = curses.initscr()
    stdscr.clear()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(True)
    game_loop(stdscr)
    curses.endwin()


if __name__ == '__main__':
    main()
