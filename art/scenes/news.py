"""Новости: кот-ведущий в студии, экран за спиной, бегущая строка."""

from svg import (
    HEAVY_FONT, INK, TEXT_FONT, W, WHITE, bug, circle, cheek, ellipse, eye,
    frame, g, line, linear, outlined, path, poly, rect, smile, tag, text,
    translate)

SLUG = "news"
TITLE = "News"

FRAME_MS = 400
TICKER_STEP = 36  # 8 кадров * 36 px = 288 px — период строки, цикл без скачка
TICKER_Y = 113

# рот: True — открыт; кот «говорит»
MOUTH = [True, False, True, True, False, True, False, False]
BLINK = {5}
TILT = {2: -4, 3: -4, 6: 3}


def studio_wall():
    return g(
        rect(0, 0, W, TICKER_Y, "url(#wall)"),
        *[rect(x, 0, 14, TICKER_Y, "#ffffff", opacity="0.05") for x in (112, 150, 188, 226)],
        # подсветка за ведущим
        ellipse(166, 52, 48, 40, "#6fa8ff", opacity="0.25"),
    )


def house_picture():
    return g(
        rect(16, 16, 78, 46, "#9fdcff"),
        circle(82, 25, 6, "#ffd23f"),
        ellipse(40, 66, 50, 18, "#6cc24a"),
        ellipse(88, 68, 34, 14, "#58ad3c"),
        rect(36, 38, 22, 16, "#ffe3a3", **outlined(1.2)),
        poly([(33, 39), (47, 27), (61, 39)], "#e8483b", **outlined(1.2)),
        rect(44, 45, 6, 9, "#8a5a3c"),
    )


def balloon_picture():
    return g(
        rect(16, 16, 78, 46, "#bfe8ff"),
        ellipse(32, 52, 12, 5, WHITE),
        ellipse(78, 30, 10, 4, WHITE),
        path("M55,20 C44,20 42,33 49,40 L53,45 L57,45 L61,40 C68,33 66,20 55,20 Z",
             fill="#ff6b6b", **outlined(1.2)),
        path("M55,20 C51,24 51,36 53,45 M55,20 C59,24 59,36 57,45",
             stroke="#ffd23f", stroke_width=2),
        line(53, 45, 53.5, 49, INK, 1), line(57, 45, 56.5, 49, INK, 1),
        rect(52, 49, 6, 5, "#a86b3c", **outlined(1)),
    )


def back_screen(index):
    picture = house_picture() if index < 4 else balloon_picture()
    return g(
        rect(10, 10, 90, 60, "#0e1a3a", rx=4),
        tag("clipPath", rect(16, 16, 78, 46, WHITE), id="pic"),
        g(picture, clip_path="url(#pic)"),
        rect(16, 16, 78, 46, "none", stroke="#ffffff", stroke_width=0.8, opacity="0.4"),
    )


def anchor(index):
    open_mouth = MOUTH[index]
    blink = index in BLINK
    fur, fur_dark = "#a5adbf", "#7f889c"
    head = g(
        # уши
        poly([(149, 38), (147, 17), (163, 31)], fur, **outlined(1.6)),
        poly([(181, 38), (183, 17), (167, 31)], fur, **outlined(1.6)),
        poly([(151, 33), (150, 22), (159, 30)], "#f4a3b4"),
        poly([(179, 33), (180, 22), (171, 30)], "#f4a3b4"),
        circle(165, 48, 20, fur, **outlined(1.8)),
        # полоски на лбу
        path("M160,30 l1,6 M165,29 v7 M170,30 l-1,6", stroke=fur_dark,
             stroke_width=1.6, stroke_linecap="round"),
        ellipse(165, 57, 11, 8, "#f3f1f6"),
        eye(157, 46, 3.6, look=(0.3, 0.2), blink=blink),
        eye(173, 46, 3.6, look=(0.3, 0.2), blink=blink),
        cheek(152, 54), cheek(178, 54),
        poly([(162, 52), (168, 52), (165, 55)], "#e36b86", **outlined(0.8)),
        smile(165, 58, 4, open_=open_mouth) if open_mouth
        else path("M161,57 Q163,60 165,57 Q167,60 169,57", stroke=INK,
                  stroke_width=1.4, stroke_linecap="round"),
        # усы
        path("M150,56 l-9,-2 M150,59 l-9,1 M180,56 l9,-2 M180,59 l9,1",
             stroke=INK, stroke_width=0.9, stroke_linecap="round"),
    )
    tilt = TILT.get(index, 0)
    return g(
        # пиджак, рубашка, галстук
        path("M128,100 C130,80 142,70 165,70 C188,70 200,80 202,100 Z",
             fill="#2d3a7c", **outlined(1.8)),
        poly([(156, 70), (174, 70), (165, 86)], WHITE, **outlined(1.2)),
        poly([(162, 73), (168, 73), (169, 88), (165, 93), (161, 88)], "#e63946",
             **outlined(1.2)),
        path("M156,70 L150,84 L160,80 Z M174,70 L180,84 L170,80 Z", fill="#23306a",
             **outlined(1.2)),
        g(head, transform=f"rotate({tilt} 165 68)"),
    )


def desk():
    return g(
        path("M0,93 Q120,86 240,93 L240,113 L0,113 Z", fill="#d63447", **outlined(1.8)),
        path("M0,93 Q120,86 240,93 L240,98 Q120,91 0,98 Z", fill="#f2f4fa"),
        rect(0, 104, W, 3, "#ffffff", opacity="0.6"),
        # лапы и листки на столе
        rect(140, 88, 22, 8, WHITE, rx=1, **outlined(1.1),
             transform="rotate(-6 151 92)"),
        ellipse(141, 94, 6, 4, "#a5adbf", **outlined(1.4)),
        ellipse(189, 94, 6, 4, "#a5adbf", **outlined(1.4)),
        # глобус-эмблема на столе
        circle(52, 103, 7, "#ffd23f", **outlined(1.4)),
        ellipse(52, 103, 3, 7, "none", stroke=INK, stroke_width=1),
        line(45, 103, 59, 103, INK, 1),
    )


TICKER_ITEMS = [(0, "Kitten finds ball"), (124, "★"), (144, "Sunny day ahead"), (268, "★")]


def ticker(index):
    shift = index * TICKER_STEP
    period = len(MOUTH) * TICKER_STEP
    words = []
    for copy in range(-1, 3):
        for offset, word in TICKER_ITEMS:
            x = 76 + offset + copy * period - shift
            color = "#e63946" if word == "★" else "#1b2340"
            words.append(text(x, TICKER_Y + 15, word, 9.5, color, font=TEXT_FONT))
    return g(
        rect(0, TICKER_Y, W, 22, WHITE),
        tag("clipPath", rect(72, TICKER_Y, W - 72, 22, WHITE), id="tick"),
        g(*words, clip_path="url(#tick)"),
        rect(0, TICKER_Y, 72, 22, "#e63946"),
        poly([(72, TICKER_Y), (78, TICKER_Y + 11), (72, TICKER_Y + 22)], "#e63946"),
        text(36, TICKER_Y + 16, "NEWS", 12, WHITE, font=HEAVY_FONT, anchor="middle"),
    )


def news_frame(index):
    return frame(
        studio_wall(),
        back_screen(index),
        anchor(index),
        desk(),
        ticker(index),
        bug("globe", "#2d3a7c"),
        defs=[linear("wall", (0, "#2b58b8"), (1, "#162f6e"))],
    )


def frames():
    return [(news_frame(i), FRAME_MS) for i in range(len(MOUTH))]
