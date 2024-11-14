import streamlit as st
import time
import copy

from gif import Gif

from patterns import Pattern, Canvas, CanvasPattern

from util import clean_basename
from inputs import Inputs

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
        for pkg, module_name, _ in modules:
            importlib.import_module(module_name, pkg)

inputs = Inputs()
args = {}

st.logo("logo.png", icon_image=None, link="http://localhost:8501/")

st.markdown(
    "<style>div.st-emotion-cache-qeahdt h1, div.st-emotion-cache-qeahdt { padding-top: 0 } </style>",
    unsafe_allow_html=True,
)
with st.sidebar:
    with st.expander("## Pattern", True):
        patterns = Pattern.patterns()
        pattern_labels = [d["label"] for d in patterns]
        selected_pattern = inputs.load(
            st.selectbox,
            "pattern",
            label="Pattern",
            options=pattern_labels,
            label_visibility="collapsed",
            index=pattern_labels.index(st.query_params.get("pattern", "Random Walk")),
            # when the pattern changes, unset any existing query parameters
            on_change=lambda: st.query_params.from_dict({}),
        )
        selected_pattern = next(d for d in patterns if d["label"] == selected_pattern)

        if "options" in selected_pattern:
            for key, option in selected_pattern["options"].items():
                # this will display a `st.` input defined in the pattern
                args[key] = inputs.load(option["function"], key, **option["args"])

    with st.expander("## Canvas"):
        col1, col2, col3 = st.columns(3)
        with col1:
            width = inputs.load(
                st.number_input, "canvas_width", value=1000, label="Width"
            )
        with col2:
            height = inputs.load(
                st.number_input, "canvas_height", value=1000, label="Height"
            )
        with col3:
            margin = inputs.load(
                st.number_input, "canvas_margin", value=10, label="Margin"
            )

        col1, col2 = st.columns(2)
        with col1:
            initial_color = inputs.load(
                st.color_picker,
                "canvas_initial_thread_color",
                value="#DDDDDD",
                label="Initial Thread Color",
            )
        with col2:
            background_color = inputs.load(
                st.color_picker,
                "canvas_background_color",
                value="#0E1117",
                label="Background Color",
            )

    canvas = Canvas(width, height, margin, initial_color)
    pattern_class = selected_pattern["class"](canvas)

    with st.expander("## Build", True):
        pattern = None
        start = time.time()
        pattern_snapshots = []
        with st.spinner("Generating Pattern..."):
            for i, pattern_snapshot in enumerate(pattern_class.pattern(**args)):
                pattern_snapshots.append(copy.copy(pattern_snapshot))
                pattern = pattern_snapshot

        if pattern == None:
            st.markdown(f"- :red[ERROR] no stitches generated")
        else:
            pattern_generation_time = time.time() - start

            num_stitches = len(pattern.stitches)
            num_threads = len(pattern.threadlist)

            pattern_details = []

            for log in pattern_class.log:
                pattern_details.append(f"- {log}")

            if not canvas.pattern.in_bounds():
                pattern_details.append(f"- :red[ERROR] pattern does not fit in bounds")

            pattern_details.append(f"- `{round(pattern_generation_time, 2)}` seconds")
            pattern_details.append(f"- _Stitches_ `{num_stitches}`")

            if num_threads > 1:
                pattern_details.append(f"- _Threads_ `{num_threads}`")

            pattern_details.append(f"- _Bounds_ `{pattern.bounds()}`")
            bx, by = pattern.stitch_bounds()
            pattern_details.append(f"- _Size_ `{round(bx,2)}` x `{round(by,2)}`")

            pattern_details.append(f" - [Permalink]({inputs.permalink()})")

            st.markdown(
                f"""
                    {'\n' + '\n'.join([f"\t {p}" for p in pattern_details])}
                  """
            )

    with st.expander("## Output", True):
        output_formats = st.multiselect(
            "Formats",
            options=["PNG", "PES", "GIF"],
            default=["PNG"],
        )

        file_basename = selected_pattern["label"].lower()

        if pattern_class.basename != None:
            file_basename = pattern_class.basename

        file_basename = clean_basename(file_basename)

        file_basename_override = st.text_input(
            "File basename", placeholder=file_basename
        )

        if file_basename_override != "":
            file_basename = clean_basename(file_basename_override)

        image_config = {"background": background_color, "linewidth": 2}

        if not os.path.isdir("build"):
            os.makedirs("build")

        if "PES" in output_formats:
            filename_pes = f"build/{file_basename}.pes"
            start = time.time()
            write_pes(
                pattern,
                filename_pes,
                {
                    "version": "6",
                    "tie_on": CONTINGENCY_TIE_ON_NONE,
                    "tie_off": CONTINGENCY_TIE_OFF_NONE,
                },
            )

            pes_generation_time = time.time() - start
            st.markdown(
                f" - `{filename_pes}`\n    - `{round(pes_generation_time, 2)}` seconds"
            )

        filename_png = None
        if "PNG" in output_formats:
            filename_png = f"build/{file_basename}.png"
            start = time.time()
            with st.spinner("Generating PNG..."):
                write_png(pattern, filename_png, image_config)
            png_generation_time = time.time() - start
            st.markdown(
                f" - `{filename_png}`\n    - `{round(png_generation_time, 2)}` seconds"
            )

        filename_gif = None
        if "GIF" in output_formats:
            with st.spinner("Generating GIF..."):
                start = time.time()
                gif = Gif(CanvasPattern(width=width, height=height), image_config)
                for i, pattern_snapshot in enumerate(pattern_snapshots):
                    gif.frame_from_pattern(pattern_snapshot)
                    if i > 1000:
                        st.write("ERROR: too many gif frames")
                        break

                try:
                    filename_gif = f"build/{file_basename}.gif"
                    gif_frames = gif.save(filename_gif)
                    gif_generation_time = time.time() - start
                    st.markdown(
                        f" - `{filename_gif}`\n   - `{round(gif_generation_time, 2)}` seconds\n   - Frames: `{len(gif_frames)}`"
                    )
                except ValueError as e:
                    st.write("GIF Error:", str(e))
                    filename_gif = None

if filename_png:
    st.image(filename_png)

if filename_gif:
    st.image(filename_gif)

# used by playwright to detect when the page has finished loading
st.html('<span data-testid="completed">&nbsp;</span>')
