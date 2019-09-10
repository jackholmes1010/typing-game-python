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
        return "Herp derpsum tee sherper perp derps derperker derpler ler merpus nerpy. Sherper perper derpsum herpderpsmer derperker, me merpus nerpy herpsum. Nerpy perp herp berps sherp terpus derpler. Derps perp ter serp derpy herpler herderder derpsum. Derpus herpy derp derps derpy herp merp berps nerpy. Herderder re derpsum, sherper derperker! Herpy merp nerpy merpus. Re derp ner derperker se sherlamer herpy ze cerp tee. Sherper herpsum er berp serp derpler derpus terpus. Derp herpderpsmer, merp berp perper herderder sherpus sherper herpy. Re herp herpler herpderpsmer sherlamer derperker dee derps. Sherpus herpler derperker perper re perp se ter sherp. Derps herpem herderder pee herpsum terpus sherlamer jerpy herpler? Derps de herpsum me herpderpsmer berps derpsum herderder, ner derpy?"