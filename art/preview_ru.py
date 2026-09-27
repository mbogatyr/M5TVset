"""Russian version of the preview page, built from the same template.

The template (art/preview.template.html) stays the only source of the page's
CSS and JS. build.py writes art/preview.ru.html by replacing each English
text below with its Russian counterpart. Every English text must occur in the
template, so an edit to the template that is not mirrored here fails the
build instead of leaving the Russian page half translated.

Longer texts come first where a shorter one is part of them.
"""

REPLACEMENTS = [
    ("<title>M5TVset toy TV</title>", "<title>Телевизор M5TVset</title>"),
    ("<h1>M5TVset toy TV</h1>", "<h1>Телевизор M5TVset</h1>"),
    ("Channel preview · M5StickS3 · 240×135 screen",
     "Превью каналов · M5StickS3 · экран 240×135"),
    ("A preview of all <strong>11 channels</strong> of a toy TV for a brick-built house. "
     "These are the same PNG frames the firmware shows, with the same timings.",
     "<strong>Одиннадцать каналов</strong> игрушечного телевизора для домика из кубиков, "
     "все надписи на экране по-английски. Кадры и их длительности здесь те же, что "
     "показывает прошивка: это одни и те же PNG."),

    ('aria-label="TV simulator"', 'aria-label="Симулятор телевизора"'),
    ('aria-label="TV screen"', 'aria-label="Экран телевизора"'),
    ('aria-label="KEY1: next channel"', 'aria-label="KEY1: следующий канал"'),
    ('<span class="key-label">channel</span>', '<span class="key-label">канал</span>'),
    ('aria-label="KEY2: turn on or off"', 'aria-label="KEY2: включить или выключить"'),
    ('<span class="key-label">on/off</span>', '<span class="key-label">вкл/выкл</span>'),

    ('<span class="now-label">Now on air</span>', '<span class="now-label">Сейчас в эфире</span>'),
    ('id="now-frame">frame 1 of 8<', 'id="now-frame">кадр 1 из 8<'),
    ('aria-label="Channels"', 'aria-label="Каналы"'),
    ('aria-label="Screen size"', 'aria-label="Размер экрана"'),
    (">Large, ×2<", ">Крупно, ×2<"),
    (">Actual size, 25 mm<", ">Как на плате, 25 мм<"),

    ("<li><b>KEY1</b> (<kbd>→</kbd> or <kbd>Enter</kbd>): 0.4 s of static, then the next "
     "channel. Its number stays in the corner for 2 s. After the last channel comes the "
     "first.</li>",
     "<li><b>KEY1</b> (<kbd>→</kbd> или <kbd>Enter</kbd>): помехи 0,4 с, следующий канал, "
     "номер в углу горит 2 с. После последнего снова первый.</li>"),
    ("<li><b>KEY2</b> (<kbd>Space</kbd>): the screen shuts off like an old CRT. Any key "
     "turns it back on at the same channel.</li>",
     "<li><b>KEY2</b> (<kbd>пробел</kbd>): экран гаснет, как у старого кинескопа. Любая "
     "кнопка включает на том же канале.</li>"),
    ("<li><b>3 minutes without a key press</b>: the TV turns itself off.</li>",
     "<li><b>3 минуты без нажатий</b>: телевизор гаснет сам.</li>"),
    ("<li>The channel chips are only for this preview. On the board, KEY1 cycles through "
     "the channels.</li>",
     "<li>Кружки с каналами нужны только для просмотра, на плате каналы листаются по "
     "кругу.</li>"),

    ("Frame numbers match the files in <q>art/frames/&lt;NN&gt;_&lt;channel&gt;/&lt;MM&gt;.png</q>. "
     "NN is the channel number and MM is the frame number minus one, both zero-padded. "
     "For example, Sports frame 4 is <q>art/frames/05_sport/03.png</q>.",
     "Номера кадров совпадают с файлами "
     "<q>art/frames/&lt;NN&gt;_&lt;channel&gt;/&lt;MM&gt;.png</q>: NN — номер канала, MM — "
     "номер кадра минус один, оба с ведущим нулём. Например, кадр 4 канала Sports — это "
     "<q>art/frames/05_sport/03.png</q>."),

    ('<h2 id="boards-title">Storyboards</h2>', '<h2 id="boards-title">Раскадровка</h2>'),
    ("<p>Each channel plays in a loop. The loop runs on the left. On the right are all "
     "frames with their numbers and durations. The frame that is playing now is "
     "highlighted.</p>",
     "<p>Каждый канал крутится по кругу. Слева цикл в движении, справа все кадры с "
     "номерами и временем показа. Кадр, который сейчас идёт в цикле, подсвечен.</p>"),

    # JS: plurals, numbers and the strings the simulator writes at run time.
    ("const plural = (n, one, many) => (n === 1 ? one : many);",
     "const plural = (n, one, few, many) => {\n"
     "    const m10 = n % 10, m100 = n % 100;\n"
     "    if (m10 === 1 && m100 !== 11) return one;\n"
     "    if (m10 >= 2 && m10 <= 4 && (m100 < 12 || m100 > 14)) return few;\n"
     "    return many;\n"
     "  };"),
    ("toLocaleString('en-US',", "toLocaleString('ru-RU',"),
    ("frameText = 'TV is off'", "frameText = 'телевизор выключен'"),
    ("frameText = 'static, switching'", "frameText = 'помехи, переключаемся'"),
    ("frameText = 'turning on'", "frameText = 'включается'"),
    ("frameText = 'turning off'", "frameText = 'выключается'"),
    ("`frame ${frameAt(ch, now - tv.channelSince) + 1} of ${ch.frames.length}`",
     "`кадр ${frameAt(ch, now - tv.channelSince) + 1} из ${ch.frames.length}`"),
    ("${n} ${plural(n, 'frame', 'frames')} · ${seconds(ch.cycle)} s loop",
     "${n} ${plural(n, 'кадр', 'кадра', 'кадров')} · цикл ${seconds(ch.cycle)} с"),
    ('aria-label="${ch.title}: frame loop"', 'aria-label="${ch.title}: цикл кадров"'),
    ("<figcaption>loop in motion, ×2</figcaption>", "<figcaption>цикл в движении, ×2</figcaption>"),
    ('alt="${ch.title}, frame ${i + 1}"', 'alt="${ch.title}, кадр ${i + 1}"'),
    ("<b>frame ${i + 1}</b> · ${f.ms} ms", "<b>кадр ${i + 1}</b> · ${f.ms} мс"),
]


def translate(page):
    for english, russian in REPLACEMENTS:
        if english not in page:
            raise RuntimeError(
                f"art/preview_ru.py: the template no longer has {english[:60]!r}; "
                "update REPLACEMENTS to match art/preview.template.html")
        page = page.replace(english, russian)
    return page
