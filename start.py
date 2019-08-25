import curses
from curses import wrapper

stdscr = curses.initscr()
stdscr.keypad(True)
curses.noecho()
curses.cbreak()
curses.curs_set(False)

def main(stdscr):
    # Clear the screen
    stdscr.clear()

    # Keep track of (y, x) coordinates
    positions = []

    while True:
        key = stdscr.getkey()

        if (key == 'KEY_BACKSPACE'):
            if (len(positions) > 0):
                (previous_pos_y, previous_pos_x) = positions.pop()
                stdscr.delch(previous_pos_y, previous_pos_x)
        else:
            positions.append(stdscr.getyx())
            stdscr.addstr(key)

        stdscr.refresh()

wrapper(main)
