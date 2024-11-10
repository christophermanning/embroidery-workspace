import streamlit as st
import random

from patterns import Pattern

import numpy as np


class Grid(Pattern):
    def options():
        return {
            "label": "Grid",
            "options": {
                "width": {
                    "function": st.slider,
                    "args": {
                        "label": "width",
                        "min_value": 50,
                        "max_value": 1000,
                        "step": 10,
                        "value": 1000,
                    },
                },
                "height": {
                    "function": st.slider,
                    "args": {
                        "label": "Height",
                        "min_value": 50,
                        "max_value": 1000,
                        "step": 10,
                        "value": 1000,
                    },
                },
                "dimension": {
                    "function": st.slider,
                    "args": {
                        "label": "Dimension",
                        "min_value": 2,
                        "max_value": 50,
                        "step": 1,
                        "value": 10,
                    },
                },
                "path": {
                    "function": st.selectbox,
                    "args": {
                        "label": "Path",
                        "options": ["Random", "Horizontal", "Spiral", "Diagonal"],
                    },
                },
                "random_seed": {
                    "function": st.number_input,
                    "args": {"label": "Random Seed", "value": None, "step": 1},
                },
            },
        }

    def pattern(self, width, height, dimension, path, random_seed):
        nx, ny = (dimension, dimension)
        random.seed(random_seed if random_seed else random.randint(0, 999_999_999))

        x0 = self.canvas.margin
        x1 = self.canvas.margin + width - self.canvas.margin
        x, step = np.linspace(x0, x1, nx, True, True)
        self.log.append(f"_Stitch Distance_ `{round(step,2)}`")

        y0 = self.canvas.margin
        y1 = self.canvas.margin + height - self.canvas.margin
        y = np.linspace(y0, y1, ny)
        xv, yv = np.meshgrid(x, y)

        coords = np.vstack(list(zip(xv.ravel(), yv.ravel())))

        if path == "Random":
            np.random.shuffle(coords)
        elif path == "Horizontal":
            for i in range(1, dimension):
                if i % 2 != 0:
                    start = dimension * i
                    end = start + dimension
                    coords[start:end] = coords[start:end][::-1]
        elif path == "Spiral":
            tcoords = []

            xi = -1
            yi = 0
            direction = 1
            rows = dimension
            cols = dimension - 1
            for _ in range(dimension * dimension):
                for _ in range(0, rows):
                    xi += direction
                    tcoords.append(coords[yi * dimension + xi])
                rows -= 1

                for _ in range(0, cols):
                    yi += direction
                    tcoords.append(coords[yi * dimension + xi])
                cols -= 1

                direction *= -1

            coords = tcoords
        elif path == "Diagonal":
            tcoords = []

            for k in range(0, dimension * 2):
                tmp = []

                for j in range(0, k):
                    i = k - j
                    if i < dimension and j < dimension:
                        tmp.append(coords[i * dimension + j])

                if k % 2 == 0:
                    tcoords.extend(tmp[::-1])
                else:
                    tcoords.extend(tmp)

            coords = tcoords
        else:
            raise ValueError("Unknown Path Type")

        for i, v in enumerate(coords):
            self.canvas.pattern += (v[0], v[1])

        yield self.canvas.pattern
