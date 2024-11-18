import re


def clean_basename(basename: str):
    return re.sub(r"[^a-z0-9-]", "_", basename.lower())
