import streamlit as st

import numpy as np

from patterns import Pattern, bbox_contains

from patterns.tsp import tsp

from PIL import Image, ImageDraw, ImageFont


class Text(Pattern):
    def options():
        return {
            "label": "Text",
            "inputs": {
                "text": {
                    "function": st.text_area,
                    "args": {
                        "label": "Text",
                        "value": " Hello\nWorld",
                    },
                },
                "cross_stitch": {
                    "function": st.checkbox,
                    "args": {
                        "label": "Cross Stitch",
                        "value": True,
                    },
                },
            },
        }

    def pattern(self, text, cross_stitch):
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
        x = np.linspace(0, self.canvas.width, 50)
        y = np.linspace(0, self.canvas.height, 50)
        xv, yv = np.meshgrid(x, y)
        coords = list(np.vstack(list(zip(xv.ravel(), yv.ravel()))))

        # only use coords that overlap with a black image pixel
        coords = [c for c in coords if image.getpixel(c) == 0x000000]

        # create an optimized path using a TSP solver
        coords = tsp(coords)

        turtle = self.canvas.turtle

        for i, c in enumerate(coords):
            turtle.goto(*c)
            if cross_stitch:
                for z in range(0, 4):
                    turtle.setheading(45 + (z * 90))
                    turtle.forward(self.canvas.MU)
                    turtle.backward(self.canvas.MU)

            if i % 50 == 0:
                yield self.canvas.pattern

        turtle.center(*self.canvas.centroid)
        turtle.write(self.canvas.pattern)

        yield self.canvas.pattern
