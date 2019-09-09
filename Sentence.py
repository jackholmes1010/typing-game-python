class Sentence:
    def __init__(self):
        self.original_sentence = list(self.generate_sentence())
        self.sentence = self.original_sentence.copy()
        self.index = -1

    def next_char(self):
        if (self.index < len(self.sentence)):
            self.index += 1
            return self.sentence[self.index]

        return None

    def previous_char(self):
        if (self.index > 0):
            self.index -= 1
            return self.sentence[self.index]

    def has_more_chars(self):
        return self.index < len(self.sentence)

    def get_sentence(self):
        return self.original_sentence

    def generate_sentence(self):
        return "Hello World!"
