import os
import pkgutil
import importlib

import unittest

from patterns import Pattern, Canvas
from inputs import Inputs

patterns_dir = os.path.dirname(__file__) + "/../patterns"
packages = pkgutil.walk_packages(path=[patterns_dir])
for importer, name, is_package in packages:
    if is_package:
        modules = pkgutil.iter_modules(path=[os.path.join(importer.path, name)])
        for pkg, module_name, ip in modules:
            importlib.import_module(module_name, pkg)


class TestPatterns(unittest.TestCase):
    def test_all_patterns(self):
        patterns = Pattern.patterns()

        width = 1000
        height = 1000
        margin = 10
        initial_color = "white"

        self.assertGreater(len(patterns), 0, "no patterns found")

        inputs = Inputs()

        for pattern in patterns:
            canvas = Canvas(width, height, margin, initial_color)
            pattern_class = pattern["class"](canvas)
            args = []
            if "inputs" in pattern:
                # get default input values to manually construct the args
                # because loading input options in the test env causes streamlit warnings
                for key, option in pattern["inputs"].items():
                    option["args"] = inputs.input_value(
                        option["function"].__name__, None, None, **option["args"]
                    )[0]

                    if "value" in option["args"]:
                        args.append(option["args"]["value"])
                    else:
                        match option["function"].__name__:
                            case "selectbox":
                                args.append(option["args"]["options"][0])
                            case "multiselect":
                                args.append(option["args"]["default"])
                            case _:
                                args.append("")

            # generate the pattern
            list(pattern_class.pattern(*args))

            self.assertGreater(
                len(canvas.pattern.stitches),
                10,
                f"{pattern['label']} pattern didn't generate enough stitches",
            )
