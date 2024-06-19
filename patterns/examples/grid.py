import streamlit as st

from patterns import Pattern

import numpy as np


class Grid(Pattern):
    def options():
        return {
            "label": "Grid",
            "options": {
                "size": {
                    "function": st.slider,
                    "args": {
                        "label": "Size",
                        "min_value": 2,
                        "max_value": 100,
                        "step": 1,
                        "value": 10,
                    },
                },
                "shuffle": {
                    "function": st.checkbox,
                    "args": {"label": "Shuffle", "value": True},
                },
            },
        }

    def pattern(self, size, shuffle):
        nx, ny = (size, size)

        x = np.linspace(self.canvas.margin, self.canvas.width - self.canvas.margin, nx)
        y = np.linspace(self.canvas.margin, self.canvas.height - self.canvas.margin, ny)
        xv, yv = np.meshgrid(x, y)

        coords = np.vstack(list(zip(xv.ravel(), yv.ravel())))

        if shuffle:
            np.random.shuffle(coords)

        for i, v in enumerate(coords):
            self.canvas.pattern += (v[0], v[1])

        yield self.canvas.pattern
