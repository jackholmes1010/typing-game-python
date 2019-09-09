import curses
from curses import wrapper

stdscr = curses.initscr()
stdscr.keypad(True)
curses.noecho()
curses.cbreak()
curses.curs_set(False)


class Sentence:
    def __init__(self):
        self.original_sentence = list(self.generate_sentence())
        self.sentence = self.original_sentence.copy()
        self.sentence.reverse()

    def get_next_char(self):
        if (len(self.sentence) > 0):
            return self.sentence.pop()

        return None

    def has_more_chars(self):
        return (len(self.sentence) > 0)

    def get_sentence(self):
        return self.original_sentence

    def generate_sentence(self):
        return "Hello World!"


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
    next_char = sentence.get_next_char()

    while True:
        key = stdscr.getkey()

        if (key == 'KEY_BACKSPACE'):
            if (incorrect_characters_on_screen > 0):
                incorrect_characters_on_screen -= 1
        else:
            cursor_positions.append(stdscr.getyx())

            # Typed character cannot be correct if there are 
            # incorrectly typed characters currently on screen.
            if (incorrect_characters_on_screen > 0):
                continue

            if (key == next_char):
                if (sentence.has_more_chars() == False):
                    print("Success")
                    break

                next_char = sentence.get_next_char()
            else:
                incorrect_characters_on_screen += 1

main(stdscr)