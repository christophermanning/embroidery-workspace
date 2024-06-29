import streamlit as st
import random

from patterns import Pattern, Turtle


class RandomWalk(Pattern):
    def options():
        return {
            "label": "Random Walk",
            "options": {
                "steps": {
                    "function": st.slider,
                    "args": {
                        "label": "Steps",
                        "min_value": 10,
                        "max_value": 2000,
                        "step": 1,
                        "value": 500,
                    },
                },
                "step_size": {
                    "function": st.slider,
                    "args": {
                        "label": "Step Size",
                        "min_value": 10,
                        "max_value": 100,
                        "step": 1,
                        "value": (20, 40),
                    },
                },
                "pseudorandom": {
                    "function": st.checkbox,
                    "args": {"label": "Pseudorandom", "value": True},
                },
            },
        }

    def pattern(self, steps, step_size, pseudorandom):
        min_step, max_step = step_size

        if pseudorandom:
            random.seed(1)

        turtle = Turtle()

        for i in range(0, steps):
            turtle.setheading(random.uniform(0, 360))
            turtle.forward(random.uniform(min_step, max_step))

        turtle.center(*self.canvas.centroid)

        for i, pos in enumerate(turtle.points):
            self.canvas.pattern += pos
            if i % 50 == 0:
                yield self.canvas.pattern

        yield self.canvas.pattern
