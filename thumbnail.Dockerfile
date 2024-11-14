FROM python:3.12.7-slim

RUN pip install --upgrade pip

# use playwright to interact with streamlit
# https://playwright.dev/python/docs/library
RUN pip install playwright
RUN playwright install-deps
RUN playwright install firefox

# used for image generation
RUN pip install pillow

# use imagemagick to compress example images
RUN apt-get update
RUN apt-get install -y imagemagick

WORKDIR /src
