import streamlit as st
import random

from patterns import Pattern, Turtle, bbox_contains


class RandomWalk(Pattern):
    def options():
        return {
            "label": "Random Walk",
            "inputs": {
                "steps": {
                    "function": st.slider,
                    "args": {
                        "label": "Steps",
                        "min_value": 10,
                        "max_value": 2000,
                        "step": 1,
                        "value": 1000,
                    },
                },
                "heading_step": {
                    "function": st.slider,
                    "args": {
                        "label": "Heading Step",
                        "min_value": 1,
                        "max_value": 180,
                        "step": 1,
                        "value": 1,
                    },
                },
                "step_size": {
                    "function": st.slider,
                    "args": {
                        "label": "Step Size",
                        "min_value": 20,
                        "max_value": 100,
                        "step": 1,
                        "value": (20, 40),
                    },
                },
                "random_seed": {
                    "function": st.number_input,
                    "args": {
                        "label": "Random Seed",
                        "value": lambda: random.randint(0, 999_999_999),
                        "step": 1,
                    },
                },
            },
        }

    def pattern(self, steps, heading_step, step_size, random_seed):
        min_step, max_step = step_size
        random.seed(random_seed)

        turtle = Turtle()

        turtle.goto(*self.canvas.centroid)

        headings = range(0, 360, heading_step)
        for i in range(0, steps):
            turtle.setheading(random.choice(headings))
            turtle.forward(random.uniform(min_step, max_step))

            pos = turtle.pos()
            bbox = [pos[0], pos[1], pos[0] + 1, pos[1] + 1]
            if not bbox_contains(self.canvas.bbox, bbox):
                turtle.undo()
                continue

            self.canvas.pattern += pos

            if i % 50 == 0:
                yield self.canvas.pattern

        self.canvas.pattern.center(*self.canvas.centroid)

        yield self.canvas.pattern
