"""Каналы телевизора в порядке переключения KEY1.

Каждый модуль сцены задаёт SLUG, TITLE и frames() -> [(svg, мс), ...].
"""

from . import animals, cartoons, news, space, sport, underwater, weather

CHANNELS = [news, animals, cartoons, weather, sport, space, underwater]
