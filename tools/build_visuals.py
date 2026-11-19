#!/usr/bin/env python3
"""Draws the showcase diagrams (EN and RU twins) with the numbers from tools/facts.py.

    python3 tools/build_visuals.py

Writes guide/assets/banner/hero-banner.{en,ru}.svg and guide/assets/diagrams/*.{en,ru}.svg.
Every label is checked against its box before writing: the build aborts when a label would not fit
(estimated width) or when a font is smaller than 12 px. Standard library only.
"""
import os
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import facts as factsmod  # noqa: E402

ROOT = factsmod.ROOT
FONT = "'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
MIN_FONT = 12
CHAR_W = 0.56  # average glyph width in em for the sans stack (conservative)


class Fit(Exception):
    pass


class Svg:
    def __init__(self, w, h, title, desc):
        self.w, self.h = w, h
        self.title, self.desc = title, desc
        self.parts = []

    def rect(self, x, y, w, h, fill, stroke=None, rx=12, sw=1.6):
        s = ' stroke="%s" stroke-width="%s"' % (stroke, sw) if stroke else ""
        self.parts.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"%s/>'
                          % (x, y, w, h, rx, fill, s))

    def text(self, x, y, s, size, fill, weight=400, anchor="start", label="", box_w=None):
        if size < MIN_FONT:
            raise Fit("font %s < %s in %r" % (size, MIN_FONT, s))
        if box_w is not None and len(s) * size * CHAR_W > box_w:
            raise Fit("label does not fit (%d px > %d px): %r" % (len(s) * size * CHAR_W, box_w, s))
        self.parts.append('<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s" font-weight="%s" '
                          'text-anchor="%s">%s</text>' % (x, y, FONT, size, fill, weight, anchor, escape(s)))

    def line(self, x1, y1, x2, y2, stroke="#6f9bff", sw=2):
        self.parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" '
                          'marker-end="url(#arr)"/>' % (x1, y1, x2, y2, stroke, sw))

    def render(self):
        head = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
                'role="img" aria-labelledby="t d">' % (self.w, self.h, self.w, self.h))
        defs = ("<defs><marker id='arr' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' "
                "orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='#8ea0d6'/></marker>"
                "<linearGradient id='bg' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#070b18'/>"
                "<stop offset='1' stop-color='#0d1530'/></linearGradient></defs>")
        return ('%s<title id="t">%s</title><desc id="d">%s</desc>%s<rect width="%d" height="%d" rx="18" '
                'fill="url(#bg)"/>\n%s\n</svg>\n'
                % (head, escape(self.title), escape(self.desc), defs, self.w, self.h, "\n".join(self.parts)))


def write(rel, svg):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg.render())


def hero(F, lang):
    en = lang == "en"
    s = Svg(1200, 300, "QTDSA",
            ("Hero banner: QTDSA concept stage, %s sensor types, %s to %s channels, %s roadmap phases, none started."
             % (F["sensor_types"], F["channels_min"], F["channels_target"], F["phases"]) if en else
             "Баннер: QTDSA, стадия концепции, %s типа датчиков, %s–%s каналов, %s фазы дорожной карты, ни одна не начата."
             % (F["sensor_types"], F["channels_min"], F["channels_target"], F["phases"])))
    s.text(48, 100, "QTDSA", 48, "#e6ecff", 800, box_w=520)
    if en:
        s.text(48, 146, "Quantum-Grade Time Deviation Sensor Array", 22, "#8ea0d6", 500, box_w=1100)
        s.text(48, 176, "Concept stage: specification only, no hardware, firmware or data yet", 16, "#4ecdc4", 600, box_w=1100)
        chips = [("%s sensor types" % F["sensor_types"], "quartz, TCXO, OCXO, MCU"),
                 ("%s to %s channels" % (F["channels_min"], F["channels_target"]), "minimum to target"),
                 ("%s phases, none started" % F["phases"], "roadmap"),
                 ("Concept / design", "status")]
    else:
        s.text(48, 146, "Массив сенсоров отклонения времени квантового класса", 22, "#8ea0d6", 500, box_w=1100)
        s.text(48, 176, "Стадия концепции: только ТЗ, без оборудования и данных", 16,
               "#4ecdc4", 600, box_w=1100)
        chips = [("%s типа датчиков" % F["sensor_types"], "кварц, TCXO, OCXO, MCU"),
                 ("%s–%s каналов" % (F["channels_min"], F["channels_target"]), "минимум–цель"),
                 ("%s фазы, ни одна не начата" % F["phases"], "дорожная карта"),
                 ("Концепция / проект", "статус")]
    for i, (big, small) in enumerate(chips):
        x = 48 + i * 280
        s.rect(x, 210, 256, 64, "#0b1430", "#6f9bff", rx=12)
        s.text(x + 16, 238, big, 16, "#e6ecff", 700, box_w=232)
        s.text(x + 16, 260, small, 13, "#8ea0d6", 400, box_w=232)
    write("guide/assets/banner/hero-banner.%s.svg" % lang, s)


def chain(F, lang):
    en = lang == "en"
    s = Svg(1200, 360, "Measurement chain" if en else "Цепочка измерения",
            ("Measurement chain: oscillators, FPGA and TDC core, delay compensation, metrics; reference clocks feed the core."
             if en else
             "Цепочка измерения: осцилляторы, ядро FPGA и TDC, компенсация задержек, метрики; эталоны питают ядро."))
    cols = [
        ("Oscillators" if en else "Осцилляторы",
         ["quartz, TCXO, OCXO" if en else "кварц, TCXO, OCXO", "MCU: experimental" if en else "MCU: экспериментально"]),
        ("Measurement core" if en else "Ядро измерения",
         ["FPGA + TDC" if en else "FPGA + TDC", "resolution ≤ %s ps" % F["resolution_ps"] if en else
          "разрешение ≤ %s пс" % F["resolution_ps"]]),
        ("Delay compensation" if en else "Компенсация задержек",
         ["T_corrected = T_meas −", "T_cable − T_hw − T_comm"]),
        ("Metrics" if en else "Метрики",
         ["Δf / f, Δφ(t)", "Allan deviation σ_y(τ)" if en else "девиация Аллана σ_y(τ)"]),
    ]
    bw, gap, y, bh = 255, 36, 70, 150
    for i, (head, body) in enumerate(cols):
        x = 40 + i * (bw + gap)
        s.rect(x, y, bw, bh, "#0b1430", "#6f9bff" if i != 1 else "#34d399")
        s.text(x + 16, y + 34, head, 17, "#e6ecff", 700, box_w=bw - 32)
        for j, line in enumerate(body):
            s.text(x + 16, y + 70 + j * 26, line, 14, "#8ea0d6", 400, box_w=bw - 32)
        if i < len(cols) - 1:
            s.line(x + bw + 4, y + bh // 2, x + bw + gap - 4, y + bh // 2)
    ref_x = 40 + 1 * (bw + gap)
    s.rect(ref_x, 262, bw, 72, "#0b1430", "#ffa657")
    s.text(ref_x + 16, 292, "Reference" if en else "Эталон", 17, "#e6ecff", 700, box_w=bw - 32)
    s.text(ref_x + 16, 316, "GPSDO, rubidium, OCXO" if en else "GPSDO, рубидий, OCXO", 14, "#8ea0d6", 400, box_w=bw - 32)
    s.line(ref_x + bw // 2, 262, ref_x + bw // 2, 224, stroke="#ffa657")
    s.text(40, 40, "Concept only: no hardware exists; this is the planned chain" if en else
           "Только концепция: цепочка по ТЗ, оборудования нет", 15, "#4ecdc4", 700,
           box_w=1120)
    write("guide/assets/diagrams/measurement-chain.%s.svg" % lang, s)


def claimed(F, lang):
    en = lang == "en"
    s = Svg(1200, 400, "Claimed versus shown" if en else "Заявлено и показано",
            ("Five design claims of the README and their state in the repository: design targets, a formula, a plan and "
             "an unasserted patent basis; nothing is measured or built." if en else
             "Пять проектных утверждений README и их состояние в репозитории: проектные цели, формула, план и "
             "непроверенная патентная основа; ничего не измерено и не построено."))
    heads = (["Topic", "What the README states (claim)", "State in this repository"] if en else
             ["Тема", "Что сказано в README (заявлено)", "Состояние в репозитории"])
    xs = [24, 200, 700]
    widths = [160, 480, 476]
    for x, h, w in zip(xs, heads, widths):
        s.text(x, 84, h, 14, "#4ecdc4", 700, box_w=w)
    rows = ([
        ("Channels", "Minimum %s, target %s–%s channels" % (F["channels_min"], F["channels_target_min"], F["channels_target"]),
         "DESIGN TARGET: no hardware"),
        ("Resolution", "≤ %s–%s ps (issue template: ≤ %s ps)" % (F["resolution_ps_min"], F["resolution_ps"], F["issue_phase_ps"]),
         "NOT SHOWN: no measurement"),
        ("Delay model", "T_corrected = T_measured − T_cable − T_hw − T_comm", "FORMULA ONLY: not validated"),
        ("Roadmap", "%s phases, atomic clock integration last" % F["phases"], "PLAN ONLY: none started"),
        ("Patent basis", "No filing; none asserted in the README", "NOT ASSERTED: exploratory"),
    ] if en else [
        ("Каналы", "Минимум %s, цель %s–%s каналов" % (F["channels_min"], F["channels_target_min"], F["channels_target"]),
         "ПРОЕКТНАЯ ЦЕЛЬ: нет оборудования"),
        ("Разрешение", "≤ %s–%s пс (шаблон задачи: ≤ %s пс)" % (F["resolution_ps_min"], F["resolution_ps"], F["issue_phase_ps"]),
         "НЕ ПОКАЗАНО: нет измерений"),
        ("Модель задержек", "T_corrected = T_measured − T_cable − T_hw − T_comm", "ТОЛЬКО ФОРМУЛА: не проверена"),
        ("Дорожная карта", "%s фазы, интеграция атомных часов последней" % F["phases"], "ТОЛЬКО ПЛАН: ни одна не начата"),
        ("Патентная основа", "Заявки нет; в README не утверждается", "НЕ УТВЕРЖДАЕТСЯ: поисковое"),
    ])
    for i, (a, b, c) in enumerate(rows):
        y = 112 + i * 56
        s.rect(16, y, 1168, 46, "#0b1430", "#6f9bff", rx=10, sw=1)
        s.text(24, y + 29, a, 15, "#e6ecff", 700, box_w=160)
        s.text(200, y + 29, b, 14, "#8ea0d6", 400, box_w=480)
        s.text(700, y + 29, c, 14, "#ffa657", 700, box_w=476)
    write("guide/assets/diagrams/claimed-vs-shown.%s.svg" % lang, s)


def main():
    F = factsmod.facts()
    for lang in ("en", "ru"):
        hero(F, lang)
        chain(F, lang)
        claimed(F, lang)
    print("visuals: 3 diagrams x 2 languages written")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Fit as e:
        print("FIT ERROR:", e)
        sys.exit(1)
