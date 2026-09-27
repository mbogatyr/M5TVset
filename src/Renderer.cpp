#include "Renderer.h"

#include "Frames.h"

namespace {

// Landscape orientations: kRotation puts KEY1 to the right of the screen, like
// the buttons on a TV (checked on the board); kFlippedRotation, on the left.
constexpr uint8_t kRotation = 1;
constexpr uint8_t kFlippedRotation = 3;

constexpr int kWidth = 240;
constexpr int kHeight = 135;

// Share of the CRT effect spent squeezing the picture into a line; the rest
// goes to shrinking the line into a dot.
constexpr float kSqueezeShare = 0.6f;

using Mode = Screen::Mode;

bool sameScreen(const Screen &a, const Screen &b) {
    return a.mode == b.mode && a.channel == b.channel && a.frame == b.frame &&
           a.showNumber == b.showNumber && a.progress == b.progress;
}

} // namespace

void Renderer::begin() {
    M5.Display.setRotation(kRotation);
    M5.Display.fillScreen(TFT_BLACK);

    // 65 KB per sprite; the StickS3 has 8 MB of PSRAM.
    canvas_.setColorDepth(16);
    canvas_.setPsram(true);
    canvas_.createSprite(kWidth, kHeight);

    picture_.setColorDepth(16);
    picture_.setPsram(true);
    picture_.createSprite(kWidth, kHeight);
}

void Renderer::invalidate() { hasPrevious_ = false; }

void Renderer::setFlipped(bool flipped) {
    if (flipped == flipped_) {
        return;
    }
    flipped_ = flipped;
    M5.Display.setRotation(flipped ? kFlippedRotation : kRotation);
    invalidate();
}

void Renderer::draw(const Screen &screen) {
    const bool unchanged = hasPrevious_ && screen.mode != Mode::Static &&
                           sameScreen(screen, previous_);
    if (unchanged) {
        return;
    }

    switch (screen.mode) {
    case Mode::Off:
        canvas_.fillSprite(TFT_BLACK);
        break;
    case Mode::PowerOn:
        loadPicture(screen.channel, screen.frame);
        paintCollapse(255 - screen.progress);
        break;
    case Mode::PowerOff:
        loadPicture(screen.channel, screen.frame);
        paintCollapse(screen.progress);
        break;
    case Mode::Static:
        paintStatic();
        break;
    case Mode::Picture:
        loadPicture(screen.channel, screen.frame);
        picture_.pushSprite(&canvas_, 0, 0);
        break;
    }
    if (screen.showNumber) {
        paintNumber(screen.channel);
    }
    canvas_.pushSprite(0, 0);

    hasPrevious_ = true;
    previous_ = screen;
}

void Renderer::loadPicture(uint8_t channel, uint8_t frame) {
    // The PNG is decoded only when the frame changes, not on every tick.
    if (hasPicture_ && pictureChannel_ == channel && pictureFrame_ == frame) {
        return;
    }
    const FrameImage &image = frameImage(channel, frame);
    picture_.drawPng(image.png, image.size, 0, 0);

    hasPicture_ = true;
    pictureChannel_ = channel;
    pictureFrame_ = frame;
}

void Renderer::paintStatic() {
    // Grey "snow" in 2x2 blocks, written straight into the sprite buffer:
    // drawPixel is noticeably slower. The sprite stores RGB565 with its
    // bytes swapped, so the grey is packed and byte-swapped by hand.
    auto *pixels = static_cast<uint16_t *>(canvas_.getBuffer());
    for (int y = 0; y < kHeight; y += 2) {
        for (int x = 0; x < kWidth; x += 2) {
            noise_ ^= noise_ << 13;
            noise_ ^= noise_ >> 17;
            noise_ ^= noise_ << 5;
            const uint8_t v = noise_ & 0xFF;
            const uint16_t rgb = ((v >> 3) << 11) | ((v >> 2) << 5) | (v >> 3);
            const uint16_t swapped = (rgb >> 8) | (rgb << 8);

            uint16_t *row = pixels + y * kWidth + x;
            row[0] = row[1] = swapped;
            if (y + 1 < kHeight) {
                row[kWidth] = row[kWidth + 1] = swapped;
            }
        }
    }
}

void Renderer::paintCollapse(uint8_t collapse) {
    // collapse: 0 is the full picture, 255 means the screen has gone dark.
    const float p = collapse / 255.0f;
    canvas_.fillSprite(TFT_BLACK);

    if (p < kSqueezeShare) {
        const float zoomY = 1.0f - p / kSqueezeShare;
        const float minZoom = 2.0f / kHeight;
        picture_.pushRotateZoom(&canvas_, kWidth / 2, kHeight / 2, 0.0f, 1.0f,
                                zoomY > minZoom ? zoomY : minZoom);
    } else if (collapse < 255) {
        const float left = 1.0f - (p - kSqueezeShare) / (1.0f - kSqueezeShare);
        const int w = left * kWidth > 3 ? static_cast<int>(left * kWidth) : 3;
        canvas_.fillRect((kWidth - w) / 2, kHeight / 2 - 1, w, 3, TFT_WHITE);
    }
}

void Renderer::paintNumber(uint8_t channel) {
    const String label(channel + 1);
    canvas_.setFont(&fonts::Font4);
    canvas_.setTextDatum(top_left);

    canvas_.setTextColor(TFT_BLACK);
    canvas_.drawString(label, 10, 8);
    canvas_.setTextColor(canvas_.color565(0x39, 0xff, 0x5a));
    canvas_.drawString(label, 8, 6);
}
