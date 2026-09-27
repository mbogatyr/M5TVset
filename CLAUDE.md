# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

M5TVset is a toy TV on an M5StickS3 for a room in a LEGO house. The screen is
landscape, with eleven channels (News, Animals, Cartoons, Weather, Sports,
Space, Underwater, Science, Playtime, UFO, History); each loops 6–8 cartoon
frames. KEY1 flips channels with TV static and a channel number in the
corner, KEY2 turns the TV on and off with a CRT effect.

All characters are our own. Do not draw other people's characters
(SpongeBob and the like): they are someone else's copyright.

Everything shown on screen is in English. Documentation, code comments and
commit messages are in English too. Commits up to `da86162` are in Russian.

## Commands

PlatformIO is not installed globally but through the official installer, in
a venv. The binary lives at `~/.platformio/penv/bin/pio`. It is not on
`PATH`, so call it by its full path.

```bash
~/.platformio/penv/bin/pio test -e native                         # unit tests of the logic, on the host
~/.platformio/penv/bin/pio test -e native -f test_tv              # a single test suite
~/.platformio/penv/bin/pio run -e sticks3                         # build the firmware
~/.platformio/penv/bin/pio run -e sticks3 -t upload               # flash the board
~/.platformio/penv/bin/pio run -e sticks3 -t merged               # single image for M5Burner
~/.platformio/penv/bin/pio device monitor -e sticks3              # serial monitor, 115200
python3 art/build.py                                              # rebuild the frames after editing scenes
python3 art/build.py --sheet                                      # plus storyboards in art/.cache/
python3 tools/channel_sheet.py                                    # docs/channels.png for the README
```

The xtensa-esp32s3 toolchain is installed into `~/.platformio/packages` once
per machine (about eight minutes) and shared by all projects. The first
build of a new project downloads the latest M5Unified into `.pio/` and takes
about 20 seconds.

## Architecture

The split between `lib/` and `src/` is load-bearing, not cosmetic:

- `lib/` — logic: plain C++ with no Arduino, no M5Unified and no hardware
  access of any kind.
  - `Tv` — the TV: Off / PowerOn / PowerOff / Static / Picture modes,
    channel switching, the channel number in the corner, and `frameAt()`
    over frame durations. Its output is a `Screen`: what should be on the
    display right now.
  - `DisplayTimeout` — idle detector (3 minutes without a button press);
    `Tv` uses it to turn itself off.
  - `Orientation` — decides from the accelerometer whether the TV is turned
    over by 180°: the sign of the acceleration along the board's X axis, a
    0.6 g threshold, the new position has to hold for 400 ms, and shaking or
    standing upright or lying flat are ignored.
  - `ChannelInfo.h` — the frame durations of a channel; the logic never sees
    the images.
- `src/` — everything that knows about the board: `Renderer` draws a
  `Screen` on the display, `Frames.h` plus the generated
  `generated/Frames.cpp` hold the frame PNGs in flash, and `main.cpp` ties the
  logic to the hardware.

The `native` environment builds only `lib/` (PlatformIO's `test_build_src`
defaults to `no`), so the logic is tested on the Mac without the board.
**Do not pull hardware dependencies into `lib/` — that breaks the tests.**

### Time comes in as a parameter

The logic in `lib/` never calls `millis()` itself; it gets the current time
as an argument. Tests can then jump to any moment without waiting, and the
logic has no `delay()`: `loop()` runs at 50 Hz and just passes `millis()`
along.

`millis()` wraps around after about 49 days. Compute intervals with unsigned
subtraction, `now - since`, so the wraparound goes unnoticed.

### Drawing

`Renderer` assembles the whole frame in an `M5Canvas` (a sprite in PSRAM) and
pushes it with a single `pushSprite`. Drawing straight to the screen
flickers visibly.

`Renderer::draw()` compares its input with the previous frame and returns if
nothing changed; static (`Static`) is redrawn on every tick. `invalidate()`
clears that memory; `main.cpp` calls it when the display wakes up, because
the panel's contents are lost during sleep.

A second sprite, `picture_`, holds the current decoded frame, so `drawPng`
runs only when the channel or the frame changes. The CRT effect squeezes
`picture_` with `pushRotateZoom`, and the static is written straight into
the sprite buffer (which stores RGB565 byte-swapped).

Orientation: `kRotation = 1` puts KEY1 to the right of the screen and
`kFlippedRotation = 3` is the turned-over one. `main.cpp` reads
`M5.Imu.getAccel()` on every tick (a BMI270; M5Unified enables it on its own
and remaps the axes for the StickS3) and passes the `Orientation` decision to
`Renderer::setFlipped()`. Both the rotation and the sign of X in
`Orientation::sideOf()` were checked on the board.

### Channel images

The frames are drawn by code, not by hand: `art/scenes/<channel>.py` builds
the SVG of each frame from one parameterized scene function, and the shared
parts (eyes, smiles, the channel logo) live in `art/svg.py`.
`art/scenes/__init__.py` sets the channel order. `art/build.py`:

1. screenshots each SVG with headless Chrome at 4x and scales it down to
   240x135 with Pillow (the antialiasing comes out smoother); the shots are
   cached in `art/.cache/` by SVG hash;
2. quantizes to a 256-color palette with median cut: the PNG gets about 4
   times smaller, and the water and sky gradients don't break into bands the
   way they do with octree;
3. writes `art/frames/`, `src/generated/Frames.cpp` (the PNGs as arrays in
   flash plus the frame durations) and `art/preview.html` (a preview with a
   button simulator), plus its Russian copy `art/preview.ru.html`.

There is one page template, `art/preview.template.html`, in English. The
Russian page is made from it by the replacement table in `art/preview_ru.py`,
so the CSS and JS exist only once. Every English text in the table must occur
in the template, otherwise `build.py` fails: when you change a text in the
template, update its entry in `preview_ru.py` too.

Never edit `src/generated/Frames.cpp` by hand — change the scenes and rerun
the script. Run Chrome without `--user-data-dir`: on macOS it then takes the
shot but never exits. Everything that moves across the frame (fish, bird,
rocket, the news ticker) moves by "period / number of frames" per frame, so
the loop closes without a jump.

## Board notes

M5StickS3 — ESP32-S3-PICO-1-N8R8, 8 MB flash, 8 MB octal PSRAM, ST7789P3
135x240 display.

- PlatformIO has **no** `m5stack-sticks3` board id. The project uses
  `esp32-s3-devkitc-1` plus `board_build.arduino.memory_type = qio_opi` and
  the `default_8MB.csv` partitions. Don't "fix" this to a board id that
  doesn't exist.
- USB is native, with no CH9102 bridge, so on macOS the port is called
  `/dev/cu.usbmodem*`, not `/dev/cu.usbserial*`. Serial output needs
  `-DARDUINO_USB_CDC_ON_BOOT=1`, which is already set.
- Buttons: KEY1 on G11 (`M5.BtnA`), KEY2 on G12 (`M5.BtnB`). Grove (G9/G10)
  and HAT2 (G1–G8, G43, G44) are free.

### Publishing to M5Burner

M5Burner writes the uploaded file starting at address 0x0, so it needs a full
image. The app-only `firmware.bin` belongs at 0x10000; flashed at 0x0 it
would overwrite the bootloader. `pio run -e sticks3 -t merged` (the
`tools/merged_image.py` extra script) stitches the bootloader, partition
table, `boot_app0` and the app into `.pio/build/sticks3/firmware-merged.bin`
with esptool `merge_bin`. It takes the offsets and flash parameters from
PlatformIO's own upload configuration, so the image matches what `upload`
writes.

The upload form at burner.m5stack.com/developer/firmware/upload asks for:
- name, category and supported devices (StickS3);
- description and version description, both Markdown;
- version and project link;
- the `.bin` package;
- visibility: Public needs review;
- a cover image: `docs/channels.png` works.

### The side button is handled by the PMIC, not the firmware

| Action | Result |
|---|---|
| Single press | Power on / reset |
| Double press | Power off |
| Long hold | Download mode (the internal green LED blinks) |

That is why the firmware has no power-off button of its own. If the board
ever has to power off in software (on idle, say), note that on the StickS3
`M5.Power.powerOff()` used to wake the board right back up on a timer —
[M5Unified#235](https://github.com/m5stack/M5Unified/issues/235), fixed in
0.2.23. That has not been checked on a board with the fixed version.

`M5.Power` does not set `_wakeupPin` for the StickS3, so there is no
ready-made wake-up from deep sleep by button either; it would have to be set
up by hand with `esp_sleep_enable_ext0_wakeup`.

### If flashing fails

`A fatal error occurred: Failed to connect to ESP32-S3: No serial data received.`

The board shows up as `USB JTAG_serial debug unit` (VID 0x303A, PID 0x1001):
the built-in USB-Serial-JTAG rather than a CDC port (a consequence of
`ARDUINO_USB_MODE=1`). The automatic reset into download mode through it
doesn't always work, and neither `--before usb_reset` nor `--before
no_reset` helps. The only fix is manual: hold the side button until the
green LED blinks. After such a flash the board may stay in the bootloader;
one short press of the side button starts the firmware.

### If the board is stuck in the bootloader

The firmware doesn't start, and the port shows `boot:0x0
(DOWNLOAD(USB/UART0))` and `waiting for download`. This happened when a
pyserial script opened and closed the port as a check: macOS toggles
DTR/RTS then, and the USB-Serial-JTAG takes that as a command to enter the
bootloader. The way out is one short press of the side button. So don't
check the firmware by opening the port from a script; whether
`pio device monitor` does the same has not been checked.

## Tests

Unit tests cover the logic in `lib/`, one `test/test_<module>/test_main.cpp`
directory per module. Rendering is checked by eye on the board — don't try
to write tests for `Renderer`: that would need a mock of all of LovyanGFX
and would prove nothing useful.

`main` in the tests returns the failure count from `UNITY_END()`, and
PlatformIO reports a non-zero exit code as a signal number. A line like
`Program received signal SIGALRM` with failing tests is an artifact of the
report, not a separate problem; it disappears once the tests pass.
