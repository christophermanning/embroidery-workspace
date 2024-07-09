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
        if len(self.points) == 0:
            return None

        ls = LineString([p[0:2] for p in self.points])

        midpoint = [
            (ls.bounds[2] + ls.bounds[0]) / 2,
            (ls.bounds[3] + ls.bounds[1]) / 2,
        ]

        offset_x = x - midpoint[0]
        offset_y = y - midpoint[1]
        ls = affinity.translate(ls, x - midpoint[0], y - midpoint[1])

        self.teleport(*ls.coords[-1])

        # restore any additional elements that were in self.points
        self.points = [c + tuple(self.points[i][2:]) for i, c in enumerate(ls.coords)]

        return (offset_x, offset_y)
