import streamlit as st

import numpy as np
import random

from patterns import Pattern, bbox_contains

from PIL import Image, ImageDraw, ImageFont

from shapely import LineString


class Lettering(Pattern):
    def options():
        return {
            "label": "Lettering",
            "options": {
                "text": {
                    "function": st.text_area,
                    "args": {
                        "label": "Text",
                        "value": "Hello\nWorld",
                    },
                },
            },
        }

    def pattern(self, text):
        # create a black and white image +1 in size to match the 0 based lists
        image = Image.new("1", (self.canvas.width + 1, self.canvas.height + 1), "white")
        draw = ImageDraw.Draw(image)

        # incrementally increase the font size until the text bbox fills the canvas
        font_size = 100
        while True:
            font_size += 1
            font = ImageFont.load_default(font_size)
            bbox = draw.textbbox(
                (self.canvas.margin, self.canvas.margin), text, font=font
            )
            # if the bbox of the text no longer fits in the canvas bbox, stop increasing the font size
            if not bbox_contains(self.canvas.bbox, bbox):
                break

        draw.text((self.canvas.margin, self.canvas.margin), text, font=font)

        # create an evenly spaced grid of points
        x = np.linspace(0, self.canvas.width, 100)
        y = np.linspace(0, self.canvas.height, 100)
        xv, yv = np.meshgrid(x, y)
        coords = list(np.vstack(list(zip(xv.ravel(), yv.ravel()))))
        # only use coords that overlap with a black image pixel
        coords = [c for c in coords if image.getpixel(c) == 0x000000]

        for i, c in enumerate(coords):
            line = LineString([self.canvas.pattern.stitches[-1][0:2], c]).segmentize(10)

            # if every line segment is not overlayed on the text, add a random color to the pattern to change the thread
            if not all([image.getpixel(c) == 0x000000 for c in line.coords]):
                self.canvas.pattern += f"#{random.randint(0x000000, 0xFFFFFF):6x}"

            self.canvas.pattern += tuple(c)

            if i % 50 == 0:
                yield self.canvas.pattern

        self.canvas.pattern.center(*self.canvas.centroid)

        yield self.canvas.pattern
