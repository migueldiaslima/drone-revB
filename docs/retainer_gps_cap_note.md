# GPS cap v1 (production part)

Main chat, 2026-10-13. Generator `scripts/geometry_main/s07_gps_cap.py`; renders `scripts/figures/gps_cap_render.py`, `figures/gps_cap_1..2.png`. Files `geometry/retainers/`: GPS_CAP_v1.step (model frame), GPS_CAP_v1_TPU.stl (print frame, plate top on the bed; git-ignored, sent to Miguel), gps_cap_checks.json. Basis: brief v04-B section 5 (TPU cap, window over the antenna, two M2 screws into inserts), D-073, D-076, D-086 (deck on the TUB).

## Part

| Item | Value |
|---|---|
| Material | TPU 95A HF (compliant clamp on the module, vibration damping), as the brief |
| Plate | x -54 to -34, y +-12, 1.2 thick, corner radius 2, underside z 28.7 (module top 29.0 less 0.3 preload), top z 29.9 |
| Window | 9 x 9, radius 1, centred on the module (-44, 0): clamp band 4.0 at the x ends, 1.5 at the y sides |
| Legs | dia 5.4 (same as the cap bosses) from the boss tops z 26.5 to the plate, holes dia 2.4 (M2, TPU) at (-44, +-9.3) |
| Screws | 3.4 mm of cap above the boss top: M2 x 6 engages 2.6 mm, M2 x 8 engages 4.6 mm (insert hole 6.0 deep); use M2 x 8 if the insert is 4 mm long or more. Cap top with an M2 pan head: z 31.2 |
| Mass, CG | 539.6 mm^3, 0.65 g (density 1.21e-3 assumed); CG (-44, 0, 29.0) |

## Checks (all pass)

One solid, STL manifold. Clamp interference 37.2 mm^3 on the module envelope (0.3 mm preload). No overlap with the TUB; legs seated on the cap bosses; plate 2.2 mm above the rim top (the rim locates the module, the cap only holds it down). LID 5.1 mm, battery 4.5 mm, strap 26.9 mm; no interference with any other component dummy; the K9 cable hole stays under the module, not under the cap.

## Inputs to confirm when the module arrives (Q-63)

The listing gives 12 x 17 x 5 for the compass version (GetFPV lists 12 x 16 x 4.5 for a version without the compass, so the height differs by version). The cap assumes:
- module height 5.0: if it is 4.5, the 0.3 mm preload becomes a 0.2 mm gap; change `preload` to 0.8 (one parameter, reprint);
- antenna patch centred on the module and at least 9 x 9: the window must not cut into the clamp band over the PCB edges;
- the cable leaves through the floor hole (K9 at (-38.2, -3.0)), so the cap needs no cable notch; if the plug sits on an end face, the plate still clears it (the plug is within the module height).

## For the set-up chat

The cap is in RP_GPS (4.23 g, cap counted as 0.84 g). Actual 0.65 g (-0.19 g): RP_GPS conservative, no change to the export.

## Print and assembly

Plate top on the bed, legs up, TPU 95A HF, 0.2 mm layers, 100 % infill, no supports. Assembly step 13: module into the pocket (arrow along +x, D-076), cable down K9, cap on, two M2 screws into the boss inserts, tighten until the legs seat on the bosses.
