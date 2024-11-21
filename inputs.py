import streamlit as st
import urllib
from typing import Tuple


class Inputs:
    def __init__(self):
        self.inputs = {}

    # get the input value and session state for an input
    #
    # the default value is loaded in this priority order:
    #  1. session
    #  2. URL query_params
    #  3. lambda function
    #  4. constant
    #
    # this function should have no `st` dependencies
    def input_value(
        self,
        func_name: str,
        session_state_value: str | int | float,
        query_param_value: str | int | float,
        **args,
    ) -> Tuple[dict, str | int | float]:
        if func_name == "selectbox":
            pass
        elif func_name == "slider":
            if query_param_value:
                if type(query_param_value) == str:
                    if "(" in query_param_value:
                        args["value"] = tuple(
                            [int(i) for i in query_param_value[1:-1].split(",")]
                        )
                    else:
                        args["value"] = int(query_param_value)

        elif func_name == "checkbox":
            if query_param_value:
                args["value"] = str(query_param_value) == "True"
        elif func_name == "number_input":
            if session_state_value:
                args["value"] = session_state_value
            elif query_param_value:
                if type(query_param_value) == str and "." in query_param_value:
                    args["value"] = float(query_param_value)
                else:
                    args["value"] = int(query_param_value)
            elif "value" in args and callable(args["value"]):
                # defining the value as a lambda is helpful for generating
                # runtime defaults that should persist after they are initially set
                # e.g. random.randint()
                value = args["value"]()
                session_state_value = value
                args["value"] = value

        return args, session_state_value

    # the load and input_value parsing are separate functions so loading the value
    # can be tested outside of a streamlit context
    def load(self, func, key, **args):
        if key in self.inputs:
            raise ValueError(f"duplicate key: {key}")

        session_state_value = st.session_state.get(key)
        query_param_value = st.query_params.get(key)

        [args, st.session_state[key]] = self.input_value(
            func.__name__, session_state_value, query_param_value, **args
        )

        val = func(**args)

        self.inputs[key] = val

        return val

    def permalink(self):
        params = {}

        for name, sli in self.inputs.items():
            if sli is not None:
                params[name] = sli

        return f"/?{urllib.parse.urlencode(params)}"
