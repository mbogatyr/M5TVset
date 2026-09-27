#pragma once

#include <stdint.h>

// Канал — несколько кадров, которые крутятся по кругу. Логике нужны только
// их длительности; сами картинки лежат в src/ и логике не видны.
struct ChannelInfo {
    const uint16_t *frameMs;
    uint8_t frameCount;
};
