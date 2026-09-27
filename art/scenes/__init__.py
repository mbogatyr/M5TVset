"""TV channels in the order KEY1 switches through them.

Each scene module defines SLUG, TITLE and frames() -> [(svg, ms), ...].
"""

from . import (animals, cartoons, history, news, playtime, science, space, sport, ufo,
               underwater, weather)

CHANNELS = [news, animals, cartoons, weather, sport, space, underwater, science, playtime, ufo,
            history]
