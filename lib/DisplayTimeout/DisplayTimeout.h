#pragma once

#include <stdint.h>

// Decides when an idle screen should turn off.
//
// Does not handle power-off: a double click on the StickS3 side button
// powers the board off by itself, in the PMIC, with no firmware involved.
//
// Like everything in lib/, it never touches hardware: time and a
// button-press flag go in, a decision comes out.
class DisplayTimeout {
  public:
    static constexpr uint32_t kIdleMs = 180000; // 3 minutes

    explicit DisplayTimeout(uint32_t idleMs = kIdleMs);

    // Sets the point the idle time is counted from. Call once at startup.
    void begin(uint32_t nowMs);

    // activity: whether any button was pressed in this tick.
    bool shouldBeOn(uint32_t nowMs, bool activity);

  private:
    uint32_t idleMs_;
    uint32_t lastActivityMs_ = 0;
};
