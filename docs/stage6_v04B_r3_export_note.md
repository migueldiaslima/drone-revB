# v04-B revision 3 export note (F-17 fix)

Main chat, 2026-10-12, for the set-up chat. Decisions D-083 to D-085 (journal v0.53). Background, checks and the holder: claude/stage6_v04B_r3_F17_note.md.

## Files (geometry/v04B_r3/)

| File | sha256 |
|---|---|
| TUB.step | b6347c32f8405ad685693db1c41352195971c6b27c5fbb9c16a1825f754eb728 |
| LID.step | 63d3b611c45754c02e279ea7b5c3fc4b53055360a8f91c1e16fb27d83b25f53f |
| KEEPOUTS_v04B.step | fa0e87f31c75e7663368d81a456e0c60da87ab618710b8a0b9fd0476b0777283 |
| COMPONENTS_v04B.step | c53721c15933f8d76903b3aaf48549ee5e6b7c67d2492224325597e5ace79952 |
| ARM_pp.step | 26ccb379820b85676ddd666d66afa79c6e259102c1940c2d16ecae5fe433b987 |
| reference_points_v04B.csv | 1187b20bfa67b4625b5a32b29ef4741b693b0ad49987b2b6d6abcced12afe42d |

ARM_xx.step are the revision 2 arms unchanged (G0: identical to v03-B after moving back by (3 sx, 3 sy, 0)). LID.step changes only in the GPS cable hole, now at (-38.2, -3.0).

Generated with `python3 scripts/geometry_main/s06_geometry_v04B.py` (CadQuery 2.8, from the repository layout); gates `python3 scripts/geometry_main/s06_gates_v04B.py`: G0 to G5 all PASS (gates_v04B_log.txt, gates_v04B.json).

## What changed against revision 2 (the H4 model)

| Item | Revision 2 | Revision 3 |
|---|---|---|
| TUB solids | 19 (1 design, 18 fixed) | 18 (1 design, 17 fixed): the antenna boss is gone and the antenna spine is fused with the rear-left lid boss (-21, +5) into one fixed solid of 1461.2 mm^3 |
| TUB design / fixed (mm^3) | 40,676.1 / 10,496.1 | 39368.8 / 11711.1 |
| K8 antenna channel | z 7, R5 bend at x -33, exit (-38, +3.5) | z 6.5, R7 bend at x -42, exit (-49, +3.5) |
| K9 GPS channel | leg (-38.2, -1.5), rear-wall hole y -3.5 | leg (-38.2, -3.0), hole y -5.0 |
| Pad underside S_ANT_PAD | - | one planar face at z = 0 of the spine solid, 175.93 mm^2 (x -53..-39.7, y -8..8, less the insert, locating and K8 holes) |
| Point masses | 200.0 g | 199.58 g: RP_FC 22.91, RP_GPS 4.23, new RP_ANT 2.24 at (-48.6, 3.5, -4.0) coupled to S_ANT_PAD (antenna 0.9, TPU holder 0.94, M2 screw 0.23, insert 0.17) |

Unchanged: arms, joints, fin and FC bosses, the other four lid bosses, floor, seat and lid; S_FLOOR, S_FC_SEAT, fin boss faces, tub top under the lid and the LID surfaces of item 34 keep their values (the rear-left lid boss is now longer downwards, z 7 to 21.5, but its top annulus is unchanged).

## Gate values

| Gate | Result |
|---|---|
| G0 file identity | PASS (volumes within 2e-6 relative of v04B_volumes.json after the STEP round trip; arms identical by vertices and volumes, since OCP 7.8 Booleans of coincident solids are unreliable) |
| G1 Boolean bookkeeping | PASS, no keep-out overlap, no floating fixed solids |
| G2 face test | PASS (TUB smallest face 2.866 mm^2, narrowest 0.651 mm) |
| G3 tangency | PASS, no new flags; antenna spine min interior angle 80.4 deg, min distance 1.0 mm |
| G4 gmsh 1.5 / 1.0 mm | PASS; TUB at 1.0 mm 25 tets below 0.05 at the same v03-B places as revision 2 |
| G5 clash | no interferences; C-7 K8 to K11 7.75, K8 to K9 4.87, K9 to K11 7.58; C-9 antenna to ARM_mp 5.49, to ARM_mm 8.43, to prop sweep 13.75 mm |

## For the set-up chat

1. Rebuild the CAE model from these files (cell counts and the volume checks of V1 change as above; RP_ANT with its coupling to S_ANT_PAD; point masses 199.58 g).
2. Debug and 1.0 mm meshes, reference job (G6, G7b settings), then H4 with the D-083 caps (2.0 x cycle 0) and the DV-24 shift; report the cycle 0 ALLSE in N mm.
3. TH at iso 0.4 with the island check (D-085), and TH with the five boss ties (D-082 item 3 later in Stage 7).
4. Restoration (D-044) with SPINE_fixed_v04B_r3.stl (from s06_f17_spine.py) as the exact fixed solid of the spine, fillet pass B, T-1 to T-7.
