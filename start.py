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
    (max_y, max_x) = stdscr.getmaxyx()
    sentence_window_height = 10
    sentence_window_width = 30
    sentence_window_y = int((max_y - sentence_window_height) / 2)
    sentence_window_x = int((max_x - sentence_window_width) / 2)
    sentence_window = stdscr.derwin(
        sentence_window_height,
        sentence_window_width,
        sentence_window_y,
        sentence_window_x,
    )
    sentence_window.border("|", "|", "-", "-", "+", "+", "+", "+")
    sentence_window.addstr(1, 1, sentence.get_sentence(), curses.A_DIM)
    sentence_window.move(1, 1)
    sentence_window.keypad(1)

    while True:
        key = sentence_window.getkey()

        if key == "KEY_BACKSPACE":
            if len(cursor_positions) < 1:
                continue

            # Remove previous character
            (previous_pos_y, previous_pos_x) = cursor_positions.pop()
            overwritten_char = overwritten_chars.pop()
            sentence_window.addstr(
                previous_pos_y, previous_pos_x, overwritten_char
            )
            sentence_window.move(previous_pos_y, previous_pos_x)

            # If there are incorrect characters on
            # screen, backspacing must be to remove these.
            if incorrect_characters_on_screen > 0:
                incorrect_characters_on_screen -= 1
            # If there are no incorrect characters on screen,
            # we must be removing correctly typed characters.
            else:
                next_char = sentence.previous_char()
        else:
            # Keep track of characters that have been overwritten
            (current_pos_y, current_pos_x) = sentence_window.getyx()
            char_at_cursor = sentence_window.instr(
                current_pos_y, current_pos_x, 1
            )
            cursor_positions.append((current_pos_y, current_pos_x))
            overwritten_chars.append(char_at_cursor)

            # Typed character cannot be correct if there are
            # incorrectly typed characters currently on screen.
            if key == next_char and incorrect_characters_on_screen <= 0:
                if sentence.has_more_chars() == False:
                    print("Success")
                    break

                # Draw correcly typed character
                sentence_window.addstr(key, curses.A_BOLD)
                next_char = sentence.next_char()
            else:
                # Draw incorrectly typed character
                sentence_window.addstr(key, curses.A_UNDERLINE)
                incorrect_characters_on_screen += 1


wrapper(main)
