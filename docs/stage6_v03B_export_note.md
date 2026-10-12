# Stage 6: v03-B export note (2026-10-08; BODY revised 2026-10-09 for D-056)

For the Abaqus set-up chat. Decision records are in `claude/journal_quadcopter.md` (D-054, D-055, F-028, N-06-05, Q-53).

## Decisions
- **D-054** (accepted): arm design/fixed split with through-fork Ø12 bolt bosses, upper boss extended to the arm top (z = +10); one tool set splits the envelope, so design and fixed faces coincide.
- **D-055** (Q-54 accepted by Miguel): the same rule applied to the BODY fin bosses: Ø12 bosses extended over their 12 mm width up to the fin top (z = +10, upper boss) and down to the fin bottom (z = -15, lower boss). Removes the 16 tangent faces (0.028 mm^2, 0.027 mm wide). +0.93 cm^3 = +1.21 g fixed.
- FC boss cylinders removed from the design body in the generator (set-up chat DV-2), so no manual cut is needed after import.

## Files (`stage6_abaqus_v03B.zip`)
`BODY.step`, `ARM_pp.step`, `ARM_pm.step`, `ARM_mp.step`, `ARM_mm.step` (each: solids named `*_DESIGN` and `*_FIXED`), `reference_points.csv` (unchanged: no seat surface or component position moved), generator and test scripts.

## Volumes and mesh test

Mesh test (`s06_split_acceptance.py`): general fuse of all solids of the file; pass = no face below 0.5 mm^2 and none narrower than 0.3 mm (2 x area / perimeter).

| File | Design (mm^3) | Fixed (mm^3) | Faces | Smallest face | Narrowest | Test |
|---|---|---|---|---|---|---|
| BODY.step | 33353.9 | 12597.9 | 210 | 8.04 mm^2 | 0.80 mm | pass |
| ARM_pp.step | 8036.9 | 2933.5 | 88 | 2.50 mm^2 | 0.40 mm | pass |
| ARM_pm.step | 8036.9 | 2933.5 | 88 | 2.50 mm^2 | 0.40 mm | pass |
| ARM_mp.step | 8036.9 | 2933.5 | 88 | 2.50 mm^2 | 0.40 mm | pass |
| ARM_mm.step | 8036.9 | 2933.5 | 88 | 2.50 mm^2 | 0.40 mm | pass |
| **Total** | **65501.5** | **24331.9** | | | | |

The arms are identical (Boolean difference 0.000 mm^3) to the set-up chat's `abaqus_v03B_fix` files; only BODY changed. BODY design + fixed = 45951.8 mm^3, the same envelope as the build log (fin bosses grew, design shrank by the same amount).

## Fixed mass per region (PET-CF, 1.30 g/cm^3, solid)

| Region | Volume (mm^3) | Mass (g) |
|---|---|---|
| Fin bosses (8, with extensions), BODY | 8755.2 | 11.38 |
| FC bosses (4), BODY | 792.7 | 1.03 |
| Battery plate frame and strap band, BODY | 2640.0 | 3.43 |
| GPS frame, BODY | 410.0 | 0.53 |
| Prong bosses (8 pairs through the fork, upper extended), arms | 9164.3 | 11.91 |
| Motor pads (ring and screw bosses, 4), arms | 2569.8 | 3.34 |
| **Total fixed** | **24331.9** | **31.63** |

## Mass budget
- Frame, solid design space: design 85.15 g + fixed 31.63 g = 116.78 g (unchanged envelope).
- Point masses: 205.4 g (battery 100, FC 15.2 + other hardware 12, GPS 8, motors 4 x 13.75, joint hardware 4 x 3.8).
- **Expected model total: 322.2 g for the D-055 export (confirmed in Phase 8: 322.1 g); 333.7 g with the flared D-056 keel (confirmed in the set-up chat: 333.70 g).**
- R-01 (AUW < 250 g): 250 - 205.4 = 44.6 g of printed frame, minus 31.6 g fixed = **B design-material allowance about 13.0 g** (Q-53; was 14.2 g after D-054, 15.6 g before).
- Variant C (no joint): fixed 8.3 g, about 59.8 g of printed frame allowed.

## What changes in the CAE model
1. Re-import BODY.step (Combine into single part, merge, retain boundaries). The FC-hole cut (DV-2) is no longer needed: the generator already removed the boss cylinders.
2. Redo on BODY: cell sets `FIXED_BODY` / `DESIGN_BODY`, the floor and top-face partitions (DV-5, DV-6), and the BODY surfaces (`S_BATT_SEAT`, `S_GPS_SEAT`, `S_FC_SEAT`, `S_FLOOR`, `S_FIN_BOSS_xx_L/_R`).
3. Re-import the arms from this set or keep the `abaqus_v03B_fix` arms (identical).
4. Ties (DV-8, secondary = fin boss faces): the fin boss side faces are now the extended outline (Ø12 discs plus the bands to the fin top and bottom). The prong side matches at the top (both extended to z = +10). At the bottom the fin face reaches z = -15 while the arm bottom rises from z = -15 to about -12.7 across the boss, so about 12 mm^2 per fin face (bottom strip) has no prong opposite: expect unconstrained secondary nodes there only.
5. Reference points, couplings, point masses, steps and loads: unchanged.

## Revision 2026-10-09: D-056 GPS keel (Q-55), flared version (final)

Phase 8 found the first elastic mode (365.2 Hz) to be a local bending mode of the GPS overhang, a 2.5 mm plate cantilevered about 30 mm behind the body (x = -20 to -50) under the 8 g GPS. Tosca could not raise it (the plate is already at its design-space limit), so the 417 Hz band would be infeasible from the first iteration.

Change: a **keel design region** under the overhang, on the frame centreline, built as a block x = -50 to -19 (fused 1 mm into the body rear face; both are design, so no internal face remains), y = -9 to +9, z = 0 to 21.5, with the rear prop keep-outs cut from it. Result:

| x (mm) | -49.5 | -45 | -40 | -35 | -30 | -25 | -24.8 to -20 |
|---|---|---|---|---|---|---|---|
| Width at z = 10 to 21.5 (mm) | 4.1 | 4.5 | 6.1 | 8.7 | 12.6 | 17.8 | 18.0 |
| Width at z = 0 to 10 (mm) | 18 | 18 | 18 | 18 | 18 | 18 | 18 |

- Above z = 10 the keel fills the corridor between the rear prop keep-outs (the maximum allowed); below z = 10 (no blades) it is the full 18 mm.
- Half-width 9, not 11: the fin root fillets (R5) meet the body rear face tangentially at y = +-10.86 for z = -15 to 10. A keel side at y = 11 would meet them 0.14 mm from that tangent line and leave slivers (gmsh test below: 9 tets of quality down to 0.002 at (-20, +-11, 9 to 11)). At y = 9 the keel is 1.86 mm clear.
- Bottom at z = 0: the rear-left motor-wire channel exits the rear face near the centreline at z = -8 to -3; 3 mm clear.

Only BODY.step changes (arms, reference points, seats unchanged):

| File | Design (mm^3) | Fixed (mm^3) | Faces | Smallest face | Narrowest | Face test |
|---|---|---|---|---|---|---|
| BODY.step (D-056 flared) | 42206.2 | 12597.9 | 223 | 8.04 mm^2 | 0.80 mm | pass |

Change check (Boolean, against the D-055 BODY): design +8852.3 mm^3, all inside x -50 to -20, y +-9, z 0 to 21.5; nothing removed (0.000 mm^3); fixed solids and all arm solids unchanged (0.000 mm^3 both ways).

Mesh test (gmsh, `s06_gmsh_meshtest.py`: fragment all solids as Abaqus merge/retain does, linear tets, element quality gamma, 1 = ideal, near 0 = sliver). The test reproduces the old failure, so it is meaningful:

| File | Size | Tets | Min quality | Tets below 0.05 |
|---|---|---|---|---|
| Old D-051 arm split (reconstructed) | 1.5 mm | 24,530 | 0.0010 | 81 |
| ARM_pp / pm / mp / mm (D-054) | 1.5 mm | about 27,700 each | 0.054 to 0.206 | 0 |
| BODY, D-056 thin keel | 1.5 mm | 102,473 | 0.1265 | 0 |
| BODY, keel half-width 11 (rejected) | 1.5 mm | 114,280 | 0.0022 | 9 |
| **BODY, D-056 flared, half-width 9** | 1.5 mm | 111,749 | **0.1265** | **0** |
| BODY, thin keel / flared 9, both | 1.0 mm | 269,123 / 299,754 | 0.0227 / 0.0227 | 25 / 25 |

At 1.0 mm both versions show the same 25 low-quality tets: they are existing BODY features, not the keel (fin root fillet ends at the z = 10 level near y = +-11.4, and the 1 mm waist between the two fin bosses at z = -3 to -2 near the fin nose). Quality 0.02, not failures; watch them at the 0.8 mm production mesh.

Mass:
- Fixed mass unchanged: 31.63 g. The keel is design space (+8852 mm^3 = +11.5 g only if Tosca kept it all).
- Expected model total with the solid design space: **333.7 g** (frame 128.3 g + 205.4 g).
- B allowance (Q-53) unchanged: about 13.0 g of design material.
- CAE: re-import BODY only (R2 to R4). The keel joins `DESIGN_BODY`; no new surfaces. Recompute the compliance caps C_i,0 on the mesh Tosca will use.
