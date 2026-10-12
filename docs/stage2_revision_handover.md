# Stage 2 revision: handover to the main chat

Date: 2026-10-05. Source: a separate revision chat that rebuilt the Stage 2 sizing model from first principles (Chapters 0 to 10) and recomputed every number from the P1604 + 3520 bench table. No design decision changes. The corrections below are wording, rounding and formula fixes, plus one new point for Q-18.

## How to use this file

1. Re-read `claude/journal_quadcopter.md` before editing (your earlier context may be older than the file).
2. Apply the ten corrections in the table below, in order. Each row gives the location, the current text and the replacement.
3. Add the Q-18 point and the open items (sections below) where the journal keeps open questions.
4. Add a changelog line: "Stage 2 revision (2026-10-05): ten corrections from the first-principles revision; see claude/stage2_revision_handover.md."
5. Leave this file in the project as the record of where the corrections came from.

## Corrections

| # | Location in the journal | Current text | Replace with | Why |
|---|---|---|---|---|
| 1 | Register N-02-04, Method column | AUW/4 x (1 + N-02-03) | AUW/4 / (1 - N-02-03) | Exact form of T - F_d = W/4. Value 64.4 g unchanged at f = 3 % |
| 2 | Register N-02-01, Uncertainty column; Stage 2 notes "largest residual over the five test points is 1.4 %" | max residual 1.4 % | max residual 1.5 % (1.46 %, at the 20 % row) | Rounding: fit gives 92.5 g against 91.2 g measured |
| 3 | Register N-02-25, disk loading | 99 | 102 (at 64.4 g hover thrust) | 99 N/m^2 was for 62.5 g without download. Hover induced velocity 6.45 m/s, ideal power 4.1 W per motor |
| 4 | Register N-02-14, Value column; Stage 2 notes "0.330 at 514 g" | 0.265 to 0.330 | 0.265 to 0.331 | Rounding: 91.8 / 277.8 = 0.3306 |
| 5 | Stage 2 notes, Propulsion model paragraph | "All fit the data, but hover ... lies below the lowest point" | "Only M4 fits all five points within about 1 %; M1, M2 and M3 miss the lowest point by 16, 12 and 8 %. Hover ... lies below the lowest point" | M1 -16.3 %, M2 +11.7 %, M3 +7.9 % at the 20 % row |
| 6 | Audit F-002 | "interpolation gives 12.4 to 14.8 W per motor, so the law underestimates hover power by 30 to 40 %" | "interpolation gives 12.4 W per motor at the spreadsheet's 212.8 g (14.8 W at 250 g), so the law (8.8 W per motor) underestimates hover power by about 30 %" | Like-for-like comparison is at 212.8 g only |
| 7 | Register N-02-12, Value column; Stage 2 notes "each millimetre of arm width costs 0.033 min" | -0.033 | -0.035 | Exact 1/(1 - f) download form; 0.0037 per mm in f, thrust +0.39 % per mm, x 1.12 power exponent x 8.15 min |
| 8 | Lesson L-008; Stage 2 notes "1 mm of arm width is worth about 0.9 g of frame mass" | 0.9 g | about 1.0 g (0.96 g) | Follows from #7: 0.035 / 0.036 |
| 9 | Requirement R-08 | about 237 Hz ... about 711 Hz | about 241 Hz ... about 722 Hz | Old values were for 14,200 RPM (62.5 g, no download). Register hover is 14,440 RPM (N-02-06) |
| 10 | Stage 2 notes, F-013 correction bullet "Low pitch and laminar flow" | Reynolds number of about 26,000 | Reynolds number of about 27,000 | At the 64.4 g hover with an assumed 8 mm chord at 0.75 R |

## New point for Q-18 (hover power model)

Both accepted models overpredict the lowest bench point (91.2 g): M3 by 8 %, M2 by 12 %. That point is the closest to hover. If the bias continues to hover, the 18.3 W central value (N-02-07) is conservative, true hover power may be about 15 to 18 W per motor, and the endurance (N-02-10) is more likely in the upper half of its 6.6 to 9.0 min band. This does not rescue M4, which is rejected for a physical reason (negative constant loss, efficiency rising at light load).

## Open items found in the revision

| Item | Affects | How to close |
|---|---|---|
| Hover power is extrapolated (A-003) | N-02-07, N-02-10 | Hover with a current log (Blackbox or meter); measured power replaces the model. Largest single gain in certainty |
| Pack internal resistance (A-004) | N-02-19, sagged top speed | Charger or tester with an IR function |
| Drag areas (A-013) | N-02-21, N-02-22 | Stage 3 projected areas |
| Thrust against forward speed (A-014) | N-02-21 | Propeller data against airspeed, or full-throttle flight with GPS speed |
| Motor spin-up time | Dynamic factor for thrust steps (estimated about 1, bound 1.03) | Blackbox log of a punch-out |
| Blade chord at 0.75 R (assumed 8 mm) | Reynolds numbers only | Measure a blade |
| Frame damping (assumed 0.02 to 0.05) | Resonant amplification 10 to 25 | Tap test or Blackbox gyro FFT on the built frame |

Two Stage 4 inputs the revision added that the register does not yet hold (add as new N-02 entries if wanted):

- Inertial force on the battery mount at n_z = 8.2: 8.1 N (100 g battery).
- Arm root bending moment at maximum thrust: 0.40 N m with an assumed 80 mm arm (Stage 3 sets the length); about 20 % conservative because the motor's own inertia (0.94 N) relieves the arm.

## Reference material

- Revision document (Chapters 0 to 10, appendices, references): https://claude.ai/code/artifact/afdb9982-8b85-415b-a50d-37df14156189
- Propeller Inflow Explorer (interactive, section 8.5): https://claude.ai/artifact/WHp9dq1HRSok2n6t88CjQT

Both are private to Miguel's account; the main chat can read them by link with the Artifact or Docs tools.
