# v04-B revision 3: F-17 fix (antenna spine), validation note

Main chat, 2026-10-12. Proposal for Miguel's approval before the new H4. Nothing here is recorded in the journal yet.

## Why revision 3

F-17 (set-up chat, H4 cycle 31): the fixed antenna boss at (-44, 0) had no fixed connection to the frame and became a loose 0.15 g part after thresholding. Agreed with Miguel: straight T antenna (the moulded T junction cannot bend), mounted under the keel, held by a TPU holder, with a fixed connection to the frame. While validating the version shown in the viewer (v2), three problems were found and fixed here:

| Problem in viewer v2 | Fix in revision 3 |
|---|---|
| Antenna leg tips only about 2.6 mm from the rear-left arm (gate C-9 needs >= 5); found with an arm plan model that reproduces the rev 2 C-9 result within 0.05 mm (15.46 vs 15.41) | T moved back to x = -49 (5.32 mm with the measured 52 mm span) |
| Coax bent about R2 into the stem of the flat T; I-PEX recommends a minimum bend radius of 6 x the cable diameter (6.8 mm for 1.13 mm coax) | T hangs vertical, stem up, directly under the K8 exit: the coax goes straight into the stem. K8 rerouted with one R7 bend (was R5) |
| Insert hole in a 4.5 mm pad with no cap; peg hole and pad corners too thin; pad top grazing the sleeve (would fail the CAD tangency gate G3) | Local insert boss (1.7 wall, 1.7 cap), pad 2.2 thick and 1.05 below the sleeve, peg hole 1.1 deep |

## Geometry changes (all in s06_geometry_v04B.py, revision 3)

| Item | Revision 2 (H4) | Revision 3 |
|---|---|---|
| K8 antenna channel | z 7, bend R5 at x -33, exit (-38, +3.5) | z 6.5, bend R7 at x -42, exit (-49, +3.5) |
| K9 GPS channel | vertical leg (-38.2, -1.5), rear-wall hole y -3.5 | (-38.2, -3.0), hole y -5.0 (no fixed material around it) |
| Lid GPS cable hole | (-38.2, -1.5) | (-38.2, -3.0) |
| TUB fixed, antenna | boss dia 5.4 x 6.5 at (-44, 0), insert dia 3.2 x 4.5 | antenna spine: sleeve 1.5 mm wall around K8 from the bay face to the exit, pad x -53..-39, y -8..8, z 0..2.2, insert boss dia 6.6 to z 5.7 with a dia 3.2 x 4.0 hole (M2 x 3 insert) at (-43, -1.0), locating hole dia 2 x 1.1 at (-43, -5.3), web dia 3.5 up the rear wall into the rear lid boss (-21, +5) |
| Antenna | 90 deg V lying under the keel | straight T, moulding vertical under the exit, legs along y at z -5.75, span 50 |
| Point masses | RP_FC 27.2, RP_GPS 2.6 | RP_FC 22.91, RP_GPS 4.23 (+ cap, 2 screws, 2 inserts), RP_ANT 2.24 at (-48.6, 3.5, -4.0) on the pad underside (antenna 0.9 + holder 0.94 + screw 0.23 + insert 0.17); total 199.58 g (was 200.0) |

The spine joins the rear lid boss, which carries the lid tie, so the antenna mount is held by fixed material all the way (new rule: every fixed solid touches another fixed solid or carries a load that needs a solid path).

## Checks (s06_f17_spine.py, signed distance fields, no CAD kernel)

All 35 pass (antenna dimensions measured by Miguel: legs 1.4, tip-to-tip 52, moulding 14 x 7.5). Values in mm unless stated; output also in geometry/v04B_r3_f17/checks.json.

| Check | Value | Limit | Result |
|---|---|---|---|
| K8 centreline minimum bend radius (mm) | 7.00 | >= 6.8 (6 x OD) | PASS |
| coax route receiver -> bay entry -> K8 -> stem (mm) | 43.74 | <= 62 (measured) | PASS |
| K8 to K9 surface gap (mm) | 2.90 | >= 1.0 | PASS |
| K8 to keel side (mm) | 3.75 | >= 1.0 + wall | PASS |
| K9 (moved) to keel side (mm) | 2.01 | >= 1.0 | PASS |
| K8 opening above K11 in the rear wall (mm) | 7.75 | >= 1.0 | PASS |
| K9 opening above K11 in the rear wall (mm) | 6.00 | >= 1.0 | PASS |
| lid GPS hole moves to (x, y) | (-38.2, -3.0) | inside pocket | PASS |
| spine connected components | 1.00 | == 1 | PASS |
| spine new fixed volume (mm^3) / mass (g) | 1314 / 1.71 | - | PASS |
| spine to K9 (mm) | 1.19 | >= 1.0 | PASS |
| spine to keel side (mm) | 1.09 | >= 1.0 | PASS |
| spine to keel rear end x = -54 (mm) | 1.09 | >= 1.0 | PASS |
| K8 wall >= 1.0 mm all round (probe points solid) | 2136/2136 | all | PASS |
| M2 insert hole: 1.5 mm wall and cap (probe points solid) | 324/324 | all | PASS |
| locating hole: 1.0 mm wall and cap | 324/324 | all | PASS |
| insert hole to K8 (mm) | 1.75 | >= 1.0 | PASS |
| spine to keel lid boss (-30, 0) (mm) | 4.19 | >= 1.0 or merged | PASS |
| spine joined to rear lid boss (-21, +5) | yes | yes | PASS |
| spine STL closed (edges not shared by exactly 2 faces) | 0.00 | == 0 | PASS |
| C-9 antenna to rear arms, plan (mm) | 5.32 | >= 5.0 | PASS |
| antenna legs z (mm) | -5.75 | above -12, below 10 | PASS |
| C-clip opening / leg diameter (snap if < 1) | 0.76 | 0.6 .. 0.85 | PASS |
| holder connected components | 1.00 | == 1 | PASS |
| holder volume (mm^3) / mass TPU (g) | 776 / 0.94 | - | PASS |
| holder lowest point to landing plane (mm) | 6.09 | >= 5 | PASS |
| holder top within the pad footprint | x -52.2..-41.0 y -7.5..8.0 | inside pad | PASS |
| holder thinnest feature away from the clip ends (mm) | 0.80 | >= 0.8 (2 lines) | PASS |
| bar pocket clearance (holder material inside the bar) | 0.00 | == 0 | PASS |
| stem slot clearance (holder material inside the stem) | 0.00 | == 0 | PASS |
| stem top to K8 exit: coax goes straight up (offset mm) | 0.00 | == 0 | PASS |
| screw M2 x 5: engagement / tip below hole bottom (mm) | 3.5 / 0.5 | >= 3.0 / > 0 | PASS |
| screw head to front cheek (mm) | 0.80 | >= 0.3 | PASS |
| holder STL closed | 0.00 | == 0 | PASS |
| holder/antenna to motor-lead passages K11 (x gap, mm) | 12.19 | >= 5 | PASS |

## Antenna holder (print file ANTENNA_HOLDER_v04B_r3_TPU.stl)

The STL files are git-ignored (repository rule for *.stl). Regenerate both with `python3 scripts/geometry_main/s06_f17_spine.py` (numpy and scipy only, about 1 min); it writes geometry/v04B_r3_f17/ANTENNA_HOLDER_v04B_r3_TPU.stl (binary, about 280,000 triangles, closed) and SPINE_fixed_v04B_r3.stl (about 160,000 triangles, closed).

| Item | Value |
|---|---|
| Material | TPU 95A (density 1.21 g/cm3 assumed); 0.94 g |
| Print | top plate on the bed (the plate is flat at z = 0 in use); cheeks run full height to the plate so every feature starts on the bed; no supports |
| Thinnest feature | 0.8 mm (lips), away from the clip ends, which taper to an edge as the snap lead-in |
| Bar pocket | bar 4.0 thick + 0.10 per side (snug in TPU); lips 1.0 x 1.0 under the bar: the T snaps in from below |
| Stem slot | stem 3.0 x 3.2 + 0.20 per side |
| Leg clips | C-clips 3 mm from the moulding, bore = leg dia + 0.2 (1.6), wall 1.0, cut flat 0.75 x bore radius below the leg axis: the clip wraps 277 deg and the opening is 1.06 mm (0.76 x the 1.4 mm leg), so the leg snaps in from below and is retained |
| Fixing | one M2 x 5 socket head screw from below at (-43, -1.0), through a dia 2.2 hole in the 1.5 mm plate, into an M2 x 3 heat-set insert in the spine (3.5 mm engagement, tip 0.5 mm short of the hole bottom); peg dia 1.8 x 0.9 into the dia 2.0 x 1.1 locating hole stops rotation |
| Lowest point | z -8.9, 6.1 mm above the landing plane (z -15) |

Assembly order: thread the IPEX end up through the K8 exit and the channel into the bay, connect it to the receiver; snap the T into the holder (stem first, then the legs into the clips); offer the holder to the pad with the stem in the slot and the peg in the hole; one M2 screw. The 18 mm of coax slack lies as a gentle S in the bay against the rear wall, clear of the FC nut access columns (K5).

## Antenna dimensions

Measured by Miguel (2026-10-12): legs dia 1.4, tip-to-tip 52, moulding 14 along the legs and 7 to 7.5 along the cable, coax 60 to 62 from the receiver plug to the moulding. Assumed (not measurable without cutting): split of the 7.5 into bar 4.5 and stem 3.0, stem section 3.0 x 3.2 (the slot has 0.2 per side; TPU tolerates a wrong guess of a few tenths). M2 x 3 heat-set insert in a dia 3.2 hole (project value).

## Not validated here

1. The CAD build: CadQuery cannot be installed in this session (the package servers are blocked by the session's network policy), so the revision 3 generator was edited, syntax-checked and its reference-point writer exercised with the CAD kernel stubbed out, but not run. It now also runs from the GitHub repository layout (inputs from geometry/v03B_arms and geometry/v04B, output to geometry/v04B_r3); gates skip the v03-B BODY baseline when BODY.step is absent. Expected: TUB_FIXED changes by (spine CAD volume, about 1,300 mm^3 less the part inside the rear lid boss) minus 112.7 (old boss); no floating fixed solids; G3 with no new flags; C-7 K8 to K11 7.75, K9 to K11 6.0; C-9 about 5.7.
2. The real arm geometry for C-9 (plan model, calibrated on the rev 2 gate).
3. Print orientation of the tub. The pad underside (z = 0) is a downward face 15 mm above the bed if the tub prints floor-down, like the rest of the keel underside. Printing rim-down would give the flattest lid seat (D-082 asks for 0.1 mm), but then the floor and the fin bosses need support. Open decision.
4. RF: a straight dipole under the keel, 12 mm from the motor-lead exits, is the standard arrangement; not tested.

## Next (after approval)

1. Main chat: run the revision 3 generator and gates (or Miguel); journal v0.53 (TH04 record, D-082 item 2 closed, DV-25 confirmed, F-17 fix and rule, revision 3, measured coax 62 mm, strap 3.25 g).
2. Set-up chat: rebuild the model from the revision 3 STEP (cell counts change: the spine fuses with the rear lid boss), S_ANT_PAD and RP_ANT, new point masses, new H4 (about 31 cycles at about 16 min, 8 to 9 h, caps 2.0 x cycle 0 as DV-25), TH at iso 0.4 with the island check, restoration with SPINE_fixed_v04B_r3.stl as the exact fixed solid.
