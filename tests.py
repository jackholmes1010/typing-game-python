import unittest
from Sentence import Sentence


class TestSentence(unittest.TestCase):
    def test_gets_all_characters(self):
        sentence = Sentence()
        while sentence.has_more_chars():
            next_char = sentence.next_char()
            self.assertIsNotNone(next_char)

    def test_gets_next_char(self):
        sentence = Sentence()
        sentence_content = sentence.get_sentence()
        next_char = sentence.next_char()
        self.assertEqual(sentence_content[0], next_char)

    def test_gets_previous_character(self):
        sentence = Sentence()
        next_char = sentence.next_char()
        self.assertIsNotNone(next_char)
        previous_char = sentence.previous_char()
        self.assertEqual(next_char, previous_char)


if __name__ == '__main__':
    unittest.main()
