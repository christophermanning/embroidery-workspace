# https://docs.python.org/3/library/turtle.html
from turtle import TNavigator, Vec2D

from shapely import LineString, affinity


# Extend TNavigator to track points for processing
class Turtle(TNavigator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.points = []

    def _goto(self, end):
        # round the values to simplify coordinates and remove any -0 values that aren't needed
        super()._goto(Vec2D(round(end[0], 2), round(end[1], 2)))
        self.points.append(self.pos())

    def reset(self):
        super().reset()
        self.points = []

    def undo(self):
        self.points = self.points[0:-1]
        if len(self.points) > 0:
            self.teleport(*self.points[-1])

    # setting max_length will split a single line into multiple if the length of the line is longer than the max_length
    def forward(self, distance, max_length=None):
        pos0 = self.pos()
        super().forward(distance)
        if max_length is not None:
            pos1 = self.pos()
            ls = LineString([pos0, pos1])
            if ls.length > max_length:
                self.undo()
                ls = ls.segmentize(max_length)
                for [x, y] in ls.coords:
                    super().goto(x, y)

    # update all existing points so they are uniformly centered around x,y
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

    # helper function to write all turtle stitches to the pattern
    def write(self, pattern):
        for i, pos in enumerate(self.points):
            pattern += pos
