# ⏱️ QTDSA — Quantum Time Deviation Sensor Array / QTDSA — Массив сенсоров отклонения времени

---

## 📦 Repository Name

`qtdsa-quantum-time-deviation-sensor-array`

---

## 📄 Repository Description (EN)

Advanced multi-channel system for ultra-precise measurement of time and frequency deviations using heterogeneous oscillator arrays (quartz, TCXO, OCXO, MCU-based clocks) with delay-compensated phase analysis and high-resolution visualization.

---

## 📄 Описание репозитория (RU)

Многоканальная система сверхточного измерения отклонений времени и частоты на основе массива гетерогенных осцилляторов (кварц, TCXO, OCXO, MCU) с компенсацией задержек и высокоточным фазовым анализом.

---

# 🧠 TECHNICAL SPECIFICATION / ТЕХНИЧЕСКОЕ ЗАДАНИЕ

---

## 1. System Concept / Концепция системы

**EN:**
Time deviation is inferred from phase and frequency instability across multiple independent oscillators.

**RU:**
Отклонение времени определяется через анализ нестабильности фазы и частоты между независимыми осцилляторами.

---

## 2. Architecture / Архитектура

* Sensor Layer (датчики)
* Measurement Core (измерительное ядро)
* Reference System (эталон)
* Delay Compensation (компенсация задержек)
* Software & UI

---

## 3. Sensor Array / Массив датчиков

### Supported Sensors / Типы датчиков

* Quartz Resonators (32 kHz – 50 MHz)
* TCXO
* OCXO
* MCU-based clocks (экспериментально)

⚠️ MCU не является точным источником времени — используется как вспомогательный канал.

---

### Topology / Топология

* Минимум: 8 каналов
* Цель: 16–64 каналов
* Поддержка распределённых датчиков

---

## 4. Measurement Core / Измерительное ядро

* FPGA (обязательно)
* TDC (Time-to-Digital Converter)
* Разрешение: ≤ 10–50 пс
* Синхронная обработка каналов

---

## 5. Reference System / Эталон

* GPSDO
* Rubidium standard
* OCXO (fallback)

---

## 6. Delay Compensation / Компенсация задержек

### Model / Модель

T_corrected = T_measured − T_cable − T_hw − T_comm

---

### Sources / Источники

* кабели
* разъёмы
* FPGA latency
* коммуникация

---

## 7. Communication / Связь

* USB-C
* Ethernet
* Wi-Fi / Bluetooth (только UI)

---

## 8. Software / Программное обеспечение

### Features / Возможности

* графики фазы
* частотный дрейф
* сравнение каналов
* запись данных

---

### Metrics / Метрики

* Δf / f
* Δφ(t)
* Allan deviation σ_y(τ)

---

## 9. UI / Интерфейс

* научный стиль
* overlay графики
* масштаб до наносекунд
* dark mode

---

## 10. Environmental Factors / Внешние факторы

* температура
* вибрации
* электромагнитные поля

---

## 11. Experimental Modes / Режимы

* Differential Mode
* Reference Mode
* Distributed Mode

---

## 12. Hardware Blocks / Блоки

* sensor boards
* FPGA core
* reference module
* power system

---

## 13. Repository Structure

```text
/hardware
  /sensor_boards
  /fpga_core
  /reference_clock

/firmware
  /fpga
  /mcu

/software
  /backend
  /ui

/docs
  architecture.md
  calibration.md
  experiments.md
```

---

## 14. Limitations / Ограничения

* кварц ≠ абсолютное время
* MCU ≠ прецизионный источник
* беспроводная связь ≠ точные измерения

---

## 15. Roadmap / Дорожная карта

**Phase 1:** 4–8 каналов
**Phase 2:** 16+ каналов + компенсация
**Phase 3:** распределённая система
**Phase 4:** интеграция атомных часов

---

## 16. Key Principle / Ключевой принцип

Система измеряет не время напрямую, а:

→ фазу
→ частоту
→ их флуктуации

---

# 🧾 ISSUE TEMPLATE (EN)

## Title:

Implement Multi-Channel Time Deviation Measurement Core

## Description:

Develop FPGA-based measurement core capable of detecting phase and frequency differences across multiple oscillator channels with picosecond-level resolution.

## Requirements:

* Support ≥ 8 channels
* Phase resolution ≤ 50 ps
* Synchronous acquisition
* Integration with reference clock

## Tasks:

* Design TDC module
* Implement phase comparator
* Add calibration routine
* Validate with identical signal input

---

# 🧾 ШАБЛОН ISSUE (RU)

## Заголовок:

Реализация многоканального ядра измерения отклонений времени

## Описание:

Разработать FPGA-ядро для измерения фазовых и частотных различий между каналами с разрешением на уровне пикосекунд.

## Требования:

* ≥ 8 каналов
* разрешение ≤ 50 пс
* синхронная обработка
* интеграция с эталоном

## Задачи:

* разработка TDC
* фазовый компаратор
* калибровка
* тестирование на одинаковом сигнале

---

# 🚀 FINAL NOTE / ЗАМЕТКА

**EN:**
This system is not a clock — it is a detector of instability.

**RU:**
Это не часы — это детектор нестабильности.

---
