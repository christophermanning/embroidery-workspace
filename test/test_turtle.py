import unittest

from patterns.turtle import Turtle


class TestTurtle(unittest.TestCase):
    def test_goto(self):
        turtle = Turtle()
        turtle.goto(0, 10, 5)
        turtle.goto(0, 20, 5)
        self.assertEqual(turtle.points, [(0, 5), (0, 10), (0, 15), (0, 20)])

    def test_undo(self):
        turtle = Turtle()
        turtle.goto(0, 0)
        turtle.forward(10)
        turtle.forward(10)
        self.assertEqual(turtle.points, [(0, 0), (10, 0), (20, 0)])

        turtle.undo()
        self.assertEqual(turtle.points, [(0, 0), (10, 0)])

    def test_forward(self):
        turtle = Turtle()
        turtle.forward(10)
        self.assertEqual(turtle.points, [(0, 0), (10, 0)])

    def test_forward_with_goto(self):
        turtle = Turtle()
        turtle.goto(1, 0)
        turtle.forward(10)
        self.assertEqual(turtle.points, [(1, 0), (11, 0)])

    def test_forward_max_length(self):
        turtle = Turtle()
        turtle.forward(10, 5)
        self.assertEqual(turtle.points, [(0, 0), (5, 0), (10, 0)])

    def test_remove_negative_zero(self):
        turtle = Turtle()
        turtle.forward(10)
        turtle.setheading(180)
        turtle.forward(10)
        self.assertEqual(turtle.points, [(0, 0), (10, 0), (0, 0)])
