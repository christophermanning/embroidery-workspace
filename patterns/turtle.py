# https://docs.python.org/3/library/turtle.html
from turtle import TNavigator


# Extend TNavigator to track points for processing
class Turtle(TNavigator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.points = []

    def _goto(self, end):
        super()._goto(end)
        self.points.append(self.pos())
