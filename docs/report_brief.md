# Report brief (both reports, both chats)

Main chat, 2026-10-14. Binding for every line of report text, LaTeX and figure caption written by either chat. Read this file, `docs/writing_style_guide.md` and `CLAUDE.md` sections 4 and 5 before writing. Both chats have been compacted: work from the repo documents named here, never from chat memory, and re-read a source before quoting any number from it.

## 1. The two reports

| | Extensive report | Compact report |
|---|---|---|
| Title | From first principles to a printed airframe: sizing, topology optimisation and verification of a 3.5-inch quadcopter in PET-CF | A frequency-driven airframe: first-principles sizing and topology optimisation of a 3.5-inch quadcopter frame in PET-CF |
| Subtitle line | 3.5-inch quadcopter frame, Siraya PET-CF, Abaqus/Tosca | same |
| Length | 50+ pages | about 15 pages with figures |
| Purpose | complete record: all theory, explained slowly, and the whole development with its decisions | portfolio piece: the project as an engineering case, readable in 15 minutes |
| Due | after the compact report (2026-10-14, later in the day) | **2026-10-14, 09:00 Lisbon** |
| Folder | `report/extensive/` | `report/compact/` |
| Writers | main chat (assembly, most chapters), set-up chat (chapters in section 6) | main chat only |

Cover of both: title, subtitle line, "Miguel Dias de Lima", "migueldiaslima@gmail.com", date, and the assembly render (R1) as the cover image. No logo of any institution or company. The compact report states once, in its first page or the closing section, that a full report documents the complete development, the theory and every decision behind this summary. It gives no link and no repository.

## 2. Framing rules (absolute)

The project is presented as a self-contained, first project: the design, analysis and verification of a new frame for a set of selected components. It does not continue, revise, correct or remake anything.

Never write, in text, captions, file names shown, figure labels, tables or comments:
- "rev A", "rev B", "revision B", "v03-B", "v04-B", "rev 2/3/4" as project versions, "remake", "rework", "rebuild", "redo", "previous version", "earlier project", "original design", "February";
- anything about an old report, an old spreadsheet, an audit, corrected theory, wrong components, a BOM error, order history or purchase dates (journal Section 9 audit findings, the "Corrections to the old report's theory" paragraph, theory doc 5.2 "The old spreadsheet's error" and any sentence that compares with them are excluded entirely);
- the name of any company the report may be sent to, any job opening or application;
- chats, assistants, accounts, "main chat", "set-up chat", the two-role workflow, PRs, build log item numbers;
- internal IDs: D-xxx, F-xxx, N-xx-xx, A-xxx, L-xxx, Q-xx, R-xx, DV-xx, H1 to H4, TH, TH04, G0 to G7, T-1 to T-7, C-1 to C-9, K1 to K12, job names (TH_r4b_i30_final, TO_v04B_r4_H4) and script names in running text.

Use instead (extensive report may keep a curated, renumbered log in an appendix):

| Internal | Report wording |
|---|---|
| v04-B revision 1 to 4 | "design-space iteration 1 to 4" (extensive only); compact: "the design space was iterated as verification exposed issues" |
| H4 (rev 4) | "the production optimisation run" |
| TH, TH_r4b_i30_final | "the thresholded verification model", "the final thresholded check" |
| G0 to G5 gates | "geometry checks at export" (named by what they check: file identity, Boolean bookkeeping, face quality, tangency, test meshing, clearances) |
| T-1 to T-7 | "print-geometry checks" (named by what they check) |
| K1 to K12 | keep-out by name ("FC bay", "antenna channel", "propeller sweep plus 3 mm") |
| D-085 / D-088 rules | "fixed-region connectivity rule", "fixed-region stiffness rule" |
| F-036 / F-037 / F-038 | the antenna boss island, the keel lid boss island, the grey support under the GPS deck |
| R-01 to R-13 | requirements by name; the extensive report may number them R1 to R13 in its own table |
| decisions | "Decision 1 ..." only in the extensive appendix, numbered in the order they appear there |

Components are "the selected components" (T-Motor P1604 3800 KV, Gemfan 3520 three-blade, SpeedyBee F405 AIO 40A, SpeedyBee Nano 2.4 GHz ELRS, Tattu R-Line 850 mAh 4S, Flywoo GOKU GM10 Nano V3). The FlyFishRC Volador VX3.5 carbon frame is the commercial reference frame (benchmark, not a target). Measured values from the built Volador aircraft are "measured on a reference build with the same components".

## 3. Style

- `docs/writing_style_guide.md` in full: banned constructions, headings that name the thing, specifics over adjectives, the three validation passes (layout, language, truth). No em dashes anywhere, including LaTeX source comments (`---` is forbidden too).
- UK English (optimisation, modelling, behaviour, centre, metre).
- Voice: first person singular is allowed sparingly in the compact report for decisions ("I chose ..."); otherwise impersonal, active where possible ("The optimiser removed ...", "The check found ...").
- Theory (extensive report, and short boxes in the compact one): `CLAUDE.md` section 5. Slow, sequenced, from the basic physics or definition upwards; one idea per paragraph; derivations as phrased steps (a sentence, then the equation on its own line, general form before substitution); a small numeric example with project numbers; the consequence for this project stated with its numbers; easily confused concepts separated explicitly.
- Every number traces to journal Section 4 (numbers register) or to `docs/stage6_v04B_H4_report.md`, `docs/stage7_strength_report.md`, the export notes, or a calculation shown in the text. No number from memory. Round consistently: masses to 0.01 g, frequencies to 0.1 Hz, stresses to 0.01 MPa, volumes to 0.1 mm^3, percentages to one decimal unless the source shows more meaning.
- Shortfalls are stated plainly inside normal sentences, with the first-principles reason and the next step: take-off mass about 289 g against the 250 g target (frame 89.22 g against the 61.4 g frame budget); vertical capacity ordering not controlled (arm-to-joint failure force ratio 0.95, redesign: prongs as the fuse). No concede-then-recover sentences.
- Units: SI with mm, N, MPa, g, Hz in text; siunitx (`\SI{89.22}{\gram}`, `\SI{417}{\hertz}`).

## 4. Sources (read before writing a section)

| Topic | Source |
|---|---|
| Goals, requirements, decisions, numbers | `docs/journal_quadcopter.md` (Sections 1 to 5, Stage notes in Section 8; not Section 9) |
| Sizing theory (thrust, momentum theory, motor, hover power, endurance, cost of mass, loads) | `docs/stage2_sizing_model_first_principles_rev34.md` (skip 5.2 and any comparison with old documents) |
| Topology optimisation theory | journal Stage 6 notes (minimal supports, theory part 1 and 2, Q&A), `docs/stage6_concepts_explained.md`, `docs/stage6_v04B_checks_explained.md` |
| Optimisation model and runs | `docs/stage6_model_setup_part1.md`, `docs/stage6_model_setup_part2_tosca.md`, `docs/stage6_hpc_*`, `docs/stage6_v04B_G7_report.md`, `docs/stage6_v04B_H4_report.md`, build log (`docs/stage6_build_log_v03B.md`, read only for facts) |
| Design iterations | `docs/stage6_v04B_design_brief.md`, export notes (`stage6_v04B_export_note.md`, `_r3_`, `_r4_`, `_r4_keels_`), `stage6_v04B_r3_F17_note.md`, `stage6_v04B_r4_keel_note.md` |
| Strength and capacity | `docs/stage7_brief.md`, `docs/stage7_strength_report.md`, `docs/stage7_data/` |
| Retainers | `docs/retainer_rx_cradle_note.md`, `docs/retainer_gps_cap_note.md`, `docs/stage6_v04B_r3_F17_note.md` (antenna holder) |

## 5. LaTeX conventions

- `report/common/`: `preamble.tex` (class options, packages, colours, siunitx, headings), `macros.tex`, `references.bib`. Both reports `\input` them. `report/make_overleaf.sh` builds `report/dist/extensive_overleaf.zip` and `report/dist/compact_overleaf.zip`, each self-contained (common files and figures copied in), for upload to Overleaf ("New project, upload project").
- Class: `scrreprt` (extensive, chapters) and `scrartcl` (compact, sections), A4, 11 pt, pdfLaTeX, `lmodern` + `microtype`; figures in `report/figures/` (PDF for plots, PNG at 300 dpi for renders), referenced by file name only.
- One `.tex` file per chapter (extensive: `report/extensive/chapters/NN_name.tex`; compact: `report/compact/sections/NN_name.tex`). Labels `fig:`, `tab:`, `eq:`, `sec:` with the chapter file stem as prefix (`fig:topopt-history`).
- Equations: `equation`/`align`, each derivation step on its own line with a sentence before it. Symbols defined at first use and in the nomenclature table (extensive).
- Tables: `booktabs`, no vertical rules. Captions say what is shown and the key reading in one or two sentences.
- No `\\` for spacing, no manual page breaks except before appendices. ASCII only in the source (`\textdegree`, `\times`, `\approx`).

## 6. Who writes what (extensive report)

| No. | Chapter | Writer | Main sources |
|---|---|---|---|
| 1 | Introduction: goals, components, reference frame, report map | main | journal Section 1 goals, Section 2 |
| 2 | Requirements | main | journal Stage 1 |
| 3 | Sizing from first principles | main | theory doc chapters 0 to 6 |
| 4 | Loads | main | theory doc chapter 7, journal Stage 4 |
| 5 | Material selection | main | journal Stage 5 |
| 6 | Architecture, joint and design space | main | journal Stage 3, Stage 6 joint notes, design brief |
| 7 | Topology optimisation theory | main | journal Stage 6 theory, concepts explained |
| 8 | Optimisation model, solver set-up and runs | **set-up** | model set-up docs, HPC reports, G7 report, H4 report |
| 9 | Design iterations driven by verification | main | F17 note, export notes, keel notes |
| 10 | Thresholded verification and print geometry | **set-up** | H4 report, build log items on TH, restoration, T-checks |
| 11 | Strength and capacity | **set-up** writes the method and results (11.1 to 11.3); main writes the capacity reasoning (11.4) | Stage 7 brief and report |
| 12 | Retainers and integration | main | retainer notes |
| 13 | Results, limitations and future work | main | all |
| A | Decision log (curated, renumbered), numbers, assumptions | main | journal Sections 3 to 5 |
| B | Scripts and workflow (described, no links) | main + set-up paragraph for its scripts | repo |

Set-up chat chapters: write them as LaTeX into `report/extensive/chapters/08_optimisation_model.tex`, `10_verification.tex`, `11_strength.tex` (sections 11.1 to 11.3), with figures into `report/figures/` (prefix `su_`) and a short list of the numbers used with their source line, one PR per chapter. Same framing and style rules; the main chat edits for one voice.

## 7. Compact report outline (main chat)

1. Summary: what was designed, the method chain, key results (frame 89.22 g, first elastic mode 431.0 Hz against the 417 Hz target, strength margin about 25 x, shortfalls stated), cover render.
2. Requirements and approach.
3. Sizing and loads from first principles (one page, one figure).
4. Material (merit index, anisotropy, design values).
5. Architecture and design space (true X, bolted arms, fixed and design regions, keep-outs).
6. Topology optimisation (formulation: minimum volume under frequency and compliance constraints; model; production run history; result).
7. Verification-driven design iterations (islands, connectivity and stiffness rules, keels under the GPS deck).
8. Strength and capacity (checks, results, the capacity finding and the joint redesign).
9. Integration and manufacture (retainers, print geometry, print checks, print orientation, mass breakdown).
10. Results, lessons and next steps (includes the one-line pointer to the full report).

## 8. Figures

Renders (main chat, Blender Cycles, matte dark-grey PET-CF, TPU orange, white background, soft shadows; components as detailed representative models from datasheet dimensions): R1 full printed assembly (cover), R2 exploded view, R3 design space over the optimised tub and arm, R4 arm and joint close-up, R5 rear underside (keels, antenna spine and holder, GPS deck), R6 fixed regions in colour on the optimised parts.
Plots (main chat, one style, vector PDF, from CSV in the repo): optimisation history, mass and endurance sizing plots, material merit chart, verification comparison of the keel variants, Stage 7 utilisation summary.
Set-up figures: see `docs/report_figures_setup.md` (inventory from the set-up chat).
Photos of the printed parts: optional, added only if they arrive before sending.
