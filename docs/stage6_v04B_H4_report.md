# Stage 6: v04-B revision 4, H4 and the print set, report

From the set-up chat, 2026-10-13. Full record: `docs/stage6_build_log_v03B.md` items 48 to 65, DV-26 to DV-28. Inputs: `geometry/v04B_r4/` (export note `stage6_v04B_r4_export_note.md`), `geometry/v04B_r4_keels/` (export note `stage6_v04B_r4_keels_export_note.md`), journal v0.56 (D-086, D-087, D-088, F-038, N-06-20 to N-06-22).

## Result

| Check | Result |
|---|---|
| G6 CAE mesh (1.0 mm) | PASS: 765,252 C3D10 (TUB 391,649, LID 51,191, ARM 4 x 80,603), warnings 0.02 % or less |
| G7b reference job (full density, seat tie) | PASS: modes 7 to 12 = 448.70 to 648.71 Hz; mass 332.182 g (+0.007 %) |
| H4 rev 4 | converged at cycle 28 (Tosca stop criteria), volume -55.4 % |
| T-4 on the print geometry (iso 0.3, exact keels A + B, keel cell cleaned) | **PASS**: f7 431.0 Hz, SE/cap at most 0.91 |
| T-5 restoration | PASS: one piece per part |
| T-6 wall thickness | TUB within the limits (ray method); LID and ARM_pp above the limits by measure; slicer check of all parts passed (Miguel) |
| T-7 assembly clash | PASS: largest overlap 0.215 mm^3 (meshing noise), parts against each other 0.000 mm^3 |
| Print set (iso 0.3) | frame 89.22 g: TUB 47.21, LID 6.61, ARM_pp 8.85 g (x 4) |

## Model and reference job

- V1r4 (item 49): every cell and surface matched the export (TUB design / fixed 39,538.45 / 12,796.26 mm^3, LID 2,356.98 / 3,417.08 mm^3, S_RIM_UNDER_LID 363.23 mm^2, S_BATT_SEAT 1,056.00 mm^2, S_GPS_SEAT 209.19 mm^2 on the TUB), point masses 199.58 g, arm gaps 0.150 mm.
- G7b_r4_ref (item 49): modes 1 to 6 below 0.002 Hz; modes 7 to 10 arms 448.70 / 465.11 / 476.51 / 483.41 Hz, mode 11 lid plate 569.85 Hz, mode 12 lid tab 648.71 Hz; GPS deck (now on the TUB) at mode 14, 836.85 Hz; reactions below 8.7e-11 N.
- Deviation DV-26: no lid pad circles, so no five-boss model (G7a and its TH deferred to Stage 7, D-082 item 3).

## H4 run

TO_v04B_r4_H4 on nexus (item 50): minimise volume, modes 7 to 12 at least 417 Hz, SE of each load case at most 2.0 x cycle 0, member size 2.5 mm on DESIGN_ALL, Lanczos shift DV-24, 60 threads. Started 02:15, stopped by Tosca after cycle 28 at 09:49 (7 h 34 min, about 15.5 min per cycle).

| Quantity | Cycle 0 | Cycle 28 |
|---|---|---|
| Design volume | 74,242 mm^3 | 33,100 mm^3 (-55.4 %) |
| f7 / f8 / f9 / f10 / f11 / f12 | (full density) | 416.7 / 417.2 / 418.4 / 423.7 / 461.7 / 496.5 Hz |
| ALLSE LC1 / LC2a / LC2b / LC3a | 0.1095564 / 0.1022435 / 0.0520785 / 0.2020444 N mm | 1.58 / 1.40 / 1.60 / 2.02 x cycle 0 |

- History: f7 constraint active from cycle 4; LC3a rising from cycle 13; an overshoot at cycles 15 to 22 (f7 down to 325.1 Hz at cycle 15, LC3a up to 2.12 x cycle 0 at cycles 17 to 19), recovered from cycle 23.
- At Tosca's stop f7 is 0.3 Hz under 417 and LC3a 1 % over its cap (revision 2: 0.6 Hz and 5 %). Both are judged on the thresholded model (T-4), not on the grey one.
- cyclecheck cycle 28: modes 7 to 10 arm bending with peaks at the motor seats; mode 11 at the GPS deck rear corner and mode 12 at the keel rear underside, both in a region of mean density about 0.5 (the deck is fixed, the keel under it grey).

## The GPS deck support (F-038) and the keel fix

- TH at iso 0.4 failed (item 51): mode 7 at 146.8 Hz at the GPS deck, LC3a 1.20 x cap. At iso 0.3 the same mode is 162.3 Hz (item 52).
- Cause (item 52, figures `fig_r4_deck_sections.png`, `fig_r4_deck_long.png`): at any threshold from 0.3 to 0.5 the keel between the deck underside (z 21.5) and the antenna spine (z 0 to 10) is empty over the whole deck length; the deck hangs from two thin straps at y about +-9 near the rear wall. In Tosca the same volume held a grey block (mean density 0.5) that carried the deck at 461.7 Hz. The island check (connectivity, D-085) passed; what was missing was stiffness, which led to D-088.
- Variants on cycle 28 without a new optimisation (items 53 and 58; figures `fig_r4_keel_variants_3d.png`, `fig_r4_keel_variants_sections.png`):

| Variant | Mass g | f7 (Hz) | f12 (Hz) | LC3a SE/cap | Result |
|---|---|---|---|---|---|
| L: local iso 0.15 in the keel box | 281.5 | 380.6 | | 0.99 | FAIL |
| S: two side webs forced solid | 283.4 | 430.7 | 553.0 | 0.93 | PASS |
| cA: keel A, keel zone cleaned | 282.2 | 420.7 | 458.5 | 0.95 | PASS |
| cB: keel B, keel zone cleaned | 281.1 | 7.8 | 55.7 | 28.05 | FAIL |
| cAB: keels A + B, keel zone cleaned | 282.3 | 428.4 | 529.6 | 0.94 | PASS |

- cAB was chosen (D-087): it meets every requirement with 1.1 g less than S at about the same margins. The main chat exported A and B as exact solids (N-06-22, deviations D1 to D5 from the TH shapes).

## Print set

Restoration (D-044, `scripts/post/restore_r4.py`, items 59 to 63): the iso surface of cycle 28 (marching tetrahedra, 6 Taubin iterations) joined with the exact fixed solids and keels from the STEP files.

- Print level iso 0.3 (Miguel, item 63), chosen over 0.4 for margin at the LID front openings and under the motor pads.
- Deviation DV-27: the keel zone is cleaned with the keel design cell of TUB.step (x -54 to -23, abs(y) <= 11, z -2.0 to 21.5) instead of the D-087 box (abs(y) <= 9, z 0 to 21.5), which left 34.1 mm^3 of 0.15 to 0.2 mm skins on the cell faces (item 62, found by Miguel in Fusion).
- Item 62 also removed zero-thickness flaps from coincident faces: the iso surface is now cut by the envelope before the exact solids are added, and the written mesh is cleaned (back-to-back and degenerate triangles, sheets up to 1 mm^3).
- Deviation DV-28: fillet pass B of D-081 not applied (Miguel).

| Part | Iso 0.4 (item 62) | Iso 0.3 (item 63) | Pieces | Dropped loose pieces |
|---|---|---|---|---|
| TUB | 35,218.3 mm^3 = 45.78 g | 36,318.1 mm^3 = 47.21 g | 1 | 0.213, 0.188, 0.017 mm^3 inside the tub |
| LID | 4,950.0 mm^3 = 6.43 g | 5,087.6 mm^3 = 6.61 g | 1 | 0.003 mm^3 |
| ARM_pp | 6,434.5 mm^3 = 8.36 g (item 60) | 6,811.1 mm^3 = 8.85 g | 1 | none |
| Frame (TUB + LID + 4 x ARM_pp) | 85.65 g | **89.22 g** | | |

Density 1.30e-3 g/mm^3 (PET-CF). Frame iso 0.3 against 0.4: +3.57 g, of which the four arms +1.96 g.

## T-4 on the print geometry

TH_r4b_i30_final (items 64 and 65): cycle 28 cut at iso 0.3; TUB elements with the centroid inside the exact keel STLs forced solid (10,549 elements, 1,399.6 mm^3 against 1,400.5 mm^3 expected, -0.1 %); TUB design elements in the keel cell outside the keels set to air (205.7 mm^3); fixed elements always solid; solid stiffness and mass factor 1, air 1e-6 and 1e-9; seat tie; Lanczos shift DV-24. The selection rule was tested offline against an independent method before the run (`scripts/hpc/TH04/test_final/`).

| Model | Mass g | f7 | f8 | f9 | f10 | f11 | f12 (Hz) | SE/cap LC1 | LC2a | LC2b | LC3a | Result |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Tosca cycle 28 (grey) | - | 416.7 | 417.2 | 418.4 | 423.7 | 461.7 | 496.5 | 0.79 | 0.70 | 0.80 | 1.01 | - |
| TH_r4b (iso 0.4, no keels) | 281.3 | 146.8 | 428.3 | 432.1 | 436.5 | 440.1 | 494.9 | 0.78 | 0.67 | 0.78 | 1.20 | FAIL |
| TH_r4b_cAB (iso 0.4, keel shapes, box) | 282.3 | 428.4 | 430.2 | 434.8 | 437.8 | 455.6 | 529.6 | 0.72 | 0.65 | 0.75 | 0.94 | PASS |
| **TH_r4b_i30_final** (iso 0.3, exact keels, keel cell) | 283.5 | **431.0** | 432.5 | 437.2 | 441.4 | 457.2 | 533.4 | 0.70 | 0.64 | 0.73 | **0.91** | **PASS** |

- Mass is the whole model at element level including the 205.4 g point masses; it is not the print mass.
- Support reactions below 2.2e-9 N.
- f7 is 3.4 % above Tosca's grey value; all four compliances are below Tosca's. As in every TH of this project, the thresholded part is stiffer than the grey model predicts.
- Mode peaks: modes 8 and 10 at the motor seats (arm bending); modes 7, 9, 11 and 12 at (-54, -9, 0), the rear lower corner of the antenna spine (fixed geometry). The same pattern was seen in cA and cAB (item 58). Four modes interleaved with the arm modes and within 10 Hz of each other read as coupled global modes in which the spine tail has the largest amplitude, not as a local spine mode; not checked further, since all six modes pass.

## Post-run checks T-1 to T-7

| # | Check | Result |
|---|---|---|
| T-1 | Freeze the final cycle | `c28.odb`, `TO_v04B_r4_H4-Job.inp`, `tosca_distribution.inp` in /tmp/mdias_H4r4/TH; SAVE.inp has every cycle. Open: /tmp is not permanent (below) |
| T-2 | Separation | 259,292 of 765,252 elements below 0.3 (33.9 %); kept volume at iso 0.3 / 0.5 63,912 / 61,947 mm^3 = 83.1 / 80.5 g, so 1,965 mm^3 (2.6 g) between 0.3 and 0.5 (item 50; element level, fixed included). Counts per band 0.3 to 0.5 and at or above 0.5 not extracted |
| T-3 | Iso surfaces (marching tetrahedra, 6 Taubin iterations) | closed; TUB 34,772.6 / 36,151.4 mm^3, LID 4,987.0 / 5,123.8, ARM_pp 6,498.5 / 6,884.9 at iso 0.4 / 0.3 (before restoration) |
| T-4 | TH on the print geometry | PASS (above) |
| T-5 | Restoration | PASS, one piece per part (above) |
| T-6 | Wall thickness, both methods | below; slicer check passed |
| T-7 | Clash against the 45 keep-out solids and between parts | PASS; largest 0.215 mm^3 (TUB, keep-out solid 37), parts 0.000 mm^3 |

T-6, iso 0.3 print set (item 63; maps `figures/fig_t6_r4_iso030_{TUB,LID,ARM_pp}.png`). Brief limits: surface below 0.8 mm at most 1 %, below 1.2 mm at most 3 %.

| Part | Ray, surface below 0.8 / 1.2 mm | Sphere, surface below 0.8 / 1.2 mm | Sphere, volume below 0.8 / 1.2 mm | Ray median |
|---|---|---|---|---|
| TUB | 0.95 / 2.27 % | 0.39 / 3.25 % | 0.06 / 0.54 % | 3.45 mm |
| LID | 1.33 / 2.94 % | 2.58 / 7.48 % | 0.32 / 1.17 % | 2.52 mm |
| ARM_pp | 2.05 / 3.52 % | 5.47 / 12.17 % | 0.50 / 1.33 % | 4.98 mm |

- The sphere method gives zero thickness at every sharp convex edge, and the print set carries the exact fixed geometry with sharp edges (holes, rims, bosses, pads), so its surface shares are upper bounds; the ray method is the better measure here (item 61).
- Remaining thin areas (ray below 0.8 mm): TUB fin roots and floor edge at z about -2; LID front openings (x 22 to 26, y +-2 to +-6); ARM_pp prong ends and motor pad rim.
- The slicer preview of all three parts showed no dropped walls (Miguel, 2026-10-13), which is the practical acceptance for these areas.

## Deviations

| ID | Deviation |
|---|---|
| DV-26 | No lid pad circles in V1r4, no G7a or five-boss TH; deferred to Stage 7 (D-082 item 3) |
| DV-27 | Keel zone cleaned with the keel design cell instead of the D-087 box |
| DV-28 | Fillet pass B of D-081 not applied |

## For the main chat

Proposed for the journal (numbers register IDs to be assigned by the main chat):

1. Print level iso 0.3 (Miguel) and DV-27, DV-28 (notes against D-087 and D-081).
2. Print set iso 0.3: TUB 36,318.1 mm^3 = 47.21 g, LID 5,087.6 mm^3 = 6.61 g, ARM_pp 6,811.1 mm^3 = 8.85 g, frame 89.22 g (item 63).
3. T-4 on the print geometry: TH_r4b_i30_final f7 to f12 431.0 / 432.5 / 437.2 / 441.4 / 457.2 / 533.4 Hz, SE/cap 0.70 / 0.64 / 0.73 / 0.91, PASS (item 65).
4. T-6 iso 0.3 (table above) and the slicer acceptance.
5. Stage 6 post-processing complete; open items below.

## Open

| Item | Owner |
|---|---|
| T-1: /tmp on nexus is not permanent. Copy `TO_v04B_r4_H4-Job.inp`, `tosca_distribution.inp` and the restoration inputs (`mt_c28_*_030.stl`) to the laptop with Bitvise; `c28.odb` (3.0 GB) only if space allows | Miguel |
| T-2 counts per density band (0.3 to 0.5, at or above 0.5), if the report needs them: one short odb script on nexus | set-up chat, on request |
| Mode shape of the spine tail peak in TH_r4b_i30_final, if the report discusses it | set-up chat, on request |
| Tub print orientation (D-082 flatness) | Miguel |
| Five-boss sensitivity (DV-26) | Stage 7 |
