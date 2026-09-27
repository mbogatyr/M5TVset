"""Cartoons: a ginger kitten jumps over a bouncing ball, the sun winks."""

from svg import (
    INK, W, WHITE, bug, circle, cheek, ellipse, eye, frame, g, linear, outlined,
    path, poly, rect, smile, translate)

SLUG = "cartoons"
TITLE = "Cartoons"

FRAME_MS = 320
GROUND = 110

GINGER = "#f7923a"
GINGER_DARK = "#d9661f"
CREAM = "#ffe7c7"

# (paw x, height above the ground, pose, facing right)
KITTEN = [
    (66, 0, "crouch", True),
    (120, 52, "leap", True),
    (174, 0, "stand", True),
    (174, 0, "crouch", False),
    (120, 52, "leap", False),
    (66, 0, "stand", False),
]
# (ball center height above the ground, squashed)
BALL = [(34, False), (10, True), (26, False), (40, False), (10, True), (26, False)]
SUN_WINK = {3}


def meadow():
    return g(
        rect(0, 0, W, 135, "url(#sky)"),
        g(ellipse(140, 24, 16, 7, WHITE), ellipse(152, 20, 11, 8, WHITE),
          ellipse(128, 22, 9, 6, WHITE), opacity="0.95"),
        g(ellipse(208, 44, 13, 5, WHITE), ellipse(216, 41, 8, 6, WHITE), opacity="0.9"),
        path("M0,98 Q60,88 120,98 T240,96 L240,135 L0,135 Z", fill="#6cc24a"),
        path("M0,116 Q70,110 140,117 T240,114 L240,135 L0,135 Z", fill="#58ad3c"),
        *[g(circle(x, y, 2.6, color), circle(x, y, 1, "#ffd23f"))
          for x, y, color in ((20, 104, "#ff6b9a"), (36, 124, "#ffffff"),
                              (214, 124, "#ff6b9a"), (228, 104, "#b388ff"),
                              (96, 128, "#ffffff"), (146, 129, "#b388ff"))],
    )


def sun(index):
    wink = index in SUN_WINK
    rays = [
        rect(-2, -26, 4, 8, "#ffb627", rx=2, transform=f"rotate({angle + index * 8})")
        for angle in range(0, 360, 45)
    ]
    return translate(
        30, 28,
        *rays,
        circle(0, 0, 15, "#ffd23f", **outlined(1.6)),
        eye(-5, -2, 2.4),
        eye(5, -2, 2.4, blink=wink),
        cheek(-8, 4, 2.2), cheek(8, 4, 2.2),
        smile(0, 5, 5, open_=wink),
    )


def ball(index):
    height, squashed = BALL[index]
    rx, ry = (13, 8) if squashed else (10, 10)
    cy = GROUND - ry if squashed else GROUND - height
    return g(
        ellipse(120, GROUND + 1, 11 - height * 0.08, 2.5, "#2f7d2a", opacity="0.35"),
        translate(
            120, cy,
            ellipse(0, 0, rx, ry, "#e63946", **outlined(1.6)),
            path(f"M{-rx},0 Q0,{-ry * 0.5} {rx},0 Q0,{ry * 0.5} {-rx},0 Z",
                 fill=WHITE, opacity="0.95"),
            ellipse(0, 0, rx * 0.35, ry, "#ffd23f", opacity="0.85"),
            ellipse(0, 0, rx, ry, "none", stroke=INK, stroke_width=1.6),
            ellipse(-rx * 0.4, -ry * 0.5, 2.5, 1.5, WHITE, opacity="0.8"),
        ),
    )


def kitten_head(happy):
    return g(
        poly([(-9, -4), (-10, -16), (-2, -10)], GINGER, **outlined(1.4)),
        poly([(9, -4), (10, -16), (2, -10)], GINGER, **outlined(1.4)),
        poly([(-8, -7), (-8.5, -13), (-4, -10)], "#ffb3c1"),
        poly([(8, -7), (8.5, -13), (4, -10)], "#ffb3c1"),
        circle(0, 0, 11, GINGER, **outlined(1.6)),
        path("M-3,-10 l0.5,4 M0,-11 v4 M3,-10 l-0.5,4", stroke=GINGER_DARK,
             stroke_width=1.4, stroke_linecap="round"),
        ellipse(1.5, 4, 6.5, 4.5, CREAM),
        eye(-3, -1, 2.8, look=(0.6, 0)),
        eye(6, -1, 2.8, look=(0.6, 0)),
        cheek(-6, 4), cheek(9, 4),
        poly([(0.5, 2.3), (3.5, 2.3), (2, 4)], "#e36b86"),
        smile(2, 5, 2.6, open_=happy),
    )


def kitten(index):
    x, lift, pose, facing_right = KITTEN[index]
    leg = lambda lx, ly, angle=0, ry=5: ellipse(
        lx, ly, 3.2, ry, GINGER, **outlined(1.3), transform=f"rotate({angle} {lx} {ly})")
    if pose == "crouch":
        parts = [
            path("M-13,-8 Q-24,-6 -24,-16", stroke=INK, stroke_width=5.4, stroke_linecap="round"),
            path("M-13,-8 Q-24,-6 -24,-16", stroke=GINGER, stroke_width=3, stroke_linecap="round"),
            leg(-8, -2, 70, 4), leg(8, -2, -70, 4),
            ellipse(0, -8, 15, 7, GINGER, **outlined(1.6)),
            ellipse(2, -6, 8, 3.5, CREAM),
            translate(13, -16, kitten_head(False)),
        ]
    elif pose == "leap":
        parts = [
            path("M-14,-12 Q-26,-14 -32,-8", stroke=INK, stroke_width=5.4, stroke_linecap="round"),
            path("M-14,-12 Q-26,-14 -32,-8", stroke=GINGER, stroke_width=3, stroke_linecap="round"),
            leg(-14, -5, 60), leg(-10, -4, 50), leg(14, -6, -60), leg(18, -8, -70),
            ellipse(0, -11, 17, 7.5, GINGER, **outlined(1.6), transform="rotate(-6 0 -11)"),
            ellipse(1, -8, 9, 3.5, CREAM),
            translate(18, -21, kitten_head(True)),
        ]
    else:
        parts = [
            path("M-12,-12 Q-22,-14 -20,-28", stroke=INK, stroke_width=5.4, stroke_linecap="round"),
            path("M-12,-12 Q-22,-14 -20,-28", stroke=GINGER, stroke_width=3, stroke_linecap="round"),
            leg(-8, -4), leg(-3, -4), leg(5, -4), leg(10, -4),
            ellipse(0, -12, 13, 8.5, GINGER, **outlined(1.6)),
            ellipse(2, -10, 7, 4, CREAM),
            translate(12, -25, kitten_head(False)),
        ]
    body = g(*parts, transform="" if facing_right else "scale(-1,1)")
    shadow = ellipse(x, GROUND + 1, 16 - lift * 0.12, 3, "#2f7d2a", opacity="0.35")
    return g(shadow, translate(x, GROUND - lift, body))


def cartoons_frame(index):
    return frame(
        meadow(),
        sun(index),
        ball(index),
        kitten(index),
        bug("star", "#e8a200"),
        defs=[linear("sky", (0, "#6ec6ff"), (1, "#c9ecff"))],
    )


def frames():
    return [(cartoons_frame(i), FRAME_MS) for i in range(len(KITTEN))]
