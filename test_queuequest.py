import unittest

from main import (
    find_best_plan,
    greedy_plan,
    total_time,
    total_preference,
    validate_session
)


class QueueQuestTests(unittest.TestCase):

    def setUp(self):
        self.items = [
            {
                "name": "Coaster",
                "waiting_time": 60,
                "ride_time": 10,
                "preference": 10
            },
            {
                "name": "Wheel",
                "waiting_time": 25,
                "ride_time": 15,
                "preference": 7
            },
            {
                "name": "Carousel",
                "waiting_time": 20,
                "ride_time": 10,
                "preference": 6
            }
        ]

    def test_best_combination(self):
        plan = find_best_plan(self.items, 70)

        self.assertEqual(
            [item["name"] for item in plan],
            ["Wheel", "Carousel"]
        )
        self.assertEqual(total_preference(plan), 13)
        self.assertEqual(total_time(plan), 70)

    def test_no_attractions(self):
        self.assertEqual(find_best_plan([], 100), [])

    def test_zero_available_time(self):
        self.assertEqual(find_best_plan(self.items, 0), [])

    def test_nothing_fits(self):
        self.assertEqual(find_best_plan(self.items, 29), [])

    def test_all_attractions_fit(self):
        plan = find_best_plan(self.items, 140)

        self.assertEqual(len(plan), 3)
        self.assertEqual(total_time(plan), 140)
        self.assertEqual(total_preference(plan), 23)

    def test_equal_scores_choose_shorter_time(self):
        items = [
            {
                "name": "Slow",
                "waiting_time": 15,
                "ride_time": 5,
                "preference": 8
            },
            {
                "name": "Fast",
                "waiting_time": 5,
                "ride_time": 5,
                "preference": 8
            }
        ]

        plan = find_best_plan(items, 20)

        self.assertEqual(
            [item["name"] for item in plan],
            ["Fast"]
        )

    def test_greedy_skips_item_that_does_not_fit(self):
        plan = greedy_plan(self.items, 40)

        self.assertEqual(
            [item["name"] for item in plan],
            ["Wheel"]
        )

    def test_valid_session(self):
        data = {
            "available_time": 70,
            "attractions": self.items
        }

        validate_session(data)

    def test_invalid_available_time(self):
        data = {
            "available_time": -10,
            "attractions": self.items
        }

        with self.assertRaises(ValueError):
            validate_session(data)

    def test_duplicate_names(self):
        data = {
            "available_time": 70,
            "attractions": [self.items[0], self.items[0]]
        }

        with self.assertRaises(ValueError):
            validate_session(data)

    def test_invalid_preference(self):
        invalid_item = dict(self.items[0])
        invalid_item["preference"] = 11

        data = {
            "available_time": 70,
            "attractions": [invalid_item]
        }

        with self.assertRaises(ValueError):
            validate_session(data)


if __name__ == "__main__":
    unittest.main()