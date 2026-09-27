"""UFO: a flying saucer comes to a farm, gives a cow a ride in its beam and flies away."""

import random

from svg import (
    INK, W, WHITE, bug, circle, cheek, ellipse, eye, frame, g, limb, linear,
    outlined, path, poly, rect, smile, translate)

SLUG = "ufo"
TITLE = "UFO"

GROUND = 114
COW_X = 112

# saucer (x, y, tilt), beam, cow lift, cow tilt, cow face, alien waving
STATES = [
    ((34, 34, 10), False, 0, 0, "graze", False),
    ((112, 38, 0), False, 0, 0, "oh", False),
    ((112, 38, 0), True, 12, 0, "oh", True),
    ((112, 38, 0), True, 34, 22, "laugh", False),
    ((112, 38, 0), True, 0, 0, "happy", True),
    ((196, 28, -12), False, 0, 0, "happy", True),
]
DURATIONS = [500, 600, 500, 700, 600, 600]
LIGHTS = ["#ffe14d", "#ff6fae", "#5ce1ff"]

_rng = random.Random(3)
STARS = [(_rng.uniform(0, W), _rng.uniform(0, 80), _rng.uniform(0.5, 1.2)) for _ in range(30)]


def night(index):
    stars = [circle(x, y, r * (1.3 if (i + index) % 3 == 0 else 1), WHITE, opacity="0.85")
             for i, (x, y, r) in enumerate(STARS)]
    return g(
        rect(0, 0, W, 135, "url(#night)"),
        *stars,
        circle(30, 26, 11, "#fff3c4", **outlined(1.2)),
        circle(35, 23, 10, "#1b2a5c"),
        path("M0,104 Q60,94 120,102 T240,98 L240,135 L0,135 Z", fill="#2e6b40"),
        path("M0,120 Q80,112 150,120 T240,118 L240,135 L0,135 Z", fill="#27593a"),
    )


def barn():
    return g(
        rect(188, 78, 38, 30, "#d64545", **outlined(1.5)),
        poly([(184, 80), (207, 62), (230, 80)], "#9c2f2f", **outlined(1.5)),
        rect(200, 90, 14, 18, "#f5e6c8", **outlined(1.2)),
        path("M200,90 L214,108 M214,90 L200,108", stroke="#d64545", stroke_width=1.6),
        rect(203, 70, 8, 7, "#ffe98a", **outlined(1)),
        *[rect(x, 100, 3, 12, "#c9a27a", **outlined(0.9)) for x in (160, 168, 176)],
        rect(157, 103, 24, 2.5, "#c9a27a", **outlined(0.8)),
    )


def cow(lift, angle, face):
    graze = face == "graze"
    head_x, head_y = (-16, -10) if graze else (-17, -20)
    if face == "laugh":
        eyes = [path(f"M{x - 2.4},-2 Q{x},-4.6 {x + 2.4},-2", stroke=INK, stroke_width=1.4,
                     stroke_linecap="round") for x in (-3.5, 3.5)]
    else:
        eyes = [eye(-3.5, -2, 2.3), eye(3.5, -2, 2.3)]
    mouth = (ellipse(0, 6.5, 1.8, 2.2, "#7a2231") if face == "oh"
             else smile(0, 6, 2.4, open_=face in ("laugh", "happy")))
    head = translate(
        head_x, head_y,
        poly([(-7, -6), (-11, -10), (-6, -9)], "#f5e6c8", **outlined(1)),
        poly([(7, -6), (11, -10), (6, -9)], "#f5e6c8", **outlined(1)),
        ellipse(-9, -3, 3.5, 2, "#ffffff", **outlined(1.1)),
        ellipse(9, -3, 3.5, 2, "#ffffff", **outlined(1.1)),
        ellipse(0, 0, 8, 8.5, WHITE, **outlined(1.5)),
        ellipse(2.5, -4, 3, 2.5, INK),
        ellipse(0, 5.5, 6.5, 4.2, "#ffb3c7", **outlined(1.2)),
        circle(-2, 5, 0.9, INK), circle(2, 5, 0.9, INK),
        *([] if graze else eyes),
        "" if graze else mouth,
    )
    body = g(
        *[limb(x, -6, x, 4, WHITE, 3.6) for x in (-8, -3, 5, 10)],
        path("M14,-14 Q20,-12 19,-4", stroke=INK, stroke_width=1.4),
        ellipse(1, -12, 16, 10, WHITE, **outlined(1.6)),
        ellipse(6, -15, 5, 4, INK), ellipse(-5, -8, 4, 3, INK),
        ellipse(2, -4, 4, 2.5, "#ffb3c7", **outlined(1)),
        head,
    )
    return translate(COW_X, GROUND - 4 - lift, body, rotate=angle)


def beam(x, y):
    return g(
        poly([(x - 10, y + 6), (x + 10, y + 6), (x + 30, GROUND + 4), (x - 30, GROUND + 4)],
             "#fff6a8", opacity="0.45"),
        ellipse(x, GROUND + 3, 30, 4, "#fff6a8", opacity="0.6"),
    )


def saucer(x, y, angle, index, waving):
    arm = (limb(4, -9, 9, -17, "#7bd66f", 2.4) if waving else limb(4, -8, 9, -5, "#7bd66f", 2.4))
    lights = [circle(lx, 3.5, 2.2, LIGHTS[(i + index) % 3], **outlined(0.8))
              for i, lx in enumerate((-18, -9, 0, 9, 18))]
    return translate(
        x, y,
        path("M-13,-2 A13,12 0 0 1 13,-2 Z", fill="#bdf2ff", opacity="0.55"),
        # alien under the dome
        arm,
        line_antenna(),
        ellipse(0, -8, 5.5, 6, "#7bd66f", **outlined(1.2)),
        ellipse(-2.2, -8.5, 1.6, 2.4, INK), ellipse(2.2, -8.5, 1.6, 2.4, INK),
        path("M-2,-4.5 Q0,-3 2,-4.5", stroke=INK, stroke_width=0.9, stroke_linecap="round"),
        path("M-13,-2 A13,12 0 0 1 13,-2", stroke=INK, stroke_width=1.5),
        ellipse(0, 1, 28, 7, "#c3cfdf", **outlined(1.6)),
        ellipse(0, 3.5, 20, 3.2, "#8e9bb0"),
        *lights,
        rotate=angle,
    )


def line_antenna():
    return g(path("M0,-14 V-18", stroke=INK, stroke_width=1.2), circle(0, -19, 1.6, "#ff6fae"))


def speed_lines(x, y, leaving):
    side = -1 if leaving else -1
    return g(*[path(f"M{x + side * (34 + i * 4)},{y + dy} h{side * 14}", stroke=WHITE,
                    stroke_width=1.4, stroke_linecap="round", opacity="0.7")
               for i, dy in enumerate((-4, 2, 8))])


def ufo_frame(index):
    (sx, sy, tilt), beam_on, lift, cow_angle, cow_face, waving = STATES[index]
    moving = index in (0, 5)
    return frame(
        night(index),
        barn(),
        beam(sx, sy) if beam_on else "",
        ellipse(COW_X, GROUND + 1, 16, 3, "#1e4a2c", opacity="0.6"),
        cow(lift, cow_angle, cow_face),
        speed_lines(sx, sy, index == 5) if moving else "",
        saucer(sx, sy, tilt, index, waving),
        bug("ufo", "#2e3f7a"),
        defs=[linear("night", (0, "#0d1b3d"), (1, "#34488a"))],
    )


def frames():
    return [(ufo_frame(i), ms) for i, ms in enumerate(DURATIONS)]
