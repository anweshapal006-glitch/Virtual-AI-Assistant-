"""The interactive number guessing game."""

import random
from collections.abc import Callable


MIN_NUMBER = 1
MAX_NUMBER = 20
MAX_ATTEMPTS = 5


def play_guessing_game(
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
    secret_number: int | None = None,
) -> str:
    """Play one round, counting only valid integer guesses in the allowed range."""
    answer = secret_number if secret_number is not None else random.randint(MIN_NUMBER, MAX_NUMBER)
    if not MIN_NUMBER <= answer <= MAX_NUMBER:
        raise ValueError(f"The secret number must be between {MIN_NUMBER} and {MAX_NUMBER}.")

    output_fn(f"I'm thinking of a number from {MIN_NUMBER} to {MAX_NUMBER}. You have {MAX_ATTEMPTS} guesses.")
    valid_guesses = 0
    while valid_guesses < MAX_ATTEMPTS:
        raw_guess = input_fn(f"Guess {valid_guesses + 1}/{MAX_ATTEMPTS}: ").strip()
        try:
            guess = int(raw_guess)
        except ValueError:
            output_fn("Please enter a whole number.")
            continue

        if not MIN_NUMBER <= guess <= MAX_NUMBER:
            output_fn(f"Choose a number from {MIN_NUMBER} to {MAX_NUMBER}; this did not use an attempt.")
            continue

        valid_guesses += 1
        if guess == answer:
            return f"You guessed {answer} correctly in {valid_guesses} valid guess(es). You win!"
        if guess < answer:
            output_fn("Too low!")
        else:
            output_fn("Too high!")

    return f"Out of guesses! The correct number was {answer}."
