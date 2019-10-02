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
        "Curses module setup."
        curses.noecho()
        curses.cbreak()
        curses.curs_set(True)

    def init_screen(self):
        "Initial screen setup."
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
            self.add_str(self.get_next_bubble_animation_frame(), y=10, x=0)
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
            "    :::       ::::::::::::   :::   :::",
            "   :+:       :+::+:    :+: :+:+: :+:+:",
            "  +:+       +:++:+    +:++:+ +:+:+ +:+",
            " +#+  +:+  +#++#++:++#+ +#+  +:+  +#+",
            "+#+ +#+#+ +#++#+       +#+       +#+",
            "#+#+# #+#+# #+#       #+#       #+#",
            "###   ###  ###       ###       ###",
        ]

        curses.curs_set(False)

        (max_y, max_x) = self.stdscr.getmaxyx()
        start_y = int(max_y / 2) - 5
        start_x = int(max_x / 2) - 30

        for i in range(len(frames)):
            curses.napms(70)
            self.add_str(frames[i], y=start_y + i, x=start_x)
            self.stdscr.refresh()

        (y, _x) = self.stdscr.getyx()

        for i in range(33):
            curses.napms(20)
            self.add_str("::", y=y + 1, x=start_x + i)
            self.stdscr.refresh()

        self.add_str("Press any key to start", y=y + 2, x=start_x + 6)
        self.stdscr.getkey()
        curses.curs_set(True)
        self.stdscr.clear()

    def update_current_wpm(self, correctly_typed=True):
        "Update current WPM display."
        if correctly_typed:
            self.metrics_counter.increment_correct_character_count()

        current_wpm = self.metrics_counter.current_wpm()
        self.add_str("WPM: {}".format(current_wpm), y=10, x=2, move_cursor=False)

    def display_overall_wpm(self):
        "Update overall WPM display."
        overall_wpm = self.metrics_counter.overall_wpm()
        self.add_str("WPM: {}. Press any key to exit...".format(overall_wpm), y=10, x=2)
        self.stdscr.getkey()

    def add_str(self, text, y=None, x=None, attr=curses.A_NORMAL, move_cursor=True):
        "Paint text to the screen."
        if move_cursor == False:
            self.push_cursor_position()

        if x != None and y != None:
            self.stdscr.addstr(y, x, text, attr)
        else:
            self.stdscr.addstr(text, attr)

        if move_cursor == False:
            self.pop_cursor_position()

    def start_game_loop(self):
        "Start main game loop."
        self.add_str(self.game_state.get_sentence(), attr=curses.A_LOW)
        self.stdscr.move(0, 0)

        while True:
            key = self.stdscr.getkey()

            if key == "KEY_BACKSPACE" or key == '\x7f':
                if len(self.cursor_positions) < 1:
                    continue

                result = self.game_state.process_backspace()

                # Move cursor back to previous position
                self.pop_cursor_position()

                self.add_str(result, move_cursor=False)
                self.update_current_wpm(correctly_typed=False)
            elif len(key) == 1:
                if (key == '\n'):
                    continue

                result = self.game_state.process_key(key)

                # Save current cursor position to support backspacing
                self.push_cursor_position()

                if result == True:
                    self.add_str(key, attr=curses.A_BOLD)
                    self.update_current_wpm(correctly_typed=True)

                    if self.game_state.has_more_characters() == False:
                        self.display_overall_wpm()
                        break
                else:
                    self.update_current_wpm(correctly_typed=False)
                    self.add_str(key, attr=curses.A_UNDERLINE)

            curses.napms(10)


def main(stdscr):
    game = Game(stdscr)
    game.play_start_animation()
    game.start_game_loop()


wrapper(main)
