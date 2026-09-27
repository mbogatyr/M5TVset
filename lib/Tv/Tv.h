#pragma once

#include <stdint.h>

#include "ChannelInfo.h"
#include "DisplayTimeout.h"

// Index of the channel frame shown elapsedMs after the channel came on.
// Frames play in a loop, each with its own duration.
uint8_t frameAt(const ChannelInfo &channel, uint32_t elapsedMs);

// What should be on the screen right now. Renderer draws exactly this.
struct Screen {
    enum class Mode : uint8_t {
        Off,      // screen is off
        PowerOn,  // a dot expands into the picture
        PowerOff, // the picture collapses into a line, then into a dot
        Static,   // static between channels
        Picture,  // a channel frame
    };

    Mode mode;
    uint8_t channel;
    uint8_t frame;    // for Picture; also the one PowerOn/PowerOff animates
    bool showNumber;  // channel number in the corner
    uint8_t progress; // PowerOn/PowerOff phase: 0 is the start, 255 the end
};

// A toy TV: KEY1 cycles through the channels, KEY2 turns it off, any key
// turns it back on, and it turns itself off when left idle.
//
// Like everything in lib/, it never touches hardware: time and key presses
// go in, a Screen comes out.
class Tv {
  public:
    static constexpr uint32_t kPowerMs = 400;   // CRT effect
    static constexpr uint32_t kStaticMs = 400;  // static when switching
    static constexpr uint32_t kNumberMs = 2000; // channel number after a switch

    Tv(const ChannelInfo *channels, uint8_t channelCount,
       uint32_t idleMs = DisplayTimeout::kIdleMs);

    // Turns on with the CRT effect, on the first channel. Call once at
    // startup.
    void begin(uint32_t nowMs);

    // Call every tick. nextPressed and powerPressed are KEY1 and KEY2
    // presses in this tick (the press edge, not the key being held).
    void update(uint32_t nowMs, bool nextPressed, bool powerPressed);

    Screen screen(uint32_t nowMs) const;

  private:
    void powerOn(uint32_t nowMs);
    void powerOff(uint32_t nowMs);
    void switchChannel(uint32_t nowMs);
    void showNumber(uint32_t sinceMs, uint32_t forMs);
    void finishTransitions(uint32_t nowMs);

    const ChannelInfo *channels_;
    uint8_t channelCount_;
    DisplayTimeout idle_;

    Screen::Mode mode_ = Screen::Mode::Off;
    uint8_t channel_ = 0;
    uint8_t frozenFrame_ = 0; // the frame that collapses on power-off
    uint32_t modeSinceMs_ = 0;
    uint32_t pictureSinceMs_ = 0;

    bool numberShown_ = false;
    uint32_t numberSinceMs_ = 0;
    uint32_t numberForMs_ = 0;
};
