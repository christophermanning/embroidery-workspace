# embroidery-workspace

[![Hello World Screenshot](screenshot.png)](patterns/examples/text.py)

Streamlit app for generating embroidery patterns using pyembroidery.

Patterns are classes that implement `Pattern` and are defined in `patterns/$NAMESPACE/*.py`.
Refer to [`patterns/examples`](patterns/examples) for examples.

Pattern namespaces may also define a newline delimited `packages.txt` and `requirements.txt` file to install
Debian and Python dependencies into the Docker image.

## Running

```
make up
```

## Examples

[![Grid](patterns/examples/thumbnails/grid.png)](patterns/examples/grid.py) | [![Hilbert Curve](patterns/examples/thumbnails/hilbert_curve.png)](patterns/examples/hilbert_curve.py)
-- | --
[![Random Walk](patterns/examples/thumbnails/random_walk.png)](patterns/examples/random_walk.py) | [![Spiral](patterns/examples/thumbnails/spiral.png)](patterns/examples/spiral.py)
