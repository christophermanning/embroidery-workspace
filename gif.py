import os, glob
from pyembroidery import write_png, EmbThread
import imageio.v3 as iio


class Gif:
    def __init__(self, pattern, image_config):
        self.frame_index = 0
        self.image_config = image_config
        self.pattern = pattern

        os.makedirs("build/gif", exist_ok=True)
        for f in glob.glob("build/gif/*.png"):
            os.remove(f)

    def frame_from_pattern(self, pattern):
        write_png(
            pattern,
            "build/gif/%d.png" % self.frame_index,
            self.image_config,
        )
        self.frame_index += 1

    def save(self, filename):
        images = []
        frames = sorted(glob.glob("build/gif/*.png"), key=os.path.getmtime)

        if len(frames) == 0:
            raise ValueError("No Frames Found")

        for i, f in enumerate(frames):
            images.append(iio.imread(f))

        durations = [1] * len(images)

        # pause before looping
        durations[-1] = 5000

        # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif-saving
        iio.imwrite(filename, images, duration=durations, loop=0)
        return frames
