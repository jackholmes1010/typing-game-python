import curses
import time
from curses import wrapper
from GameState import GameState
from MetricsCounter import MetricsCounter


class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.game_state = GameState()
        self.metrics_counter = MetricsCounter()
        self.cursor_positions = []
        self.init_screen()
        self.init_curses()
        self.push_cursor_position()

    def init_curses(self):
        curses.noecho()
        curses.cbreak()
        curses.curs_set(True)
        curses.resize_term(100, 60)

    def init_screen(self):
        self.stdscr.keypad(True)
        self.stdscr.clear()
        self.stdscr.addstr(self.game_state.get_sentence(), curses.A_LOW)
        self.stdscr.move(0, 0)

    def push_cursor_position(self):
        "Save current cursor position."
        cursor_position = self.stdscr.getyx()
        self.cursor_positions.append(cursor_position)

    def pop_cursor_position(self):
        "Move to previous cursor position."
        if len(self.cursor_positions) > 0:
            previous_cursor_position = self.cursor_positions.pop()
            self.stdscr.move(previous_cursor_position[0], previous_cursor_position[1])

    def start_game_loop(self):
        "Start main game loop."
        while True:
            key = self.stdscr.getkey()

            if key == "KEY_BACKSPACE":
                if len(self.cursor_positions) < 1:
                    continue

                result = self.game_state.process_backspace()
                self.pop_cursor_position()
                self.push_cursor_position()
                self.stdscr.addstr(result)
                self.pop_cursor_position()
            else:
                self.push_cursor_position()

                result = self.game_state.process_key(key)

                if result == True:
                    self.stdscr.addstr(key, curses.A_BOLD)
                    self.push_cursor_position()
                    current_wpm = self.metrics_counter.current_wpm()
                    self.stdscr.addstr(10, 0, "WPM: {}".format(current_wpm))
                    self.pop_cursor_position()

                    if self.game_state.has_more_characters() == False:
                        overall_wpm = self.metrics_counter.overall_wpm()
                        self.stdscr.addstr(
                            10,
                            0,
                            "WPM: {}. Press any key to exit...".format(overall_wpm),
                        )
                        key = self.stdscr.getkey()
                        break
                else:
                    self.stdscr.addstr(key, curses.A_UNDERLINE)

            curses.napms(10)


def main(stdscr):
    game = Game(stdscr)
    game.start_game_loop()


wrapper(main)
