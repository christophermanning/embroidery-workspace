import unittest

from patterns.turtle import Turtle


class TestTurtle(unittest.TestCase):
    def test_undo(self):
        turtle = Turtle()
        turtle.goto(0, 0)
        turtle.forward(10)
        turtle.forward(10)
        self.assertEqual(turtle.points, [(0, 0), (10, 0), (20, 0)])

        turtle.undo()
        self.assertEqual(turtle.points, [(0, 0), (10, 0)])

    def test_forward_max_length(self):
        turtle = Turtle()
        turtle.forward(10, 5)
        self.assertEqual(turtle.points, [(0, 0), (5, 0), (10, 0)])

    def test_remove_negative_zero(self):
        turtle = Turtle()
        turtle.forward(10)
        turtle.setheading(180)
        turtle.forward(10)
        self.assertEqual(turtle.points, [(10, 0), (0, 0)])
