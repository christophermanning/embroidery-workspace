import streamlit as st
import random

from patterns import Pattern, Turtle


class Spiral(Pattern):
    def options():
        return {
            "label": "Spiral",
            "options": {
                "steps": {
                    "function": st.slider,
                    "args": {
                        "label": "Steps",
                        "min_value": 1,
                        "max_value": 100,
                        "step": 1,
                        "value": 46,
                    },
                },
                "angle_scale": {
                    "function": st.slider,
                    "args": {
                        "label": "Angle Scale",
                        "min_value": 0,
                        "max_value": 100,
                        "step": 1,
                        "value": 10,
                    },
                },
                "size_scale": {
                    "function": st.slider,
                    "args": {
                        "label": "Size Scale",
                        "min_value": 1,
                        "max_value": 30,
                        "step": 1,
                        "value": 10,
                    },
                },
            },
        }

    def pattern(self, steps, angle_scale, size_scale):
        pattern = self.canvas.pattern

        turtle = Turtle()
        turtle.teleport(*self.canvas.centroid)

        size = 10
        for i in range(steps):
            turtle.setheading(i * angle_scale)
            turtle.forward(size)
            turtle.right(90)
            turtle.forward(size)
            turtle.right(90)
            turtle.forward(size)
            turtle.right(90)
            turtle.forward(size)
            size += size_scale

        turtle.center(*self.canvas.centroid)

        for i, pos in enumerate(turtle.points):
            self.canvas.pattern += pos
            if i % 50 == 0:
                yield self.canvas.pattern

        yield pattern
