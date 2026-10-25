"""Tests for fixed-rule activity and perceptron demonstrations."""

from datetime import datetime
import unittest

from ai_concepts import calculate_perceptron, recommend_activity


class ActivityRecommendationTests(unittest.TestCase):
    def test_representative_hours(self):
        cases = {
            2: "rest",
            8: "morning",
            12: "lunch",
            16: "afternoon",
            20: "evening",
        }
        for hour, expected in cases.items():
            with self.subTest(hour=hour):
                self.assertIn(expected, recommend_activity(datetime(2025, 1, 1, hour)))

    def test_each_range_boundary(self):
        cases = {
            0: "rest",
            5: "rest",
            6: "morning",
            10: "morning",
            11: "lunch",
            13: "lunch",
            14: "afternoon",
            17: "afternoon",
            18: "evening",
            23: "evening",
        }
        for hour, expected in cases.items():
            with self.subTest(hour=hour):
                self.assertIn(expected, recommend_activity(datetime(2025, 1, 1, hour)))


class PerceptronTests(unittest.TestCase):
    def test_positive_negative_and_zero_weighted_sum(self):
        self.assertEqual(calculate_perceptron((2, 0))["output"], 1)
        self.assertEqual(calculate_perceptron((0, 0))["output"], 0)
        self.assertEqual(calculate_perceptron((1, 0))["weighted_sum"], 0)
        self.assertEqual(calculate_perceptron((1, 0))["output"], 0)

    def test_three_inputs_and_details(self):
        result = calculate_perceptron((1, 2, 3))
        self.assertEqual(len(result["inputs"]), 3)
        self.assertEqual(len(result["weights"]), 3)
        self.assertEqual(result["weighted_sum"], 1.75)
        self.assertEqual(result["output"], 1)

    def test_invalid_count_and_non_numeric_inputs(self):
        for values in ((), (1,), (1, 2, 3, 4), (1, "invalid"), (float("inf"), 2)):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    calculate_perceptron(values)


if __name__ == "__main__":
    unittest.main()
