# https://docs.python.org/3/library/turtle.html
from turtle import TNavigator

from shapely import LineString, affinity


# Extend TNavigator to track points for processing
class Turtle(TNavigator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.points = []

    def _goto(self, end):
        super()._goto(end)
        self.points.append(self.pos())

    def undo(self):
        self.points = self.points[0:-1]
        self.teleport(*self.points[-1])

    def center(self, x, y):
        ls = LineString(self.points)

        midpoint = [
            (ls.bounds[2] + ls.bounds[0]) / 2,
            (ls.bounds[3] + ls.bounds[1]) / 2,
        ]

        ls = affinity.translate(ls, x - midpoint[0], y - midpoint[1])

        self.points = list(ls.coords)
        self.teleport(*self.points[-1])
