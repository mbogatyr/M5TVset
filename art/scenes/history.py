"""History: a pharaoh cat talks about Ancient Egypt, with pyramids, a camel and hieroglyphs."""

from svg import (
    HEAVY_FONT, INK, W, WHITE, bug, cheek, circle, ellipse, eye, frame, g, limb,
    line, linear, outlined, path, poly, rect, smile, text, translate, wrap)

SLUG = "history"
TITLE = "History"

FRAMES = 6
FRAME_MS = 650
BAND_Y = 118

MOUTH = [True, False, True, False, True, True]
GLYPHS = ["ankh", "eye", "bird", "scarab", "sun", "water"]

GOLD = "#ffc933"
LAPIS = "#1f4fa8"
SAND = "#f2c46d"
GLYPH_INK = "#7a4b2a"


def desert():
    return g(
        rect(0, 0, W, 135, "url(#sky)"),
        circle(186, 26, 16, "#fff3b0", opacity="0.5"),
        circle(186, 26, 11, "#ffd23f", **outlined(1.4)),
        # pyramids: lit and shaded faces
        poly([(108, 96), (156, 44), (204, 96)], "#f6cf7a", **outlined(1.6)),
        poly([(156, 44), (204, 96), (170, 96)], "#d9a24a"),
        poly([(108, 96), (156, 44), (204, 96)], "none", **outlined(1.6)),
        poly([(186, 96), (216, 64), (246, 96)], "#f6cf7a", **outlined(1.5)),
        poly([(216, 64), (246, 96), (226, 96)], "#d9a24a"),
        poly([(186, 96), (216, 64), (246, 96)], "none", **outlined(1.5)),
        path("M0,94 Q70,86 140,95 T240,92 L240,135 L0,135 Z", fill=SAND),
        path("M0,106 Q90,100 170,107 T240,104 L240,135 L0,135 Z", fill="#e7b458"),
        # palm tree
        rect(96, 74, 4, 26, "#8a5a3c", rx=2, **outlined(1.1), transform="rotate(6 98 100)"),
        *[ellipse(98 + dx, 72 + dy, 11, 3.5, "#4f9a35", **outlined(1.2),
                  transform=f"rotate({a} {98 + dx} {72 + dy})")
          for dx, dy, a in ((-8, 0, 20), (8, 0, -20), (-6, -4, -30), (6, -4, 30))],
    )


def camel(index):
    period = W + 60
    x = wrap(40 + index * period / FRAMES, period) - 30
    stride = index % 2 == 0
    legs = ([(-10, -6, -14, 8), (-4, -6, -2, 8), (8, -6, 4, 8), (13, -6, 16, 8)] if stride
            else [(-10, -6, -8, 8), (-4, -6, -6, 8), (8, -6, 10, 8), (13, -6, 11, 8)])
    return translate(
        x, 102,
        *[limb(*l, "#d9a066", 2.8) for l in legs],
        path("M-13,-10 Q-17,-6 -16,0", stroke=INK, stroke_width=1.3),
        ellipse(2, -10, 15, 7, "#d9a066", **outlined(1.5)),
        path("M-6,-15 Q2,-30 10,-15 Z", fill="#d9a066", **outlined(1.5)),
        path("M14,-12 Q20,-18 20,-27", stroke=INK, stroke_width=7.4, stroke_linecap="round"),
        path("M14,-12 Q20,-18 20,-27", stroke="#d9a066", stroke_width=5, stroke_linecap="round"),
        ellipse(24, -29, 6, 4, "#d9a066", **outlined(1.3)),
        circle(23, -30, 1, INK),
        ellipse(20, -33, 1.6, 2.4, "#d9a066", **outlined(1)),
        rect(-4, -18, 12, 4, "#e63946", rx=1.5, **outlined(1)),
    )


def glyph(name):
    s = {"stroke": GLYPH_INK, "stroke_width": 2.2, "stroke_linecap": "round",
         "stroke_linejoin": "round"}
    if name == "ankh":
        return g(ellipse(0, -6, 3.6, 4.6, "none", **s), path("M0,-1 V10 M-6,0 H6", **s))
    if name == "eye":
        return g(path("M-9,0 Q0,-8 9,0 Q0,6 -9,0 Z", fill="none", **s), circle(0, -0.5, 2.4, GLYPH_INK),
                 path("M-2,4 L-3,10 M3,4 Q8,10 4,11", fill="none", **s))
    if name == "bird":
        return g(ellipse(-1, 1, 6, 4, GLYPH_INK), path("M4,-1 Q7,-8 4,-10 L9,-9", fill="none", **s),
                 path("M-2,5 V10 M1,5 V10 M-7,0 L-11,3", fill="none", **s))
    if name == "scarab":
        return g(circle(0, -9, 3.4, "none", **s), ellipse(0, 2, 5, 6, GLYPH_INK),
                 path("M-5,0 L-9,-2 M-5,4 L-9,6 M5,0 L9,-2 M5,4 L9,6", fill="none", **s))
    if name == "sun":
        return g(circle(0, 0, 7, "none", **s), circle(0, 0, 1.8, GLYPH_INK))
    return path("M-10,-3 l3.3,4 l3.3,-4 l3.3,4 l3.3,-4 l3.3,4 M-10,4 l3.3,4 l3.3,-4 l3.3,4 l3.3,-4 l3.3,4",
                fill="none", **s)


def speech(index):
    return g(
        path("M76,18 H128 Q134,18 134,24 V52 Q134,58 128,58 H90 L80,66 L82,58 H76 Q70,58 70,52 "
             "V24 Q70,18 76,18 Z", fill="#f7e3b0", **outlined(1.6)),
        translate(102, 38, glyph(GLYPHS[index]), scale=1.3),
    )


def pharaoh(index):
    stripes = [path(f"M{x1},{y1} L{x2},{y2}", stroke=LAPIS, stroke_width=2.4)
               for x1, y1, x2, y2 in ((24, 62, 18, 98), (30, 58, 25, 100), (60, 58, 65, 100),
                                     (66, 62, 72, 98))]
    return g(
        # nemes: the striped headcloth
        path("M20,58 Q24,36 45,34 Q66,36 70,58 L74,100 L62,104 L58,70 L32,70 L28,104 L16,100 Z",
             fill=GOLD, **outlined(1.6)),
        *stripes,
        # broad collar necklace
        path("M18,118 Q20,94 45,92 Q70,94 72,118 Z", fill="#e6f0ff", **outlined(1.5)),
        path("M24,112 Q45,96 66,112", stroke=LAPIS, stroke_width=3),
        path("M28,117 Q45,104 62,117", stroke=GOLD, stroke_width=3),
        path("M32,108 Q45,100 58,108", stroke="#e63946", stroke_width=2.4),
        # cat head
        poly([(31, 48), (29, 32), (40, 42)], "#b89a70", **outlined(1.4)),
        poly([(59, 48), (61, 32), (50, 42)], "#b89a70", **outlined(1.4)),
        circle(45, 60, 16, "#c9aa7c", **outlined(1.7)),
        path("M32,45 Q45,38 58,45 L58,50 Q45,44 32,50 Z", fill=GOLD, **outlined(1.2)),
        rect(42, 38, 6, 7, LAPIS, rx=2, **outlined(1)),
        eye(39, 58, 3.2, look=(0.5, 0)), eye(51, 58, 3.2, look=(0.5, 0)),
        path("M33,58 H28 M57,58 H62", stroke=INK, stroke_width=1.6, stroke_linecap="round"),
        cheek(35, 65), cheek(55, 65),
        ellipse(45, 67, 8, 5.5, "#eadcc4"),
        poly([(42.5, 64), (47.5, 64), (45, 66.5)], "#e36b86"),
        smile(45, 68.5, 3.4, open_=MOUTH[index]),
        rect(42, 74, 6, 8, LAPIS, rx=1, **outlined(1)),
    )


def band():
    diamonds = [poly([(x, BAND_Y + 3), (x + 3, BAND_Y + 8.5), (x, BAND_Y + 14), (x - 3, BAND_Y + 8.5)],
                     GOLD) for x in (90, 226)]
    return g(
        rect(0, BAND_Y, W, 17, LAPIS),
        rect(0, BAND_Y, W, 2, GOLD),
        *diamonds,
        text(158, BAND_Y + 13, "ANCIENT EGYPT", 10.5, GOLD, font=HEAVY_FONT, anchor="middle"),
    )


def history_frame(index):
    return frame(
        desert(),
        camel(index),
        speech(index),
        band(),
        pharaoh(index),
        bug("pyramid", "#c9772a"),
        defs=[linear("sky", (0, "#7fcbff"), (0.7, "#ffe7b3"))],
    )


def frames():
    return [(history_frame(i), FRAME_MS) for i in range(FRAMES)]
