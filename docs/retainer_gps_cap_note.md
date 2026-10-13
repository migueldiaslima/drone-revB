# GPS cap v2 (production part, press pins)

Main chat, 2026-10-13. Generator `scripts/geometry_main/s07_gps_cap.py`; renders `scripts/figures/gps_cap_render.py`, `figures/gps_cap_1..2.png`. Files `geometry/retainers/`: GPS_CAP_v2.step (model frame), GPS_CAP_v2_TPU.stl (print frame, plate top on the bed; git-ignored, sent to Miguel), gps_cap_checks.json. Basis: brief v04-B section 5 (TPU cap, window over the antenna, two M2 screws into inserts, replaced in v2 by press pins, Miguel 2026-10-13), D-073, D-076, D-086 (deck on the TUB).

## Part

| Item | Value |
|---|---|
| Material | TPU 95A HF (compliant clamp on the module, vibration damping), as the brief |
| Plate | x -54 to -34, y +-12, 0.8 thick (2 lines, flexible clamp), corner radius 2, underside z 28.7 (module top 29.0 less 0.3 preload), top z 29.5 |
| Window | 9 x 9, radius 1, centred on the module (-44, 0): clamp band 4.0 at the x ends, 1.5 at the y sides |
| Legs | dia 5.4 (same as the cap bosses) from the boss tops z 26.5 to the plate, at (-44, +-9.3) |
| Press pins | dia 3.325 x 4.0 below each leg into the boss hole dia 3.2 (0.125 mm diametral interference, Miguel's proven fit), 0.4 mm lead-in chamfer, tip at z 22.5 (above the deck underside 21.5) |
| Fastening | no inserts and no screws in the cap bosses; the holes stay dia 3.2, so inserts and the v1 screw cap remain a fallback |
| Mass, CG | 480.5 mm^3, 0.58 g (density 1.21e-3 assumed); CG (-44, 0, 28.1) |

## Checks (all pass)

One solid, STL manifold. Clamp interference 37.2 mm^3 on the module envelope (0.3 mm preload). No overlap with the TUB outside the pins; pin interference 4.65 mm^3 in the two holes; plate 2.2 mm above the rim top (the rim locates the module, the cap only holds it down). LID 5.1 mm, battery 4.5 mm, strap 26.9 mm; no interference with any other component dummy; the K9 cable hole stays under the module, not under the cap.

## Inputs to confirm when the module arrives (Q-63)

The listing gives 12 x 17 x 5 for the compass version (GetFPV lists 12 x 16 x 4.5 for a version without the compass, so the height differs by version). The cap assumes:
- module height 5.0: if it is 4.5, the 0.3 mm preload becomes a 0.2 mm gap; change `preload` to 0.8 (one parameter, reprint);
- antenna patch centred on the module and at least 9 x 9: the window must not cut into the clamp band over the PCB edges;
- the cable leaves through the floor hole (K9 at (-38.2, -3.0)), so the cap needs no cable notch; if the plug sits on an end face, the plate still clears it (the plug is within the module height).

## For the set-up chat

The cap is in RP_GPS (4.23 g, cap counted as 0.84 g). Actual 0.58 g (-0.26 g; the 2 screws 0.46 g and 2 inserts 0.33 g in RP_GPS are also gone): RP_GPS conservative, no change to the export.

## Print and assembly

Plate top on the bed, legs and pins up, TPU 95A HF, 0.2 mm layers, 100 % infill, no supports. Assembly step 13: module into the pocket (arrow along +x, D-076), cable down K9, press the cap on until the legs seat on the bosses (no inserts in the cap bosses). Removal: lift the plate edge next to each pin.
