"""Predefined entertainment and general-interest content."""

import random


QUOTES = [
    "Great things are done by a series of small things brought together. - Vincent van Gogh",
    "It always seems impossible until it's done. - Nelson Mandela",
    "The secret of getting ahead is getting started. - Mark Twain",
    "You are never too old to set another goal or to dream a new dream. - C. S. Lewis",
]

JOKES = [
    "Why did the computer go to the doctor? It had a virus!",
    "Why was the math book sad? It had too many problems.",
    "What do you call a bear with no teeth? A gummy bear!",
    "Why did the scarecrow win an award? It was outstanding in its field.",
]

FACTS = [
    "An octopus has three hearts.",
    "A group of flamingos is called a flamboyance.",
    "The shortest war in recorded history lasted less than an hour.",
    "Bananas are berries, while strawberries are not botanical berries.",
]


def get_quote() -> str:
    """Select a motivational quote from the predefined collection."""
    return random.choice(QUOTES)


def get_joke() -> str:
    """Select a family-friendly joke from the predefined collection."""
    return random.choice(JOKES)


def get_fact() -> str:
    """Select a general-interest fact from the predefined collection."""
    return random.choice(FACTS)
