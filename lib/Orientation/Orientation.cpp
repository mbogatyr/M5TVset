#include "Orientation.h"

#include <math.h>

bool Orientation::update(uint32_t nowMs, float ax, float ay, float az) {
    const Side side = sideOf(ax, ay, az);
    if (side == Side::Unknown) {
        pending_ = Side::Unknown;
        return flipped_;
    }

    const bool wantFlipped = side == Side::Flipped;
    if (!decided_) {
        flipped_ = wantFlipped;
        decided_ = true;
        pending_ = Side::Unknown;
        return flipped_;
    }

    if (wantFlipped == flipped_) {
        pending_ = Side::Unknown;
    } else if (pending_ != side) {
        pending_ = side;
        pendingSinceMs_ = nowMs;
    } else if (nowMs - pendingSinceMs_ >= kSettleMs) {
        // Unsigned subtraction handles the millis() rollover correctly.
        flipped_ = wantFlipped;
        pending_ = Side::Unknown;
    }
    return flipped_;
}

void Orientation::reset() {
    decided_ = false;
    pending_ = Side::Unknown;
}

Orientation::Side Orientation::sideOf(float ax, float ay, float az) {
    // Being shaken or carried: the reading holds more than just gravity.
    const float g2 = ax * ax + ay * ay + az * az;
    const float lo = 1.0f - kShakeG;
    const float hi = 1.0f + kShakeG;
    if (g2 < lo * lo || g2 > hi * hi) {
        return Side::Unknown;
    }

    const float x = fabsf(ax);
    if (x < kMinG || x < fabsf(ay) || x < fabsf(az)) {
        return Side::Unknown;
    }
    // The sign is chosen so that Normal matches setRotation(1), with KEY1
    // to the right of the screen. Checked on the board.
    return ax > 0 ? Side::Normal : Side::Flipped;
}
