import curses
from curses import wrapper
from Sentence import Sentence

stdscr = curses.initscr()
stdscr.keypad(True)
curses.noecho()
curses.cbreak()
curses.curs_set(False)


def main(stdscr):
    # Clear the screen
    stdscr.clear()

    # Keep track of (y, x) coordinates
    cursor_positions = []

    # Generate sentence to type
    sentence = Sentence()

    # State indicates if there are incorrectly typed characters on screen
    incorrect_characters_on_screen = 0

    # The next character which must be typed
    next_char = sentence.next_char()

    while True:
        key = stdscr.getkey()

        if (key == 'KEY_BACKSPACE'):
            # Remove previous character
            (previous_pos_y, previous_pos_x) = cursor_positions.pop()
            stdscr.delch(previous_pos_y, previous_pos_x)

            # If there are incorrect characters on
            # screen, backspacing must be to remove these.
            if (incorrect_characters_on_screen > 0):
                incorrect_characters_on_screen -= 1
            # If there are no incorrect characters on screen,
            # we must be removing correctly typed characters.
            else:
                next_char = sentence.previous_char()
        else:
            cursor_positions.append(stdscr.getyx())

            # Typed character cannot be correct if there are
            # incorrectly typed characters currently on screen.
            if (key == next_char and incorrect_characters_on_screen <= 0):
                if (sentence.has_more_chars() == False):
                    print("Success")
                    break

                # Draw correcly typed character
                stdscr.addstr(key, curses.A_BOLD)
                next_char = sentence.next_char()
            else:
                # Draw incorrectly typed character
                stdscr.addstr(key, curses.A_UNDERLINE)
                incorrect_characters_on_screen += 1


wrapper(main)
