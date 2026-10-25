"""Tests for command routing and the main interactive session."""

from datetime import datetime
from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch

import main
from content import FACTS, JOKES, QUOTES
from help_menu import HELP_TEXT


class AssistantCommandTests(unittest.TestCase):
    def setUp(self):
        self.state = {"user_name": "Ada"}

    def test_empty_and_unknown_commands(self):
        self.assertIn("please enter", main.process_command("  ", self.state)[0])
        response, should_exit = main.process_command("timekeeper", self.state)
        self.assertIn("not sure", response)
        self.assertFalse(should_exit)

    def test_date_time_commands_use_current_helpers(self):
        with patch("main.get_current_date", return_value="Current Date"), patch(
            "main.get_current_time", return_value="Current Time"
        ):
            self.assertIn("Current Date", main.process_command(" WHAT IS TODAY'S DATE? ", self.state)[0])
            self.assertIn("Current Time", main.process_command("what time is it", self.state)[0])

    def test_calculator_routing_and_errors(self):
        self.assertIn("20", main.process_command("calculate 12 + 8", self.state)[0])
        self.assertIn("division by zero", main.process_command("calculate 5 / 0", self.state)[0])
        self.assertIn("Supported operators", main.process_command("calculate 5 +", self.state)[0])

    def test_content_commands_use_predefined_collections(self):
        for command, choices in (
            ("quote", QUOTES),
            ("joke", JOKES),
            ("tell me a fact", FACTS),
        ):
            with self.subTest(command=command):
                response, should_exit = main.process_command(command, self.state)
                self.assertFalse(should_exit)
                self.assertTrue(any(item in response for item in choices))

    def test_help_is_complete_and_name_is_personalized(self):
        response, _ = main.process_command("help", self.state)
        self.assertEqual(response, HELP_TEXT)
        personalized, _ = main.process_command("quote", self.state)
        self.assertTrue(personalized.startswith("Ada,"))

    def test_exit_aliases(self):
        for command in ("exit", "quit", "bye", "goodbye"):
            with self.subTest(command=command):
                response, should_exit = main.process_command(command, self.state)
                self.assertTrue(should_exit)
                self.assertIn("Ada", response)

    def test_unrelated_words_do_not_trigger_features(self):
        for command in ("timeout", "timely", "quoted", "joking", "factual"):
            with self.subTest(command=command):
                response, should_exit = main.process_command(command, self.state)
                self.assertIn("not sure", response)
                self.assertFalse(should_exit)

    def test_number_game_command_passes_inputs_and_secret(self):
        guesses = iter(["10"])
        with patch("main.play_guessing_game", return_value="You win!") as game:
            response, _ = main.process_command(
                "game", self.state, input_fn=lambda _prompt: next(guesses), random_number=10
            )
        game.assert_called_once()
        self.assertIn("You win", response)

    def test_activity_command_is_personalized(self):
        with patch("main.recommend_activity", return_value="Take a break."):
            response, _ = main.process_command("recommend activity", self.state)
        self.assertEqual(response, "Ada, Take a break.")

    def test_perceptron_prompt_and_invalid_input(self):
        answers = iter(["2", "2", "0"])
        response, _ = main.process_command(
            "perceptron", self.state, input_fn=lambda _prompt: next(answers)
        )
        self.assertIn("Inputs: (2.0, 0.0)", response)
        self.assertIn("Weighted sum (including bias): 0.5", response)
        invalid_response, should_exit = main.process_command(
            "perceptron", self.state, input_fn=lambda _prompt: "four"
        )
        self.assertIn("Choose either 2 or 3 inputs", invalid_response)
        self.assertFalse(should_exit)


class AssistantLoopTests(unittest.TestCase):
    def test_eof_at_name_prompt_exits_cleanly(self):
        output = []

        def read_input(_prompt):
            raise EOFError

        main.run_assistant(input_fn=read_input, output_fn=output.append)
        self.assertTrue(any("Goodbye, Friend" in line for line in output))

    def test_name_capture_welcome_and_personalized_farewell(self):
        answers = iter(["Ada", "quote", "goodbye"])
        output = []
        main.run_assistant(input_fn=lambda _prompt: next(answers), output_fn=output.append)
        self.assertTrue(any("Hello, Ada" in line for line in output))
        self.assertTrue(any("Welcome, Ada" in line for line in output))
        self.assertTrue(any(line.startswith("Ada, here's a motivational quote") for line in output))
        self.assertTrue(any("Goodbye, Ada" in line for line in output))

    def test_empty_name_uses_friend_default(self):
        answers = iter(["", "exit"])
        output = []
        main.run_assistant(input_fn=lambda _prompt: next(answers), output_fn=output.append)
        self.assertTrue(any("Hello, Friend" in line for line in output))

    def test_eof_exits_cleanly(self):
        answers = iter(["Grace"])

        def read_input(_prompt):
            try:
                return next(answers)
            except StopIteration:
                raise EOFError

        output = []
        main.run_assistant(input_fn=read_input, output_fn=output.append)
        self.assertTrue(any("Goodbye, Grace" in line for line in output))

    def test_game_messages_use_the_assistant_output_handler(self):
        answers = iter(["Ada", "game", "3", "9", "7", "goodbye"])
        output = []
        unexpected_stdout = StringIO()

        with patch("game.random.randint", return_value=7), redirect_stdout(unexpected_stdout):
            main.run_assistant(input_fn=lambda _prompt: next(answers), output_fn=output.append)

        self.assertEqual(unexpected_stdout.getvalue(), "")
        self.assertTrue(any("You have 5 guesses" in line for line in output))
        self.assertIn("Too low!", output)
        self.assertIn("Too high!", output)
        self.assertTrue(any("You win!" in line for line in output))


if __name__ == "__main__":
    unittest.main()
