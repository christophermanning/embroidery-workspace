import streamlit as st
import time

from gif import Gif

from patterns import Pattern
from patterns.canvas import Canvas

from pyembroidery import (
    write_png,
    write_pes,
    CONTINGENCY_TIE_ON_NONE,
    CONTINGENCY_TIE_OFF_NONE,
)

# dynamically import pattern package namespace modules so streamlit reloads the app when those files change
# modules must be imported in this file so streamlit rerun this file when modules are updated
import os
import pkgutil
import importlib

patterns_dir = os.path.dirname(__file__) + "/patterns"
packages = pkgutil.walk_packages(path=[patterns_dir])
for importer, name, is_package in packages:
    if is_package:
        modules = pkgutil.iter_modules(path=[os.path.join(importer.path, name)])
        for _, module_name, _ in modules:
            mod = importlib.import_module(module_name)

args = {}

st.markdown(
    "<style>div.st-emotion-cache-qeahdt h1, div.st-emotion-cache-qeahdt { padding-top: 0 } </style>",
    unsafe_allow_html=True,
)
with st.sidebar:
    st.title("Embroidery Workspace")

    st.markdown("## Pattern")
    patterns = Pattern.patterns()
    selected_pattern = st.selectbox(
        "Pattern", [d["label"] for d in patterns], label_visibility="collapsed"
    )
    selected_pattern = next(d for d in patterns if d["label"] == selected_pattern)

    if "options" in selected_pattern:
        for key, option in selected_pattern["options"].items():
            # this will display a `st.` input defined in the pattern
            args[key] = option["function"](**option["args"])

    st.markdown("## Canvas")
    col1, col2, col3 = st.columns(3)
    with col1:
        width = st.number_input("Width", value=1000)
    with col2:
        height = st.number_input("Height", value=1000)
    with col3:
        margin = st.number_input("Margin", value=10)

    col1, col2 = st.columns(2)
    with col1:
        initial_color = st.color_picker("Initial Thread Color", "#DDDDDD")
    with col2:
        background_color = st.color_picker("Background Color", "#0E1117")

    canvas = Canvas(width, height, margin, initial_color)
    pattern_class = selected_pattern["class"](canvas)

    st.markdown("## Output")
    output_formats = st.multiselect(
        "Formats",
        options=["PNG", "PES", "GIF"],
        default=["PNG"],
    )

    image_config = {"background": background_color, "linewidth": 2}
    gif = Gif(Canvas.new_pattern(width, height), image_config)

    # generate the pattern
    pattern = None
    start = time.time()
    with st.spinner("Generating Pattern..."):
        for pattern_snapshot in pattern_class.pattern(**args):
            if "GIF" in output_formats:
                gif.frame_from_pattern(pattern)
            pattern = pattern_snapshot

    pattern_generation_time = time.time() - start

    pattern_norm = pattern.get_normalized_pattern()
    num_stitches = len(pattern_norm.stitches)
    st.markdown(
        f"""
            - Pattern
                - `{round(pattern_generation_time, 2)}` seconds
                - _Stitches_ `{num_stitches}`
                - _Bounds_ `{pattern_norm.bounds()}`
          """
    )

    if "PES" in output_formats:
        filename_pes = "build/pattern.pes"
        write_pes(
            pattern,
            filename_pes,
            {
                "version": "6",
                "tie_on": CONTINGENCY_TIE_ON_NONE,
                "tie_off": CONTINGENCY_TIE_OFF_NONE,
            },
        )

        st.markdown(
            f"""
            - `{filename_pes}`
             """
        )

    filename_png = None
    if "PNG" in output_formats:
        filename_png = "build/pattern.png"
        start = time.time()
        with st.spinner("Generating PNG..."):
            write_png(pattern, filename_png, image_config)
        png_generation_time = time.time() - start
        st.markdown(
            f" - `{filename_png}`\n    - `{round(png_generation_time, 2)}` seconds"
        )

    gif_file = None
    if "GIF" in output_formats:
        with st.spinner("Generating GIF..."):
            try:
                gif_file = gif.save()
                st.markdown(
                    f" - `{gif_file['filename']}`\n   - Frames: `{len(gif_file['frames'])}`"
                )
            except ValueError as e:
                st.write("GIF Error:", str(e))

if filename_png:
    st.image(filename_png)

if gif_file:
    st.image(gif_file["filename"])
