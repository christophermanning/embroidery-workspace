import os
import importlib.util


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


# recursively import pattern files in subdirectories
base_dir = os.path.dirname(__file__)
for root, _, files in os.walk(base_dir):
    for file in files:
        if root != base_dir and file.endswith(".py") and file != "__init__.py":
            file_path = os.path.join(root, file)
            module_name = file[:-3]
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
