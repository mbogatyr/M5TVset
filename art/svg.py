"""Помощники для рисования кадров в SVG.

Холст 240x135 — экран StickS3 в альбомной ориентации. Экран физически
около 25x14 мм, поэтому рисуем крупно: жирные фигуры, обводка не тоньше
1.5 px, мелких деталей минимум.
"""

W, H = 240, 135

INK = "#2b2238"  # обводка персонажей
WHITE = "#ffffff"

HEAVY_FONT = "Arial Black, Arial, sans-serif"  # крупные надписи
TEXT_FONT = "Verdana, Arial, sans-serif"  # мелкий текст


def _attrs(kw):
    parts = []
    for key, value in kw.items():
        if value is None:
            continue
        parts.append(f'{key.rstrip("_").replace("_", "-")}="{value}"')
    return " ".join(parts)


def tag(name, children="", **kw):
    attrs = _attrs(kw)
    if children:
        return f"<{name} {attrs}>{children}</{name}>"
    return f"<{name} {attrs}/>"


def g(*children, **kw):
    return tag("g", "".join(children), **kw)


def rect(x, y, w, h, fill, rx=None, **kw):
    return tag("rect", x=x, y=y, width=w, height=h, rx=rx, fill=fill, **kw)


def circle(cx, cy, r, fill, **kw):
    return tag("circle", cx=cx, cy=cy, r=r, fill=fill, **kw)


def ellipse(cx, cy, rx, ry, fill, **kw):
    return tag("ellipse", cx=cx, cy=cy, rx=rx, ry=ry, fill=fill, **kw)


def path(d, fill="none", **kw):
    return tag("path", d=d, fill=fill, **kw)


def poly(points, fill, **kw):
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return tag("polygon", points=pts, fill=fill, **kw)


def line(x1, y1, x2, y2, stroke=INK, width=2, **kw):
    return tag(
        "line", x1=x1, y1=y1, x2=x2, y2=y2, stroke=stroke,
        stroke_width=width, stroke_linecap="round", **kw)


def text(x, y, s, size, fill, font=HEAVY_FONT, anchor="start", weight="bold", **kw):
    return tag(
        "text", s, x=x, y=y, font_family=font, font_size=size,
        font_weight=weight, fill=fill, text_anchor=anchor, **kw)


def outlined(width=2):
    """Атрибуты мультяшной обводки для фигур персонажей."""
    return {"stroke": INK, "stroke_width": width, "stroke_linejoin": "round"}


def linear(id_, *stops, vertical=True):
    """Линейный градиент; stops — пары (смещение 0..1, цвет)."""
    x2, y2 = ("0", "1") if vertical else ("1", "0")
    inner = "".join(
        tag("stop", offset=offset, stop_color=color) for offset, color in stops)
    return tag("linearGradient", inner, id=id_, x1="0", y1="0", x2=x2, y2=y2)


def frame(*children, defs=()):
    body = "".join(children)
    defs_block = f"<defs>{''.join(defs)}</defs>" if defs else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">{defs_block}{body}</svg>')


def translate(x, y, *children, rotate=0, scale=None):
    transform = f"translate({x:.2f},{y:.2f})"
    if rotate:
        transform += f" rotate({rotate:.2f})"
    if scale is not None:
        sx, sy = scale if isinstance(scale, tuple) else (scale, scale)
        transform += f" scale({sx:.3f},{sy:.3f})"
    return g(*children, transform=transform)


# --- детали персонажей -----------------------------------------------------


def eye(cx, cy, r=3.2, look=(0, 0), blink=False):
    """Мультяшный глаз: белок, зрачок и блик. blink — закрытый глаз-дуга."""
    if blink:
        return path(
            f"M{cx - r},{cy} Q{cx},{cy + r * 0.9} {cx + r},{cy}",
            stroke=INK, stroke_width=1.6, stroke_linecap="round")
    px, py = cx + look[0] * r * 0.35, cy + look[1] * r * 0.35
    return g(
        ellipse(cx, cy, r, r * 1.1, WHITE, stroke=INK, stroke_width=1.3),
        circle(px, py, r * 0.55, INK),
        circle(px + r * 0.2, py - r * 0.25, r * 0.2, WHITE),
    )


def smile(cx, cy, w, open_=False, fill="#c2334d"):
    """Улыбка. open_ — открытый рот (говорит или радуется)."""
    if open_:
        return path(
            f"M{cx - w},{cy} Q{cx},{cy + w * 1.4} {cx + w},{cy} Z",
            fill=fill, stroke=INK, stroke_width=1.3, stroke_linejoin="round")
    return path(
        f"M{cx - w},{cy} Q{cx},{cy + w * 0.8} {cx + w},{cy}",
        stroke=INK, stroke_width=1.5, stroke_linecap="round")


def cheek(cx, cy, r=2.4):
    return ellipse(cx, cy, r, r * 0.7, "#ff8a9a", opacity="0.7")


def wrap(value, period):
    """Координата, которая проходит период и возвращается без скачка."""
    return value % period


# --- логотип канала в правом верхнем углу ----------------------------------

_BUG_ICONS = {
    "globe": lambda c: g(
        circle(8, 8, 5.5, "none", stroke=c, stroke_width=1.4),
        ellipse(8, 8, 2.4, 5.5, "none", stroke=c, stroke_width=1.2),
        line(2.5, 8, 13.5, 8, c, 1.2),
    ),
    "paw": lambda c: g(
        ellipse(8, 10.2, 3.4, 2.8, c),
        circle(4, 6.4, 1.5, c), circle(6.8, 4.2, 1.5, c),
        circle(9.6, 4.2, 1.5, c), circle(12.2, 6.4, 1.5, c),
    ),
    "star": lambda c: poly(
        [(8, 2), (9.8, 6.1), (14.2, 6.3), (10.8, 9.2), (11.9, 13.6),
         (8, 11.2), (4.1, 13.6), (5.2, 9.2), (1.8, 6.3), (6.2, 6.1)], c),
    "sun": lambda c: g(
        circle(6.5, 6.5, 3.4, c),
        path("M6,13 h7 a2.6,2.6 0 0 0 -1,-5 a3.4,3.4 0 0 0 -6.3,1.2 a2,2 0 0 0 0.3,3.8 z",
             fill=c, stroke=WHITE, stroke_width=0.9),
    ),
    "ball": lambda c: g(
        circle(8, 8, 5.6, "none", stroke=c, stroke_width=1.4),
        poly([(8, 5.4), (10.4, 7.2), (9.5, 10), (6.5, 10), (5.6, 7.2)], c),
    ),
    "planet": lambda c: g(
        circle(8, 8, 3.8, c),
        ellipse(8, 8, 6.8, 2, "none", stroke=c, stroke_width=1.2,
                transform="rotate(-20 8 8)"),
    ),
    "fish": lambda c: g(
        ellipse(7, 8, 4.8, 3.3, c),
        poly([(10.5, 8), (14.5, 4.5), (14.5, 11.5)], c),
        circle(5, 7.3, 0.9, WHITE),
    ),
}


def bug(icon, color):
    """Полупрозрачный значок канала, как у настоящего телеканала."""
    return translate(
        W - 22, 5,
        rect(0, 0, 17, 16, WHITE, rx=4, opacity="0.82"),
        translate(0.5, 0, _BUG_ICONS[icon](color)),
    )
