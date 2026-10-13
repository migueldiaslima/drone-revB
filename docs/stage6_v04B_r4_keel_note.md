# v04-B rev 4: keels under the GPS deck (proposal)

Set-up chat, 2026-10-13, for Miguel and the main chat. Build log items 50 to 55. Proposal only: geometry exports stay with the main chat.

## Why

TH of H4 rev 4 cycle 28 at iso 0.4 fails on the GPS deck: mode 7 at 146.8 Hz, LC3a 1.20 x cap (item 51). The keel under the deck held only low-density material in Tosca, mostly below 0.15 (items 52 to 54), so no threshold keeps a support. The deck is connected (D-085 met), but only through two thin straps at its front. Forcing two full-depth side webs solid (variant S, +2.11 g) passes TH. Miguel prefers a shape closer to what the optimiser was building.

## Constraints under the deck

| Item | Value |
|---|---|
| Keel design space | x -54 to -22, abs(y) <= 9, z 0 to 21.5 (generator `keel`) |
| Prop sweep + 3 mm (K12) | z 10 to 21.5, inside radius 47.45 of the rear motor axes (-52.5, +-52.5): abs(y) <= 52.5 - sqrt(47.45^2 - (x + 52.5)^2) above z 10, i.e. 5.1 at x -50, 6.2 at x -42, 8.0 at x -36, 9.0 forward of about x -35 |
| K9 (GPS cable) | vertical dia 4 at (-38.2, -3.0) from z 5 to 24.5; leg at y -3, z 5 from x -38.2 to the wall |
| K8 (antenna) | dia 3.5 at y 3.5, z 6.5 forward of x -42, then the R7 bend down to the exit (-49, 3.5); fixed sleeve 1.5 mm around it |

## A: twin tapered keels (confirmed by Miguel)

- Plan, mirrored in y: inner contour abs(y) = 5.0 from x -50 to -27, then a U through (-26, 4.8), (-24.5, 4.0), (-23, 2.6) to the centreline at the rear wall x -22; outer contour abs(y) = 9 (deck edge) where the prop sweep allows it, otherwise the prop sweep boundary above (from 9 at about x -35 to 5.1 at x -50), flaring at the wall to abs(y) 11.0 at x -23 and 12.5 at x -22.
- Depth: from the deck underside z 21.5 down to z_bot(x) = 21.5 - 11.5 (0.6 t + 0.4 t^2), t = (x + 50) / 28: zero depth at x -50, bottom at z 10 at the wall x -22.
- Each keel tapers in width from 4 mm at x -32 to zero near x -50 (prop sweep), and in depth from 11.5 mm at the wall to zero at x -50.
- Volume 1,165 mm^3 = 1.51 g (0.25 mm voxels, clipped by K8, K9 and the prop sweep).

## B: web under the antenna tunnel (B1, confirmed by Miguel)

- 2 mm thick, y 2.5 to 4.5 (centred on the tunnel), x -40 to the wall x -22.
- Top: sleeve underside z 3.25; bottom: z_bot(x) = 3.25 (1 - t)^1.5, t = (x + 40) / 14, reaching the keel underside z 0 at x -26 and running along it to the wall.
- Inside the design space: 81 mm^3 = 0.10 g.
- Extension (Miguel): continue the web down the outside of the rear wall below z 0, to 1 mm above the opening there. This is outside the optimisation design space: print geometry only, not testable by TH (no elements). The opening and its z are to be identified by the main chat in the generator (K11 motor-lead passages are at the corners, K9 enters the wall at y -5, z 5).

## Definition and files

- `scripts/post/keels_r4.py`: the shapes as functions `in_A(x, y, z)`, `in_B(x, y, z)` (same code for the preview and the TH element selection); `python3 keels_r4.py <dir>` writes `keel_A_preview.stl`, `keel_B_preview.stl` (0.25 mm voxel previews, for a visual check against `mt_c28_TUB_040.stl`).
- For restoration the main chat builds A and B as exact solids in `s06_geometry_v04B.py` (or a separate script) from the definitions above.

## Next

1. Miguel checks the previews in Fusion.
2. TH on H4 cycle 28 with A, B and A + B forced solid (elements with the centroid inside the shape), mass and modes against S.
3. Main chat: decision, exact solids, the B extension, restoration (D-044), T-1 to T-7.
