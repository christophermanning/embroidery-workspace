import streamlit as st
import random

from patterns import Pattern


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
                        "max_value": 1000,
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
                        "value": (50, 60),
                    },
                },
                "pseudorandom": {
                    "function": st.checkbox,
                    "args": {"label": "Pseudorandom", "value": True},
                },
            },
        }

    def pattern(self, steps, step_size, pseudorandom):
        if pseudorandom:
            random.seed(1)

        min_step, max_step = step_size
        pattern = self.canvas.pattern

        pattern += self.canvas.rand_point()

        for i in range(0, steps):
            ls = pattern.stitches[len(pattern.stitches) - 1]
            rp = self.canvas.rand_point_from(ls[0], ls[1], min_step, max_step)
            if rp:
                pattern += rp

            if i % 10 == 0:
                yield pattern

        sls = pattern.stitches[len(pattern.stitches) - 2]

        yield pattern
