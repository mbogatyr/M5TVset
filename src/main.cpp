#include <M5Unified.h>

#include "Frames.h"
#include "Renderer.h"
#include "Tv.h"

namespace {

constexpr uint8_t kBrightness = 120;

Renderer renderer;
Tv tv(kChannels, kChannelCount);

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
    } else {
        // Подсветка — главный потребитель, гасим её отдельно от
        // усыпления самой панели.
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

    // Выключение питания здесь не обрабатывается: боковая кнопка
    // делает это сама двойным щелчком через PMIC. KEY2 только гасит
    // экран, как кнопка на игрушечном телевизоре.
    tv.update(now, M5.BtnA.wasPressed(), M5.BtnB.wasPressed());

    const Screen screen = tv.screen(now);
    setDisplayAwake(screen.mode != Screen::Mode::Off);

    if (displayAwake) {
        renderer.draw(screen);
    }

    delay(20);
}
