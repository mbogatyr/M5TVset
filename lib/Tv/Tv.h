#pragma once

#include <stdint.h>

#include "ChannelInfo.h"
#include "DisplayTimeout.h"

// Номер кадра канала через elapsedMs после начала показа. Кадры идут по
// кругу, у каждого своя длительность.
uint8_t frameAt(const ChannelInfo &channel, uint32_t elapsedMs);

// Что должно быть на экране прямо сейчас. Renderer рисует ровно это.
struct Screen {
    enum class Mode : uint8_t {
        Off,      // экран погашен
        PowerOn,  // точка разворачивается в картинку
        PowerOff, // картинка схлопывается в полосу, потом в точку
        Static,   // помехи между каналами
        Picture,  // кадр канала
    };

    Mode mode;
    uint8_t channel;
    uint8_t frame;    // кадр для Picture; для PowerOn/PowerOff — тот, что схлопывается
    bool showNumber;  // номер канала в углу
    uint8_t progress; // фаза PowerOn/PowerOff: 0 — начало, 255 — конец
};

// Игрушечный телевизор: KEY1 листает каналы, KEY2 включает и выключает,
// после простоя гаснет сам.
//
// Как и всё в lib/, железа не касается: на входе время и нажатия, на выходе
// Screen.
class Tv {
  public:
    static constexpr uint32_t kPowerMs = 400;   // эффект кинескопа
    static constexpr uint32_t kStaticMs = 400;  // помехи при переключении
    static constexpr uint32_t kNumberMs = 2000; // номер канала после смены

    Tv(const ChannelInfo *channels, uint8_t channelCount,
       uint32_t idleMs = DisplayTimeout::kIdleMs);

    // Включается с эффектом кинескопа на первом канале. Вызывать один раз
    // при старте.
    void begin(uint32_t nowMs);

    // Вызывать каждый такт. nextPressed и powerPressed — нажатия KEY1 и
    // KEY2 в этом такте (фронт, а не удержание).
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
    uint8_t frozenFrame_ = 0; // кадр, который схлопывается при выключении
    uint32_t modeSinceMs_ = 0;
    uint32_t pictureSinceMs_ = 0;

    bool numberShown_ = false;
    uint32_t numberSinceMs_ = 0;
    uint32_t numberForMs_ = 0;
};
