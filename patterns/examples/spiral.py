import streamlit as st

from patterns import Pattern, Turtle


class Spiral(Pattern):
    def options():
        return {
            "label": "Spiral",
            # each entry in the `inputs` dict is a streamlit input function
            "inputs": {
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
        # use Turtle to simplify the drawing process
        turtle = Turtle()

        # start the drawing at the center of the canvas
        turtle.teleport(*self.canvas.centroid)

        # set the initial step size to the minimum stich unit size
        size = self.canvas.MU
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

        # center the entire drawing on the canvas
        turtle.center(*self.canvas.centroid)

        # convert the turtle drawing into a pattern
        for i, pos in enumerate(turtle.points):
            # add each turtle drawing step to the pattern
            self.canvas.pattern += pos

            # incrementally yield the canvas pattern to create a frame for an animated GIF output
            if i % 50 == 0:
                yield self.canvas.pattern

        # yield the finished pattern
        yield self.canvas.pattern
