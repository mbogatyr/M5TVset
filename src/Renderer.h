#pragma once

#include <M5Unified.h>

#include "Tv.h"

// Draws the TV on the StickS3's built-in display in landscape orientation
// (240x135): channel frames, static, the channel number and the CRT effect.
//
// Each frame is built in full in a sprite and pushed out in a single call:
// drawing straight to the screen causes visible flicker.
class Renderer {
  public:
    // Call after M5.begin().
    void begin();

    // Redraws the screen only when the picture has changed. Static changes
    // every tick, so static frames are always drawn.
    void draw(const Screen &screen);

    // Forgets the last frame drawn. Needed after the display wakes up: its
    // contents are lost, and otherwise the comparison with the previous
    // frame would decide there is nothing to redraw.
    void invalidate();

    // Flips the picture by 180° when the TV is stood on its other long
    // edge. The 240x135 sprites fit both orientations.
    void setFlipped(bool flipped);

  private:
    void loadPicture(uint8_t channel, uint8_t frame);
    void paintStatic();
    void paintCollapse(uint8_t collapse);
    void paintNumber(uint8_t channel);

    M5Canvas canvas_{&M5.Display};
    M5Canvas picture_; // the current channel frame, decoded

    bool flipped_ = false;

    bool hasPrevious_ = false;
    Screen previous_{};

    bool hasPicture_ = false;
    uint8_t pictureChannel_ = 0;
    uint8_t pictureFrame_ = 0;

    uint32_t noise_ = 0x9e3779b9u; // xorshift state for the static
};
