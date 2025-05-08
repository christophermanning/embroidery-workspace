import streamlit as st

from patterns import Pattern


class Diagnostics(Pattern):
    @staticmethod
    def options():
        return {
            "label": "Diagnostics",
            "inputs": {
                "size": {
                    "function": st.slider,
                    "args": {
                        "label": "Size",
                        "min_value": 10,
                        "max_value": 100,
                        "step": 1,
                        "value": 50,
                    },
                },
                "stitch_distances": {
                    "function": st.slider,
                    "args": {
                        "label": "Stitch Distances",
                        "min_value": 10,
                        "max_value": 35,
                        "step": 1,
                        "value": (15, 35),
                    },
                },
            },
        }

    def pattern(self, size, stitch_distances):
        min_stitch_distance, max_stitch_distance = stitch_distances

        turtle = self.canvas.turtle

        turtle.goto(0, 0)

        # canvas outline
        for i in range(0, 4):
            dim = self.canvas.width if i % 2 == 0 else self.canvas.height
            turtle.forward(dim, max_stitch_distance)
            turtle.right(-90)

        turtle.goto(size, size)

        # lines
        for i, sd in enumerate(range(min_stitch_distance, max_stitch_distance + 1, 2)):
            turtle.forward(200, sd)

            turtle.setheading(90)
            turtle.forward(size)
            turtle.setheading(180 if i % 2 == 0 else 0)

        cursor = turtle.pos()
        turtle.setheading(0)

        # squares
        for i, sd in enumerate(range(min_stitch_distance, max_stitch_distance + 1, 2)):
            turtle.goto(size + i * size, cursor[1] + size)

            for i in range(0, 4):
                turtle.forward(sd)
                turtle.right(-90)

        turtle.write(self.canvas.pattern)

        yield self.canvas.pattern
