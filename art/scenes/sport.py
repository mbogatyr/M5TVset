"""Sports: a player shoots at the goal, the goalie dives and misses, GOAL!, the crowd cheers."""

from svg import (
    HEAVY_FONT, INK, W, WHITE, bug, circle, ellipse, eye, frame, g, line, outlined,
    path, poly, rect, smile, text, translate)

SLUG = "sport"
TITLE = "Sports"

GROUND = 112
SKIN = "#f2c29b"

# (player x, lift, pose), (ball x, y), goalie pose, score, GOAL!
STATES = [
    ((40, 0, "run"), (64, GROUND - 5), "ready", "0:0", False),
    ((54, 0, "kick"), (74, GROUND - 8), "ready", "0:0", False),
    ((58, 0, "stand"), (128, 82), "ready", "0:0", False),
    ((58, 0, "stand"), (180, 68), "dive", "0:0", False),
    ((62, 6, "cheer"), (221, 72), "down", "1:0", True),
    ((62, 12, "cheer"), (223, 100), "down", "1:0", True),
]
DURATIONS = [450, 300, 300, 350, 1300, 1000]

CROWD = ["#ff6b6b", "#ffd23f", "#4da6ff", "#6cc24a", "#ff9f43", "#b388ff", "#ffffff"]


def stands(cheering):
    heads = []
    for row, y in enumerate((13, 27)):
        for i, x in enumerate(range(6 + row * 6, W, 12)):
            color = CROWD[(i + row * 3) % len(CROWD)]
            lift = 2 if cheering and (i + row) % 2 == 0 else 0
            if cheering:
                heads.append(path(f"M{x - 4},{y - lift + 2} l-2,-8 M{x + 4},{y - lift + 2} l2,-8",
                                  stroke=SKIN, stroke_width=1.8, stroke_linecap="round"))
            heads.append(circle(x, y - lift, 4, SKIN))
            heads.append(rect(x - 5, y - lift + 3, 10, 6, color, rx=2))
    return g(rect(0, 0, W, 36, "#3b4466"), *heads)


def pitch():
    stripes = [rect(x, 36, 20, 99, "#4caf50" if (x // 20) % 2 else "#43a047")
               for x in range(0, W, 20)]
    ads = [rect(x, 34, 40, 6, color) for x, color in
           zip(range(0, W, 40), ("#ffffff", "#ff6b6b", "#ffffff", "#4da6ff", "#ffffff", "#ffd23f"))]
    return g(
        *stripes, *ads,
        line(96, 40, 96, 135, WHITE, 1.5, opacity="0.8"),
        circle(96, 96, 18, "none", stroke=WHITE, stroke_width=1.5, opacity="0.8"),
        path("M240,62 H182 V124 H240", stroke=WHITE, stroke_width=1.5, opacity="0.8"),
    )


def goal_back():
    net = [line(x, 60, x, GROUND, "#d7dde8", 0.8) for x in range(208, 238, 5)]
    net += [line(206, y, 238, y, "#d7dde8", 0.8) for y in range(62, GROUND, 5)]
    return g(rect(206, 58, 34, GROUND - 58, "#2e7d32", opacity="0.35"), *net)


def goal_front():
    return g(
        rect(203, 56, 5, GROUND - 56, WHITE, **outlined(1.2)),
        rect(203, 56, 37, 5, WHITE, **outlined(1.2)),
    )


def limb(x1, y1, x2, y2, color, width=3.4):
    return g(line(x1, y1, x2, y2, INK, width + 2.2), line(x1, y1, x2, y2, color, width))


def kid(pose, shirt, gloves=None, happy=False):
    """Soccer player in local coordinates: (0, 0) is the point between the feet."""
    hand = gloves or SKIN
    legs = {
        "run": [(-3, -8, -9, 0), (3, -8, 8, -2)],
        "kick": [(-3, -8, -4, 0), (3, -8, 14, -8)],
        "stand": [(-3, -8, -4, 0), (3, -8, 4, 0)],
        "cheer": [(-3, -8, -7, 0), (3, -8, 7, 0)],
        "ready": [(-3, -8, -7, 0), (3, -8, 7, 0)],
    }[pose]
    arms = {
        "run": [(-6, -20, -11, -12), (6, -20, 11, -26)],
        "kick": [(-6, -20, -13, -24), (6, -20, 12, -17)],
        "stand": [(-6, -20, -8, -11), (6, -20, 8, -11)],
        "cheer": [(-6, -20, -11, -33), (6, -20, 11, -33)],
        "ready": [(-6, -20, -14, -18), (6, -20, 14, -18)],
    }[pose]
    parts = [limb(*l, SKIN) for l in legs]
    parts += [ellipse(l[2], l[3], 3.2, 2, INK) for l in legs]
    parts.append(rect(-6, -12, 12, 5, WHITE, rx=1, **outlined(1.1)))
    parts.append(rect(-7, -24, 14, 13, shirt, rx=3, **outlined(1.4)))
    parts += [limb(*a, shirt, 3) for a in arms]
    parts += [circle(a[2], a[3], 2.3, hand, **outlined(1)) for a in arms]
    parts += [
        circle(0, -31, 7.5, SKIN, **outlined(1.4)),
        path("M-7.5,-32 Q-7,-40 0,-39.5 Q7,-40 7.5,-32 Q3,-35 -7.5,-32 Z", fill="#6b3e23"),
        eye(-2.5, -31, 1.8, look=(0.6, 0)), eye(3, -31, 1.8, look=(0.6, 0)),
        smile(0.5, -27, 2.4, open_=happy),
    ]
    return g(*parts)


def goalie(pose):
    figure = kid("ready", "#2f6fdc", gloves="#ffd23f")
    if pose == "ready":
        return translate(222, GROUND, figure)
    if pose == "dive":
        return translate(214, GROUND - 4, figure, rotate=-70)
    return translate(214, GROUND - 3, figure, rotate=-90)


def ball(x, y):
    return translate(
        x, y,
        circle(0, 0, 5, WHITE, **outlined(1.3)),
        poly([(0, -2), (1.9, -0.6), (1.2, 1.6), (-1.2, 1.6), (-1.9, -0.6)], INK),
    )


def scoreboard(score):
    return g(
        rect(98, 2, 44, 15, "#15192b", rx=3, stroke=WHITE, stroke_width=1),
        text(120, 14, score, 11, "#ffd23f", font=HEAVY_FONT, anchor="middle"),
    )


def goal_title(big):
    size = 32 if big else 28
    return g(
        text(132, 80, "GOAL!", size, "#ffd23f", font=HEAVY_FONT, anchor="middle",
             stroke=INK, stroke_width=5, stroke_linejoin="round", paint_order="stroke"),
        transform=f"rotate({-6 if big else -3} 132 70)",
    )


def sport_frame(index):
    (px, lift, pose), (bx, by), goalie_pose, score, goal = STATES[index]
    return frame(
        stands(cheering=goal),
        pitch(),
        scoreboard(score),
        goal_back(),
        ball(bx, by) if bx > 205 else "",
        goalie(goalie_pose),
        goal_front(),
        ellipse(px, GROUND + 1, 10, 2.5, "#1b5e20", opacity="0.4"),
        translate(px, GROUND - lift, kid(pose, "#e63946", happy=goal)),
        ball(bx, by) if bx <= 205 else "",
        goal_title(big=index == 5) if goal else "",
        bug("ball", "#2e7d32"),
    )


def frames():
    return [(sport_frame(i), ms) for i, ms in enumerate(DURATIONS)]
