"""Space: stars twinkle, a rocket flies by, an astronaut waves."""

import random

from svg import (
    INK, W, WHITE, bug, circle, ellipse, frame, g, linear, outlined, path, poly,
    rect, smile, translate, wrap)

SLUG = "space"
TITLE = "Space"

FRAMES = 6
FRAME_MS = 500

_rng = random.Random(7)
STARS = [(_rng.uniform(0, W), _rng.uniform(0, 135), _rng.uniform(0.6, 1.4), _rng.randrange(3))
         for _ in range(42)]
SPARKLES = [(96, 20), (214, 60), (132, 118), (20, 70), (170, 16)]


def sky(index):
    stars = []
    for x, y, r, phase in STARS:
        scale = (0.55, 1.0, 1.35)[(index + phase) % 3]
        stars.append(circle(x, y, r * scale, WHITE, opacity="0.9"))
    sparkles = []
    for i, (x, y) in enumerate(SPARKLES):
        s = 4.5 if (index + i) % 2 else 2.5
        sparkles.append(poly(
            [(x, y - s), (x + s * 0.28, y - s * 0.28), (x + s, y), (x + s * 0.28, y + s * 0.28),
             (x, y + s), (x - s * 0.28, y + s * 0.28), (x - s, y), (x - s * 0.28, y - s * 0.28)],
            "#fff6c2"))
    return g(rect(0, 0, W, 135, "url(#space)"), *stars, *sparkles)


def ringed_planet():
    ring = "M-40,0 A40,9 0 0 1 40,0"
    return translate(
        46, 104,
        g(path(ring, stroke=INK, stroke_width=6.4), path(ring, stroke="#ffd98a", stroke_width=3.6),
          transform="rotate(-14) scale(1,-1)"),
        circle(0, 0, 22, "#ff9f43", **outlined(1.8)),
        path("M-21,-6 Q0,-2 21,-8 M-19,8 Q0,12 20,5", stroke="#e67a22", stroke_width=4),
        circle(-7, -9, 3, "#ffc27a"),
        g(path(ring, stroke=INK, stroke_width=6.4), path(ring, stroke="#ffd98a", stroke_width=3.6),
          transform="rotate(-14)"),
    )


def moon():
    return translate(
        150, 104,
        circle(0, 0, 9, "#b388ff", **outlined(1.5)),
        circle(-3, -2, 2.4, "#9a6cf0"), circle(3, 3, 1.6, "#9a6cf0"),
    )


def rocket(index):
    period = W + 70
    x = wrap(20 + index * period / FRAMES, period) - 35
    y = 50 - (x - 120) * 0.12
    flame_big = index % 2 == 0
    flame = (
        path("M-5,11 Q-6,22 0,30 Q6,22 5,11 Z", fill="#ff7b29", **outlined(1.2)) if flame_big
        else path("M-5,11 Q-5,18 0,23 Q5,18 5,11 Z", fill="#ff7b29", **outlined(1.2)))
    inner = (path("M-2.5,11 Q-3,18 0,23 Q3,18 2.5,11 Z", fill="#ffe14d") if flame_big
             else path("M-2.5,11 Q-2.5,15 0,18 Q2.5,15 2.5,11 Z", fill="#ffe14d"))
    return translate(
        x, y,
        flame, inner,
        poly([(-7, 2), (-14, 13), (-7, 11)], "#e63946", **outlined(1.3)),
        poly([(7, 2), (14, 13), (7, 11)], "#e63946", **outlined(1.3)),
        path("M0,-22 C8,-14 9,0 7,12 L-7,12 C-9,0 -8,-14 0,-22 Z", fill=WHITE, **outlined(1.6)),
        path("M0,-22 C4,-18 6,-14 6.5,-11 L-6.5,-11 C-6,-14 -4,-18 0,-22 Z", fill="#e63946",
             **outlined(1.3)),
        circle(0, -2, 4, "#4da6ff", **outlined(1.4)),
        circle(-1.3, -3.3, 1.2, WHITE),
        rotate=78,
    )


def astronaut(index):
    bob = (0, -2, -3, -2, 0, 1)[index]
    wave_up = index % 2 == 0
    hand = (-17, -4) if wave_up else (-19, 6)
    return translate(
        188, 84 + bob,
        rect(4, -2, 9, 16, "#c7cfdc", rx=2, **outlined(1.3)),
        path(f"M-6,4 L{hand[0]},{hand[1]}", stroke=INK, stroke_width=7.4, stroke_linecap="round"),
        path(f"M-6,4 L{hand[0]},{hand[1]}", stroke=WHITE, stroke_width=5, stroke_linecap="round"),
        circle(hand[0], hand[1], 3, "#ff9f43", **outlined(1.2)),
        path("M-3,18 L-6,28 M4,18 L7,28", stroke=INK, stroke_width=7.4, stroke_linecap="round"),
        path("M-3,18 L-6,28 M4,18 L7,28", stroke=WHITE, stroke_width=5, stroke_linecap="round"),
        rect(-8, 0, 16, 20, WHITE, rx=5, **outlined(1.6)),
        rect(-4, 6, 8, 5, "#4da6ff", rx=1, **outlined(1)),
        path("M6,4 L12,14", stroke=INK, stroke_width=7.4, stroke_linecap="round"),
        path("M6,4 L12,14", stroke=WHITE, stroke_width=5, stroke_linecap="round"),
        circle(0, -8, 11, WHITE, **outlined(1.7)),
        ellipse(0, -8, 8, 6.5, "#243b7a"),
        path("M-5,-11 Q-3,-13 0,-13", stroke=WHITE, stroke_width=1.6, stroke_linecap="round",
             opacity="0.8"),
        smile(0, -6, 3, fill="#ff8a9a") if wave_up else smile(0, -6, 3),
        rotate=-8,
    )


def space_frame(index):
    return frame(
        sky(index),
        moon(),
        ringed_planet(),
        rocket(index),
        astronaut(index),
        bug("planet", "#6a3fd1"),
        defs=[linear("space", (0, "#0b1033"), (1, "#2d1a63"))],
    )


def frames():
    return [(space_frame(i), FRAME_MS) for i in range(FRAMES)]
