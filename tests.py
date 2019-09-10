import unittest
from Helper import Helper


class TestHelper(unittest.TestCase):
    def test_processes_all_keys(self):
        helper = Helper("Hello")
        process_result = helper.process_key("H")
        process_result = helper.process_key("e")
        process_result = helper.process_key("l")
        process_result = helper.process_key("l")
        process_result = helper.process_key("o")
        process_result = helper.process_key("!")
        self.assertTrue(process_result)

    def test_process_backspace_returns_original_character(self):
        helper = Helper("Hi")
        helper.process_key("H")
        helper.process_key("0")
        process_backspace_result = helper.process_backspace()
        process_key_result = helper.process_key("i")
        self.assertEqual("i", process_backspace_result)
        self.assertTrue(process_key_result)

    def test_returns_whitespace_if_no_characters_left_to_backspace(self):
        helper = Helper("hi")
        helper.process_backspace()
        helper.process_backspace()
        helper.process_backspace()
        process_result = helper.process_backspace()
        self.assertTrue(process_result)


if __name__ == "__main__":
    unittest.main()
