import streamlit as st
import os
import json
from pathlib import Path
from PIL import Image

st.logo("logo.png", icon_image=None, link="http://localhost:8501/")

build_dir = os.path.dirname(__file__) + "/../build"


images = []

for file in os.listdir(build_dir):
    if file.endswith(".png"):
        images.append(os.path.join(build_dir, file))

images.sort(key=lambda x: os.path.getmtime(x))
images.reverse()

with st.sidebar:
    st.markdown(f"`{len(images)}` images")

i = 0
with st.container():
    while i < len(images):
        for col in st.columns(3):
            col.image(images[i], width=200)

            img = Image.open(images[i])
            if img.text:
                key = "embroidery-workspace/v1/params"
                if key in img.text:
                    col.markdown(
                        f'<a href="{img.text[key]}" target="_self">Permalink</a>',
                        unsafe_allow_html=True,
                    )

            pes_file = images[i][0:-4] + ".pes"
            if os.path.isfile(pes_file):
                with open(pes_file, "rb") as f:
                    file = os.path.basename(pes_file)
                    col.download_button(
                        f"Download {file}",
                        f,
                        file_name=file,
                        key=f"download{i}",
                    )

            i += 1
            if i >= len(images):
                break

        st.divider()
