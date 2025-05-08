import streamlit as st

from patterns import Pattern, Turtle


class Spiral(Pattern):
    @staticmethod
    def options():
        return {
            "label": "Spiral",
            # each entry in the `inputs` dict is a streamlit input function
            "inputs": {
                "initial_size": {
                    "function": st.slider,
                    "args": {
                        "label": "Initial Size",
                        "min_value": 25,
                        "max_value": 100,
                        "step": 1,
                        "value": 50,
                    },
                },
                "steps": {
                    "function": st.slider,
                    "args": {
                        "label": "Steps",
                        "min_value": 1,
                        "max_value": 200,
                        "step": 1,
                        "value": 150,
                    },
                },
                "step_offset": {
                    "function": st.slider,
                    "args": {
                        "label": "Step Offset",
                        "min_value": 0,
                        "max_value": 100,
                        "step": 1,
                        "value": 3,
                    },
                },
                "angle_increment": {
                    "function": st.slider,
                    "args": {
                        "label": "Angle Increment",
                        "min_value": 0,
                        "max_value": 360,
                        "step": 1,
                        "value": 125,
                    },
                },
                "size_increment": {
                    "function": st.slider,
                    "args": {
                        "label": "Size Increment",
                        "min_value": 1,
                        "max_value": 30,
                        "step": 1,
                        "value": 1,
                    },
                },
            },
        }

    def pattern(
        self, initial_size, steps, step_offset, angle_increment, size_increment
    ):
        # use Turtle to simplify the drawing process
        turtle = self.canvas.turtle

        # start the drawing at the center of the canvas
        turtle.goto(*self.canvas.centroid)

        # set the initial step size to the minimum stich unit size
        size = initial_size
        for i in range(steps):
            turtle.setheading(turtle.heading() + angle_increment)
            turtle.forward(size)
            turtle.right(90)
            turtle.forward(size)
            turtle.right(90)
            turtle.forward(size)
            turtle.right(90)
            turtle.forward(size)

            # skip offsetting if it's the last step
            if i < steps - 1:
                turtle.left(45)
                turtle.forward(step_offset * i)
                turtle.right(135)

            size += size_increment

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
