from SentenceGenerator import SentenceGenerator


class GameState:
    def __init__(self, sentence=""):
        if sentence == "":
            self.sentence = SentenceGenerator().generate_sentence()
        else:
            self.sentence = sentence

        self.index = 0
        self.incorrect_character_count = 0

    def process_key(self, key):
        index = self.index
        self.index += 1

        if index >= len(self.sentence.text):
            return False

        if self.sentence.text[index] == key and self.incorrect_character_count <= 0:
            return True

        self.incorrect_character_count += 1
        return False

    def process_backspace(self):
        if self.incorrect_character_count > 0:
            self.incorrect_character_count -= 1

        if self.index > 0:
            self.index -= 1

        if self.index >= len(self.sentence.text):
            return " "

        if self.index < 1:
            return self.sentence.text[0]

        return self.sentence.text[self.index]

    def has_more_characters(self):
        return self.index < len(self.sentence.text)

    def get_sentence(self):
        return self.sentence.text
