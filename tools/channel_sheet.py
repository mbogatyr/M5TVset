"""Builds docs/channels.png: one frame from every channel, for the README.

The frames are the PNGs in art/frames/, the same images the firmware draws.
Run art/build.py first if the scenes changed.

    python3 tools/channel_sheet.py
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FRAMES = ROOT / "art" / "frames"
OUTPUT = ROOT / "docs" / "channels.png"
sys.path.insert(0, str(ROOT / "art"))

from scenes import CHANNELS  # noqa: E402

# The most telling frame of each channel, by slug.
PICK = {
    "news": 0, "animals": 2, "cartoons": 1, "weather": 5, "sport": 4, "space": 2,
    "underwater": 2, "science": 4, "playtime": 3, "ufo": 3, "history": 0,
}

SCALE = 2
COLUMNS = 3
GAP = 16
LABEL = 30
BACKGROUND = "#1c222a"
TEXT = "#e7ebf0"


def main():
    cell_w, cell_h = 240 * SCALE, 135 * SCALE
    rows = (len(CHANNELS) + COLUMNS - 1) // COLUMNS
    sheet = Image.new("RGB", (COLUMNS * (cell_w + GAP) + GAP,
                              rows * (cell_h + LABEL + GAP) + GAP), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=20)

    for number, channel in enumerate(CHANNELS, start=1):
        folder = FRAMES / f"{number:02d}_{channel.SLUG}"
        with Image.open(folder / f"{PICK[channel.SLUG]:02d}.png") as frame:
            big = frame.convert("RGB").resize((cell_w, cell_h), Image.NEAREST)
        index = number - 1
        # The last row is centered when it is not full.
        in_row = min(COLUMNS, len(CHANNELS) - index // COLUMNS * COLUMNS)
        offset = (COLUMNS - in_row) * (cell_w + GAP) // 2
        x = GAP + offset + (index % COLUMNS) * (cell_w + GAP)
        y = GAP + (index // COLUMNS) * (cell_h + LABEL + GAP)
        sheet.paste(big, (x, y))
        draw.text((x, y + cell_h + 6), f"{number}  {channel.TITLE}", fill=TEXT, font=font)

    OUTPUT.parent.mkdir(exist_ok=True)
    sheet.save(OUTPUT, optimize=True)
    print(f"{OUTPUT.relative_to(ROOT)}: {sheet.width}x{sheet.height}")


if __name__ == "__main__":
    main()
