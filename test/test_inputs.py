import unittest

from inputs import Inputs


class TestInputs(unittest.TestCase):
    def test_input_value(self):
        inputs = Inputs()

        cases = [
            {
                "name": "selectbox: noop",
                "input": [
                    "selectbox",
                    123,
                    456,
                    {},
                ],
                "expected": ({}, 123),
            },
            {
                "name": "number_input: no value set",
                "input": [
                    "number_input",
                    None,
                    None,
                    {},
                ],
                "expected": ({}, None),
            },
            {
                "name": "number_input: returns default value",
                "input": [
                    "number_input",
                    None,
                    None,
                    {"value": 1000},
                ],
                "expected": ({"value": 1000}, None),
            },
            {
                "name": "number_input: query_param_value instead of default value",
                "input": [
                    "number_input",
                    None,
                    123,
                    {"value": 1000},
                ],
                "expected": ({"value": 123}, None),
            },
            {
                "name": "number_input: query_param_value int string returned as float",
                "input": [
                    "number_input",
                    None,
                    "1234",
                    {"value": 1000},
                ],
                "expected": ({"value": 1234}, None),
            },
            {
                "name": "number_input: query_param_value float string returned as float",
                "input": [
                    "number_input",
                    None,
                    "123.4",
                    {"value": 1000},
                ],
                "expected": ({"value": 123.4}, None),
            },
            {
                "name": "number_input: lambda value returns a session_state_value",
                "input": [
                    "number_input",
                    None,
                    None,
                    {"value": lambda: 123},
                ],
                "expected": ({"value": 123}, 123),
            },
            {
                "name": "slider: converts query value string to int",
                "input": [
                    "slider",
                    None,
                    "1234",
                    {},
                ],
                "expected": ({"value": 1234}, None),
            },
            {
                "name": "slider: converts query string to tuple",
                "input": [
                    "slider",
                    None,
                    "(1,2)",
                    {},
                ],
                "expected": ({"value": (1, 2)}, None),
            },
            {
                "name": "checkbox: value True",
                "input": [
                    "checkbox",
                    None,
                    None,
                    {"value": True},
                ],
                "expected": ({"value": True}, None),
            },
            {
                "name": "checkbox: query param: convert 'True' to True",
                "input": [
                    "checkbox",
                    None,
                    "True",
                    {},
                ],
                "expected": ({"value": True}, None),
            },
        ]

        for case in cases:
            self.assertEqual(
                inputs.input_value(*case["input"][0:3], **case["input"][3]),
                case["expected"],
                f"failed test '{case['name']}'",
            )
