# v04-B rev 4 keels A and B: exact solids for restoration

Main chat, 2026-10-13, for the set-up chat. Decision D-087 (print fix A + B with the clean keel zone), D-088 (D-085 extended to stiffness), finding F-038, lesson L-017, numbers N-06-21 and N-06-22 (journal v0.56). Basis: `docs/stage6_v04B_r4_keel_note.md`, build log items 50 to 58, `scripts/post/keels_r4.py`.

## Files (geometry/v04B_r4_keels/)

| File | Content |
|---|---|
| KEEL_A_r4.step | keel A, 2 solids (+y 658.8, -y 656.3 mm^3), model coordinates |
| KEEL_B_r4.step | web B, straight lower edge down to the rear wall face, 1 solid, 119.7 mm^3 |
| KEEL_A_r4.stl, KEEL_B_r4.stl | same, 0.02 mm chord (git-ignored: regenerate with the script, or from the chat) |
| KEEL_ZONE_r4.step | GPS deck + spine + A + B fused and cut by K8, K9, K12 (the G3 test body) |
| keels_r4_checks.json | all checks below |

Generator: `python3 scripts/geometry_main/s07_keels_r4.py` (10 s). Renders: `scripts/figures/keels_r4_render.py`, `figures/keels_r4_1..3.png`.

## Shapes

As the keel note, with four changes for printable, mesh-clean solids:

| # | TH definition (keels_r4.py) | Exact solid | Reason |
|---|---|---|---|
| D1 | A from x -50, depth 0 (feather) | A from x -46, depth 1.08, vertical end face | the feather meets the deck underside at 14 deg (G3 wedge, unprintable edge) |
| D2 | A inner contour abs(y) 5.0 | 4.6 (U scaled by 4.6 / 5), and behind x -42 a line to 4.30 at x -46, minimum width 1.2 | K9 (dia 4 at y -3) reaches abs(y) 5.0 exactly: tangent contact; behind x -42 the TH shape is 0.1 to 1.2 mm wide against the prop sweep |
| D3 | B top z 3.25 | B top z 4.0, inside the sleeve wall (3.25 to 4.75) | a flat top at 3.25 leaves a 0.16 mm crescent under the round sleeve at y 2.5 and 4.5 |
| D4 | B from x -40, depth 0 | B from x -36.9, 1.0 mm front face | 19 deg wedge on the sleeve |
| D5 | B lower edge curved, z_b = 3.25 (1 - t)^1.5 to z 0 at x -26, then a 45 deg gusset to z -2.0 on the wall | one straight line from (-36.9, 2.25) to (-23, -2.0), about 17 deg (Miguel, rev b) | depth grows linearly to the wall, where the bending moment is largest; deeper than the TH shape at every x behind about x -34, equal ahead of it; the part below z 0 (x -23 to -29.6) is print only |

B extension (Miguel): the opening below the web on the rear wall face (x -23, y 2.5 to 4.5) is the K11 motor-lead passage, z -8.0 to -3.0. The straight lower edge (D5) ends on the wall face at z -2.0, 1 mm above the opening top. Outside the TUB design envelope (print only): A 13.9 mm^3 (wall flares), B 11.4 mm^3 (below z 0).

## Volumes against the TH

| Item | TH_r4b_cAB (elements) | Exact | Difference |
|---|---|---|---|
| A | 1,149.4 mm^3 | 1,315.1 mm^3 = 1.71 g | +165.7 mm^3 (+0.22 g): D2 wider inner contour, wall flares outside the TUB, element-centroid selection |
| B | 85.6 mm^3 | 119.7 mm^3 incl. sleeve overlap 20.8 and 11.4 below z 0 = 0.16 g | +11.9 inside the design space (deeper edge, D5) |

The exact solids hold more material than the TH shapes everywhere except D1 (A behind x -46: depth below 1.08 mm, width below 1.2 mm) and D4 (B ahead of x -36.9: depth below 1 mm). Both removed pieces are thinner than one 1.0 mm element. Recommendation: one confirmation TH with the exact solids (elements with the centroid inside KEEL_A_r4.stl / KEEL_B_r4.stl forced solid, same clean box), expected at or above TH_r4b_cAB; skip it if time is short.

## Checks (all pass)

| Check | Result |
|---|---|
| Overlap with keep-outs K1 to K12 | none (A, B) |
| Overlap with component dummies | none (A, B) |
| Overlap with the LID | 0 (A top at z 21.5 under the plate x -32 to -22 becomes part of the seat) |
| A to the GPS deck | in contact (both sides), shared face at z 21.5 |
| A to the spine | merged at the wall (the rear-left lid boss web) |
| A to K9 | groove cut, not tangent |
| B to the sleeve | merged, 20.8 mm^3 common |
| B to the antenna coax and holder | 1.9 mm |
| A minimum width / rear depth | 1.2 / 1.08 mm |
| B front depth below the sleeve | 1.02 mm |
| G2 face test | A: 124 faces, smallest 0.633 mm^2, narrowest 0.364 mm, 0 failing; B: 0 failing |
| G3 keel zone (deck + spine + A + B) | 0 wedges, 0 strips |

## For the set-up chat

1. Restoration (D-044): iso 0.4 of H4 rev 4 cycle 28, keel zone cleaned (x -54 to -23, abs(y) <= 9, z 0 to 21.5), exact fixed solids: spine (SPINE_fixed_v04B_r3.stl), GPS deck, bosses, KEEL_A_r4 and KEEL_B_r4.
2. Optional confirmation TH with the exact keels (above).
3. T-1 to T-7 and the H4 report.
