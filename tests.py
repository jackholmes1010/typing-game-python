import unittest
from Sentence import Sentence
from start2 import Helper


class TestHelper(unittest.TestCase):
    def test_processes_all_keys(self):
        helper = Helper('Hello')
        process_result = helper.process_key('H')
        process_result = helper.process_key('e')
        process_result = helper.process_key('l')
        process_result = helper.process_key('l')
        process_result = helper.process_key('o')
        process_result = helper.process_key('!')
        self.assertTrue(process_result)

    def test_process_backspace_returns_original_character(self):
        helper = Helper("Hi")
        helper.process_key('H')
        helper.process_key('0')
        process_backspace_result = helper.process_backspace()
        process_key_result = helper.process_key('i')
        self.assertEqual('i', process_backspace_result)
        self.assertTrue(process_key_result)

    def test_returns_whitespace_if_no_characters_left_to_backspace(self):
        helper = Helper("hi")
        helper.process_backspace()
        helper.process_backspace()
        helper.process_backspace()
        process_result = helper.process_backspace()
        self.assertTrue(process_result)


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
        sentence.next_char()
        next_char = sentence.next_char()
        self.assertEqual(sentence.get_sentence()[1], next_char)
        previous_char = sentence.previous_char()
        self.assertEqual(sentence.get_sentence()[0], previous_char)

    def test_immediately_get_previous_char(self):
        sentence = Sentence()
        previous_char = sentence.previous_char()
        self.assertIsNone(previous_char)

if __name__ == '__main__':
    unittest.main()
