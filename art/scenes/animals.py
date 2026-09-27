"""Animals: savanna, a giraffe chews leaves, a baby elephant flaps its ears, a bird flies by."""

from svg import (
    INK, W, WHITE, bug, circle, cheek, ellipse, eye, frame, g, line, linear,
    outlined, path, poly, rect, translate, wrap)

SLUG = "animals"
TITLE = "Animals"

FRAMES = 6
FRAME_MS = 600

GIRAFFE_HEAD = ["up", "up", "mid", "mid", "mid", "up"]
GIRAFFE_CHEW = [False, False, True, False, True, False]
ELEPHANT_EAR = [0, 16, 0, 16, 0, 16]
ELEPHANT_TRUMPET = [False, False, False, True, True, False]

GIRAFFE = "#f6b93b"
GIRAFFE_SPOT = "#c9772a"
ELEPHANT = "#9ba6b8"


def savanna():
    return g(
        rect(0, 0, W, 135, "url(#sky)"),
        circle(40, 26, 18, "#fff3b0", opacity="0.5"),
        circle(40, 26, 12, "#ffd23f", **outlined(1.4)),
        ellipse(40, 90, 70, 12, "#c7cf72"),
        ellipse(150, 92, 90, 10, "#bcc86a"),
        path("M0,88 Q60,82 120,88 T240,86 L240,135 L0,135 Z", fill="#e9c35c"),
        path("M0,112 Q70,106 140,112 T240,110 L240,135 L0,135 Z", fill="#dcb24c"),
        *[path(f"M{x},{y} l-2,-7 M{x},{y} l1,-8 M{x},{y} l4,-6", stroke="#9a7d2a",
               stroke_width=1.4, stroke_linecap="round")
          for x, y in ((14, 128), (100, 131), (118, 126), (226, 130), (30, 110))],
    )


def acacia():
    return g(
        poly([(207, 122), (216, 122), (213, 70), (226, 38), (221, 36), (210, 60),
              (200, 36), (194, 38), (206, 68)], "#8a5a3c", **outlined(1.4)),
        ellipse(196, 30, 26, 9, "#4f9a35", **outlined(1.6)),
        ellipse(222, 27, 24, 10, "#4f9a35", **outlined(1.6)),
        ellipse(236, 34, 14, 8, "#4f9a35", **outlined(1.6)),
        ellipse(198, 27, 16, 4, "#6fbf4a"),
        ellipse(222, 23, 14, 4, "#6fbf4a"),
    )


def giraffe(index):
    hx, hy = (181, 42) if GIRAFFE_HEAD[index] == "up" else (176, 51)
    chew = GIRAFFE_CHEW[index]
    legs = [
        g(rect(x, 88, 5, 32, GIRAFFE, rx=2, **outlined(1.3)),
          rect(x, 117, 5, 4, INK, rx=1))
        for x in (135, 142, 157, 164)
    ]
    neck_spots = [
        circle(164 + (hx - 164) * t, 78 + (hy - 78) * t + 2, 2.2, GIRAFFE_SPOT)
        for t in (0.2, 0.45, 0.7)
    ]
    head = translate(
        hx, hy,
        line(-3, -5, -4, -12, INK, 1.8), circle(-4, -12.5, 2, "#8a5a3c"),
        line(1, -6, 1.5, -13, INK, 1.8), circle(1.5, -13.5, 2, "#8a5a3c"),
        ellipse(-7, -3, 4.5, 2, GIRAFFE, **outlined(1.2), transform="rotate(-25 -7 -3)"),
        ellipse(0, 0, 8, 6, GIRAFFE, **outlined(1.5)),
        ellipse(7, 2.5, 5.5, 4.2, "#f9d98b", **outlined(1.3)),
        circle(0, -3, 1.6, GIRAFFE_SPOT),
        eye(2, -1.5, 2.3, look=(0.6, 0)),
        circle(9.5, 1.5, 0.8, INK),
        ellipse(11, 5, 2, 1.4, "#7a2231") if chew else line(8, 5.5, 12, 5, INK, 1.2),
        ellipse(13.5, 5.5, 3, 1.6, "#4f9a35", **outlined(0.8),
                transform="rotate(20 13.5 5.5)") if chew else "",
        scale=1.3,
    )
    return g(
        *legs,
        path("M131,82 Q126,90 127,99", stroke=INK, stroke_width=1.4),
        circle(127, 100, 2, INK),
        poly([(157, 82), (170, 76), (hx + 3, hy + 4), (hx - 5, hy + 3)], GIRAFFE,
             **outlined(1.5)),
        *neck_spots,
        ellipse(150, 84, 21, 11, GIRAFFE, **outlined(1.6)),
        ellipse(142, 82, 4, 3, GIRAFFE_SPOT), ellipse(154, 80, 3.5, 2.5, GIRAFFE_SPOT),
        ellipse(160, 87, 3, 2.5, GIRAFFE_SPOT), ellipse(147, 89, 3, 2, GIRAFFE_SPOT),
        head,
    )


def tube(d, color, width):
    """Thick outlined line: a trunk or a tentacle."""
    return g(
        path(d, stroke=INK, stroke_width=width + 2.6, stroke_linecap="round"),
        path(d, stroke=color, stroke_width=width, stroke_linecap="round"),
    )


def elephant(index):
    trumpet = ELEPHANT_TRUMPET[index]
    trunk = (
        "M38,93 Q30,86 30,76 Q30,70 25,69" if trumpet
        else "M38,94 Q31,100 32,110 Q33,114 29,115")
    return g(
        *[rect(x, 102, 8, 20, ELEPHANT, rx=3, **outlined(1.4)) for x in (57, 65, 79, 87)],
        path("M95,95 Q101,98 100,105", stroke=INK, stroke_width=1.4),
        ellipse(74, 98, 25, 15, ELEPHANT, **outlined(1.6)),
        tube(trunk, ELEPHANT, 6.5),
        circle(47, 89, 14, ELEPHANT, **outlined(1.6)),
        g(ellipse(59, 91, 9, 12, "#b8c2d1", **outlined(1.5)),
          ellipse(59, 92, 5, 8, "#f0b8c4", opacity="0.7"),
          transform=f"rotate({ELEPHANT_EAR[index]} 57 81)"),
        eye(43, 86, 2.8, look=(-0.5, 0)),
        cheek(46, 94, 2.4),
        g(path("M18,64 l-5,-4 M16,70 l-6,0 M19,58 l-2,-6", stroke=WHITE,
               stroke_width=1.6, stroke_linecap="round")) if trumpet else "",
    )


def bird(index):
    period = W + 24
    x = wrap(12 + index * period / FRAMES, period) - 12
    y = 46 + (4 if index % 2 else 0)
    wing_up = index % 2 == 0
    wing = (poly([(-1, -1), (-7, -9), (3, -2)], "#2f7de1", **outlined(1))
            if wing_up else poly([(-1, 0), (-6, 7), (3, 1)], "#2f7de1", **outlined(1)))
    return translate(
        x, y,
        ellipse(0, 0, 6, 4, "#46a0ff", **outlined(1.2)),
        circle(5, -2, 3.2, "#46a0ff", **outlined(1.2)),
        poly([(8, -2.5), (11.5, -1.5), (8, -0.5)], "#ffa62b"),
        circle(5.8, -2.6, 0.8, INK),
        wing,
    )


def animals_frame(index):
    return frame(
        savanna(),
        bird(index),
        acacia(),
        elephant(index),
        giraffe(index),
        bug("paw", "#b8741f"),
        defs=[linear("sky", (0, "#86cfff"), (0.62, "#fff0c2"))],
    )


def frames():
    return [(animals_frame(i), FRAME_MS) for i in range(FRAMES)]
