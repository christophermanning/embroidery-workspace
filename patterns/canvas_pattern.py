from pyembroidery import EmbPattern, JUMP

from shapely import Polygon, LineString, affinity


# add custom methods to EmbPattern
class CanvasPattern(EmbPattern):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

        # use JUMP stitches to set the pattern to a consistent bounds size
        self.width = kwargs["width"]
        self.height = kwargs["height"]

        self.add_stitch_absolute(JUMP, 0, 0)
        self.add_stitch_absolute(JUMP, self.width, self.height)

    # get the bounds of stiches; ignoring the 2 initial JUMP stitches to set the bounds
    def stitch_bounds(self):
        bounds = LineString(self.stitches[2:]).bounds
        return (bounds[2] - bounds[0], bounds[3] - bounds[1])

    # are the pattern stitches within the bounds of the canvas width and height
    def in_bounds(self):
        container = Polygon(
            [[0, 0], [self.width, 0], [self.width, self.height], [0, self.height]]
        )
        return container.contains(LineString(self.stitches[2:]))

    def center(self, x, y):
        if len(self.stitches) == 0:
            return None

        ls = LineString([p[0:2] for p in self.stitches[2:]])

        midpoint = [
            (ls.bounds[2] + ls.bounds[0]) / 2,
            (ls.bounds[3] + ls.bounds[1]) / 2,
        ]

        offset_x = x - midpoint[0]
        offset_y = y - midpoint[1]
        ls = affinity.translate(ls, x - midpoint[0], y - midpoint[1])

        # restore any additional elements that were in self.stitches
        self.stitches = self.stitches[0:2] + [
            list(c) + self.stitches[2:][i][2:] for i, c in enumerate(ls.coords)
        ]

        return (offset_x, offset_y)
