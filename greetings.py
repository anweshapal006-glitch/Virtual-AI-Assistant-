"""Personalized messages used by Mini Alexa."""


def greeting_message(name: str) -> str:
    """Return the assistant's introductory greeting."""
    return f"Hello, {name}! I'm Mini Alexa, your offline virtual assistant."


def welcome_message(name: str) -> str:
    """Explain how to begin after the user's name has been captured."""
    return f"Welcome, {name}! Type 'help' to see the commands I can do."


def farewell_message(name: str) -> str:
    """Return a personalized goodbye."""
    return f"Goodbye, {name}! Thanks for chatting with Mini Alexa."
