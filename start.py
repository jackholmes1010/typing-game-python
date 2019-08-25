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

    sentence = list('Hello world')
    sentence.reverse()
    next_char = sentence.pop()
    correctly_typed_character_count = 0
    incorrectly_typed_character_count = 0

    incorrect_progress_y = 6
    incorrect_progress_x = 6

    correct_progress_y = 5
    correct_progress_x = 6

    def update_incorrect_progress():
        (pos_y, pos_x) = stdscr.getyx()
        stdscr.move(incorrect_progress_y, incorrect_progress_x)
        stdscr.clrtoeol()
        stdscr.addstr('Incorrect: {}'.format(str(incorrectly_typed_character_count)))
        stdscr.move(pos_y, pos_x)

    def update_correct_progress():
        (pos_y, pos_x) = stdscr.getyx()
        stdscr.move(correct_progress_y, correct_progress_x)
        stdscr.clrtoeol()
        stdscr.addstr('Correct: {}'.format(str(correctly_typed_character_count)))
        stdscr.move(pos_y, pos_x)

    while True:
        key = stdscr.getkey()

        if (key == 'KEY_BACKSPACE'):
            if (len(positions) > 0):
                if (incorrectly_typed_character_count > 0):
                    incorrectly_typed_character_count -= 1
                    update_incorrect_progress()
                    (previous_pos_y, previous_pos_x) = positions.pop()
                    stdscr.delch(previous_pos_y, previous_pos_x)

        else:
            if (len(key) > 1):
                continue


            positions.append(stdscr.getyx())

            # Check if character was typed correctly
            if (incorrectly_typed_character_count == 0 and key == next_char):
                # All characters have been typed
                if (len(sentence) == 0):
                    break

                stdscr.addstr(key, curses.A_BOLD)
                next_char = sentence.pop()
                correctly_typed_character_count += 1
                update_correct_progress()
            else:
                stdscr.addstr(key, curses.A_UNDERLINE)
                incorrectly_typed_character_count += 1
                update_incorrect_progress()

        stdscr.refresh()

wrapper(main)
