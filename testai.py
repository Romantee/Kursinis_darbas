import unittest
from io import StringIO
from unittest.mock import patch
from itertools import cycle
from OOP_coursework import MultipleChoice, TextInput, CountryGuessGame

class TestMultipleChoice(unittest.TestCase):
    def setUp(self):
        # sukuriamas laikinas failas
        self.filename = "test_level_1.txt"
        with open(self.filename, "w") as f:
            f.write("What is the capital of France?\n")
            f.write("1. Berlin\n")
            f.write("2. London\n")
            f.write("3. Paris\n")
            f.write("3\n")

    def tearDown(self):
        import os
        os.remove(self.filename)

    def test_read_from_file(self):
        game = MultipleChoice(self.filename)
        questions = game._read_from_file(self.filename)
        expected_questions = [("What is the capital of France?", ["1. Berlin", "2. London", "3. Paris"], "3")]
        self.assertEqual(questions, expected_questions)

    @patch('builtins.input', side_effect=['3'])
    def test_play_multiple_choice_correct(self, mock_input):
        game = MultipleChoice(self.filename)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            game._play_multiple_choice()
            self.assertIn('Correct!', fake_out.getvalue())

    @patch('builtins.input', side_effect=['1'])
    def test_play_multiple_choice_incorrect(self, mock_input):
        game = MultipleChoice(self.filename)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            game._play_multiple_choice()
            self.assertIn('Incorrect', fake_out.getvalue())

class TestTextInput(unittest.TestCase):
    def setUp(self):
        self.filename = "test_level_2.txt"
        with open(self.filename, "w") as f:
            f.write("What is the capital of Germany?\n")
            f.write("Berlin\n")

    def tearDown(self):
        import os
        os.remove(self.filename)

    def test_read_from_file(self):
        game = TextInput(self.filename)
        questions = game._read_from_file(self.filename)
        expected_questions = [("What is the capital of Germany?", "Berlin")]
        self.assertEqual(questions, expected_questions)

    @patch('builtins.input', side_effect=['Berlin'])
    def test_play_text_input_correct(self, mock_input):
        game = TextInput(self.filename)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            game._play_text_input()
            self.assertIn('Correct!', fake_out.getvalue())

    @patch('builtins.input', side_effect=['Hamburg'])
    def test_play_text_input_incorrect(self, mock_input):
        game = TextInput(self.filename)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            game._play_text_input()
            self.assertIn('Incorrect', fake_out.getvalue())

class TestCountryGuessGame(unittest.TestCase):
    @patch('builtins.input', side_effect=cycle(['John', '1', 'A', 'B', 'C']))
    def test_play_game(self, mock_input):
        game = CountryGuessGame()
        game.add_level("level_1.txt", "multiple_choice")
        with patch('sys.stdout', new=StringIO()) as fake_output:
            game.play_game()
            output = fake_output.getvalue().strip()
            self.assertIn('John', output)  
            self.assertIn('Level 1', output)  
            self.assertIn('You scored', output)  
if __name__ == "__main__":
    unittest.main()
