import curses
from curses import wrapper
from Sentence import Sentence

stdscr = curses.initscr()
stdscr.keypad(True)
curses.noecho()
curses.cbreak()
curses.curs_set(False)

def generate_sentence():
    return "Hello World"

def main(stdscr):
    # Clear the screen
    stdscr.clear()

    # Get screen width/height
    (max_y, max_x) = stdscr.getmaxyx()

    # Keep track of (y, x) coordinates
    cursor_positions = []

    # Generate sentence to type
    sentence = Sentence()

    # State indicates if there are incorrectly typed characters on screen
    incorrect_characters_on_screen = 0

    # The next character which must be typed
    next_char = sentence.next_char()

    # Keep track of characters that have been overwritten
    overwritten_chars = []

    # Draw window to show sentence
    sentence_window = stdscr.derwin(max_y, max_x, 0, 0)
    sentence_window.border('|', '|', '-', '-', '+', '+', '+', '+')
    sentence_window.addstr(1, 1, sentence.get_sentence(), curses.A_DIM)
    stdscr.move(1, 1)

    while True:
        key = stdscr.getkey()

        if (key == 'KEY_BACKSPACE'):
            if (len(cursor_positions) < 1):
                continue

            # Remove previous character
            (previous_pos_y, previous_pos_x) = cursor_positions.pop()
            overwritten_char = overwritten_chars.pop()
            stdscr.addstr(previous_pos_y, previous_pos_x, overwritten_char)
            stdscr.move(previous_pos_y, previous_pos_x)

            # If there are incorrect characters on
            # screen, backspacing must be to remove these.
            if (incorrect_characters_on_screen > 0):
                incorrect_characters_on_screen -= 1
            # If there are no incorrect characters on screen,
            # we must be removing correctly typed characters.
            else:
                next_char = sentence.previous_char()
        else:
            # Keep track of characters that have been overwritten
            (current_pos_y, current_pos_x) = stdscr.getyx()
            char_at_cursor = stdscr.instr(current_pos_y, current_pos_x, 1)
            cursor_positions.append((current_pos_y, current_pos_x))
            overwritten_chars.append(char_at_cursor)

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
