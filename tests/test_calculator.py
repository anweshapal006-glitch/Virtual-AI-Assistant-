"""Tests for the restricted arithmetic parser."""

import unittest

from calculator import calculate_expression


class CalculatorTests(unittest.TestCase):
    def test_basic_operations(self):
        self.assertEqual(calculate_expression("12 + 8"), 20)
        self.assertEqual(calculate_expression("20 - 5"), 15)
        self.assertEqual(calculate_expression("6 * 7"), 42)
        self.assertEqual(calculate_expression("15 / 3"), 5)

    def test_decimal_and_negative_inputs(self):
        self.assertAlmostEqual(calculate_expression("1.5 + 2.25"), 3.75)
        self.assertEqual(calculate_expression("-4 * 2"), -8)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculate_expression("5 / 0")

    def test_missing_or_malformed_expression(self):
        for expression in ("", "5 +", "+ 2", "five + 2", "1 + 2 + 3"):
            with self.subTest(expression=expression):
                with self.assertRaises(ValueError):
                    calculate_expression(expression)

    def test_unsupported_operator_and_syntax(self):
        for expression in ("2 ^ 3", "2 ** 3", "(2 + 3)"):
            with self.subTest(expression=expression):
                with self.assertRaises(ValueError):
                    calculate_expression(expression)

    def test_rejects_non_finite_operands_and_overflow_results(self):
        huge_operand = "9" * 400
        with self.assertRaisesRegex(ValueError, "supported range"):
            calculate_expression(f"{huge_operand} + 1")

        large_finite_operand = "1" + ("0" * 200)
        with self.assertRaisesRegex(ValueError, "supported range"):
            calculate_expression(f"{large_finite_operand} * {large_finite_operand}")


if __name__ == "__main__":
    unittest.main()
