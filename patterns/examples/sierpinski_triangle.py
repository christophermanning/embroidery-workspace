from numpy import ma
import streamlit as st
import random

from patterns import Pattern, Turtle

class SierpinskiTriangle(Pattern):
    @staticmethod
    def options():
        return {
            "label": "Sierpiński Triangle",
            "inputs": {
                "process": {
                    "function": st.selectbox,
                    "args": {
                        "label": "Process",
                        "options": ["Recursive", "Lindenmayer System"],
                    },
                },
                "iterations": {
                    "function": st.slider,
                    "args": {
                        "label": "Iterations",
                        "min_value": 0,
                        "max_value": 6,
                        "step": 1,
                        "value": 5,
                    },
                },
                "size": {
                    "function": st.slider,
                    "args": {
                        "label": "Size",
                        "min_value": 100,
                        "max_value": 990,
                        "step": 1,
                        "value": 990,
                    },
                },
                "angle": {
                    "function": st.slider,
                    "args": {
                        "label": "Angle",
                        "min_value": 0,
                        "max_value": 180,
                        "step": 1,
                        "value": 120,
                    },
                },
                "angle_offset": {
                    "function": st.slider,
                    "args": {
                        "label": "Angle Offset",
                        "min_value": -180,
                        "max_value": 180,
                        "step": 1,
                        "value": 60,
                    },
                },
                "debug": {
                    "function": st.checkbox,
                    "args": {"label": "Debug", "value": False},
                },
            },
        }

    # https://en.wikipedia.org/wiki/Sierpi%C5%84ski_curve#Representation_as_Lindenmayer_system
    # F−−XF−−F−−XF
    def sierpinski_lindenmayer(self, turtle, iteration, size, angle, angle_offset):
        turtle.forward(size)
        turtle.right(angle + angle_offset)
        turtle.right(angle)
        self.sierpinski_lindenmayer_fn(turtle, iteration, size, angle)
        turtle.forward(size)
        turtle.right(angle)
        turtle.right(angle)
        turtle.forward(size)
        turtle.right(angle)
        turtle.right(angle)
        self.sierpinski_lindenmayer_fn(turtle, iteration, size, angle)
        turtle.forward(size)
        turtle.right(angle)
        turtle.right(angle)
        turtle.forward(size / 2)
        self.sierpinski_lindenmayer_fn(turtle, iteration, size, angle)

    # XF+G+XF−−F−−XF+G+X
    def sierpinski_lindenmayer_fn(self, turtle, iteration, size, angle):
        if iteration == 0:
            return

        size = size / 2
        self.sierpinski_lindenmayer_fn(turtle, iteration - 1, size, angle)
        turtle.forward(size)
        turtle.left(angle)
        turtle.forward(size)
        turtle.left(angle)

        self.sierpinski_lindenmayer_fn(turtle, iteration - 1, size, angle)
        turtle.forward(size)
        turtle.right(angle)
        turtle.right(angle)
        turtle.forward(size)
        turtle.right(angle)
        turtle.right(angle)

        self.sierpinski_lindenmayer_fn(turtle, iteration - 1, size, angle)
        turtle.forward(size)
        turtle.left(angle)
        turtle.forward(size)
        turtle.left(angle)

        self.sierpinski_lindenmayer_fn(turtle, iteration - 1, size, angle)

    def sierpinski(self, turtle, iteration, size, angle, angle_offset):
        max_length = size / (2**iteration)

        turtle.right(angle + angle_offset)
        turtle.forward(size, max_length)
        turtle.left(angle)
        turtle.forward(size, max_length)
        turtle.left(angle)

        self.sierpinski_fn(turtle, iteration, size, angle, max_length)

    def sierpinski_fn(self, turtle, iteration, size, angle, max_length):
        if iteration == 0:
            turtle.forward(size, max_length)
            return

        turtle.forward(size / 2, max_length)
        turtle.left(angle)

        self.sierpinski_fn(turtle, iteration - 1, size / 2, angle, max_length)
        turtle.right(angle)

        self.sierpinski_fn(turtle, iteration - 1, size / 2, angle, max_length)
        turtle.right(angle)

        self.sierpinski_fn(turtle, iteration - 1, size / 2, angle, max_length)
        turtle.left(angle)

        turtle.forward(size / 2, max_length)

    def pattern(self, process, iterations, size, angle, angle_offset, debug):
        turtle = Turtle()

        if process == "Lindenmayer System":
            self.sierpinski_lindenmayer(turtle, iterations, size, angle, angle_offset)
        else:
            self.sierpinski(turtle, iterations, size, angle, angle_offset)

        turtle.center(*self.canvas.centroid)

        for i, pos in enumerate(turtle.points):
            self.canvas.pattern += pos

            if debug:
                self.canvas.pattern += f"#{random.randint(10, 255):02x}{random.randint(10, 255):02x}{random.randint(10, 255):02x}"
                self.canvas.pattern += pos

            if i == 1:
                self.canvas.pattern.add_lock_stitches()

            if i % 25 == 0:
                yield self.canvas.pattern

        self.canvas.pattern.add_lock_stitches()

        yield self.canvas.pattern
