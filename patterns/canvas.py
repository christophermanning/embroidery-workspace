from pyembroidery import EmbPattern, JUMP
import random
from patterns.util import distance

from patterns import CanvasPattern


# Canvas represends the embroidery suface and the dimensions are machine specific
# 4 x 4 size hoop with a width and height of 1000 supports a maximum of 30,000 stitches.
class Canvas:
    # minimimum unit distance between stitches
    MU = 25

    pattern = None

    def __init__(self, width, height, margin, initial_color):
        self.width = width
        self.height = height
        self.margin = margin

        # setting the pattern bounds to the canvas size ensures a consistant output
        self.pattern = CanvasPattern(width=width, height=height)

        self.pattern += initial_color

    def rand_point(self):
        return (
            random.uniform(0 + self.margin, self.width - self.margin),
            random.uniform(0 + self.margin, self.height - self.margin),
        )

    def rand_point_from(self, x, y, min_dist, max_dist):
        for i in range(0, 100):
            rx, ry = self.rand_point()

            d = distance((x, y), (rx, ry))
            if d > min_dist and d < max_dist:
                return (rx, ry)
