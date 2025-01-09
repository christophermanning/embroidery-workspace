import unittest

from machine import Machine


class TestMachine(unittest.TestCase):
    def test_humanize_duration(self):
        cases = [
            {
                "name": "0 stitches",
                "input": 0,
                "expected": "0 seconds",
            },
            {
                "name": "1 stitch",
                "input": 1,
                "expected": "0 seconds",
            },
            {
                "name": "10 stitches",
                "input": 10,
                "expected": "1 second",
            },
            {
                "name": "301 stitches",
                "input": 301,
                "expected": "30 seconds",
            },
            {
                "name": "600 stitches",
                "input": 600,
                "expected": "1 minute",
            },
            {
                "name": "610 stitches",
                "input": 610,
                "expected": "1 minute 1 second",
            },
            {
                "name": "6010 stitches",
                "input": 6100,
                "expected": "10 minutes 10 seconds",
            },
        ]

        for case in cases:
            machine = Machine()
            self.assertEqual(
                machine.humanize_duration(case["input"]),
                case["expected"],
                f"failed test '{case['name']}'",
            )
