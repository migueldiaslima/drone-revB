# Stage 7: strength check of the print geometry (route A), report

From the set-up chat, 2026-10-14. Brief: `docs/stage7_brief.md` (main chat, D-089, D-090, F-040). Record: build log items 66 to 69. Raw outputs: `docs/stage7_data/stress_TH_r4b_i30_final.txt`, `docs/stage7_data/capacity_r4_iso030.txt`.

## Result

| Check | Result |
|---|---|
| Strength, LC1 / LC2a / LC2b / LC3a, every part, three criteria | PASS: largest volume-weighted P99.9 utilisation 0.04 (LID, LC3a, von Mises); no element above any limit |
| D-050, arm section modulus at the fork exit <= 260 mm^3 | NOT MET: 815.6 mm^3 at the slot end (u 43.74); recorded as a limitation (D-090) |
| Lever-corrected arm-to-joint failure force ratio | 0.95: the arm and the joint fail at about the same vertical tip force; neither is protected |
| D-051, TUB fin-root section modulus >= 390 mm^3 | PASS: 957.2 mm^3 at the root (u 27.0), at least 792.4 mm^3 along the fin to u 33 |

## Model

TH_r4b_i30_final (build log items 64, 65): H4 rev 4 cycle 28 thresholded at iso 0.3, exact keels forced solid, keel cell cleaned, seat tie, 1.0 mm C3D10, 511,770 of 765,252 elements solid, D-045 material, D-064 inertia relief with 3-2-1 supports. The stresses are those of the element-level thresholded body (staircase surfaces), not of the smoothed print surface (route B not done, brief).

`scripts/post/stress_th.py` (items 66, 67): element-average (centroid) stress, solid elements only; per part (TUB, LID, each arm) and step. Elements with a node on one of the 30 tie and coupling surfaces (motor seats, joint, prong and fin bosses, FC, GPS, antenna and battery seats, seat tie) are excluded (78,733 elements, 71,564 solid) and their maxima reported separately. Volume-weighted 99.9th percentile; elements above a limit grouped into edge-connected clusters (pass if below 1 mm^3 and on the surface). The script was tested offline against an independent computation (72 rows, ALL CHECKS PASS).

## Strength

Limits (brief a, b, d): von Mises 36.3 MPa (S_xy 54.4 / 1.5), S33 tension across the layers 15.9 MPa (S_z 23.9 / 1.5), sqrt(S13^2 + S23^2) 15.9 MPa (S_z as shear allowable, assumption). Build direction global +z for every part (TUB floor-down).

Worst step per part and check (P99.9 utilisation and its step; maximum over the checked elements and all four steps):

| Part | von Mises | S33 tension | sqrt(S13^2 + S23^2) | Clusters above a limit |
|---|---|---|---|---|
| TUB | 0.02 (LC3a), 1.60 MPa | 0.01 (LC2a), 0.57 MPa | 0.02 (LC3a), 0.77 MPa | 0 |
| LID | **0.04 (LC3a)**, 2.43 MPa | 0.02 (LC3a), 0.74 MPa | 0.02 (LC3a), 0.57 MPa | 0 |
| ARM_pp | 0.02 (LC2a), 1.47 MPa | 0.01 (LC3a), 0.21 MPa | 0.02 (LC2a), 0.47 MPa | 0 |
| ARM_pm | 0.02 (LC1), 1.36 MPa | 0.01 (LC3a), 0.20 MPa | 0.01 (LC1), 0.43 MPa | 0 |
| ARM_mp | 0.02 (LC1), 1.39 MPa | 0.01 (LC3a), 0.18 MPa | 0.01 (LC1), 0.44 MPa | 0 |
| ARM_mm | 0.02 (LC2a), 1.48 MPa | 0.01 (LC3a), 0.21 MPa | 0.02 (LC2a), 0.47 MPa | 0 |

- Excluded elements (ties and couplings): largest von Mises 2.24 MPa (LID, LC3a) and 2.11 MPa (TUB, LC3a); they would not change the result.
- Governing case: LID in LC3a (landing, battery on the plate), von Mises P99.9 1.42 MPa. Figure `figures/fig_stage7_vm_LC3a.png`: top row on the limit scale, bottom row on the 99.9th percentile scale; the highest values lie in the LID plate and the TUB floor under the battery and FC, and at the arm roots.
- Top ten elements per part and step with coordinates: raw output.
- Reading: the frame is sized by the 417 Hz requirement, not by strength under LC1 to LC3a; the margin on the design loads is about 25 x. This agrees with the Stage 4 estimate (212 N mm arm-root moment at full thrust).

## Capacity ordering (D-050, D-051)

`scripts/post/capacity_r4.py` on the print STLs: sections normal to the pp diagonal, u from the frame centre (confirmed by the main chat), Z = I_h / c_max from the exact section polygons (validated on analytic bars). Positions: motor axis u_m = 74.25 (motor pad centroid in ARM_pp.step 74.24); J3 bolt line u_j = 37.24 (v03 33 mm moved out by D-079; prong boss centroids 37.4 to 37.5); slot end (fork exit) u 43.74 (slot-end semicircle, centre 38.59, radius 5.15; traced on the STL at w 3, 4, 4.5 and 5 mm within 0.03 mm). Nearer the axis the optimiser left an open channel, so material at w = 0 starts only at u 50.

| u (mm) | 43.74 (slot end) | 45 | 47 | 49 | 50 | 51 | 53 | 54 | 55 |
|---|---|---|---|---|---|---|---|---|---|
| Z (mm^3) | **815.6** | 584.2 | 532.2 | 520.2 | 530.4 | 511.2 | 460.1 | 421.8 | 381.4 |

D-050 (Z <= 260 mm^3 at the fork exit): not met at the slot end or anywhere from u 45 to 57 (Z below 260 only beyond about u 57.5).

Lever-corrected (brief 3a): a vertical tip force F at the motor gives M(u) = F (u_m - u), so the arm section that fails first is where Z / (u_m - u) is smallest.

| u (mm) | 45 | 50 | 55 | 57 | 58 | 60 | **61** | 62 | 64 | 66 | 68 | 70 | 72 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Z / (u_m - u) (mm^2) | 19.98 | 21.88 | 19.82 | 17.52 | 12.96 | 10.90 | **9.96** | 9.96 | 13.01 | 17.62 | 20.44 | 32.58 | 44.30 |

Minimum 9.96 mm^2 at u 61 to 62 (Z 131.9 mm^3, lever 13.25 mm), the slim section just inside the motor pad. Failure force ratio:

ratio = S_xy x min[Z / (u_m - u)] x (u_m - u_j) / 21,216 N mm

= 54.4 x 9.96 x 37.00 / 21,216 = **0.95**

The arm would fail at 0.95 times the tip force that fails the joint: by this estimate the arm is marginally the weaker element, but 0.95 is inside the scatter of both estimates (bearing allowable assumed S_xy, A-022; arm in elastic bending at S_xy), so which side fails is not controlled. The 1.5 x ordering of D-050 would need a ratio at or below 0.67. The weakest arm section is near the motor, not at the fork exit, which is why the fork-exit check alone (815.6 mm^3, 3.1 x the limit) overstates how much stronger the arm is.

D-051 (fin root, TUB, cut within abs(w) <= 8 mm): the fin leaves the body corner between u 26.5 and 27.0 (section area 354.5 to 216.3 mm^2). Z = 957.2 mm^3 at u 27.0, minimum 792.4 mm^3 at u 29.5 along the fin to u 33: PASS (at least 2.0 x 390).

## Limitations (brief f)

| Item | Status |
|---|---|
| LC3b, LC4 | not analysed; the ordering above is the design argument, and it is not controlled (ratio 0.95) |
| Five-boss sensitivity (DV-26) | not analysed; seat flatness (D-082 item 1) carries the risk |
| Bolt bearing (A-022) | not analysed; allowable assumed S_xy |
| Fatigue (1P at hover) | not analysed; static stresses at most 2.4 MPa in LC1 to LC3a |
| Route B (smoothed print surface) | not done; element-level stresses |
| T-6 thin areas | slicer check passed; print-quality risk |
| Retainers, skid | outside the model |
