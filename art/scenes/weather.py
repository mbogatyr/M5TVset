"""Погода: тучка с дождиком уходит, выходит солнце, появляется радуга."""

from svg import (
    HEAVY_FONT, INK, W, WHITE, bug, circle, cheek, ellipse, eye, frame, g, line,
    outlined, path, poly, rect, smile, tag, text, translate)

SLUG = "weather"
TITLE = "Weather"

# небо, x тучи, дождь (0 — нет, 1/2 — фаза капель), радуга (0..1), температура
STATES = [
    ("#9fb3c8", 60, 0, 0.0, "15°C"),
    ("#98adc4", 60, 1, 0.0, "15°C"),
    ("#98adc4", 60, 2, 0.0, "15°C"),
    ("#8cc6ee", 104, 0, 0.0, "18°C"),
    ("#7fcbff", 158, 0, 0.55, "20°C"),
    ("#7fcbff", 170, 0, 1.0, "20°C"),
]
DURATIONS = [700, 450, 450, 600, 700, 1300]

RAINBOW = ["#ff4d4d", "#ffa62b", "#ffe14d", "#5ccf5c", "#4da6ff", "#8e6cff"]


def sun(happy):
    rays = [rect(-2, -24, 4, 7, "#ffb627", rx=2, transform=f"rotate({a})")
            for a in range(0, 360, 45)]
    return translate(
        62, 38,
        *rays,
        circle(0, 0, 14, "#ffd23f", **outlined(1.6)),
        eye(-5, -2, 2.4), eye(5, -2, 2.4),
        cheek(-8, 4), cheek(8, 4),
        smile(0, 4, 4.5, open_=happy),
    )


def cloud(x, rainy):
    color = "#8d99ab" if rainy else WHITE
    shade = "#76839a" if rainy else "#dfe9f5"
    face = (
        g(eye(-6, 0, 2.2, look=(0, 0.6)), eye(6, 0, 2.2, look=(0, 0.6)),
          path("M-3,7 Q0,4.5 3,7", stroke=INK, stroke_width=1.3, stroke_linecap="round"))
        if rainy else
        g(eye(-6, 0, 2.2), eye(6, 0, 2.2), smile(0, 5, 3))
    )
    return translate(
        x, 38,
        path("M-26,12 Q-32,12 -32,5 Q-32,-3 -23,-3 Q-22,-15 -9,-14 Q-3,-24 9,-19 "
             "Q20,-20 22,-8 Q32,-8 32,3 Q32,12 24,12 Z", fill=color, **outlined(1.6)),
        path("M-26,10 Q0,15 24,10", stroke=shade, stroke_width=3, stroke_linecap="round"),
        face,
    )


def rain(x, phase):
    drops = []
    for column, dx in enumerate((-20, -10, 0, 10, 20)):
        for row in range(3):
            y = 58 + row * 18 + (9 if (column + phase) % 2 else 0)
            drops.append(path(
                f"M{x + dx},{y} q-2.5,4 0,5.5 q2.5,-1.5 0,-5.5 z",
                fill="#3d8bff", stroke="#1f5fbf", stroke_width=0.8))
    return g(*drops)


def rainbow(alpha):
    if alpha <= 0:
        return ""
    arcs = [
        path(f"M{150 - r},104 A{r},{r} 0 0 1 {150 + r},104", stroke=color, stroke_width=5)
        for r, color in zip(range(76, 46, -5), RAINBOW)
    ]
    return g(*arcs, opacity=f"{alpha:.2f}")


def landscape():
    return g(
        path("M0,100 Q60,86 130,98 T240,94 L240,135 L0,135 Z", fill="#6cc24a"),
        path("M0,118 Q80,108 150,118 T240,116 L240,135 L0,135 Z", fill="#58ad3c"),
        # домик
        rect(178, 82, 32, 24, "#ffe3a3", **outlined(1.6)),
        poly([(173, 84), (194, 64), (215, 84)], "#e8483b", **outlined(1.6)),
        rect(189, 93, 9, 13, "#8a5a3c", **outlined(1.2)),
        rect(181, 87, 6, 6, "#9fdcff", **outlined(1.1)),
        rect(201, 87, 6, 6, "#9fdcff", **outlined(1.1)),
        # дерево
        rect(120, 88, 5, 16, "#8a5a3c", **outlined(1.2)),
        circle(122, 82, 11, "#3f9a3a", **outlined(1.5)),
        circle(118, 79, 4, "#58b84a"),
    )


def temperature(value):
    return g(
        rect(6, 102, 60, 27, "#1f5fbf", rx=7, **outlined(1.6)),
        text(36, 122.5, value, 17, WHITE, font=HEAVY_FONT, anchor="middle"),
    )


def weather_frame(index):
    sky, cloud_x, rain_phase, rainbow_alpha, temp = STATES[index]
    rainy = cloud_x < 90
    return frame(
        rect(0, 0, W, 135, sky),
        rainbow(rainbow_alpha),
        sun(happy=not rainy),
        cloud(cloud_x, rainy),
        rain(cloud_x, rain_phase) if rain_phase else "",
        landscape(),
        temperature(temp),
        bug("sun", "#f59f00"),
    )


def frames():
    return [(weather_frame(i), ms) for i, ms in enumerate(DURATIONS)]
