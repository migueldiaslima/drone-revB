# Stage 6 handover 2: from the Phase 8 reference run to the first Tosca run (v03-B)

For the Abaqus set-up chat. Written in the main chat on 2026-10-09. It brings the set-up chat up to date with everything decided since `claude/stage6_phase8_reference_results.md`, explains the reasoning, and lists the next steps in order.

Read with:
- `claude/stage6_model_setup_part2_tosca.md`: the Tosca sheet (new);
- `claude/stage6_v03B_export_note.md`: files, volumes, mesh tests;
- `claude/stage6_model_setup_part1.md`: the Abaqus model sheet (updated);
- `claude/journal_quadcopter.md`: master record (D-054 to D-059, F-028 to F-031, N-06-05, N-06-06, Q-53).

Files: `stage6_abaqus_v03B.zip` from the main chat (BODY.step with the flared keel, ARM_xx.step unchanged since D-054, reference_points.csv unchanged, scripts incl. `s06_gmsh_meshtest.py`, figure `fig06_tangency.png`).

## 1. Where we stand

| Item | State |
|---|---|
| Variant | B, repairable (J3 fin-and-fork joint, steel M3 x 20, D-047 to D-051) |
| Geometry | D-054 arms (unchanged), D-055 fin bosses, D-056 flared GPS keel (BODY only changed) |
| Model | built and run (Phase 8) with the D-055 BODY; BODY to be re-imported with the keel |
| Mass, solid design space | 333.7 g expected (frame 128.3 g: design 96.7 + fixed 31.6; point masses 205.4 g) |
| B allowance (R-01, AUW < 250 g) | about 13.0 g of design material (Q-53) |
| Variant C (one-piece) | later, same model with the joint region changed (D-053) |

## 2. Decisions since the Phase 8 summary

### D-054, D-055: design/fixed split rules (meshing)
- **What went wrong.** The old split bounded the fixed bolt bosses by flat planes and circles that touched other boundaries tangentially: the slot-end semicircle (R 5.15) touched the boss plane (5.15 mm from the arm axis), and the Ø12 upper boss circle touched the arm top (z = 10). Near a tangent contact the material between the two boundaries is a wedge whose thickness grows from zero as t = d^2 / (2R) (6 um at 0.25 mm from the contact, R = 5.15). Filling it needs either micrometre elements or flat sliver tets, so Abaqus failed ("poor boundary triangles") at any seed. The bolt hole, 0.25 mm past the slot-end tangent line, cut that wedge into 3 um crescents. See `fig06_tangency.png` (a1, a2, b).
- **Fix.** Bosses as full Ø12 cylinders through the fork; the upper boss extended straight up to the arm top (D-054); the same for the fin bosses to the fin top and bottom (D-055). Boundaries now cross at clear angles or stay apart.
- **Rule for every future change:** two region boundaries must never touch tangentially or nearly so; they cross at a clear angle or stay at least about one element size apart.

### D-056: GPS keel (Q-55)
- **Problem.** Phase 8 mode 7 (365.2 Hz) was the GPS overhang plate bending under the 8 g GPS: a 2.5 mm plate cantilevered 30 mm behind the body, already at its design-space limit, so Tosca could not raise it and the 417 Hz band would be infeasible from cycle 1.
- **Options considered.** (a) stiffen in geometry; (b) constrain global modes only (MAC filtering, feasibility in Tosca unconfirmed); (c) accept 365 Hz. Chosen (a): the GPS mount also sees the 1P sweep (241 to 679 Hz) in flight, so a resonant mount would fatigue the plate; and the band constraint stays simple.
- **First version.** A 3 mm keel on the centreline, the only corridor between the rear prop keep-outs (the centreline is 2.05 mm outside both).
- **Final version (Miguel's proposal).** Flared like the arm roots, where the root moment is largest: block x = -50 to -19, y = +-9, z = 0 to 21.5, with the rear prop keep-outs cut from it. Above z = 10 it fills the corridor (4.1 mm wide at the GPS end, 18 mm near the body); below z = 10 the full 18 mm. All design space, so Tosca trims it.
- **Why half-width 9, not 11 (F-031).** The fin root fillets (R5) meet the body rear face tangentially along y = +-10.86 (z = -15 to 10). A keel side at y = 11 sat 0.14 mm from that line: the same near-tangency. The face-size test passed it; the gmsh mesh test found 9 slivers (quality 0.002) exactly there. At y = 9 (1.86 mm clear) the mesh is as good as before the keel.
- **Bottom at z = 0:** the rear-left motor-wire channel exits the rear face near the centreline at z = -8 to -3 (3 mm clear).
- **Overlap of 1 mm into the body rear face:** keel and body are both design space and merge into one region with no internal face; this is not a design/fixed boundary.

### D-057, D-058, D-059: first Tosca run (Q-49, Q-56, Q-57)
- **D-057, member size 2.5 mm** (6 lines of 0.42 mm with a 0.4 mm nozzle). On the debug mesh it is only one to two elements across, so it is approximate there; meaningful at the 0.8 mm HPC mesh.
- **D-058, first-run mesh:** BODY 2.0 mm (tie faces 1.2), arms 1.2 mm, if the data-check memory estimate stays under about 10 GB; otherwise the Phase 8 mesh (2.5 / 1.5). Purpose: prove the chain works quickly, then move to the HPC.
- **D-059, identical arms:** one optimised arm for all four positions (repairability). One arm part instanced four times (rotations 0, -90, +90, 180 deg about z) plus a Tosca cyclic symmetry restriction on the arm design sets. Verified in the main chat: rotating ARM_pp by -90 / +90 / 180 deg reproduces ARM_pm / mp / mm exactly (Boolean difference 0.0000 mm^3). No symmetry for the body.

## 3. Numbers to carry

| Item | Value |
|---|---|
| BODY design / fixed | 42,206.2 / 12,597.9 mm^3 |
| Each arm design / fixed | 8,036.9 / 2,933.5 mm^3 |
| Fixed mass | 31.63 g (fin bosses 11.38, prong bosses 11.91, plate frame 3.43, motor pads 3.34, FC bosses 1.03, GPS frame 0.53) |
| Model total, solid design space | 333.7 g |
| Phase 8 (D-055 BODY, 2.5 / 1.5 mesh) | modes 7 to 12: 365.2 (GPS, local) / 487.6 / 521.0 / 523.9 / 566.6 / 689.0 (local) Hz; ALLSE x 2 = 0.1898 / 0.1436 / 0.0976 / 0.2981 N mm |
| Caps | recompute on the Tosca mesh with the keel: ALLSE_i <= 2 ALLSE_i,0 |
| Mesh tests, D-056 BODY | face test pass (smallest 8.04 mm^2, narrowest 0.80 mm); gmsh 1.5 mm: 0 slivers, min quality 0.1265 |
| Watch item | at 1.0 mm, 25 tets of quality about 0.02 in existing BODY features (fin fillet ends at z = 10 near y = +-11.4; 1 mm waist between the two fin bosses near the fin nose); present before the keel; check at 0.8 mm |

## 4. Next steps (in order)

| # | Step | Pass criteria |
|---|---|---|
| 1 | Re-import BODY.step (R2 to R4); arms as in step 2 of the Tosca sheet (one part, four instances) | BODY design 42,206.2, fixed 12,597.9 mm^3; arm gaps 0.150 mm; 0 mesh errors |
| 2 | Choose the Tosca mesh (sheet section 1): data check at 2.0 / 1.2 | memory to minimize I/O under about 10 GB, else 2.5 / 1.5 |
| 3 | Reference job on that mesh | mass 333.7 g (+-0.1 %); rigid modes < 1 Hz; GPS mode now well above 417 Hz; record modes 7 to 12 and their shapes; flag any local mode left in the band |
| 4 | Inertia relief smoke test (D-041) | LC1 with inertia relief against LC1 on 3-2-1 supports: reactions near zero; whole-model strain energies within a few per cent |
| 5 | Caps | ALLSE_i,0 for the four load cases on this mesh; caps 2 x ALLSE_i,0 |
| 6 | Build the Tosca task (part 2 sheet) | every CHECK item answered and recorded |
| 7 | First Tosca run, 30 cycles | sheet section 8 |
| 8 | Report to the main chat | sheet section 8, item 6 |

Later (main chat decides): HPC production runs at 0.8 mm; frequency sweep 290 / 350 / 417 Hz (D-035); variant C (D-053); Stage 7 checks (fin-root section modulus >= 390 mm^3, D-051; arm section modulus at the fork exit <= 260 mm^3, D-050; LC3b, LC4; buckling; battery support rib spacing A-023).

## 5. Working rules (unchanged)
- Miguel builds by hand in CAE; scripts only where already agreed (R1 to R4) or as a fallback.
- Explain the physics and the effect on the project of each setting; label assumptions; never invent values.
- Record every deviation from the sheets, with the reason, in the build log.
- Any geometry change goes back to the main chat; new exports must pass both the face test (`s06_split_acceptance.py`) and the gmsh test (`s06_gmsh_meshtest.py`).
- No em dashes; direct headings; derivations as phrased steps.
