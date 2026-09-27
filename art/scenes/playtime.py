"""Мультик: щенок и зайка строят домик из кубиков, а он с грохотом разваливается."""

from svg import (
    INK, W, WHITE, bug, cheek, circle, ellipse, eye, frame, g, limb, outlined,
    path, poly, rect, smile, translate)

SLUG = "playtime"
TITLE = "Playtime"

FLOOR = 110
HOUSE_X = 96  # левый край домика
BRICK_W, BRICK_H = 24, 11

PUPPY = {"fur": "#e8b77a", "belly": "#fbe3c2", "ear": "#9c6b3f"}
BUNNY = {"fur": "#f1eef7", "belly": "#ffffff", "ear": "#ffb3c7"}

# (x, поза, лицо, в руках) щенка и зайки, этап домика, наклон, развалился, кубиков в куче
FRAMES = [
    ((56, "carry", "smile", "brick"), (184, "wave", "smile", None), 0, 0, False, 3),
    ((78, "carry", "smile", "brick"), (184, "carry", "smile", "roof"), 2, 0, False, 1),
    ((78, "place", "happy", None), (172, "carry", "smile", "roof"), 4, 0, False, 0),
    ((78, "wave", "happy", None), (162, "reach", "happy", None), 5, 0, False, 0),
    ((74, "cheer", "laugh", None), (166, "cheer", "laugh", None), 5, 0, False, 0),
    ((74, "oh", "oh", None), (166, "oh", "oh", None), 5, -10, False, 0),
    ((70, "laugh", "laugh", None), (170, "laugh", "laugh", None), 5, 0, True, 0),
]
DURATIONS = [600, 600, 600, 600, 900, 500, 1100]

# (цвет, окно, дверь) — нижний ряд слева направо, потом верхний
HOUSE_BRICKS = [("#3d7be0", False, True), ("#ffcf3f", False, False),
                ("#4cbb5a", True, False), ("#ff8c42", True, False)]
ROOF = "#e84a4a"

HANDS = {
    "carry": ((-7, -47), (7, -47)),
    "place": ((12, -24), (15, -20)),
    "wave": ((-10, -14), (13, -47)),
    "cheer": ((-13, -47), (13, -47)),
    "reach": ((-13, -44), (-6, -50)),
    "oh": ((-16, -27), (16, -27)),
    "laugh": ((-5, -18), (5, -18)),
}


def room():
    dots = [circle(x, y, 1.6, "#ffd98a") for y in range(10, 96, 16)
            for x in range(8 + (y // 16) % 2 * 8, W, 16)]
    planks = [path(f"M0,{y} H{W}", stroke="#c9955f", stroke_width=1) for y in (104, 116, 128)]
    return g(
        rect(0, 0, W, 98, "#fff0c9"),
        *dots,
        # детский рисунок на стене
        rect(150, 14, 44, 34, WHITE, **outlined(1.4), transform="rotate(3 172 31)"),
        circle(164, 26, 5, "#ffd23f"),
        path("M154,44 Q164,34 172,42 T190,40", stroke="#4cbb5a", stroke_width=2.5),
        rect(177, 30, 9, 8, "#ff6b6b"), poly([(175, 30), (181.5, 24), (188, 30)], "#3d7be0"),
        rect(0, 96, W, 39, "#e3b17a"),
        rect(0, 96, W, 3, "#c9955f"),
        *planks,
        ellipse(120, 118, 104, 13, "#7fc8f8", **outlined(1.2)),
        ellipse(120, 118, 90, 9, "none", stroke=WHITE, stroke_width=1.4, opacity="0.7"),
    )


def brick(x, y, color, window=False, door=False, angle=0):
    """Кубик: (x, y) — левый верхний угол корпуса, шипы торчат над ним."""
    parts = [
        rect(4, -3, 6, 3.6, color, rx=1, **outlined(1)),
        rect(14, -3, 6, 3.6, color, rx=1, **outlined(1)),
        rect(0, 0, BRICK_W, BRICK_H, color, rx=1.5, **outlined(1.4)),
        rect(2, 1.5, 20, 2, WHITE, opacity="0.35"),
    ]
    if window:
        parts.append(rect(8, 2.5, 8, 6, "#bfe8ff", **outlined(1)))
    if door:
        parts.append(path("M8,11 V5.5 Q12,1.5 16,5.5 V11 Z", fill="#8a5a3c", **outlined(1)))
    return translate(x, y, *parts, rotate=angle)


def roof(x, y, angle=0):
    """Крыша: (x, y) — левый нижний угол."""
    return translate(
        x, y,
        poly([(0, 0), (28, -20), (56, 0)], ROOF, **outlined(1.5)),
        path("M10,-4 L28,-16", stroke=WHITE, stroke_width=2, stroke_linecap="round",
             opacity="0.5"),
        rotate=angle,
    )


def house(stage, tilt):
    parts = []
    for i, (color, window, door) in enumerate(HOUSE_BRICKS[:min(stage, 4)]):
        row, col = divmod(i, 2)
        parts.append(brick(HOUSE_X + col * BRICK_W, FLOOR - BRICK_H * (row + 1), color, window, door))
    if stage >= 5:
        parts.append(roof(HOUSE_X - 4, FLOOR - BRICK_H * 2))
    return g(*parts, transform=f"rotate({tilt} {HOUSE_X + BRICK_W} {FLOOR})")


def ruins():
    (c1, _, _), (c2, _, _), (c3, _, _), (c4, _, _) = HOUSE_BRICKS
    dust = [ellipse(x, y, rx, ry, WHITE, opacity="0.85")
            for x, y, rx, ry in ((88, 108, 9, 4), (118, 110, 12, 4.5), (150, 108, 9, 4),
                                 (102, 101, 6, 3), (136, 102, 6, 3))]
    return g(
        brick(22, 100, c1, door=True, angle=-18),
        brick(92, 100, c3, window=True, angle=12),
        brick(126, 100, c2, angle=-6),
        brick(196, 98, c4, window=True, angle=24),
        roof(96, 98, angle=14),
        *dust,
    )


def pile(count):
    spots = [(14, 99, -8), (36, 99, 6), (22, 88, 3)]
    colors = ["#4cbb5a", "#ff8c42", "#3d7be0"]
    return g(*[brick(x, y, colors[i], angle=a) for i, (x, y, a) in enumerate(spots[:count])])


def critter(kind, pose, face):
    """Щенок или зайка в локальных координатах: (0, 0) — между лапами."""
    c = PUPPY if kind == "puppy" else BUNNY
    fur = c["fur"]
    parts = []
    if kind == "bunny":
        for side in (-1, 1):
            tilt = f"rotate({side * 10} {side * 5} -50)"
            parts.append(ellipse(side * 5, -58, 3.8, 10.5, fur, **outlined(1.4), transform=tilt))
            parts.append(ellipse(side * 5, -57, 1.8, 7.5, c["ear"], transform=tilt))
        parts.append(circle(-10, -14, 3.6, WHITE, **outlined(1.2)))
    else:
        parts.append(path("M9,-16 Q17,-18 17,-27", stroke=INK, stroke_width=5.2, stroke_linecap="round"))
        parts.append(path("M9,-16 Q17,-18 17,-27", stroke=fur, stroke_width=2.8, stroke_linecap="round"))

    parts += [limb(-4, -12, -5, -1, fur, 4.5), limb(4, -12, 5, -1, fur, 4.5),
              ellipse(-5.5, 0, 4, 2.2, fur, **outlined(1.2)),
              ellipse(5.5, 0, 4, 2.2, fur, **outlined(1.2)),
              ellipse(0, -20, 10.5, 11.5, fur, **outlined(1.6)),
              ellipse(0, -18, 6.5, 7.5, c["belly"])]
    for (sx, sy), (hx, hy) in zip(((-8, -26), (8, -26)), HANDS[pose]):
        parts += [limb(sx, sy, hx, hy, fur, 4), circle(hx, hy, 2.6, fur, **outlined(1.1))]

    parts.append(circle(0, -39, 12.5, fur, **outlined(1.6)))
    if kind == "puppy":
        parts += [ellipse(-12, -37, 4.5, 8.5, c["ear"], **outlined(1.4), transform="rotate(18 -12 -37)"),
                  ellipse(12, -37, 4.5, 8.5, c["ear"], **outlined(1.4), transform="rotate(-18 12 -37)"),
                  circle(5, -45, 3, "#d9a066")]
    parts += [ellipse(0, -33.5, 6, 4.5, c["belly"]),
              ellipse(0, -36, 2.4, 1.8, INK if kind == "puppy" else "#ff8aa8")]

    if face == "laugh":
        parts += [path(f"M{x - 3},-41 Q{x},-44.5 {x + 3},-41", stroke=INK, stroke_width=1.6,
                       stroke_linecap="round") for x in (-4.5, 4.5)]
    else:
        parts += [eye(-4.5, -41, 2.7), eye(4.5, -41, 2.7)]
    if face == "oh":
        parts.append(ellipse(0, -30.5, 2.2, 2.8, "#7a2231", **outlined(1)))
    else:
        parts.append(smile(0, -32, 3.2, open_=face in ("happy", "laugh")))
    parts += [cheek(-8, -35), cheek(8, -35)]
    return g(*parts)


def carried(x, item):
    if item == "brick":
        return brick(x - BRICK_W / 2, FLOOR - 57, "#ffcf3f")
    if item == "roof":
        return roof(x - 28, FLOOR - 48)
    return ""


def playtime_frame(index):
    (px, ppose, pface, pitem), (bx, bpose, bface, bitem), stage, tilt, crashed, piled = FRAMES[index]
    return frame(
        room(),
        pile(piled),
        roof(196, FLOOR - 2) if index == 0 else "",
        ruins() if crashed else house(stage, tilt),
        ellipse(px, FLOOR + 1, 11, 2.5, "#b07a45", opacity="0.4"),
        ellipse(bx, FLOOR + 1, 11, 2.5, "#b07a45", opacity="0.4"),
        translate(px, FLOOR, critter("puppy", ppose, pface)),
        translate(bx, FLOOR, critter("bunny", bpose, bface)),
        carried(px, pitem),
        carried(bx, bitem),
        bug("brick", "#e84a4a"),
    )


def frames():
    return [(playtime_frame(i), ms) for i, ms in enumerate(DURATIONS)]
