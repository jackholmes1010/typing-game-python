import curses
from curses import wrapper

stdscr = curses.initscr()
stdscr.keypad(True)
curses.noecho()
curses.cbreak()
curses.curs_set(True)

def main(stdscr):
    # Clear the screen
    stdscr.clear()

    stdscr.refresh()

    # Add a string
    # stdscr.addstr('this is a sample string lelelelele')

    # # Move cursor
    # stdscr.move(10, 10)

    # stdscr.addstr('i have moved')

    # stdscr.getkey()

    while True:
        key = stdscr.getkey()

        if (key == 'KEY_BACKSPACE'):
            stdscr.delch(0, 0)
        else:
            stdscr.addstr(key)

        stdscr.refresh()

wrapper(main)
