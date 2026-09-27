"""Подводный мир: плывут рыбки, поднимаются пузыри, осьминог шевелит щупальцами."""

import math

from svg import (
    INK, W, WHITE, bug, circle, cheek, ellipse, eye, frame, g, linear, outlined,
    path, poly, rect, smile, translate, wrap)

SLUG = "underwater"
TITLE = "Underwater"

FRAMES = 6
FRAME_MS = 500

SEAWEED = [(14, 52, "#2fa84f"), (28, 38, "#43c463"), (212, 44, "#2fa84f"), (228, 58, "#43c463")]
BUBBLES = [(72, 0, 3.2), (78, 50, 2.2), (68, 100, 2.6), (150, 30, 2.8), (156, 80, 2), (120, 130, 2.4)]


def water():
    rays = [poly([(x, 0), (x + 22, 0), (x + 60, 135), (x + 30, 135)], WHITE, opacity="0.08")
            for x in (30, 110, 170)]
    return g(rect(0, 0, W, 135, "url(#water)"), *rays)


def seabed():
    return g(
        path("M0,118 Q40,110 90,117 T180,115 T240,114 L240,135 L0,135 Z", fill="#f2d28b",
             **outlined(1.4)),
        circle(62, 126, 1.5, "#d9b56a"), circle(120, 124, 1.8, "#d9b56a"),
        circle(160, 129, 1.4, "#d9b56a"),
        # морская звезда
        translate(44, 124, poly(
            [(math.cos(math.radians(a)) * (7 if i % 2 == 0 else 3),
              math.sin(math.radians(a)) * (7 if i % 2 == 0 else 3))
             for i, a in enumerate(range(-90, 270, 36))], "#ff8c42", **outlined(1.2))),
        # ракушка
        translate(104, 125, path("M-6,2 Q0,-9 6,2 Z", fill="#ffb3c7", **outlined(1.2)),
                  path("M0,2 L0,-5 M-3,2 L-2,-4 M3,2 L2,-4", stroke=INK, stroke_width=0.8)),
    )


def seaweed(index):
    plants = []
    for i, (x, height, color) in enumerate(SEAWEED):
        points = []
        for seg in range(5):
            y = 122 - seg * height / 4
            sway = math.sin(2 * math.pi * index / FRAMES + i + seg * 0.7) * seg * 1.6
            points.append((x + sway, y))
        d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in points)
        plants.append(path(d, stroke=INK, stroke_width=7.4, stroke_linecap="round",
                           stroke_linejoin="round"))
        plants.append(path(d, stroke=color, stroke_width=5, stroke_linecap="round",
                           stroke_linejoin="round"))
    return g(*plants)


def bubbles(index):
    period = 150
    items = []
    for x, y0, r in BUBBLES:
        y = 120 - wrap(y0 + index * period / FRAMES, period)
        wobble = math.sin(y / 9) * 2
        items.append(g(circle(x + wobble, y, r, "#dff6ff", opacity="0.35",
                              stroke=WHITE, stroke_width=0.9),
                       circle(x + wobble - r * 0.35, y - r * 0.35, r * 0.3, WHITE)))
    return g(*items)


def fish(x, y, body, stripe, tail_up, facing_right=True):
    tail = [(-10, 0), (-18, -8 if tail_up else -5), (-18, 8 if tail_up else 5)]
    shape = g(
        poly(tail, body, **outlined(1.3)),
        ellipse(0, 0, 12, 8, body, **outlined(1.5)),
        path("M-3,-7.5 Q-6,0 -3,7.5", stroke=stripe, stroke_width=3),
        path("M4,-6.5 Q2,0 4,6.5", stroke=stripe, stroke_width=2.4),
        poly([(-2, -7), (4, -12), (6, -6)], body, **outlined(1.1)),
        eye(6.5, -1.5, 2.4, look=(0.6, 0)),
        smile(9, 3, 1.6),
    )
    return translate(x, y, shape, scale=None if facing_right else (-1, 1))


def fishes(index):
    period = W + 44
    x1 = wrap(10 + index * period / FRAMES, period) - 22
    x2 = W + 22 - wrap(90 + index * period / FRAMES, period)
    return g(
        fish(x1, 38 + (2 if index % 2 else 0), "#ff8c42", WHITE, index % 2 == 0),
        fish(x2, 64 - (2 if index % 2 else 0), "#ffd23f", "#2f7de1", index % 2 == 1,
             facing_right=False),
    )


def octopus(index):
    bend = 1 if index % 2 == 0 else -1
    legs = []
    for i, dx in enumerate((-12, -6, 0, 6, 12)):
        c = bend * (5 if i % 2 == 0 else -5)
        d = f"M{dx},-4 Q{dx + c},8 {dx * 1.4},14 Q{dx * 1.5 - c * 0.6},19 {dx * 1.4 + c * 0.7},20"
        legs.append(path(d, stroke=INK, stroke_width=6.4, stroke_linecap="round"))
        legs.append(path(d, stroke="#ff6fae", stroke_width=4, stroke_linecap="round"))
    return translate(
        168, 103,
        *legs,
        ellipse(0, -14, 15, 14, "#ff6fae", **outlined(1.7)),
        circle(-5, -22, 2.2, "#ff9ccb"), circle(6, -24, 1.6, "#ff9ccb"),
        eye(-5, -13, 3.2, look=(0, 0.3)), eye(5, -13, 3.2, look=(0, 0.3)),
        cheek(-9, -7), cheek(9, -7),
        smile(0, -7, 3.5, open_=index in (2, 3)),
    )


def underwater_frame(index):
    return frame(
        water(),
        seaweed(index),
        seabed(),
        bubbles(index),
        octopus(index),
        fishes(index),
        bug("fish", "#1565c0"),
        defs=[linear("water", (0, "#5ccdf7"), (0.55, "#1e88e5"), (1, "#0d47a1"))],
    )


def frames():
    return [(underwater_frame(i), FRAME_MS) for i in range(FRAMES)]
