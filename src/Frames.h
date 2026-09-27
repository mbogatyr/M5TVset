#pragma once

#include <stdint.h>

#include "ChannelInfo.h"

// Кадры каналов: PNG во flash. Реализацию генерирует art/build.py
// в src/generated/Frames.cpp — после правки сцен перезапустить его.
struct FrameImage {
    const uint8_t *png;
    uint32_t size;
};

extern const ChannelInfo kChannels[];
extern const uint8_t kChannelCount;

const FrameImage &frameImage(uint8_t channel, uint8_t frame);
