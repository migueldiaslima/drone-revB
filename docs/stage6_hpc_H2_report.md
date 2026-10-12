# Stage 6: HPC run H2 (stopped by D-066) and H3 interim, report

For the main chat. Set-up chat, 2026-10-10 morning. Full record: `claude/stage6_build_log_v03B.md` (Phase H items 7 to 12, DV-19 to DV-21, F-15). Items still to come are marked "pending".

## Result

- **H2 stopped at cycle 10 by the D-066 rule** (modes 8, 9 and 10 at 417 to 420 Hz with their peak region mostly in elements below density 0.3, at the arm tips). Not converged; constraints violated at the stop (f7 407 Hz, LC3a SE 1.24 x cap).
- **H3 (1.0 mm, member size 2.5 mm) was started on nexus before this review** (DV-21, Miguel: deadline). At cycle 32 it is near-feasible and still converging: design volume 31,208 mm^3, f7 = 417.6 Hz, SE / cap 0.97 / 0.96 / 0.97 / 1.01.
- **Mass: the design is about three times the B allowance.** 31,208 mm^3 x 1.30 g/cm^3 = 40.6 g of density-weighted design material against about 13 g (Q-53): printed frame about 72 g against 44.6 g, AUW about 278 g against R-01 (< 250 g). The 417 Hz goal and R-01 are not compatible in this design space. D-035 provides the next step (relax towards 290 Hz; 290 / 350 / 417 Hz sweep).

## Runs and machines

| Run | Machine | Mesh | Settings | State |
|---|---|---|---|---|
| H2 | nemix, Abaqus/Tosca 2025 | 2.5 / 1.5 mm, 149,305 el. | D-065; 32 cores thread mode, memory 90 % (DV-19); every cycle saved (DV-20) | stopped by the watcher at cycle 10 (00:46 to 01:28, about 3.8 min per cycle); 11 GB |
| H3 ref | nexus (2 x EPYC 7513, 64 cores, 251 GB), Abaqus 2024 | 1.0 mm, 723,474 el., 3.19 M variables | 64 threads | done, 671 s, peak 80 GB |
| S24 | nexus, Tosca 2024 | H1 files | 64 threads, 2 cycles | PASS: identical to H1; Tosca 2024 accepts inertia relief |
| H3 | nexus, Tosca 2024 | 1.0 mm | H3 caps, member size 2.5 mm (MIN_MEMBER), max 60 cycles, save last + every 10; 54 cores, threads, memory 80 %; run in `/tmp` (root disk) | running: cycle 32 at 10:09, about 14 min per cycle |

F-15: Abaqus 2025 refuses adjoint sensitivities with inertia relief (and with the eigenvalue step) in MPI mode; at 32 cores across two sockets it chose MPI. `mp_mode=threads` in the `.par` solver arguments fixes it (the `optimization` command line rejects `mp_mode`).

## H3 reference (1.0 mm) and caps

| Quantity | 1.0 mm | 2.5 / 1.5 mm | Difference |
|---|---|---|---|
| Mass | 333.69 g | 333.70 g | 0.00 % |
| f7 to f12 (Hz) | 486.66 / 517.87 / 520.97 / 568.67 / 673.31 / 742.66 | 489.93 / 521.51 / 524.32 / 573.63 / 681.81 / 749.44 | -0.6 to -1.3 % |
| ALLSE LC1 / LC2a / LC2b / LC3a (N mm) | 0.0919015 / 0.0709504 / 0.0461905 / 0.106569 | 0.090893 / 0.069877 / 0.045459 / 0.10466 | +1.1 to +1.8 % |
| H3 caps (2 x ALLSE, D-063) | 0.183803 / 0.141901 / 0.0923811 / 0.213138 | | |
| Support reactions | below 3.7e-10 N | below 1.5e-11 N | |

The solid design is mesh-converged at 2.5 / 1.5 mm within about 1 % in frequency and 2 % in strain energy.

## H2 history

| Cycle | Volume (mm^3) | f7 | f8 | f9 | f10 | f11 | f12 (Hz) | SE / cap LC1 | LC2a | LC2b | LC3a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 74,740 | 489.9 | 521.5 | 524.3 | 573.6 | 681.8 | 749.4 | 0.50 | 0.50 | 0.50 | 0.50 |
| 2 | 65,479 | 437.2 | 461.8 | 465.6 | 504.9 | 588.0 | 663.5 | 0.63 | 0.65 | 0.65 | 0.68 |
| 4 | 55,789 | 425.1 | 429.0 | 443.9 | 451.0 | 504.4 | 590.6 | 0.74 | 0.81 | 0.83 | 0.91 |
| 6 | 47,481 | 421.3 | 422.8 | 424.0 | 438.0 | 497.5 | 560.8 | 0.83 | 0.92 | 0.89 | 0.97 |
| 8 | 41,153 | 419.0 | 421.1 | 422.8 | 433.0 | 479.3 | 531.0 | 0.92 | 0.97 | 0.95 | 1.07 |
| 10 | 36,771 | 407.3 | 417.0 | 418.2 | 419.7 | 456.3 | 486.3 | 1.02 | 1.01 | 1.02 | 1.24 |
| 11 | 34,998 | 397.8 | 406.4 | 419.1 | 424.7 | 444.0 | 500.0 | 1.04 | 1.00 | 1.03 | 1.32 |

## D-066 item 2: mode check

Method (`h2_modecheck.py`, run by the watcher on the saved odb): peak region of a mode = nodes with |U| >= 0.8 max|U|; spurious if more than half of those nodes touch only elements of density below 0.3.

| Cycle | Elements below 0.3 | Result |
|---|---|---|
| 0 | 0 | all modes in solid material |
| 5 | 42 | all ok (mean density in the peak regions 0.79 to 1.00) |
| 10 | 32,425 | **modes 8, 9, 10 flagged** (417.0 / 418.2 / 419.7 Hz): share of peak nodes below 0.3 = 0.69 / 0.56 / 0.61, mean density 0.34 / 0.45 / 0.42, maxima at the arm tips (about +-58, +-58, 0); modes 7, 11, 12 ok (battery plate edge, x = -50, y = 10) |

Reading of the cycle 10 flag: the flagged modes are the arm bending modes (maxima at the motor seats), not void-region modes at low frequency. They sit exactly on the 417 Hz bound with the outer arm already grey. This is the C-3 concern itself: the frequency constraint is being met with grey arm material. Whether grey arms are overcredited is answered by item 3 (thresholded frequency job), which needs a finished design: pending, on H3.

### H3 saved cycles (`cyclecheck.py`, run on nexus during H3)

| Cycle | Elements below 0.3 | Modes flagged | Detail |
|---|---|---|---|
| 10 | 47,146 | none | peak regions at the arm tips, mean density 0.63 to 0.68, share below 0.3 0.01 |
| 20 | 261,847 | 9, 10 (388.4 / 405.1 Hz) | arm modes, share 0.64 / 0.75, mean density 0.37 / 0.28; modes 7, 8, 11, 12 are battery-plate-edge modes (x = -50, y = +-10, z = 24) in solid material |
| 30 | 239,454 | **all six** (417.8 / 431.5 / 433.1 / 437.1 / 498.4 / 539.0 Hz) | every mode peaks at an arm tip, share of peak nodes below 0.3 = 0.66 to 0.81, mean density 0.20 to 0.34 |

Support reactions (now found: 4 node values per step): below 9.8e-10 N in every step of cycles 10, 20, 30.

Reading: by the D-066 rule H3 would have been stopped at cycle 20. With member size on and the 1.0 mm mesh the outcome is the same as H2, only clearer: the converged design meets 417 Hz with the outer arms in grey material (density about 0.2 to 0.35). Material at that density is not printable, and an iso 0.3 cut would leave the outer arms thin or broken. The frequencies Tosca credits to the arms are therefore not those of a printable part; D-066 item 3 would quantify the gap, but the mode check alone already shows the 417 Hz arm frequencies rest on grey material.

Support reaction check in the watcher printed 0 N because the Tosca odb flattens the model into one instance (`PART-1-1`) and the assembly sets were not found; corrected in `cyclecheck.py` for the H3 checks.

## H3 history (running)

| Cycle | Volume (mm^3) | f7 | f8 | f9 | f10 | f11 | f12 (Hz) | SE / cap LC1 | LC2a | LC2b | LC3a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 74,493 | 486.7 | 517.9 | 521.0 | 568.7 | 673.3 | 742.7 | 0.50 | 0.50 | 0.50 | 0.50 |
| 5 | 61,896 | 424.3 | 449.1 | 452.0 | 485.9 | 568.8 | 633.6 | 0.70 | 0.70 | 0.70 | 0.72 |
| 10 | 43,047 | 421.2 | 422.3 | 429.9 | 439.6 | 491.5 | 541.6 | 0.94 | 0.96 | 0.95 | 0.98 |
| 15 | 31,990 | 392.3 | 415.9 | 416.4 | 423.9 | 445.9 | 488.0 | 1.03 | 1.01 | 1.05 | 1.37 |
| 18 | 28,430 | 341.2 | 387.1 | 400.0 | 407.5 | 418.4 | 448.6 | 1.15 | 1.08 | 1.25 | 1.89 |
| 20 | 27,159 | 342.9 | 369.3 | 388.4 | 405.1 | 405.9 | 438.4 | 1.19 | 1.11 | 1.27 | 1.98 |
| 25 | 29,594 | 405.2 | 406.8 | 417.3 | 420.5 | 459.2 | 481.6 | 1.03 | 1.01 | 1.02 | 1.48 |
| 28 | 32,105 | 417.4 | 431.0 | 431.7 | 435.2 | 495.1 | 537.1 | 0.97 | 0.95 | 0.95 | 1.05 |
| 30 | 31,822 | 417.8 | 431.5 | 433.1 | 437.1 | 498.4 | 539.0 | 0.96 | 0.94 | 0.95 | 1.00 |
| 32 | 31,208 | 417.6 | 428.0 | 430.7 | 432.7 | 493.2 | 532.6 | 0.97 | 0.96 | 0.97 | 1.01 |

- Cycles 13 to 20: Tosca overshot (volume to 27,159 mm^3, f7 down to 341 Hz, LC3a up to 2 x cap), then restored material; from cycle 29 all constraints are within about 1 % of feasibility and the volume falls slowly (about -0.8 % per cycle).
- Active constraints at cycle 32: f7 (417.6 Hz), LC3a (1.01), and close behind LC1 / LC2a / LC2b (0.96 to 0.97). The design is stiffness- and frequency-limited together.
- Expected end: 60 cycles about 16:45, earlier if Tosca's stop criteria are met.

## Mass against the B allowance (Q-53)

| Item | Value |
|---|---|
| H3 cycle 32, density-weighted design volume | 31,208 mm^3 = 40.6 g |
| B allowance for design material | about 13 g (about 10,000 mm^3) |
| Printed frame B (31.6 g fixed + design) | about 72 g against 44.6 g |
| AUW | about 278 g against R-01 < 250 g |

Iso masses from `cyclecheck.py` (H3 saved cycles). The script's 'design' sum covers every solid element, fixed regions included (24,353 mm^3 = 31.7 g, matching the 31.6 g fixed mass of Q-53); design-only values below subtract it and agree with Tosca's R_VOL within 0.1 %.

| Cycle | Design, density-weighted | Design at iso 0.3 | Design at iso 0.5 | Printed frame at iso 0.5 (fixed + design) |
|---|---|---|---|---|
| 10 | 43,050 mm^3, 56.0 g | 63,443 mm^3, 82.5 g | 46,540 mm^3, 60.5 g | 92.2 g |
| 20 | 27,182 mm^3, 35.3 g | 34,075 mm^3, 44.3 g | 28,926 mm^3, 37.6 g | 69.3 g |
| 30 | 31,841 mm^3, 41.4 g | 37,619 mm^3, 48.9 g | 33,047 mm^3, 43.0 g | 74.6 g |

At cycle 30 the printed frame at iso 0.5 is about 74.6 g against 44.6 g: AUW about 280 g.

## Pending

1. D-066 item 1 (documentation on frequency interpolation).
2. D-066 item 3: thresholded frequency job (not yet built: the Tosca odb renumbers the flattened model, so removing elements from the CAE input needs a label map; the alternative is editing Tosca's density-group materials in its working input). Lower priority given items above.
4. Density screenshots (iso 0.3 / 0.5, three views) of the final H3 design.

## Decisions for the main chat

1. **H2:** accept the stop at cycle 10 as the D-066 outcome; H2 is not continued (H3 supersedes it as the shape run).
2. **Mass / R-01 (D-035):** at 417 Hz the optimum design material is about 40 g against about 13 g. Options: (a) relax the frequency bound (D-035 sweep 350 / 290 Hz); (b) accept an AUW above 250 g; (c) revisit the frame concept (design C, D-053). For (a), a 2.5 / 1.5 mm run takes about 1 to 1.5 h on nexus at 64 cores and about 2.5 h on nemix, so the sweep can run today in parallel on both machines; a 1.0 mm production run then takes about 8 to 14 h.
3. **H3:** by the D-066 rule it should stop (flagged from cycle 20, all six modes at cycle 30). Recommend stopping it now; cycles 0, 10, 20, 30, 32 are saved.
4. **Formulation for the next runs (C-3):** the arms keep converging to grey material under the frequency constraint, with and without member size. Options to decide with the sweep: a stronger penalty for the frequency responses (or forcing SIMP / RAMP instead of the default interpolation), Tosca's discrete (0/1) density update ('Aggressive' or a projection setting), or a minimum-density / void-element rule for the arm region.
