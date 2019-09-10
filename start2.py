import curses
from curses import wrapper
from Helper import Helper

stdscr = curses.initscr()
stdscr.keypad(True)
curses.noecho()
curses.cbreak()
curses.curs_set(False)

# Keep track of cursor positions
cursor_positions = []

helper = Helper()

def main(stdscr):
    stdscr.clear()
    stdscr.addstr(helper.get_sentence(), curses.A_UNDERLINE)
    stdscr.move(0, 0)

    while True:
        key = stdscr.getkey()

        if (key == 'KEY_BACKSPACE'):
            if len(cursor_positions) < 1:
                continue

            process_backspace_result = helper.process_backspace()
            previous_pos = cursor_positions.pop()
            stdscr.move(previous_pos[0], previous_pos[1])
            pos = stdscr.getyx()

            if (process_backspace_result != ' '):
                stdscr.addstr(process_backspace_result, curses.A_UNDERLINE)
            else:
                stdscr.addstr(process_backspace_result)

            stdscr.move(pos[0], pos[1])
        else:
            pos = stdscr.getyx()
            cursor_positions.append(pos)

            process_key_result = helper.process_key(key)
            stdscr.addstr(key)

        curses.napms(10)

    
wrapper(main)

