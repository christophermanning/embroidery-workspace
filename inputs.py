import streamlit as st
import urllib


class Inputs:
    def __init__(self):
        self.inputs = {}

    def load(self, func, key, **args):
        if func.__name__ != "selectbox":
            args["value"] = st.query_params.get(
                key, args["value"] if "value" in args else None
            )

            if args["value"]:
                if func.__name__ == "slider":
                    if type(args["value"]) == str:
                        if "(" in args["value"]:
                            args["value"] = tuple(
                                [int(i) for i in args["value"][1:-1].split(",")]
                            )
                        else:
                            args["value"] = int(args["value"])
                elif func.__name__ == "number_input":
                    if type(args["value"]) == str and "." in args["value"]:
                        args["value"] = float(args["value"])
                    else:
                        args["value"] = int(args["value"])

        val = func(**args)

        if key in self.inputs:
            raise ValueError(f"duplicate key: {key}")

        self.inputs[key] = val
        return val

    def permalink(self):
        params = {}

        for name, sli in self.inputs.items():
            if sli is not None:
                params[name] = sli

        return f"/?{urllib.parse.urlencode(params)}"
