# https://playwright.dev/python/docs/library#usage
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
import subprocess

from util import clean_basename


with sync_playwright() as p:
    browser = p.firefox.launch()

    screenshot_size = {"width": 1200, "height": 1100}
    page = browser.new_page(color_scheme="dark", viewport=screenshot_size)

    page.goto(
        f"http://localhost:8501/?pattern=Lettering&text=+Hello%0AWorld%0A++++++%3A%29"
    )
    page.get_by_test_id("completed").wait_for()
    page.screenshot(
        path="screenshot.png", full_page=True, clip={"x": 1, "y": 10} | screenshot_size
    )
    subprocess.run(
        [f"mogrify -strip -thumbnail 800x -path /src/ /src/screenshot.png"],
        shell=True,
    )
    print(f"generated application thumbnail")

    patterns = ["Grid", "Hilbert+Curve", "Random+Walk", "Spiral"]
    for pattern in patterns:
        page.goto(f"http://localhost:8501/?pattern={pattern}&random_seed=1")
        page.get_by_test_id("completed").wait_for()
        basename = clean_basename(pattern)
        subprocess.run(
            [
                f"mogrify -strip -thumbnail 400x -path /src/patterns/examples/thumbnails /src/build/{basename}.png"
            ],
            shell=True,
        )
        print(f"generated {basename} pattern thumbnail")

    browser.close()

img = Image.new("RGBA", (900, 100), (255, 0, 0, 0))
d = ImageDraw.Draw(img)
font = ImageFont.load_default(80)
d.text((0, 0), "Embroidery Workspace", fill=(255, 255, 255), font=font)
img.save("logo.png")
