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

    typed_str = ''

    while True:
        key = stdscr.getkey()

        if (key == 'KEY_BACKSPACE'):
           typed_str = typed_str[:-1]
        else:
            typed_str += key

        stdscr.clear()
        stdscr.addstr(5, 5, typed_str)
        stdscr.refresh()

wrapper(main)
