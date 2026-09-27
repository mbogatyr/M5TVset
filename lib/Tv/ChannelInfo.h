#pragma once

#include <stdint.h>

// A channel is a few frames that play in a loop. The logic needs only their
// durations; the images themselves live in src/ and the logic never sees them.
struct ChannelInfo {
    const uint16_t *frameMs;
    uint8_t frameCount;
};
