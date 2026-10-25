"""Tests for guessing-game attempt and input rules."""

import unittest

from game import play_guessing_game


class GuessingGameTests(unittest.TestCase):
    def run_game(self, guesses, secret):
        answers = iter(guesses)
        messages = []
        outcome = play_guessing_game(
            input_fn=lambda _prompt: next(answers),
            output_fn=messages.append,
            secret_number=secret,
        )
        return outcome, messages

    def test_correct_guess_wins(self):
        outcome, _ = self.run_game(["7"], 7)
        self.assertIn("You win", outcome)
        self.assertIn("1 valid guess", outcome)

    def test_too_high_and_low_feedback(self):
        outcome, messages = self.run_game(["3", "9", "6", "7"], 7)
        self.assertIn("You win", outcome)
        self.assertIn("Too low!", messages)
        self.assertIn("Too high!", messages)

    def test_five_valid_attempts_reveal_answer(self):
        outcome, _ = self.run_game(["1", "2", "3", "4", "5"], 10)
        self.assertIn("correct number was 10", outcome)

    def test_invalid_input_does_not_consume_attempt(self):
        outcome, messages = self.run_game(["x", "0", "8"], 8)
        self.assertIn("You win", outcome)
        self.assertTrue(any("whole number" in message for message in messages))
        self.assertTrue(any("did not use an attempt" in message for message in messages))

    def test_invalid_secret_is_rejected(self):
        with self.assertRaises(ValueError):
            play_guessing_game(secret_number=21)


if __name__ == "__main__":
    unittest.main()
