import streamlit as st

from patterns import Pattern, Turtle


class HilbertCurve(Pattern):
    @staticmethod
    def options():
        return {
            "label": "Hilbert Curve",
            "inputs": {
                "iterations": {
                    "function": st.slider,
                    "args": {
                        "label": "Iterations",
                        "min_value": 1,
                        "max_value": 6,
                        "step": 1,
                        "value": 5,
                    },
                },
                "size": {
                    "function": st.slider,
                    "args": {
                        "label": "Size",
                        "min_value": 10,
                        "max_value": 100,
                        "step": 1,
                        "value": 32,
                    },
                },
                "angle": {
                    "function": st.slider,
                    "args": {
                        "label": "Angle",
                        "min_value": 0,
                        "max_value": 180,
                        "step": 1,
                        "value": 90,
                    },
                },
            },
        }

    # https://en.wikipedia.org/wiki/Hilbert_curve#Representation_as_Lindenmayer_system
    # +BF−AFA−FB+ ~= Left, Recursion B, Forward, Right, Recursion A, Forward, Recursion A, Right, Forward, Recursion B, Left
    def hilbert(self, turtle, iteration, size, angle):
        if iteration == 0:
            return

        turtle.left(angle)
        self.hilbert(turtle, iteration - 1, size, -angle)

        turtle.forward(size)
        turtle.right(angle)
        self.hilbert(turtle, iteration - 1, size, angle)

        turtle.forward(size)
        self.hilbert(turtle, iteration - 1, size, angle)

        turtle.right(angle)
        turtle.forward(size)
        self.hilbert(turtle, iteration - 1, size, -angle)
        turtle.left(angle)

    def pattern(self, iterations, size, angle):
        turtle = Turtle()
        self.hilbert(turtle, iterations, size, angle)
        turtle.center(*self.canvas.centroid)

        for i, pos in enumerate(turtle.points):
            self.canvas.pattern += pos
            if i % 50 == 0:
                yield self.canvas.pattern

        yield self.canvas.pattern
