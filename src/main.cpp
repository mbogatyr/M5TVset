#include <M5Unified.h>

#include "Frames.h"
#include "Orientation.h"
#include "Renderer.h"
#include "Tv.h"

namespace {

constexpr uint8_t kBrightness = 120;

Renderer renderer;
Tv tv(kChannels, kChannelCount);
Orientation orientation;

bool displayAwake = true;

void setDisplayAwake(bool awake) {
    if (awake == displayAwake) {
        return;
    }
    displayAwake = awake;

    if (awake) {
        M5.Display.wakeup();
        M5.Display.setBrightness(kBrightness);
        renderer.invalidate();
        // The TV may have been turned over while the screen was asleep.
        orientation.reset();
    } else {
        // The backlight draws the most power, so switch it off separately
        // from putting the panel itself to sleep.
        M5.Display.setBrightness(0);
        M5.Display.sleep();
    }
}

} // namespace

void setup() {
    auto cfg = M5.config();
    M5.begin(cfg);

    M5.Display.setBrightness(kBrightness);
    renderer.begin();
    tv.begin(millis());
}

void loop() {
    M5.update();

    const uint32_t now = millis();

    // Power-off is not handled here: the side button does that by itself
    // on a double click, through the PMIC. KEY2 only turns the screen
    // off and on, like the button on a toy TV.
    tv.update(now, M5.BtnA.wasPressed(), M5.BtnB.wasPressed());

    const Screen screen = tv.screen(now);
    setDisplayAwake(screen.mode != Screen::Mode::Off);

    if (displayAwake) {
        float ax, ay, az;
        if (M5.Imu.getAccel(&ax, &ay, &az)) {
            renderer.setFlipped(orientation.update(now, ax, ay, az));
        }
        renderer.draw(screen);
    }

    delay(20);
}
