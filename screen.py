import curses
import re
from read_file import ReadFile


class Screen:
    def __init__(self, stdscr, file_name):
        self.stdscr = stdscr
        self.file_name = file_name
        [self.center_y, self.center_x] = self.set_center_coordinates()
        self.screen_layout = self.set_screen_layout()
        [self.step_y, self.step_x] = self.set_step()
        [self.player_board_start_y, self.player_board_start_x] = self.set_player_board_start_cell()
        [self.computer_board_start_y, self.computer_board_start_x] = self.set_computer_board_start_cell()
        self.end_of_layout_y = self.set_end_of_layout_y()

    def set_center_coordinates(self) -> list:
        # calculates coordinates of central point of screen
        # Coordinate y counts from top of screen and coordinate x counts from left of screen
        maxy, maxx = self.stdscr.getmaxyx()
        return [maxy // 2, maxx // 2]

    def set_screen_layout(self):
        # Set screen layout that will be drawn by curses
        # It is main game screen
        screen_layout = ReadFile(self.file_name)
        return screen_layout.get_content()

    def set_step(self):
        y = 0
        was_border = False
        for row in self.screen_layout:
            if re.findall(r'.*┼.+', row) and was_border:
                break
            elif re.findall(r'.*┼.+', row) and not was_border:
                was_border = True
                x = len(re.findall(r'.*(┼─+)┼.*', row)[0])
            if was_border:
                y += 1
        return [y, x]

    def set_player_board_start_cell(self):
        y = 0
        layout_center_y = len(self.screen_layout) // 2
        for row in self.screen_layout:
            y += 1
            if re.findall(r'───┼.+', row):
                x = self.center_x - len(row) // 2 + len(re.findall(r'(───┼).+', row)[0]) - 1 - self.step_x // 2
                y = y - 1 - self.step_y // 2 - layout_center_y + self.center_y
                # coordinates of left top corner of player's board.
                # Coordinate y counts from top of screen and coordinate x counts from left of screen
                return [y, x]

    def set_computer_board_start_cell(self):
        y = 0
        layout_center_y = len(self.screen_layout) // 2
        for row in self.screen_layout:
            y += 1
            if re.findall(r'.+ ───┼.+', row):
                x = len(re.findall(r'(.+ ───┼).+', row)[0]) - 1 - self.step_x // 2 - len(row) // 2 + self.center_x
                y = y - 1 - self.step_y // 2 - layout_center_y + self.center_y
                # coordinates of left top corner of player's board.
                # Coordinate y counts from top of screen and coordinate x counts from left of screen
                return [y, x]

    def set_end_of_layout_y(self):
        layout_center_y = len(self.screen_layout) // 2
        return self.center_y + layout_center_y

    def print_screen_layout(self):
        # draws screen layout at center
        y_offset = self.center_y - len(self.screen_layout) // 2
        for row in self.screen_layout:
            self.stdscr.addstr(y_offset, self.center_x - len(row) // 2, row)
            y_offset += 1

    def print_winner(self, winner):
        message = winner + " IS WIN!"
        self.stdscr.addstr(self.end_of_layout_y + 1, self.center_x - len(message) // 2, message)
        
    def print_diagnostic_message(self, message):
        self.stdscr.move(self.end_of_layout_y + 2, 0)
        self.stdscr.clrtoeol()
        self.stdscr.refresh()
        self.stdscr.addstr(self.end_of_layout_y + 2, self.center_x - len(message) // 2, message)
        self.stdscr.refresh()


if __name__ == '__main__':
    deck = '■'
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    screen = Screen(stdscr, ".\screen_layout.txt")
    screen.print_screen_layout()
    curses.curs_set(0)
    y_pos = x_pos = 0
    while True:
        stdscr.addch(screen.player_board_start_y + y_pos * screen.step_y, 
                     screen.player_board_start_x + x_pos * screen.step_x, deck, curses.A_BLINK)
        ch_input = stdscr.getch()
        if ch_input == curses.KEY_UP:
            stdscr.addch(screen.player_board_start_y + y_pos * screen.step_y, 
                         screen.player_board_start_x + x_pos * screen.step_x, " ")
            y_pos = max(0, y_pos - 1)
        elif ch_input == curses.KEY_DOWN:
            stdscr.addch(screen.player_board_start_y + y_pos * screen.step_y, 
                         screen.player_board_start_x + x_pos * screen.step_x, " ")
            y_pos = min(9, y_pos + 1)
        elif ch_input == curses.KEY_LEFT:
            stdscr.addch(screen.player_board_start_y + y_pos * screen.step_y, 
                         screen.player_board_start_x + x_pos * screen.step_x, " ")
            x_pos = max(0, x_pos - 1)
        elif ch_input == curses.KEY_RIGHT:
            stdscr.addch(screen.player_board_start_y + y_pos * screen.step_y, 
                         screen.player_board_start_x + x_pos * screen.step_x, " ")
            x_pos = min(9, x_pos + 1)
        elif ch_input == ord('q') or ch_input == ord('Q'):
            break
        elif ch_input == ord('r') or ch_input == ord('R'):
            break        
    # for i in range(10):
    #     stdscr.addch(start_y + i * step_y, start_x + i * step_x, deck)
    #     stdscr.refresh()
    #     time.sleep(1)
    #     stdscr.addch(start_y + i * step_y, start_x + i * step_x, " ")
    #     stdscr.refresh()
    # [start_y, start_x] = screen.player_board_start_cell
    # for i in range(10):
    #     stdscr.addch(start_y + i * step_y, start_x + i * step_x, deck)
    #     stdscr.refresh()
    #     time.sleep(1)
    #     stdscr.addch(start_y + i * step_y, start_x + i * step_x, " ")
    #     stdscr.refresh()
    stdscr.move(screen.end_of_layout_y, screen.center_x)
    curses.curs_set(1)
    stdscr.getkey()
