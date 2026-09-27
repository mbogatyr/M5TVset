"""Каналы телевизора в порядке переключения KEY1.

Каждый модуль сцены задаёт SLUG, TITLE и frames() -> [(svg, мс), ...].
"""

from . import (animals, cartoons, history, news, playtime, science, space, sport, ufo,
               underwater, weather)

CHANNELS = [news, animals, cartoons, weather, sport, space, underwater, science, playtime, ufo,
            history]
