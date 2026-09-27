#include <unity.h>

#include "Tv.h"

// Три канала с разными длительностями кадров: цикл 600, 1000 и 1000 мс.
static const uint16_t kFirstMs[] = {100, 200, 300};
static const uint16_t kSecondMs[] = {500, 500};
static const uint16_t kThirdMs[] = {1000};
static const ChannelInfo kChannels[] = {{kFirstMs, 3}, {kSecondMs, 2}, {kThirdMs, 1}};
static const uint8_t kCount = 3;

static constexpr uint32_t kPower = Tv::kPowerMs;
static constexpr uint32_t kStatic = Tv::kStaticMs;
static constexpr uint32_t kNumber = Tv::kNumberMs;

using Mode = Screen::Mode;

static Tv startedTv(uint32_t idleMs = DisplayTimeout::kIdleMs) {
    Tv tv(kChannels, kCount, idleMs);
    tv.begin(0);
    return tv;
}

// Включился и уже показывает первый канал: картинка пошла с момента kPower.
static Tv watchingTv(uint32_t idleMs = DisplayTimeout::kIdleMs) {
    Tv tv = startedTv(idleMs);
    tv.update(kPower, false, false);
    return tv;
}

static void pressNext(Tv &tv, uint32_t now) { tv.update(now, true, false); }
static void pressPower(Tv &tv, uint32_t now) { tv.update(now, false, true); }
static void idle(Tv &tv, uint32_t now) { tv.update(now, false, false); }

void setUp(void) {}
void tearDown(void) {}

// --- frameAt -----------------------------------------------------------------

void test_frame_at_follows_frame_durations(void) {
    TEST_ASSERT_EQUAL_UINT8(0, frameAt(kChannels[0], 0));
    TEST_ASSERT_EQUAL_UINT8(0, frameAt(kChannels[0], 99));
    TEST_ASSERT_EQUAL_UINT8(1, frameAt(kChannels[0], 100));
    TEST_ASSERT_EQUAL_UINT8(1, frameAt(kChannels[0], 299));
    TEST_ASSERT_EQUAL_UINT8(2, frameAt(kChannels[0], 300));
    TEST_ASSERT_EQUAL_UINT8(2, frameAt(kChannels[0], 599));
}

void test_frame_at_loops_over_the_cycle(void) {
    TEST_ASSERT_EQUAL_UINT8(0, frameAt(kChannels[0], 600));
    TEST_ASSERT_EQUAL_UINT8(1, frameAt(kChannels[0], 1300));
    TEST_ASSERT_EQUAL_UINT8(0, frameAt(kChannels[2], 123456));
}

// --- включение ---------------------------------------------------------------

void test_starts_with_the_power_on_effect_on_the_first_channel(void) {
    Tv tv = startedTv();
    Screen s = tv.screen(0);
    TEST_ASSERT_EQUAL(Mode::PowerOn, s.mode);
    TEST_ASSERT_EQUAL_UINT8(0, s.channel);
    TEST_ASSERT_EQUAL_UINT8(0, s.progress);
}

void test_power_on_progress_grows_to_full(void) {
    Tv tv = startedTv();
    idle(tv, kPower / 2);
    TEST_ASSERT_UINT8_WITHIN(2, 127, tv.screen(kPower / 2).progress);
    // screen() без update() не переходит к картинке, но и за 255 не уходит
    TEST_ASSERT_EQUAL_UINT8(255, tv.screen(kPower * 2).progress);
}

void test_picture_follows_the_power_on_effect(void) {
    Tv tv = watchingTv();
    Screen s = tv.screen(kPower);
    TEST_ASSERT_EQUAL(Mode::Picture, s.mode);
    TEST_ASSERT_EQUAL_UINT8(0, s.channel);
    TEST_ASSERT_EQUAL_UINT8(0, s.frame);
}

void test_channel_number_shows_after_power_on_for_a_while(void) {
    Tv tv = watchingTv();
    idle(tv, kPower + kNumber - 1);
    TEST_ASSERT_TRUE(tv.screen(kPower + kNumber - 1).showNumber);
    idle(tv, kPower + kNumber);
    TEST_ASSERT_FALSE(tv.screen(kPower + kNumber).showNumber);
}

void test_frames_advance_from_the_start_of_the_picture(void) {
    Tv tv = watchingTv();
    idle(tv, kPower + 100);
    TEST_ASSERT_EQUAL_UINT8(1, tv.screen(kPower + 100).frame);
    idle(tv, kPower + 350);
    TEST_ASSERT_EQUAL_UINT8(2, tv.screen(kPower + 350).frame);
    idle(tv, kPower + 600);
    TEST_ASSERT_EQUAL_UINT8(0, tv.screen(kPower + 600).frame);
}

// --- KEY1: переключение канала ------------------------------------------------

void test_next_shows_static_with_the_new_channel_number(void) {
    Tv tv = watchingTv();
    pressNext(tv, 5000);
    Screen s = tv.screen(5000);
    TEST_ASSERT_EQUAL(Mode::Static, s.mode);
    TEST_ASSERT_EQUAL_UINT8(1, s.channel);
    TEST_ASSERT_TRUE(s.showNumber);
}

void test_new_channel_starts_from_its_first_frame_after_static(void) {
    Tv tv = watchingTv();
    pressNext(tv, 5000);
    idle(tv, 5000 + kStatic);
    Screen s = tv.screen(5000 + kStatic);
    TEST_ASSERT_EQUAL(Mode::Picture, s.mode);
    TEST_ASSERT_EQUAL_UINT8(1, s.channel);
    TEST_ASSERT_EQUAL_UINT8(0, s.frame);
    idle(tv, 5000 + kStatic + 500);
    TEST_ASSERT_EQUAL_UINT8(1, tv.screen(5000 + kStatic + 500).frame);
}

void test_channel_number_hides_after_static_and_its_delay(void) {
    Tv tv = watchingTv();
    pressNext(tv, 5000);
    const uint32_t hide = 5000 + kStatic + kNumber;
    idle(tv, hide - 1);
    TEST_ASSERT_TRUE(tv.screen(hide - 1).showNumber);
    idle(tv, hide);
    TEST_ASSERT_FALSE(tv.screen(hide).showNumber);
}

void test_last_channel_is_followed_by_the_first(void) {
    Tv tv = watchingTv();
    pressNext(tv, 5000);
    idle(tv, 6000);
    pressNext(tv, 7000);
    idle(tv, 8000);
    pressNext(tv, 9000);
    idle(tv, 10000);
    TEST_ASSERT_EQUAL_UINT8(0, tv.screen(10000).channel);
}

void test_next_during_static_switches_again_and_restarts_static(void) {
    Tv tv = watchingTv();
    pressNext(tv, 5000);
    pressNext(tv, 5000 + kStatic - 50);
    idle(tv, 5000 + kStatic + 10);
    Screen s = tv.screen(5000 + kStatic + 10);
    TEST_ASSERT_EQUAL(Mode::Static, s.mode);
    TEST_ASSERT_EQUAL_UINT8(2, s.channel);
}

// --- KEY2: выключение и включение ------------------------------------------

void test_power_key_plays_the_power_off_effect_then_turns_off(void) {
    Tv tv = watchingTv();
    pressPower(tv, 5000);
    TEST_ASSERT_EQUAL(Mode::PowerOff, tv.screen(5000).mode);
    TEST_ASSERT_EQUAL_UINT8(0, tv.screen(5000).progress);
    idle(tv, 5000 + kPower);
    TEST_ASSERT_EQUAL(Mode::Off, tv.screen(5000 + kPower).mode);
}

void test_power_off_keeps_the_frame_that_was_on_screen(void) {
    Tv tv = watchingTv();
    idle(tv, kPower + 350); // третий кадр первого канала
    pressPower(tv, kPower + 350);
    Screen s = tv.screen(kPower + 360);
    TEST_ASSERT_EQUAL(Mode::PowerOff, s.mode);
    TEST_ASSERT_EQUAL_UINT8(0, s.channel);
    TEST_ASSERT_EQUAL_UINT8(2, s.frame);
}

void test_any_key_turns_the_tv_back_on_the_same_channel(void) {
    Tv tv = watchingTv();
    pressNext(tv, 5000); // второй канал
    idle(tv, 6000);
    pressPower(tv, 7000);
    idle(tv, 8000);
    pressPower(tv, 9000);
    TEST_ASSERT_EQUAL(Mode::PowerOn, tv.screen(9000).mode);
    idle(tv, 9000 + kPower);
    Screen s = tv.screen(9000 + kPower);
    TEST_ASSERT_EQUAL(Mode::Picture, s.mode);
    TEST_ASSERT_EQUAL_UINT8(1, s.channel);
}

void test_waking_press_does_not_switch_the_channel(void) {
    Tv tv = watchingTv();
    pressPower(tv, 5000);
    idle(tv, 6000);
    pressNext(tv, 7000);
    TEST_ASSERT_EQUAL(Mode::PowerOn, tv.screen(7000).mode);
    idle(tv, 7000 + kPower);
    TEST_ASSERT_EQUAL_UINT8(0, tv.screen(7000 + kPower).channel);
}

void test_key_during_power_off_turns_the_tv_back_on(void) {
    Tv tv = watchingTv();
    pressPower(tv, 5000);
    pressNext(tv, 5100);
    TEST_ASSERT_EQUAL(Mode::PowerOn, tv.screen(5100).mode);
}

// --- простой -------------------------------------------------------------------

void test_tv_turns_itself_off_after_idle_time(void) {
    Tv tv = watchingTv(10000);
    idle(tv, 9999);
    TEST_ASSERT_EQUAL(Mode::Picture, tv.screen(9999).mode);
    idle(tv, 10000);
    TEST_ASSERT_EQUAL(Mode::PowerOff, tv.screen(10000).mode);
    idle(tv, 10000 + kPower);
    TEST_ASSERT_EQUAL(Mode::Off, tv.screen(10000 + kPower).mode);
}

void test_key_press_restarts_the_idle_countdown(void) {
    Tv tv = watchingTv(10000);
    pressNext(tv, 8000);
    idle(tv, 17999);
    TEST_ASSERT_EQUAL(Mode::Picture, tv.screen(17999).mode);
    idle(tv, 18000);
    TEST_ASSERT_EQUAL(Mode::PowerOff, tv.screen(18000).mode);
}

void test_tv_turned_on_after_idle_off_stays_on(void) {
    Tv tv = watchingTv(10000);
    idle(tv, 10000);
    idle(tv, 10000 + kPower);
    pressNext(tv, 50000);
    idle(tv, 50000 + kPower);
    idle(tv, 59999);
    TEST_ASSERT_EQUAL(Mode::Picture, tv.screen(59999).mode);
}

// --- переполнение millis() ---------------------------------------------------

void test_tv_survives_the_millis_rollover(void) {
    const uint32_t start = 0xFFFFFF00u; // до переполнения 256 мс
    Tv tv(kChannels, kCount, 10000);
    tv.begin(start);
    idle(tv, start + kPower); // уже после нуля
    TEST_ASSERT_EQUAL(Mode::Picture, tv.screen(start + kPower).mode);
    idle(tv, start + kPower + 100);
    TEST_ASSERT_EQUAL_UINT8(1, tv.screen(start + kPower + 100).frame);
    pressNext(tv, start + 1000);
    idle(tv, start + 1000 + kStatic);
    TEST_ASSERT_EQUAL(Mode::Picture, tv.screen(start + 1000 + kStatic).mode);
    TEST_ASSERT_EQUAL_UINT8(1, tv.screen(start + 1000 + kStatic).channel);
    idle(tv, start + 1000 + 10000);
    TEST_ASSERT_EQUAL(Mode::PowerOff, tv.screen(start + 1000 + 10000).mode);
}

int main(int, char **) {
    UNITY_BEGIN();

    RUN_TEST(test_frame_at_follows_frame_durations);
    RUN_TEST(test_frame_at_loops_over_the_cycle);

    RUN_TEST(test_starts_with_the_power_on_effect_on_the_first_channel);
    RUN_TEST(test_power_on_progress_grows_to_full);
    RUN_TEST(test_picture_follows_the_power_on_effect);
    RUN_TEST(test_channel_number_shows_after_power_on_for_a_while);
    RUN_TEST(test_frames_advance_from_the_start_of_the_picture);

    RUN_TEST(test_next_shows_static_with_the_new_channel_number);
    RUN_TEST(test_new_channel_starts_from_its_first_frame_after_static);
    RUN_TEST(test_channel_number_hides_after_static_and_its_delay);
    RUN_TEST(test_last_channel_is_followed_by_the_first);
    RUN_TEST(test_next_during_static_switches_again_and_restarts_static);

    RUN_TEST(test_power_key_plays_the_power_off_effect_then_turns_off);
    RUN_TEST(test_power_off_keeps_the_frame_that_was_on_screen);
    RUN_TEST(test_any_key_turns_the_tv_back_on_the_same_channel);
    RUN_TEST(test_waking_press_does_not_switch_the_channel);
    RUN_TEST(test_key_during_power_off_turns_the_tv_back_on);

    RUN_TEST(test_tv_turns_itself_off_after_idle_time);
    RUN_TEST(test_key_press_restarts_the_idle_countdown);
    RUN_TEST(test_tv_turned_on_after_idle_off_stays_on);

    RUN_TEST(test_tv_survives_the_millis_rollover);

    return UNITY_END();
}
