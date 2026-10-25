# Virtual AI Assistant (Mini Alexa)

## Project overview

Mini Alexa is an offline, terminal-based, rule-based assistant built for the Nexbridge Technologies AI Internship Program beginner assignment (AI-INT-P1-VAA). It responds to typed commands with small Python functions and includes educational demonstrations of fixed-rule classification and a perceptron calculation.

## Problem statement

This project demonstrates how a simple command-line program can recognize a small set of user intents and provide useful responses while making basic AI concepts understandable to a beginner.

## Objectives

- Practice Python functions, conditionals, lists, input validation, imports, and unit testing.
- Build an assistant that works without network access or third-party dependencies.
- Demonstrate the difference between hand-written rules and a model trained from data.

## Scope and exclusions

The application accepts and produces text in a terminal. It uses in-memory session state and forgets the user's name when it exits. It does not use voice input/output, a GUI, external services, network access, persistent history, a trained ML model, or a deep neural network.

## Features and functional requirements

| Requirement | Feature |
|---|---|
| FR-01, FR-02 | Banner, name capture, welcome, in-session name, default name |
| FR-03, FR-04 | Current date and time |
| FR-05 | Restricted safe four-operation calculator |
| FR-06, FR-07, FR-08 | Predefined quotes, jokes, and facts selected at random |
| FR-09 | Number guessing game (1–20, five valid guesses) |
| FR-10 | Help menu with supported commands and examples |
| FR-11 | Personalized exit aliases |
| FR-12 | Friendly response for unknown input |
| FR-13 | Hour-based activity recommendation using fixed rules |
| FR-14 | Two- or three-input fixed-weight perceptron demonstration |

## Technology and prerequisites

- Python 3.10 or newer (the code uses built-in union type syntax).
- Python standard library only; no package installation is required.
- A terminal or command prompt.

## Project structure

```text
virtual-ai-assistant/
├── main.py
├── greetings.py
├── datetime_utils.py
├── calculator.py
├── content.py
├── game.py
├── ai_concepts.py
├── help_menu.py
├── tests/
│   ├── test_calculator.py
│   ├── test_assistant.py
│   ├── test_ai_concepts.py
│   └── test_game.py
└── README.md
```

## Setup, run, and test

1. Install Python 3.10+ and open a terminal in the project folder.
2. No dependency installation is needed.
3. Start the application:

   ```text
   python main.py
   ```

4. Run all automated tests:

   ```text
   python -m unittest discover -s tests -v
   ```

Verified with Python 3.13.5: `python -m unittest discover -s tests -v` ran **28 tests; all passed**.

## Command reference

| Command | Examples |
|---|---|
| Date | `date`, `today`, `current date`, `what is the date`, `what is/what's today's date` |
| Time | `time`, `current time`, `what time is it`, `what is/what's the time` |
| Calculator | `calculate 12 + 8`, `calculate 20 - 5`, `calculate 6 * 7`, `calculate 15 / 3` |
| Quote | `quote`, `motivational quote`, `motivation` |
| Joke | `joke`, `tell me a joke` |
| Fact | `fact`, `random fact`, `tell me a fact` |
| Guessing game | `game`, `play game`, `number game`, `guess`, `guessing game`; then guess an integer from 1 to 20 |
| Activity | `activity`, `recommend`, `recommend activity`, `what should I do` |
| Perceptron | `perceptron`, `show perceptron`, `neuron`; then choose 2 or 3 inputs and enter each number |
| Help | `help`, `commands` |
| Exit | `exit`, `quit`, `bye`, `goodbye` |

The calculator accepts exactly two signed decimal numbers and one operator (`+`, `-`, `*`, or `/`), with optional whitespace. For example, `calculate -2.5 * 4`. It intentionally does not support parentheses, chained expressions, exponent notation, or arbitrary Python syntax. It never calls `eval()` or `exec()`.

## Architecture

```text
User
  |
  v
main.py — input loop and command routing
  |
  +--> greetings.py
  +--> datetime_utils.py
  +--> calculator.py
  +--> content.py
  +--> game.py
  +--> ai_concepts.py
  +--> help_menu.py
  |
  v
Text response
  |
  v
Next command or graceful exit
```

## Application flow

```text
Start
  |
Display banner
  |
Ask for user name
  |
Initialize in-memory session
  |
Wait for text command
  |
Normalize input
  |
Identify intent
  |
Execute matching handler
  |
Display response
  |
Exit requested?
  | No
  +----------> Wait for next command
  |
 Yes
  v
Display farewell
  |
 End
```

## Module responsibilities

- `main.py`: banner, name capture, command normalization/routing, and interactive loop.
- `greetings.py`: greeting, welcome, and farewell text.
- `datetime_utils.py`: obtains current system date and time; values are not hardcoded.
- `calculator.py`: validates and calculates one safe binary arithmetic expression.
- `content.py`: predefined content lists and random selection.
- `game.py`: number selection, guess validation, hints, and attempt limit.
- `ai_concepts.py`: fixed-rule activity recommendation and perceptron computation.
- `help_menu.py`: command reference displayed by the help intent.
- `tests/`: standard-library `unittest` checks for core behavior and edge cases.

## AI, ML, and DL learning notes

The assistant uses explicit rules, normalized keyword/phrase matching, and intent routing. This is a rule-based program, not a trained language model. Randomly choosing one item from a list is a recommendation analogy; it is not learned personalization. The user's name is held in a normal in-memory dictionary for the current run only.

The activity function uses a fixed sequence of `if`/`elif`/`else` hour checks. This is a small classification and decision-tree analogy: every hour maps to a category. The boundaries are: before 06:00 (rest), 06:00–10:59 (morning), 11:00–13:59 (lunch), 14:00–17:59 (afternoon), and 18:00–23:59 (evening). The rules do not learn or adapt.

The perceptron demonstration accepts two or three values. For two inputs, it uses weights `(0.5, -0.25)`; a third input adds weight `0.75`. The bias is `-0.5`.

```text
weighted_sum = sum(input_i * weight_i) + bias
output = 1 if weighted_sum > 0 else 0
```

Worked example with inputs `(2, 0)`:

```text
weighted_sum = (2 * 0.5) + (0 * -0.25) + (-0.5) = 0.5
output = 1, because 0.5 > 0
```

Inputs flow through multiplication and addition, then a step activation converts the weighted sum to a binary result. This illustrates forward propagation through a single artificial neuron. The weights and bias are fixed, not learned from training data; this is not a trained neural network and contains no deep learning.

## Testing strategy and actual result

The automated tests cover arithmetic operations and malformed input, command intents and exit, unknown and similar-but-unrelated words, personalized session behavior, activity boundaries, perceptron output/validation, and game hints/attempt handling. They use deterministic inputs instead of internet access or external test dependencies.

**Verified test result:** 28 automated tests passed using Python 3.13.5 (`python -m unittest discover -s tests -v`).

### Manual test checklist (25 representative inputs/actions)

1. Start the program and enter `Ada`.
2. Confirm the banner, greeting, and welcome message.
3. Enter `help`.
4. Enter `date`.
5. Enter `today`.
6. Enter `what is today's date`.
7. Enter `time`.
8. Enter `what time is it`.
9. Enter `calculate 12 + 8`.
10. Enter `calculate 20 - 5`.
11. Enter `calculate 6 * 7`.
12. Enter `calculate 15 / 3`.
13. Enter `calculate 1.5 + 2.25`.
14. Enter `calculate 5 / 0`.
15. Enter `calculate 5 +`.
16. Enter `quote` twice and confirm responses come from the quote list.
17. Enter `joke`.
18. Enter `tell me a fact`.
19. Enter `game`; try an invalid string and an out-of-range number before a valid guess.
20. Enter `game`; use five incorrect valid guesses and confirm the answer is shown.
21. Enter `activity` and check the recommendation against the current local hour.
22. Enter `perceptron`, choose `2`, then enter `2` and `0`.
23. Enter `perceptron`, choose `3`, then enter `1`, `2`, and `3`.
24. Enter `timeout`, confirm a friendly fallback and that the session continues.
25. Enter `goodbye`, confirm personalized farewell and termination.

These are manual test steps, not claimed execution results.

## Sample live demonstration

1. Run `python main.py` and enter a name.
2. Show `help`, then request the date and time.
3. Demonstrate calculator operations and the division-by-zero message.
4. Request a quote, joke, and fact.
5. Play one short guessing-game round.
6. Ask for an activity recommendation.
7. Run the perceptron with inputs `2` and `0`, explaining each displayed value.
8. Enter `goodbye` to demonstrate clean shutdown.

## Project report outline

1. Title page and project identification.
2. Abstract and problem statement.
3. Objectives, scope, and exclusions.
4. Requirements and design/architecture.
5. Implementation by module.
6. Rule-based and perceptron learning demonstrations.
7. Testing approach and verified test results.
8. Limitations and conclusion.

## Presentation outline

1. Project goal and offline constraints.
2. Folder structure and application flow.
3. Live command-line demonstration.
4. How rules route command intents.
5. Activity decision tree versus trained classification.
6. Perceptron formula and worked example.
7. Test evidence, limitations, and conclusion.

## Known limitations

- Intent recognition is based on a small set of explicit phrases and aliases.
- The calculator supports one binary operation at a time and no parentheses.
- Activity recommendations depend only on the local system hour.
- Quotes, jokes, facts, weights, and rules are predefined.
- No conversation history or user name persists after shutdown.

## Future enhancements (not implemented)

- Expand phrase coverage while retaining offline operation.
- Add additional standard-library unit tests and accessible command examples.
- Add more carefully verified content and additional fixed-rule activities.

## Requirement traceability

| Requirement | Implementation | Tests / verification |
|---|---|---|
| FR-01 | `main.py` banner | `tests/test_assistant.py` |
| FR-02 | `main.py`, `greetings.py` | assistant name/default-name tests |
| FR-03, FR-04 | `datetime_utils.py`, `main.py` | patched date/time command test |
| FR-05 | `calculator.py` | `tests/test_calculator.py`, calculator routing test |
| FR-06, FR-07, FR-08 | `content.py`, `main.py` | content selection routing test |
| FR-09 | `game.py` | `tests/test_game.py` |
| FR-10 | `help_menu.py`, `main.py` | help output test |
| FR-11 | `greetings.py`, `main.py` | exit alias and loop tests |
| FR-12 | `main.py` | unknown/empty/unrelated-word tests |
| FR-13 | `ai_concepts.py`, `main.py` | `tests/test_ai_concepts.py` |
| FR-14 | `ai_concepts.py`, `main.py` | perceptron tests |

## Conclusion

Mini Alexa is a small, explainable demonstration of Python command routing and elementary AI concepts. Its rules and perceptron parameters are fixed and transparent. It runs locally with the Python standard library and does not claim to train or contain an ML/DL model.

## References

- Python `datetime`: https://docs.python.org/3/library/datetime.html
- Python `random`: https://docs.python.org/3/library/random.html
- Python `unittest`: https://docs.python.org/3/library/unittest.html
- Python regular expressions: https://docs.python.org/3/library/re.html
