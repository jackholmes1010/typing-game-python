import curses
from curses import wrapper
from Sentence import Sentence

# Each sentence has correct parts, un typed parts
# Backspacing gives back the original char
# Processing key gives correct or false
class Helper:
    def __init__(self, sentence = ''):
        if (sentence == ''):
            self.sentence = self.generate_sentence()
        else:
            self.sentence = sentence

        self.index = 0

    def process_key(self, key):
        self.index += 1

        if (self.index >= len(self.sentence)):
            return True

        char = self.sentence[self.index]

        if (char == key):
            return True

        return False

    # Give back the original char
    def process_backspace(self):

        if (self.index > 0):
            self.index -= 1

        if (self.index >= len(self.sentence)):
            return ' '

        if (self.index < 1):
            return self.sentence[0]

        return self.sentence[self.index]

    def get_sentence(self):
        return self.sentence

    def generate_sentence(self):
        return "Hello World!"

stdscr = curses.initscr()
stdscr.keypad(True)
curses.noecho()
curses.cbreak()
curses.curs_set(False)

def main(stdscr):
    helper = Helper()
    stdscr.addstr(helper.get_sentence(), curses.A_UNDERLINE)
    stdscr.move(0, 0)

    # Keep track of cursur (y, x) coordinates
    cursor_positions = []

    while True:
        key = stdscr.getkey()

        if (key == 'KEY_BACKSPACE'):
            process_backspace_result = helper.process_backspace()
            stdscr.addstr('\b')
            stdscr.addstr(process_backspace_result, curses.A_UNDERLINE)
            stdscr.addstr('\b')

            # Remove previous character
            # (previous_pos_y, previous_pos_x) = cursor_positions.pop()
            # stdscr.addstr(previous_pos_y, previous_pos_x, process_backspace_result)
            # stdscr.move(previous_pos_y, previous_pos_x)
        else:
            process_key_result = helper.process_key(key)
            stdscr.addstr(key)

            # Keep track of the cursor position
            # (current_pos_y, current_pos_x) = stdscr.getyx()
            # cursor_positions.append((current_pos_y, current_pos_x))

    
wrapper(main)

