# Sources of the numbers in report/extensive/chapters/10_verification.tex

| Label | Source |
|---|---|
| V1 | `docs/stage6_concepts_explained.md` section 9 (measured interpolation table: density 0.4 stiffness 0.1024, mass 0.400; density 0.2 stiffness 0.0368, mass 0.200) |
| V2 | build log items 18, 43, 44 (TH method: solid factor 1, air stiffness 1e-6, mass 1e-9, responses stripped; island check with 0.2 mm proximity; island modes 45 to 200 Hz in TH04); brief T-4 (reactions < 1e-6 N) |
| V3 | `data/report/th_comparison.csv`; build log items 50, 51, 52, 58, 65; `docs/stage6_v04B_H4_report.md` tables "T-4 on the print geometry" and the GPS deck section |
| V4 | build log items 64, 65 (keel elements 10,549, 1,399.6 / 1,400.5 mm^3, 1,006.5 mm^3, 205.7 mm^3, 511,770 solid, reactions 2.2e-9 N, mode peaks); 58 (same mode-peak pattern in cA, cAB) |
| V5 | `docs/stage6_concepts_explained.md` section 4; build log item 59 (6 Taubin iterations, +0.3 / +0.7 % volume) |
| V6 | build log items 62, 63; `docs/stage6_v04B_H4_report.md` "Print set"; journal N-06-23 (masses, 45 keep-out solids, 0.215 mm^3) |
| V7 | build log items 60, 62, 63 (Boolean formula, gmsh 0.3 mm, volumes within 0.02 %, flap 2.3 mm^2, 550 back-to-back triangles, 34.1 mm^3 skins 0.15 to 0.2 mm, weld 1e-5 mm, loose pieces), DV-27 |
| V8 | set-up check 2026-10-13 (print STLs against the STEP exact solids, `scripts/post/restore_r4.py` helpers): TUB 20 solids 14,079.8 mm^3, LID 1 solid 3,417.3 mm^3, ARM 5 solids 2,934.0 mm^3, missing 0.000 and extra 0.000 mm^3; recorded in `print/r4_iso030/README.md` |
| V9 | build log items 61, 63 (thickness methods, voxel sizes, table values, thin areas); brief limits (1 % below 0.8 mm, 3 % below 1.2 mm); slicer check Miguel 2026-10-13 |
| V10 | figure run on the final thresholded model (2026-10-14): `export.log` (frequencies 431.0 to 533.4 Hz, element counts), `th_figs.npz` (mode shapes 7 to 12 on the 69,631 surface nodes); group ratios computed in the set-up workspace as max abs(u) over the nodes of S_ANT_PAD, S_BATT_SEAT, S_GPS_SEAT and each S_MOT_SEAT divided by the mode maximum; antenna mass 2.24 g from chapter 8 (S6); figures from `scripts/figures/fig_th_figs.py` (PR #44) |
