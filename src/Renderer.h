#pragma once

#include <M5Unified.h>

#include "Tv.h"

// Рисует телевизор на встроенном дисплее StickS3 в альбомной ориентации
// (240x135): кадры каналов, помехи, номер канала и эффект кинескопа.
//
// Кадр собирается целиком в спрайте и выталкивается одним вызовом:
// рисование прямо на экране даёт заметное мерцание.
class Renderer {
  public:
    // Вызывать после M5.begin().
    void begin();

    // Перерисовывает экран только тогда, когда картинка изменилась.
    // Помехи меняются каждый такт, поэтому их кадры рисуются всегда.
    void draw(const Screen &screen);

    // Сбрасывает память о последнем кадре. Нужно после пробуждения
    // дисплея: его содержимое потеряно, а сравнение с прошлым кадром
    // иначе решит, что перерисовывать нечего.
    void invalidate();

    // Переворачивает картинку на 180°, когда телевизор поставили на другую
    // длинную грань. Спрайты 240x135 подходят к обеим ориентациям.
    void setFlipped(bool flipped);

  private:
    void loadPicture(uint8_t channel, uint8_t frame);
    void paintStatic();
    void paintCollapse(uint8_t collapse);
    void paintNumber(uint8_t channel);

    M5Canvas canvas_{&M5.Display};
    M5Canvas picture_; // раскодированный текущий кадр канала

    bool flipped_ = false;

    bool hasPrevious_ = false;
    Screen previous_{};

    bool hasPicture_ = false;
    uint8_t pictureChannel_ = 0;
    uint8_t pictureFrame_ = 0;

    uint32_t noise_ = 0x9e3779b9u; // состояние xorshift для помех
};
