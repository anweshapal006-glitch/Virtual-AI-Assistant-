"""Entry point for the offline, rule-based Mini Alexa assistant."""

from typing import Callable

from ai_concepts import format_perceptron_result, recommend_activity, run_perceptron_prompt
from calculator import calculate_expression, format_number
from content import get_fact, get_joke, get_quote
from datetime_utils import get_current_date, get_current_time
from game import play_guessing_game
from greetings import farewell_message, greeting_message, welcome_message
from help_menu import HELP_TEXT


def process_command(
    command: str,
    session_state: dict[str, str],
    input_fn: Callable[[str], str] = input,
    random_number: int | None = None,
) -> tuple[str, bool]:
    """Route normalized user text to a feature and return (response, should_exit)."""
    normalized = command.strip().lower().rstrip("?!.,")
    name = session_state.get("user_name", "Friend")

    if not normalized:
        return f"{name}, please enter a command or type 'help'.", False

    if normalized in {"exit", "quit", "bye", "goodbye"}:
        return farewell_message(name), True
    if normalized in {"help", "commands"}:
        return HELP_TEXT, False

    if normalized in {
        "date",
        "today",
        "what is today's date",
        "what's today's date",
        "what is the date",
        "current date",
    }:
        return f"{name}, today's date is {get_current_date()}.", False
    if normalized in {
        "time",
        "current time",
        "what time is it",
        "what is the time",
        "what's the time",
    }:
        return f"{name}, the current time is {get_current_time()}.", False

    if normalized == "calculate" or normalized.startswith("calculate "):
        expression = normalized[len("calculate") :].strip()
        try:
            result = calculate_expression(expression)
        except ZeroDivisionError:
            return f"{name}, division by zero is not allowed.", False
        except ValueError as error:
            return f"{name}, {error}", False
        return f"{name}, the result is {format_number(result)}.", False

    if normalized in {"quote", "motivational quote", "motivation"}:
        return f"{name}, here's a motivational quote: {get_quote()}", False
    if normalized in {"joke", "tell me a joke"}:
        return f"{name}, here's a joke: {get_joke()}", False
    if normalized in {"fact", "random fact", "tell me a fact"}:
        return f"{name}, here's a fact: {get_fact()}", False

    if normalized in {"game", "play game", "number game", "guess", "guessing game"}:
        outcome = play_guessing_game(input_fn=input_fn, secret_number=random_number)
        return f"{name}, {outcome}", False

    if normalized in {"activity", "recommend", "recommend activity", "what should i do"}:
        return f"{name}, {recommend_activity()}", False

    if normalized in {"perceptron", "show perceptron", "neuron"}:
        try:
            result = run_perceptron_prompt(input_fn)
        except ValueError as error:
            return f"{name}, {error}", False
        return f"{name}, {format_perceptron_result(result)}", False

    return f"{name}, I'm not sure I understood that. Type 'help' to see what I can do.", False


def run_assistant(
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> None:
    """Run the interactive assistant until the user requests exit or sends EOF."""
    output_fn("=" * 42)
    output_fn("        Mini Alexa - Virtual AI Assistant")
    output_fn("=" * 42)

    name = input_fn("What is your name? ").strip() or "Friend"
    session_state = {"user_name": name}
    output_fn(greeting_message(name))
    output_fn(welcome_message(name))

    while True:
        try:
            command = input_fn("You: ")
            response, should_exit = process_command(command, session_state, input_fn)
        except EOFError:
            output_fn(farewell_message(name))
            break
        output_fn(response)
        if should_exit:
            break


if __name__ == "__main__":
    run_assistant()
