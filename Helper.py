class Helper:
    def __init__(self, sentence=""):
        if sentence == "":
            self.sentence = self.generate_sentence()
        else:
            self.sentence = sentence

        self.index = 0

    def process_key(self, key):
        if self.index >= len(self.sentence):
            return True

        char = self.sentence[self.index]
        self.index += 1

        if char == key:
            return True

        return False

    def process_backspace(self):
        if self.index > 0:
            self.index -= 1

        if self.index >= len(self.sentence):
            return " "

        if self.index < 1:
            return self.sentence[0]

        return self.sentence[self.index]

    def has_more_characters(self):
        return self.index < len(self.sentence)

    def get_sentence(self):
        return self.sentence

    def generate_sentence(self):
        return "Herp derpsum tee sherper perp derps derperker derpler ler merpus nerpy. Sherper perper derpsum herpderpsmer derperker, me merpus nerpy herpsum."
