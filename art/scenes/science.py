"""Наука: сова-учёный ставит опыт — колба пузырится, меняет цвет и делает POP!"""

import math

from svg import (
    HEAVY_FONT, INK, W, WHITE, bug, circle, ellipse, eye, frame, g, line, linear,
    outlined, path, poly, rect, smile, tag, translate)

SLUG = "science"
TITLE = "Science"

# жидкость, пузыри (0 — мелкие, 1 — крупные), пена, взрыв, пробирка в крыле, лицо совы
STATES = [
    ("#6fdc6f", 0, False, False, False, "look"),
    ("#6fdc6f", 1, False, False, True, "look"),
    ("#b06cff", 1, False, False, False, "wow"),
    ("#b06cff", 1, True, False, False, "wow"),
    ("#ff7bc2", 0, False, True, False, "wow"),
    ("#ff7bc2", 0, False, False, False, "happy"),
]
DURATIONS = [600, 500, 500, 500, 1000, 800]

OWL = "#8d6e63"
OWL_LIGHT = "#bca08f"


def lab():
    return g(
        rect(0, 0, W, 135, "url(#wall)"),
        # полка с баночками
        rect(6, 34, 66, 4, "#a0714f", **outlined(1.2)),
        circle(18, 27, 6, "#ff6b6b", **outlined(1.3)), rect(15.5, 18, 5, 5, "#ff6b6b", **outlined(1)),
        rect(32, 14, 10, 20, "#4da6ff", rx=2, **outlined(1.3)), rect(34, 10, 6, 4, "#8a5a3c"),
        rect(50, 22, 14, 12, "#ffd23f", rx=3, **outlined(1.3)), rect(49, 19, 16, 4, "#e0e6ee", rx=1,
                                                                    **outlined(1)),
    )


def chalkboard(index):
    cx, cy = 174, 36
    orbits, electrons = [], []
    for k, angle in enumerate((0, 60, 120)):
        orbits.append(ellipse(cx, cy, 24, 8, "none", stroke=WHITE, stroke_width=1.2,
                              opacity="0.85", transform=f"rotate({angle} {cx} {cy})"))
        t = 2 * math.pi * (index / len(STATES) + k / 3)
        ex, ey = 24 * math.cos(t), 8 * math.sin(t)
        a = math.radians(angle)
        electrons.append(circle(cx + ex * math.cos(a) - ey * math.sin(a),
                                cy + ex * math.sin(a) + ey * math.cos(a), 2.4, "#ffe14d"))
    return g(
        rect(132, 8, 84, 58, "#a0714f", rx=3, **outlined(1.4)),
        rect(136, 12, 76, 50, "#2f5d50"),
        *orbits,
        circle(cx, cy, 4.5, "#ff8a65"),
        *electrons,
        rect(150, 64, 48, 3, "#a0714f", **outlined(1)),
        rect(160, 62, 8, 2.5, WHITE),
    )


def flask(color, bubble_size, foam):
    neck = "M122,60 L132,60 L132,74 L146,98 Q147,100 144,100 L110,100 Q107,100 108,98 L122,74 Z"
    liquid = "M116.5,84 L137.5,84 L146,98 Q147,100 144,100 L110,100 Q107,100 108,98 Z"
    r = 2.6 if bubble_size else 1.6
    bubbles = [circle(x, y, r * s, WHITE, opacity="0.75")
               for x, y, s in ((120, 94, 1), (130, 90, 0.8), (136, 95, 1.1), (126, 86, 0.7))]
    rising = []
    if bubble_size:
        rising = [circle(125, 52, 2.4, color, **outlined(1)), circle(131, 44, 1.8, color, **outlined(1))]
    foam_blob = ""
    if foam:
        foam_blob = g(
            path("M120,62 Q114,50 122,46 Q124,36 132,40 Q142,38 138,50 Q142,58 134,62 Z",
                 fill="#ffd6f0", **outlined(1.4)),
            path("M132,62 Q140,70 138,80", stroke="#ffd6f0", stroke_width=5, stroke_linecap="round"),
        )
    return g(
        rect(102, 96, 50, 5, "#3b4454", rx=1.5, **outlined(1.2)),
        circle(146, 98.5, 1.2, "#ff4d4d"),
        path(liquid, fill=color),
        *bubbles,
        path(neck, fill=WHITE, fill_opacity="0.25", **outlined(1.6)),
        path("M113,96 L121,82", stroke=WHITE, stroke_width=1.6, stroke_linecap="round",
             opacity="0.8"),
        rect(120, 57, 14, 4, "#e0e6ee", rx=1.5, **outlined(1.2)),
        *rising,
        foam_blob,
    )


def pop():
    puffs = [circle(x, y, r, c, **outlined(1.4)) for x, y, r, c in (
        (116, 44, 13, "#ffd6f0"), (138, 40, 14, "#fff3b0"), (126, 28, 12, "#d9c2ff"),
        (148, 52, 10, "#c8f7c5"), (106, 56, 9, "#bfe8ff"))]
    stars = [poly([(x, y - s), (x + s * 0.3, y - s * 0.3), (x + s, y), (x + s * 0.3, y + s * 0.3),
                   (x, y + s), (x - s * 0.3, y + s * 0.3), (x - s, y), (x - s * 0.3, y - s * 0.3)],
                  "#ffe14d", **outlined(1))
             for x, y, s in ((96, 30, 5), (160, 26, 6), (154, 70, 4), (100, 74, 4))]
    return g(
        *puffs, *stars,
        tag("text", "POP!", x=128, y=45, font_family=HEAVY_FONT, font_size=19,
            font_weight="bold", fill="#ff4d8d", text_anchor="middle", stroke=INK,
            stroke_width=4, stroke_linejoin="round", paint_order="stroke",
            transform="rotate(-8 128 40)"),
    )


def goggles_eye(cx, cy, face):
    if face == "happy":
        inner = path(f"M{cx - 4},{cy + 1} Q{cx},{cy - 4} {cx + 4},{cy + 1}", stroke=INK,
                     stroke_width=1.8, stroke_linecap="round")
    else:
        big = face == "wow"
        inner = eye(cx, cy, 5 if big else 4.4, look=(0.8, 0.5) if face == "look" else (0, 0))
    return g(
        circle(cx, cy, 8.5, "#bfe6ff", opacity="0.9"),
        inner,
        circle(cx, cy, 8.5, "none", stroke="#3b4454", stroke_width=2.2),
    )


def owl(face, holding_tube):
    tufts_up = face == "wow"
    tuft = -8 if tufts_up else -4
    wing_right = (
        g(path("M88,78 Q104,66 108,52", stroke=INK, stroke_width=9, stroke_linecap="round"),
          path("M88,78 Q104,66 108,52", stroke=WHITE, stroke_width=6.4, stroke_linecap="round"),
          translate(111, 52,
                    rect(-2.5, -12, 5, 16, "#e8f6ff", rx=2.5, **outlined(1.2)),
                    rect(-2.5, -2, 5, 6, "#4da6ff", rx=2.5),
                    rotate=50),
          path("M118,58 q-1.5,2.5 0,3.5 q1.5,-1 0,-3.5 z", fill="#4da6ff", **outlined(0.8)))
        if holding_tube else
        g(path("M88,80 Q98,88 100,98", stroke=INK, stroke_width=9, stroke_linecap="round"),
          path("M88,80 Q98,88 100,98", stroke=WHITE, stroke_width=6.4, stroke_linecap="round"))
    )
    return g(
        poly([(50, 50), (52, 50 + tuft - 10), (60, 46)], OWL, **outlined(1.4)),
        poly([(92, 50), (90, 50 + tuft - 10), (82, 46)], OWL, **outlined(1.4)),
        ellipse(71, 80, 25, 32, OWL, **outlined(1.8)),
        # халат
        path("M47,86 Q48,68 60,66 L71,90 L82,66 Q94,68 95,86 L95,112 L47,112 Z", fill=WHITE,
             **outlined(1.5)),
        ellipse(71, 78, 8, 10, OWL_LIGHT),
        rect(84, 88, 7, 8, "#e0e6ee", rx=1, **outlined(1)),
        line(86, 86, 86, 91, "#e63946", 1.4),
        path("M54,80 Q44,90 46,100", stroke=INK, stroke_width=9, stroke_linecap="round"),
        path("M54,80 Q44,90 46,100", stroke=WHITE, stroke_width=6.4, stroke_linecap="round"),
        wing_right,
        # голова и очки
        rect(52, 58, 38, 4, "#3b4454", rx=2),
        goggles_eye(62, 60, face),
        goggles_eye(80, 60, face),
        poly([(68, 68), (74, 68), (71, 75)], "#ffa62b", **outlined(1.2)),
        ellipse(71, 73, 2.5, 1.6, "#7a2231") if face == "wow" else "",
    )


def bench():
    drawers = [g(rect(x, 110, 44, 18, "#7d90ab", rx=2, **outlined(1.2)),
                 rect(x + 17, 117, 10, 3, "#d7dee8", rx=1.5))
               for x in (8, 60, 170)]
    tubes = [g(rect(x, 80, 6, 18, "#e8f6ff", rx=3, **outlined(1.1)),
               rect(x, 88 + (i % 2) * 3, 6, 10 - (i % 2) * 3, color, rx=3))
             for i, (x, color) in enumerate(((176, "#ff6b6b"), (186, "#ffd23f"),
                                             (196, "#4da6ff"), (206, "#6fdc6f")))]
    return g(
        rect(0, 100, W, 35, "#6d7f99"),
        rect(0, 100, W, 5, "#8ea1bb", **outlined(1.4)),
        *drawers,
        *tubes,
        rect(172, 90, 42, 4, "#a0714f", **outlined(1.1)),
        rect(172, 97, 42, 3, "#a0714f", **outlined(1.1)),
    )


def science_frame(index):
    color, bubbles, foam, popped, tube, face = STATES[index]
    return frame(
        lab(),
        chalkboard(index),
        translate(0, -7, owl(face, tube)),
        bench(),
        flask(color, bubbles, foam),
        pop() if popped else "",
        bug("atom", "#2f5d50"),
        defs=[linear("wall", (0, "#d7f2ee"), (1, "#a9ddd5"))],
    )


def frames():
    return [(science_frame(i), ms) for i, ms in enumerate(DURATIONS)]
