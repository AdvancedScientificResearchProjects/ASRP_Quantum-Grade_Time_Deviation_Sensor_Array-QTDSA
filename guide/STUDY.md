**English** · [Русский](STUDY.ru.md)

← [Back to README](../README.md)

# Study: what QTDSA is

## What this study is

QTDSA (Quantum-Grade Time Deviation Sensor Array) is a concept for a multi-channel metrology instrument. It infers
time deviation indirectly, from the phase and frequency instability of an array of independent oscillators: quartz,
TCXO, OCXO and experimental MCU-based clocks. The concept includes delay compensation (cables, hardware,
communication) and high-resolution visualization.

The repository is a specification. It contains a technical specification, an architecture, a roadmap and an issue
template. It does not contain hardware, firmware, software or measurement data.

## Why it exists

The README states the purpose as inferring time deviation through phase and frequency instability across a
heterogeneous oscillator array. The repository gives no scientific hypothesis; the "why" is engineering: an instrument
that detects instability between oscillators.

## Question it answers

No research question or hypothesis is stated in the repository. Its content answers an instrument-design question
only: what a multi-channel system with these channels, reference clocks and delay model would look like. That is an
interpretation of the document, not a claim made by it.

## What it feeds into

The README names no downstream consumer. It states no patent, product, course, publication or other study that uses
QTDSA. It explicitly says that QTDSA does not tie to any existing ASRP Kazpatent filing and that no patent basis is
asserted. See [ECOSYSTEM](ECOSYSTEM.md#patent-connection).

## What it depends on

- **External reference standards**: GPSDO, a rubidium standard, and an OCXO as fallback (see [DESIGN](DESIGN.md#5-reference-system)).
- **Commercial oscillator types**: quartz resonators, TCXO and OCXO. MCU clocks are named as an experimental channel.
- **No ASRP study or patent** is named as a dependency.

## Relation to other ASRP studies

The README lists three hyperbolic-field studies, ASRP.art, a UAP study and PLFM RADAR as related repositories. It
says that, unlike the Hyperbolic Field and consciousness-cluster studies, QTDSA is a hardware and metrology concept
and is not tied to their filings. The full list is on [ECOSYSTEM](ECOSYSTEM.md#related-research-repositories).

## History of this repository

- The initial commit (a51adaa, 2026-04-18) held a short description under the heading
  "ASRP_Quantum-Grade_Time_Deviation_Sensor_Array-QTDSA". The second commit (e8500c9, 2026-04-18) added a fuller README
  whose title, "QTDSA — Quantum Time Deviation Sensor Array", has no "Grade", with a planned repository name
  `qtdsa-quantum-time-deviation-sensor-array`.
- On 2026-07-18 a pull request (`fix/template-alignment`) aligned the README to the house template, renamed the title
  to "Quantum-Grade", and removed the planned repository name. The prior specification text was reduced; the planned
  structure and an issue template were kept in new form.
- Only `main` and `origin/main` exist. No binary files are in the history.

## Research team

Team roster not yet published in this repository — flagged for owner to fill in rather than fabricated.
The README marks the roster "TBD".

| Name | Role | Responsibilities |
|---|---|---|
| _TBD_ | _TBD_ | _TBD_ |

Open questions about the team are listed in [EVIDENCE](EVIDENCE.md#open-questions).

## Status

Concept and technical specification defined; no hardware built, no firmware written, no measurement data collected.
The README states: "Last Updated: July 2026".
