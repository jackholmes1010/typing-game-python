import curses
import time
from curses import wrapper
from Helper import Helper
from Timer import Metrics


class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.helper = Helper()
        self.metrics = Metrics()
        self.cursor_positions = []
        self.incorrect_character_count = 0
        self.init_screen()
        self.init_curses()
        self.push_cursor_position()

    def init_curses(self):
        curses.noecho()
        curses.cbreak()
        curses.curs_set(True)
        curses.resize_term(100, 60)

    def init_screen(self):
        "Initialize screen."
        self.stdscr.keypad(True)
        self.stdscr.clear()
        self.stdscr.addstr(self.helper.get_sentence(), curses.A_LOW)
        self.stdscr.move(0, 0)

    def push_cursor_position(self):
        "Save current cursor position."
        self.position = self.stdscr.getyx()

    def pop_cursor_position(self):
        "Move to previous cursor position."
        self.stdscr.move(self.position[0], self.position[1])

    def move_cursor_to_previous_position(self):
        if (len(self.cursor_positions) > 0):
            previous_pos = self.cursor_positions.pop()
            self.stdscr.move(previous_pos[0], previous_pos[1])

    def main(self):
        while True:
            key = self.stdscr.getkey()

            if key == "KEY_BACKSPACE":
                if len(self.cursor_positions) < 1:
                    continue

                result = self.helper.process_backspace()
                self.move_cursor_to_previous_position()
                self.push_cursor_position()
                self.stdscr.addstr(result)
                self.pop_cursor_position()

                if self.incorrect_character_count > 0:
                    self.incorrect_character_count -= 1
            else:
                pos = self.stdscr.getyx()
                self.cursor_positions.append(pos)
                result = self.helper.process_key(key)

                if result == True and self.incorrect_character_count <= 0:
                    self.stdscr.addstr(key, curses.A_BOLD)
                    self.push_cursor_position()
                    current_cpm = self.metrics.current_cpm()
                    current_wpm = current_cpm / 5
                    self.stdscr.addstr(9, 0, "WPM: {}".format(current_wpm))
                    self.pop_cursor_position()

                    if self.helper.has_more_characters() == False:
                        overall_cpm = self.metrics.overall_cpm()
                        overall_wpm = overall_cpm / 5
                        self.stdscr.addstr(10, 0, "WPM: {}. Press any key to exit...".format(overall_wpm))
                        key = self.stdscr.getkey()
                        break
                else:
                    self.stdscr.addstr(key, curses.A_UNDERLINE)
                    self.incorrect_character_count += 1

            curses.napms(10)

def main(stdscr):
    game = Game(stdscr)
    game.main()

wrapper(main)
