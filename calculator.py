"""A deliberately small, safe parser for basic arithmetic."""

import re


_NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)"
_EXPRESSION_PATTERN = re.compile(rf"^\s*({_NUMBER})\s*([+\-*/^%])\s*({_NUMBER})\s*$")


def calculate_expression(expression: str) -> float:
    """Calculate one binary operation without evaluating arbitrary Python code.

    Supported grammar: signed decimal number, one of + - * /, and another
    signed decimal number. Parentheses, exponents, and chained operations are
    intentionally unsupported.
    """
    if not expression.strip():
        raise ValueError("Enter an expression like '12 + 8'.")

    match = _EXPRESSION_PATTERN.fullmatch(expression)
    if not match:
        raise ValueError(
            "Use one operation with two numbers, for example '12 + 8'. "
            "Supported operators are +, -, *, and /."
        )

    left_text, operator, right_text = match.groups()
    if operator not in {"+", "-", "*", "/"}:
        raise ValueError(f"The operator '{operator}' is not supported. Use +, -, *, or /.")

    left = float(left_text)
    right = float(right_text)

    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if right == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return left / right


def format_number(number: float) -> str:
    """Format arithmetic output without unnecessary decimal zeroes."""
    if number.is_integer():
        return str(int(number))
    return f"{number:.10g}"
