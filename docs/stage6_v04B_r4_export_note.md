# v04-B revision 4 export note (F-18 fix, option D)

Main chat, 2026-10-13, for the set-up chat. Decision D-086 (journal v0.54), finding F-037 (set-up F-18, build log items 46 and 47). Revision 3 note: `docs/stage6_v04B_r3_export_note.md`; everything not listed here is as revision 3.

## Change

The GPS deck (deck plate, pocket rim, two cap bosses with their inserts) moves from the LID to the TUB and sits on the keel top. The LID ends at the plate (x = -32), with a 0.5 mm gap to the deck front (x = -32.5). Boss 5 at (-30, 0) is deleted; the lid is clamped by the four wall bosses. Each lid screw pad is joined to the plate frame by a fixed link 4.5 mm wide. K9 continues up through the keel and the deck to the pocket floor (z 24.5), so the GPS cable never crosses the lid.

## Files (geometry/v04B_r4/)

| File | sha256 |
|---|---|
| TUB.step | 1fb13ecf779d447b6ba7d6a120c8f59a8d7fee144db4cbe856f5ec0d15327f10 |
| LID.step | f6dc02661b054b2886dedd0f9aad5c80bdf9a0a73118a4cd2a60220c3862ffa5 |
| KEEPOUTS_v04B.step | b47d5f1907b5ec8a6c49bd9b9746e31d6e67e069a8de79a55c34caa218b0ccc2 |
| COMPONENTS_v04B.step | d1ca02ad8d055946c851a959e3df1687382982b3469b03a15f25c54f8fb1c291 |
| ARM_pp.step | 86fd02c98fed0e8b47715c05321970773def02369f1f6db057de5325b05ee2e8 |
| ARM_pm.step | a05da458ba13f5d9cf6a4e691c8d3f22e697f8f4f030a618d7c80566a838a644 |
| ARM_mp.step | c16619cbdbfacecf1c94e49b031a8223b081c2741b2a3e1c1cfc30fdc8635eab |
| ARM_mm.step | fb5bdbe236c3a25be3a7296b6b597d3d89d485c78aa21501ae8dc02f5fb7a80e |
| reference_points_v04B.csv | dd7fe63666af0013dd5ab86af17af984d2cdf82259cd724cff60f1b7fbc203d8 |

ARM files are rewritten by the generator (hashes differ from revision 3), geometry identical: G0 compares them with v03-B by vertices and volumes (design 8036.91, fixed 2933.50 mm^3 each). KEEPOUTS changes only in K9 (436.35 to 467.77 mm^3, longer vertical leg). COMPONENTS: lid screw 5 removed.

Generated with `python3 scripts/geometry_main/s06_geometry_v04B.py` (CadQuery 2.8); gates `cd scripts/geometry_main && python3 s06_gates_v04B.py G0 G1 G2 G3 G4 G5`: all PASS (`gates_v04B_log.txt`, `gates_v04B.json`).

## Cells

| Part | Revision 3 | Revision 4 |
|---|---|---|
| TUB design | 1 cell, 39,368.8 mm^3 | 1 cell, 39,538.5 mm^3 (boss 5 volume returned to the keel) |
| TUB fixed | 17 cells, 11,711.1 mm^3: 8 x 1094.4 fin bosses, 4 x 240.24 FC bosses, 4 x 133.45 lid bosses, 1 x 1461.19 spine + lid boss 3 | 17 cells, 12,796.3 mm^3: 8 x 1094.40 fin bosses, 4 x 240.24 FC bosses, 3 x 133.45 lid bosses (1, 2, 4), 1 x 1461.19 spine + lid boss 3 (unchanged), **1 x 1218.56 GPS deck** (new) |
| LID design | 2 cells, 2,496.6 mm^3 | 2 cells, 2,357.0 mm^3 (1139.11 at -x, 1217.86 at +x) |
| LID fixed | 5 cells, 4,599.1 mm^3: plate frame + band + tab + GPS deck 4365.4, 4 wall pads 58.4 (boss 5 pad inside the main cell) | **1 cell**, 3,417.1 mm^3: frame, band, tab, 4 pads and 4 links |

Boss numbering as V1r3: 1 (21, 9.5), 2 (21, -9.5), 3 (-21, 5), 4 (-21, -5). GPS deck cell: x -54 to -32.5, y -9 to 9 (flush with the keel sides), z 21.5 to 24, rim z 24 to 26.5, cap bosses dia 5.4 at (-44, +-9.3) z 21.5 to 26.5 with insert holes dia 3.2 x 6.0, K9 hole dia 4 at (-38.2, -3.0). Independent check: tools 1330.405 less insert holes 80.425 less K9 31.416 = 1218.564 mm^3.

Mass at full density changes by -66.9 mm^3 (TUB +1254.8, LID -1321.7), -0.087 g: the G7 expected mass becomes 332.25 - 0.09 = 332.16 g. Point masses unchanged, 199.58 g. One lid screw and insert fewer (about 0.34 g: screw 22.1 mm^3 steel, insert 0.17 g) stay in the RP_FC lump, which is not itemised (A-024).

## Surfaces and ties

Expected values computed from the STEP files after an OCP fuse of each part by `scripts/geometry_main/s06_cae_expected_v04B.py` (output `geometry/v04B_r4/cae_expected_v04B_r4.json`); the same method reproduces the revision 3 values 625.98 and 2740.86.

| Surface | Revision 3 | Revision 4 | How to select |
|---|---|---|---|
| S_GPS_SEAT | LID, 209.19 mm^2 | **TUB**, 209.19 mm^2, 1 face at z = 24, normal +z, x -52.8 to -35.2, y -6.3 to 6.3 less the K9 hole | face of the GPS deck cell inside the rim |
| TIE_LIDRIM secondary (tub top under the lid) | 625.98 mm^2 (9 faces, partition y = +-17) | **363.23 mm^2**, incl. 4 boss annuli 4 x 20.23 | partition at y = +-17 as before **and at x = -32**; faces at z = 21.5 with x >= -32 and abs(y) <= 17. The keel strip x -32.5 to -32 (9.0 mm^2) stays free |
| TIE_LIDRIM main (lid bottom) | 2740.84 mm^2 (7 faces) | **2314.02 mm^2** (3 faces: fixed cell, 2 design cells) | all LID faces at z = 21.5 |
| S_BATT_SEAT (lid top, frame + band) | 1052.91 mm^2 (partition x = +-32, less the boss 5 pad hole) | **1056.00 mm^2** (64 x 34 - 2 x 20 x 28, no hole) | the fixed cell top is now one face with the pads and links: partition the LID with datum planes x = +-29 and y = +-14 (the frame inner edges) in addition to x = +-32; S_BATT_SEAT = fixed top faces at z = 24, abs(x) <= 32, without the 4 pad + link faces (together 131.84 mm^2; fixed top within abs(x) <= 32 is 1187.84) |
| Tub boss tops (G7a / TH sensitivity) | 5 x 20.23 | **4 x 20.23** | as before, boss 5 gone |
| Lid pad bottoms (G7a / TH sensitivity) | 5 x 24.47, separate pad cells | **4 x 24.47**, inside the fixed bottom face | partition the lid bottom face by sketch: 4 circles dia 6 at the boss xy |
| S_ANT_PAD, S_FC_SEAT, S_FLOOR, fin boss faces | | unchanged | |

No tie, contact or coupling between the GPS deck and the LID: the 0.5 mm gap (checked, 0.500 mm) is air in the model.

## Reference points and couplings

| RP | Change |
|---|---|
| RP_GPS (-44.0, 0.0, 26.5), 4.23 g | coupling CP_GPS re-pointed from the LID instance to the **TUB** instance, surface S_GPS_SEAT (same area) |
| RP_BATT | S_BATT_SEAT 1056.00 mm^2 as above |
| RP_FC, RP_ANT, RP_MOT, RP_JNT | unchanged |

## D-085 per part

| Part | Fixed cell | What needs its solid path |
|---|---|---|
| TUB | 8 fin bosses | arm ties: the arms reach each other, the FC and the battery only through the tub |
| TUB | 4 FC bosses | RP_FC (22.91 g) coupled to S_FC_SEAT, a TUB surface |
| TUB | spine + boss 3 | RP_ANT (2.24 g) on S_ANT_PAD, a TUB surface |
| TUB | GPS deck | RP_GPS (4.23 g) on S_GPS_SEAT, a TUB surface; no lid path (0.5 mm gap) |
| TUB | bosses 1, 2, 4 | seat tie only, i.e. a path through the other part: the case F-18 showed is not guaranteed. Held in H4 cycle 31 at iso 0.3 and 0.4 (item 46). Guard: per-part island check after H4 (TUB elements only, no tie proximity). If one is isolated: report it; options then are a local iso 0.3 for that boss or a fixed link, decided by Miguel |
| LID | single fixed cell | RP_BATT (100 g) on S_BATT_SEAT; the pads are inside the cell through the links, so no lid pad can be separated |

## Gate values

| Gate | Result |
|---|---|
| G0 file identity | PASS (TUB 1 + 17 solids, LID 2 + 1; arms identical to v03-B) |
| G1 Boolean bookkeeping | PASS, no keep-out overlap, no floating fixed solids |
| G2 face test | PASS (TUB smallest face 2.866 mm^2, narrowest 0.651 mm; LID 2.750 mm^2, 0.764 mm) |
| G3 tangency | PASS, no new flags; GPS deck min interior angle 90 deg, min distance 1.0 mm; pad links 90 deg, 1.1 mm |
| G4 gmsh 1.5 / 1.0 mm | PASS; TUB 1.0 mm 25 tets below 0.05 at the v03-B places; LID min gamma 0.229 / 0.281 |
| G5 clash | no interferences; C-1 0.958, C-7 7.75 / 4.87 / 7.58, C-9 5.49 / 8.43 / 13.75 mm (unchanged); extra: battery to GPS deck 3.0, GPS cap to battery 4.5 mm |

Two corrections made while running the gates. Deck width y +-10 (as on the lid) left a 1.0 mm underside strip next to the keel side (G3 flag at (-32.5, -9, 21.5)): deck narrowed to +-9, flush with the keel. Link width 4.0 gave 2 tets with gamma 0.046 at h = 1.5 (and 3.0 / 3.5 gave slivers elsewhere in the frame, so the 1.5 mm debug mesh is partly noise there); 4.5 gives min gamma 0.229, corner angle with the pad 41 deg.

## For the set-up chat

1. Rebuild from these files: TUB 18 cells (17 fixed as above, matched by volume), LID 3 cells; partitions x = -32 (TUB), x = +-29 and y = +-14 (LID), lid bottom circle sketch only for the sensitivity tie set; surface checks against the table; CP_GPS on the TUB; expected mass 332.16 g.
2. Debug and 1.0 mm meshes, reference job (G7b settings), H4 with the D-083 caps (2.0 x cycle 0) and the DV-24 shift; report the cycle 0 ALLSE in N mm.
3. TH at iso 0.4 with the island check per part, no tie proximity (TUB and LID separately): expected one main component per part; report bosses 1 to 4 and the GPS deck explicitly.
4. Restoration (D-044) with SPINE_fixed_v04B_r3.stl (spine unchanged), fillet pass B, T-1 to T-7.
