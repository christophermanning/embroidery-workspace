import os

from .canvas_pattern import CanvasPattern
from .canvas import Canvas
from .turtle import Turtle
from .util import distance, bbox_contains


class Pattern:
    _patterns = []

    def __init__(self, canvas):
        self.canvas = canvas

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._patterns.append(cls)

    # this returns a dict which defines pattern attribute and streamlit options
    # that will be rendered and passed as named parameters to pattern
    def options():
        raise NotImplementedError

    # this function must yield the pattern once it is done generating it and it
    # may yield the pattern during generation for incremental rendering
    def pattern(self):
        raise NotImplementedError

    @classmethod
    def patterns(cls):
        options = []
        for subclass in cls._patterns:
            soptions = subclass.options()
            soptions["class"] = subclass
            options.append(soptions)
        return options
