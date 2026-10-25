"""Small, fixed-rule demonstrations of introductory AI concepts."""

from collections.abc import Callable, Sequence
from datetime import datetime
import math


PERCEPTRON_WEIGHTS = (0.5, -0.25, 0.75)
PERCEPTRON_BIAS = -0.5


def recommend_activity(current_time: datetime | None = None) -> str:
    """Classify the hour into an activity using a fixed decision tree.

    The branches are hand-written rules, not a model trained from data.
    """
    hour = (current_time or datetime.now()).hour
    if hour < 6:
        return "It's very early, so a little more rest could be a good idea."
    if hour < 11:
        return "It's morning: consider having breakfast or planning your day."
    if hour < 14:
        return "It's around midday: taking a lunch break may be a good idea."
    if hour < 18:
        return "It's afternoon: consider a short break or a light activity."
    return "It's evening: consider relaxing and winding down."


def calculate_perceptron(inputs: Sequence[float]) -> dict[str, object]:
    """Apply fixed weights, a bias, and a step activation to two or three inputs.

    This demonstrates forward propagation through a single artificial neuron.
    Its weights are predefined and are not learned from training data.
    """
    if len(inputs) not in {2, 3}:
        raise ValueError("Enter exactly two or three numeric inputs.")

    values: list[float] = []
    for value in inputs:
        if isinstance(value, bool):
            raise ValueError("Every input must be a finite number.")
        try:
            number = float(value)
        except (TypeError, ValueError) as error:
            raise ValueError("Every input must be a finite number.") from error
        if not math.isfinite(number):
            raise ValueError("Every input must be a finite number.")
        values.append(number)

    weights = PERCEPTRON_WEIGHTS[: len(values)]
    weighted_sum = sum(value * weight for value, weight in zip(values, weights)) + PERCEPTRON_BIAS
    output = 1 if weighted_sum > 0 else 0
    return {
        "inputs": tuple(values),
        "weights": weights,
        "bias": PERCEPTRON_BIAS,
        "weighted_sum": weighted_sum,
        "output": output,
    }


def format_perceptron_result(result: dict[str, object]) -> str:
    """Render all intermediate values in an educational perceptron result."""
    inputs = result["inputs"]
    weights = result["weights"]
    bias = result["bias"]
    weighted_sum = result["weighted_sum"]
    output = result["output"]
    return (
        f"Perceptron demonstration\n"
        f"Inputs: {inputs}\n"
        f"Weights: {weights}\n"
        f"Bias: {bias}\n"
        f"Weighted sum (including bias): {weighted_sum:g}\n"
        f"Step activation output: {output}\n"
        "These fixed weights were not learned from training data."
    )


def run_perceptron_prompt(input_fn: Callable[[str], str] = input) -> dict[str, object]:
    """Prompt for two or three values, then calculate a perceptron output."""
    count_text = input_fn("Enter the number of inputs (2 or 3): ").strip()
    if count_text not in {"2", "3"}:
        raise ValueError("Choose either 2 or 3 inputs.")
    values = []
    for index in range(int(count_text)):
        raw_value = input_fn(f"Input {index + 1}: ").strip()
        try:
            values.append(float(raw_value))
        except ValueError as error:
            raise ValueError("Every input must be a finite number.") from error
    return calculate_perceptron(values)
