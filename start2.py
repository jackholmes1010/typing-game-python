import curses
from curses import wrapper
from Helper import Helper

stdscr = curses.initscr()
stdscr.keypad(True)
curses.noecho()
curses.cbreak()
curses.curs_set(True)
curses.resize_term(100, 50)

# Keep track of cursor positions
cursor_positions = []

helper = Helper()


def main(stdscr):
    stdscr.clear()
    stdscr.addstr(helper.get_sentence(), curses.A_LOW)

    while True:
        key = stdscr.getkey()

        if key == "KEY_BACKSPACE":
            if len(cursor_positions) < 1:
                continue

            process_backspace_result = helper.process_backspace()
            previous_pos = cursor_positions.pop()
            stdscr.move(previous_pos[0], previous_pos[1])
            pos = stdscr.getyx()

            if process_backspace_result != " ":
                stdscr.addstr(process_backspace_result)
            else:
                stdscr.addstr(process_backspace_result)

            stdscr.move(pos[0], pos[1])
        else:
            pos = stdscr.getyx()
            cursor_positions.append(pos)
            process_key_result = helper.process_key(key)

            if process_key_result == True:
                stdscr.addstr(key, curses.A_BOLD)
            else:
                stdscr.addstr(key, curses.A_UNDERLINE)

        curses.napms(10)


wrapper(main)
