import curses
import random
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
        self.bubble_frame_index = 0
        self.init_screen()
        self.init_curses()
        self.push_cursor_position()

    def init_curses(self):
        curses.noecho()
        curses.cbreak()
        curses.curs_set(True)

    def init_screen(self):
        self.stdscr.keypad(True)
        self.stdscr.clear()

    def push_cursor_position(self):
        "Save current cursor position."
        cursor_position = self.stdscr.getyx()
        self.stdscr.move(cursor_position[0], cursor_position[1])
        self.cursor_positions.append(cursor_position)

    def pop_cursor_position(self):
        "Move to previous cursor position."
        if len(self.cursor_positions) > 0:
            previous_cursor_position = self.cursor_positions.pop()
            # Displaying the bubbles is a hack fix for the bug where holding 
            # backspace causes the cursor to get stuck at the beginning of 
            # the previous line. I don't know why this works but it does... ¯\_(ツ)_/¯
            self.stdscr.addstr(10, 0, self.get_next_bubble_animation_frame())
            self.stdscr.move(previous_cursor_position[0], previous_cursor_position[1])

    def get_next_bubble_animation_frame(self):
        "Return the next frame of a bubble animation sequence."
        bubbles = [".", "o", "O", "@", "*"]
        self.bubble_frame_index += 1

        if self.bubble_frame_index >= len(bubbles):
            self.bubble_frame_index = 0

        return bubbles[self.bubble_frame_index]

    def play_start_animation(self):
        "Play the WPPM animation and clear the screen when finished."
        frames = [
            ":::       :::::::::::: :::::::::   :::   :::",
            "+:       :+::+:    :+::+:    :+: :+:+: :+:+:",
            ":+       +:++:+    +:++:+    +:++:+ +:+:+ +:+",
            "#+  +:+  +#++#++:++#+ +#++:++#+ +#+  +:+  +#+",
            "+ +#+#+ +#++#+       +#+       +#+       +#+",
            "#+#+# #+#+# #+#       #+#       #+#       #+#",
            "###   ###  ###       ###       ###       ###",
        ]

        curses.curs_set(False)

        (max_y, max_x) = self.stdscr.getmaxyx()
        start_y = int(max_y / 2) - 5
        start_x = int(max_x / 2) - 30

        for i in range(len(frames)):
            curses.napms(50)
            self.stdscr.addstr(start_y + i, start_x, frames[i])
            self.stdscr.refresh()

        (y, _x) = self.stdscr.getyx()

        for i in range(43):
            self.stdscr.addstr(y + 1, start_x + i, "::")
            self.stdscr.refresh()
            curses.napms(5)

        curses.napms(300)
        curses.curs_set(True)
        self.stdscr.clear()

    def start_game_loop(self):
        "Start main game loop."

        self.stdscr.addstr(self.game_state.get_sentence(), curses.A_LOW)
        self.stdscr.move(0, 0)

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
                    self.stdscr.addstr(10, 2, "WPM: {}".format(current_wpm))
                    self.pop_cursor_position()

                    if self.game_state.has_more_characters() == False:
                        overall_wpm = self.metrics_counter.overall_wpm()
                        self.stdscr.addstr(
                            10,
                            2,
                            "WPM: {}. Press any key to exit...".format(overall_wpm),
                        )
                        key = self.stdscr.getkey()
                        break
                else:
                    self.stdscr.addstr(key, curses.A_UNDERLINE)

            curses.napms(10)


def main(stdscr):
    game = Game(stdscr)
    game.play_start_animation()
    game.start_game_loop()


wrapper(main)
