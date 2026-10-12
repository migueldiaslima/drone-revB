# Stage 6 model set-up, part 1: the Abaqus model (v03-B)

Abaqus/CAE 2022, built by hand (D-043). Part 2 (Tosca task) follows once this model runs.
Files: `abaqus_v03B/BODY.step`, `ARM_pp/pm/mp/mm.step`, `reference_points.csv`. Revision 2026-10-08: arm STEPs regenerated with the D-054 split (identical to the set-up chat's `abaqus_v03B_fix`); BODY design without the FC boss cylinders (DV-2).

## 0. Conventions

| Item | Value |
|---|---|
| Units | mm, N, tonne, s (stress in MPa, density in t/mm^3, 1 g = 1e-6 t) |
| Axes | x forward, y left, z up; origin at the frame centre; z = 0 on the arm top under the motor |
| Corner tags | pp (+x+y, front left), pm (+x-y, front right), mp (-x+y, rear left), mm (-x-y, rear right) |
| Model name | `revB_v03B` (save the .cae and keep `abaqus.rpy`, D-043) |

## 1. Parts

Each STEP file holds two solids: `*_DESIGN` and `*_FIXED`. Both must end up in one part with an internal boundary between them (two cells), so design and fixed regions can become separate element sets that share nodes.

1. File > Import > Part > `BODY.step`. In the import dialog choose **Combine into single part**, tick **Merge solid regions** and **Retain intersecting boundaries**. Name the part `BODY`.
2. Repeat for the four arm files: parts `ARM_pp`, `ARM_pm`, `ARM_mp`, `ARM_mm`.
3. Check each part: Tools > Query > Geometry diagnostics (no invalid entities); the part shows two or more cells.

If the import dialog in 2022 does not offer the combine option: import each file with "create individual parts", instance both solids in the Assembly, then Instance > Merge/Cut, Merge Geometry, Retain intersecting boundaries. The merged part replaces the two.

## 2. Material and section

Material `PETCF_SIRAYA` (D-038, D-045, A-021):

| Field | Value |
|---|---|
| Density | 1.30e-9 t/mm^3 |
| Elastic, Type: Engineering Constants | E1 = 5058, E2 = 5058, E3 = 2890 |
| | Nu12 = 0.35, Nu13 = 0.35, Nu23 = 0.35 |
| | G12 = 1873, G13 = 1070, G23 = 1070 |

Abaqus defines Nu13 as the strain in 3 caused by stress in 1, so Nu31 = Nu13 x E3/E1 = 0.20, within the FFF range.

Section `SEC_PETCF`: solid, homogeneous, this material. Assign it to all cells of all five parts (design and fixed alike).

Material orientation: the global system (1 = x, 2 = y, 3 = z). The frame prints flat, so the build direction is global z. Assign it explicitly (Property > Assign Material Orientation, use the global CSYS) so it is visible in the input file.

## 3. Assembly

Instance all five parts (dependent instances are fine). They are already in the right place; do not move them.

Check: Tools > Query > Distance between a fin boss face and the facing prong boss face should be 0.15 mm.

## 4. Sets and surfaces

Face partitions needed first (build log DV-5, DV-6): partition the BODY floor bottom face with datum planes x = +-20 and y = +-20 to bound `S_FLOOR`; partition the BODY top face (z = 24) with a datum plane x = -32 to separate `S_BATT_SEAT` from `S_GPS_SEAT` (plate frame, strap band and GPS frame form one face).

Name them exactly as below; Part 2 refers to these names.

| Name | Type | Content |
|---|---|---|
| `DESIGN_BODY` | element set (part BODY) | the BODY_DESIGN cell(s) |
| `FIXED_BODY` | element set (part BODY) | fin bosses, FC bosses, plate frame and strap band, GPS frame |
| `DESIGN_ARM` | element set (each arm part) | the ARM_DESIGN cell(s) |
| `FIXED_ARM` | element set (each arm part) | prong bosses and the motor pad ring and screw bosses |
| `S_BATT_SEAT` | surface | top faces (z = 24) of the plate frame and strap band |
| `S_FC_SEAT` | surface | top faces (z = -6) of the four FC bosses |
| `S_GPS_SEAT` | surface | top face (z = 24) of the GPS frame |
| `S_MOT_SEAT_xx` | surface, per arm | top faces (z = 0) of the pad contact ring and the four screw bosses |
| `S_FIN_BOSS_xx_L`, `_R` | surface, per corner | the flat side faces of the two fin bosses, one surface per side of the fin |
| `S_PRONG_BOSS_xx_L`, `_R` | surface, per corner | the inner (fin-facing) faces of the prong bosses, matching side |
| `S_JNT_xx` | surface, per corner | outer faces of the four prong bosses of that corner |
| `S_FLOOR` | surface | bottom face of the body floor inside the 40 x 40 square (z = -15), including the four FC boss bottom disks (1600 mm^2 in total) |

Create the element sets after meshing (Mesh > ... or via the cell sets created now, which carry over to elements).

## 5. Reference points, couplings, point masses

Create the reference points from `reference_points.csv` (Tools > Reference Point, typed coordinates). For each RP:

1. Interaction > Constraint > **Coupling**, control point = the RP, surface = the listed seat surface, type **Distributing**, all six DOF. Note (build log F-11): CAE 2022 writes `*Distributing` without a formulation keyword; the solver takes STRUCTURAL and, since all coupling nodes sit on solid elements, drops the rotational part, so the couplings act as continuum couplings. Moments (motor torque, battery rotary inertia) still pass through as force couples. A distributing coupling carries the component's load and inertia into the frame without making the seat rigid.
2. Property > Special > Inertia > **Point mass/inertia** on the RP, mass from the CSV (column `mass_t`); for `RP_BATT` also the rotary inertia I11, I22, I33 (column values, t mm^2).

| RP | Position (mm) | Mass | Coupled to |
|---|---|---|---|
| RP_BATT | (0, 0, 40) | 1.00e-4 t, I11 0.01603, I22 0.03754, I33 0.03651 t mm^2 | S_BATT_SEAT |
| RP_FC | (0, 0, 0) | 2.72e-5 t (FC + receiver 15.2 g, other hardware and wiring 12 g, A-024) | S_FC_SEAT |
| RP_GPS | (-40, 0, 28) | 8.0e-6 t | S_GPS_SEAT |
| RP_MOT_xx | (+-49.5, +-49.5, 8.5) | 1.375e-5 t each | S_MOT_SEAT_xx |
| RP_JNT_xx | (+-23.335, +-23.335, -2.5) | 3.8e-6 t each | S_JNT_xx |

## 6. Joint ties (B only)

Eight ties, two per corner: Interaction > Constraint > **Tie**, main (master) `S_PRONG_BOSS_xx_L`, secondary (slave) `S_FIN_BOSS_xx_L` (and the same for `_R`). Revised from the first version (build log DV-8): the fin face is the smaller surface and lies within the prong face, so as slave every node finds a master and a clean tie report is a real check.

| Option | Setting | Why |
|---|---|---|
| Position tolerance | specify, 0.3 mm | the faces are 0.15 mm apart; the default tolerance may miss them |
| Adjust slave surface initial position | off | keeps the geometry as designed; the tie bridges the gap |
| Tie rotational DOFs | off (no effect on solids) | |

The tie stands for the bolt preload clamping the bosses onto the fin (D-028 fallback, D-047). The fin and prong design regions are not tied: away from the bosses they only face each other across the gap.

## 7. Steps

No boundary conditions anywhere: the frame is free (D-041).

| Step | Procedure | Settings |
|---|---|---|
| `FREQ` | Linear perturbation, Frequency | Lanczos, request 20 eigenvalues, no shift. Field output: U |
| `LC1` | Linear perturbation, Static | Field output: U, S, E, ENER (whole model) |
| `LC2a` | Linear perturbation, Static | same |
| `LC2b` | Linear perturbation, Static | same |
| `LC3a` | Linear perturbation, Static | same |

Linear perturbation steps are each solved from the unloaded base state, so the load cases do not add up. History output: ALLSE and ALLWK (whole model) in each static step.

Inertia relief: in each static step, Load > Create Load > Mechanical > **Inertia relief**, region = whole model, all six free directions (default). It computes the accelerations that balance the applied loads and applies the matching inertial forces to every mass, frame and point masses alike (D-041, Step 10). No gravity load: under inertia relief a uniform gravity field is balanced by an equal and opposite acceleration and changes no stress, so leaving it out gives the same result and keeps the loads exactly as tabulated.

If CAE 2022 does not offer inertia relief in a linear perturbation step: use Static, General steps (NLGEOM off) and set every load to "inactive" in the steps where it does not belong, so the cases stay separate. Note which route worked.

## 8. Loads

| Step | Load | Where | Value |
|---|---|---|---|
| LC1 | concentrated force CF3 | RP_MOT_pp, pm, mp, mm | +5.04 N each (N-02-16) |
| LC1 | moment CM3 | RP_MOT_pp and mm / pm and mp | +40 / -40 N mm (N-02-17; net yaw zero) |
| LC2a | CF3 | RP_MOT_pp and mm | +5.04 N each |
| LC2a | CM3 | RP_MOT_pp and mm | +40 N mm each (net yaw 80 N mm) |
| LC2b | CF3 | RP_MOT_pp and pm (front pair) | +5.04 N each |
| LC2b | CM3 | RP_MOT_pp / pm | +40 / -40 N mm |
| LC3a | pressure | S_FLOOR | 0.03525 MPa (= 56.4 N over 1600 mm^2: n = 23 x 250 g, N-04) |

Positive pressure acts into the surface, so on the floor's bottom face it pushes up, as the ground does. The rotation directions are an assumption; only their pairing matters (LC2a uses a pair that turns the same way).

Because the loads are forces, the inertia relief spreads them over whatever mass the model has. At the start (solid design space, 333.7 g in total with the D-056 keel; 322.2 g before it) the load factors come out lower than the design values; as Tosca removes material they rise towards them. This is the intended behaviour: the applied thrusts and ground force are the physical inputs.

## 9. Mesh

| Item | Setting |
|---|---|
| Element | C3D10 (quadratic tetrahedron), Standard |
| Laptop build and debugging | global seed 2.5 mm, 1.5 mm on the arms and joint (roughly 60 to 120 thousand elements, a few minutes per solve) |
| Intermediate (laptop limit) | global 1.5 mm, arms 1.0 mm: about 0.45 million elements, about 2 million DOF; likely beyond 16 GB RAM with the direct solver |
| Tosca production | 0.8 mm, to resolve 2.5 mm members with three elements across (Q-49); HPC (Abaqus 2024/2025; the .inp moves forward, the .odb does not) |

Mesh > Verify: no errors; fewer than 1 % of elements with warnings (shape factor). The 0.15 mm gaps are not meshed across; the faces mesh independently and the ties connect them.

## 10. Checks before Tosca (one plain Abaqus job, no optimisation)

Run the model as a normal job (`revB_v03B_ref`) and check:

| Check | Expected |
|---|---|
| Total mass (Tools > Query > Mass properties, whole model incl. point masses) | 333.7 g with the D-056 GPS keel (frame 128.3 g solid: design 96.7 + fixed 31.6) + point masses 205.4 g; 322.2 g for the D-055 export without the keel (build log DV-3; D-054 moves 1.41 g from design to fixed without changing the total) |
| FREQ modes 1 to 6 | close to 0 Hz (well under 1 Hz) |
| FREQ mode 7 | the first elastic frequency of the solid design space; it should be above 417 Hz (the solid arm alone gave 736 Hz clamped, N-06-01) |
| Static steps | message file confirms inertia relief; no "zero pivot" or "numerical singularity" warnings |
| Displacements | smooth and small (fractions of a millimetre); no part flying away (a broken tie or coupling shows as a large rigid motion) |
| Compliance per step | C_i,0 = 2 x ALLSE at the end of each static step; these set the caps C_i <= 2 C_i,0 (A-020) |

Please send back: element count, total mass, the frequencies and mode shapes (screenshots) of modes 7 to 12, the four ALLSE values, and any warnings. Part 2 then sets up the Tosca task with these numbers.

## Assumptions added with this sheet

- A-024: other hardware and wiring (strap, FC screws, wires, antenna) 12 g (A-005) lumped at the FC; joint hardware modelled separately (15.2 g).
- Motor and prop CG at z = 8.5 mm above the pad (motor 11.6 g at about 7.75, prop 1.75 g at 15.75, screws 0.4 g at -1).
- Battery as a rigid 59 x 30 x 32 mm box of 100 g on a distributing coupling (no stiffening of the plate).
