import curses
import time
from curses import wrapper
from Helper import Helper
from Timer import Metrics

stdscr = curses.initscr()
stdscr.keypad(True)
curses.noecho()
curses.cbreak()
curses.curs_set(True)
curses.resize_term(100, 60)

class Positions:
    def push_cursor_position(self, stdscr):
        self.position = stdscr.getyx()

    def pop_cursor_position(self, stdscr):
        stdscr.move(self.position[0], self.position[1])

def main(stdscr):
    helper = Helper()
    positions = Positions()
    metrics = Metrics()
    cursor_positions = []
    incorrect_character_count = 0
    num_chars_typed = 0

    stdscr.clear()
    stdscr.addstr(helper.get_sentence(), curses.A_LOW)
    stdscr.move(0, 0)

    while True:
        key = stdscr.getkey()

        if key == "KEY_BACKSPACE":
            if len(cursor_positions) < 1:
                continue

            result = helper.process_backspace()
            previous_pos = cursor_positions.pop()
            stdscr.move(previous_pos[0], previous_pos[1])
            pos = stdscr.getyx()
            stdscr.addstr(result)
            stdscr.move(pos[0], pos[1])

            if incorrect_character_count > 0:
                incorrect_character_count -= 1
        else:
            pos = stdscr.getyx()
            cursor_positions.append(pos)
            result = helper.process_key(key)

            if result == True and incorrect_character_count <= 0:
                stdscr.addstr(key, curses.A_BOLD)
                num_chars_typed += 1

                positions.push_cursor_position(stdscr)
                current_cpm = metrics.current_cpm()
                current_wpm = current_cpm / 5
                stdscr.addstr(9, 0, "WPM: {}".format(current_wpm))
                positions.pop_cursor_position(stdscr)

                if helper.has_more_characters() == False:
                    overall_cpm = metrics.overall_cpm()
                    overall_wpm = overall_cpm / 5
                    stdscr.addstr(10, 0, "WPM: {}. Press any key to exit...".format(overall_wpm))
                    key = stdscr.getkey()
                    break
            else:
                stdscr.addstr(key, curses.A_UNDERLINE)
                incorrect_character_count += 1

        curses.napms(10)


wrapper(main)
