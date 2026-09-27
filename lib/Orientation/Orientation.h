#pragma once

#include <stdint.h>

// Uses the accelerometer to decide whether the TV is flipped by 180°.
//
// The TV stands on a long edge, so gravity points across the board, along
// its short X axis. The sign of X tells which of the two long edges it is
// standing on. Upright (gravity along Y) or lying flat (along Z), there is
// no telling which way is up, so the orientation stays as it was.
//
// Like everything in lib/, it never touches hardware: time and acceleration
// go in, a decision comes out.
class Orientation {
  public:
    static constexpr float kMinG = 0.6f;       // min gravity along X, g
    static constexpr float kShakeG = 0.25f;    // allowed |a| deviation from 1 g
    static constexpr uint32_t kSettleMs = 400; // how long a new side must hold

    // ax, ay, az: acceleration in g in the board's axes (M5.Imu.getAccel).
    // Returns flipped().
    bool update(uint32_t nowMs, float ax, float ay, float az);

    bool flipped() const { return flipped_; }

    // The next clear reading takes effect at once, with no waiting, as it
    // does for a new Orientation. Needed after the screen sleeps: the TV may
    // have been turned over while it was off.
    void reset();

  private:
    enum class Side : uint8_t { Unknown, Normal, Flipped };

    static Side sideOf(float ax, float ay, float az);

    bool flipped_ = false;
    bool decided_ = false;
    Side pending_ = Side::Unknown;
    uint32_t pendingSinceMs_ = 0;
};
