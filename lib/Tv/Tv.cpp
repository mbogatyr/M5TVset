#include "Tv.h"

using Mode = Screen::Mode;

uint8_t frameAt(const ChannelInfo &channel, uint32_t elapsedMs) {
    uint32_t cycleMs = 0;
    for (uint8_t i = 0; i < channel.frameCount; ++i) {
        cycleMs += channel.frameMs[i];
    }
    if (cycleMs == 0) {
        return 0;
    }

    uint32_t t = elapsedMs % cycleMs;
    for (uint8_t i = 0; i < channel.frameCount; ++i) {
        if (t < channel.frameMs[i]) {
            return i;
        }
        t -= channel.frameMs[i];
    }
    return 0;
}

Tv::Tv(const ChannelInfo *channels, uint8_t channelCount, uint32_t idleMs)
    : channels_(channels), channelCount_(channelCount), idle_(idleMs) {}

void Tv::begin(uint32_t nowMs) {
    idle_.begin(nowMs);
    channel_ = 0;
    powerOn(nowMs);
}

void Tv::update(uint32_t nowMs, bool nextPressed, bool powerPressed) {
    finishTransitions(nowMs);

    const bool pressed = nextPressed || powerPressed;
    const bool awake = idle_.shouldBeOn(nowMs, pressed);

    switch (mode_) {
    case Mode::Off:
    case Mode::PowerOff:
        // A waking press only turns the TV on; the channel stays the same.
        if (pressed) {
            powerOn(nowMs);
        }
        break;
    case Mode::PowerOn:
        if (powerPressed) {
            powerOff(nowMs);
        }
        break;
    case Mode::Static:
    case Mode::Picture:
        if (powerPressed || !awake) {
            powerOff(nowMs);
        } else if (nextPressed) {
            switchChannel(nowMs);
        }
        break;
    }
}

Screen Tv::screen(uint32_t nowMs) const {
    Screen s{mode_, channel_, 0, false, 0};
    // Unsigned subtraction handles the millis() rollover correctly.
    const bool numberVisible =
        numberShown_ && (nowMs - numberSinceMs_) < numberForMs_;

    switch (mode_) {
    case Mode::PowerOn:
    case Mode::PowerOff: {
        const uint32_t elapsed = nowMs - modeSinceMs_;
        s.progress = elapsed >= kPowerMs ? 255 : elapsed * 255 / kPowerMs;
        s.frame = mode_ == Mode::PowerOff ? frozenFrame_ : 0;
        break;
    }
    case Mode::Static:
        s.showNumber = numberVisible;
        break;
    case Mode::Picture:
        s.frame = frameAt(channels_[channel_], nowMs - pictureSinceMs_);
        s.showNumber = numberVisible;
        break;
    case Mode::Off:
        break;
    }
    return s;
}

void Tv::powerOn(uint32_t nowMs) {
    mode_ = Mode::PowerOn;
    modeSinceMs_ = nowMs;
    numberShown_ = false;
}

void Tv::powerOff(uint32_t nowMs) {
    // Collapse whatever was on the screen; if power is pressed during
    // static, that is the first frame of the new channel.
    frozenFrame_ = mode_ == Mode::Picture
                       ? frameAt(channels_[channel_], nowMs - pictureSinceMs_)
                       : 0;
    mode_ = Mode::PowerOff;
    modeSinceMs_ = nowMs;
    numberShown_ = false;
}

void Tv::switchChannel(uint32_t nowMs) {
    channel_ = (channel_ + 1) % channelCount_;
    mode_ = Mode::Static;
    modeSinceMs_ = nowMs;
    // The number stays up during static and for kNumberMs after it.
    showNumber(nowMs, kStaticMs + kNumberMs);
}

void Tv::showNumber(uint32_t sinceMs, uint32_t forMs) {
    numberShown_ = true;
    numberSinceMs_ = sinceMs;
    numberForMs_ = forMs;
}

void Tv::finishTransitions(uint32_t nowMs) {
    const uint32_t elapsed = nowMs - modeSinceMs_;

    switch (mode_) {
    case Mode::PowerOn:
        if (elapsed >= kPowerMs) {
            mode_ = Mode::Picture;
            pictureSinceMs_ = modeSinceMs_ + kPowerMs;
            showNumber(pictureSinceMs_, kNumberMs);
        }
        break;
    case Mode::Static:
        if (elapsed >= kStaticMs) {
            mode_ = Mode::Picture;
            pictureSinceMs_ = modeSinceMs_ + kStaticMs;
        }
        break;
    case Mode::PowerOff:
        if (elapsed >= kPowerMs) {
            mode_ = Mode::Off;
        }
        break;
    case Mode::Off:
    case Mode::Picture:
        break;
    }
}
