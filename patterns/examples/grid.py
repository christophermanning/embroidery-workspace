import streamlit as st

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
                        "options": ["Random", "Horizontal", "Diagonal"],
                    },
                },
            },
        }

    def pattern(self, width, height, dimension, path):
        nx, ny = (dimension, dimension)

        x, step = np.linspace(
            self.canvas.margin,
            self.canvas.margin + width - self.canvas.margin,
            nx,
            True,
            True,
        )
        self.log.append(f"_Stitch Distance_ `{round(step,2)}`")
        y = np.linspace(
            self.canvas.margin, self.canvas.margin + height - self.canvas.margin, ny
        )
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
