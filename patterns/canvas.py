from pyembroidery import EmbPattern, JUMP
import random
from patterns.util import distance

from patterns import CanvasPattern, Turtle


# Canvas represents the embroidery suface and the dimensions are machine specific
# 4 x 4 size hoop with a width and height of 1000 supports a maximum of 30,000 stitches.
class Canvas:
    # minimimum unit distance between stitches
    MU = 25

    def __init__(
        self, width: int, height: int, margin: int = 10, initial_color: str = "#DDDDDD"
    ):
        self.width = width
        self.height = height
        self.centroid = (width / 2, height / 2)
        self.margin = margin

        # setting the pattern bounds to the canvas size ensures a consistant output
        self.pattern = CanvasPattern(width=width, height=height)

        # turtle instructions can be written to the pattern using turtle.write
        self.turtle = Turtle()

        # the bounding box of the content area of the canvas
        self.bbox = [
            self.margin,
            self.margin,
            self.margin + self.width - (self.margin * 2),
            self.margin + self.height - (self.margin * 2),
        ]

        self.pattern += initial_color
