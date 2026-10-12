# Stage 6 model set-up, part 2: the Tosca task (v03-B)

Abaqus/CAE 2022, Optimization module (Tosca Structure). Written in the main chat (2026-10-09) from decisions D-040 to D-059. Built by hand in the set-up chat (D-043). Read with `claude/stage6_handover_2_tosca.md` (context and step order) and `claude/stage6_model_setup_part1.md` (the Abaqus model).

Items marked **CHECK** depend on Tosca 2022 behaviour that has not been confirmed: verify each in the 2022 documentation or in the first two cycles, and record the result in the build log.

## 0. Before this sheet

The Abaqus model must already pass, on the mesh Tosca will use (handover steps 1 to 5):
- the reference job with the D-056 BODY (mass 333.7 g; modes 7 to 12 recorded);
- the inertia relief smoke test (LC1 with inertia relief against LC1 on 3-2-1 supports);
- the compliance reference values ALLSE_i,0 for LC1, LC2a, LC2b, LC3a on that mesh.

## 1. Mesh for the first Tosca run (D-058)

| Item | Setting |
|---|---|
| Target | BODY global 2.0 mm (tie faces 1.2 mm); arms 1.2 mm |
| Fallback | BODY 2.5 mm, arms 1.5 mm (the Phase 8 mesh) |
| How to decide | run a data check (`abaqus job=... datacheck`) and read in the .dat file the solver memory estimate ("memory to minimize I/O"). Keep the finer mesh only if that estimate stays under about 10 GB (16 GB laptop, 13.9 GB visible, other programs closed) |

Purpose of this run: confirm that the whole chain works (sensitivities with inertia relief, frequency constraint, symmetry, member size, smoothing), not to produce the final shape. The production mesh (0.8 mm) runs on the HPC.

## 2. Identical arms (D-059)

Goal: one optimised arm shape that fits all four positions (repairability, R-13).

Preferred route:
1. Keep one arm part (`ARM_pp`) with its sets and surfaces; delete the other three arm parts.
2. Create four instances of `ARM_pp`, rotated about the global z axis through the origin by 0, -90, +90 and 180 deg to the pp, pm, mp and mm positions. The four arms in the STEP files are exact 90 deg rotations of one another (generator: one local arm rotated to each corner), so the rotated instances coincide with the old parts. Check with Query > Distance that each fin boss and prong boss gap is still 0.150 mm.
3. Re-create the ties, couplings and loads that referred to the old arm parts (the set-up chat's R3 script).
4. Dependent instances share one mesh, so the four arms have identical meshes, which makes the symmetry restriction below exact.

Restriction in Tosca: Geometric restriction > **Cyclic symmetry** (rotational pattern), region = the four `DESIGN_ARM` sets, axis = global z through the origin, 4 repetitions (90 deg). **CHECK**: name and options of the restriction in 2022 (cyclic symmetry or rotational symmetry, number of sectors, tolerance), and that it may be applied to a region spanning four instances.

Fallback (if the restriction cannot be applied): run without it, then take the most conservative arm (the one under the highest-loaded case) and copy it to all four positions in Stage 7.

The body gets no symmetry: the load cases are not symmetric (LC2a and LC2b load only some motors) and the GPS sits at the back.

## 3. Task

Optimization > Create Task > **Topology optimization**, name `TO_v03B`.

| Field | Setting | Why |
|---|---|---|
| Algorithm | **General optimization** (sensitivity-based) | the condition-based algorithm handles only stiffness with a volume constraint; frequency constraints need the general one (D-040) **CHECK** |
| Design area | union of `DESIGN_BODY` and the four `DESIGN_ARM` sets (make a set `DESIGN_ALL`) | everything else is frozen |
| Freeze boundary condition regions | on (there are none; harmless) | |
| Freeze load regions | **on** | freezes the element layer under `S_FLOOR` (LC3a pressure) so the ground load always has material to act on; the coupling seats are fixed material anyway |
| Material interpolation | default (SIMP, penalty 3) | part 1 of the theory |
| Density update strategy | Normal; switch to Conservative only if the history oscillates | |
| Mass interpolation for eigenfrequencies | **CHECK** whether 2022 applies a modified mass interpolation by default (low-density elements otherwise give fake local modes, theory part 2, Step 4) | |

## 4. Design responses

Create Design Response, all single-term:

| Name | Variable | Region / step | Operator | Notes |
|---|---|---|---|---|
| `R_VOL` | Volume | `DESIGN_ALL` | sum | objective |
| `R_FREQ` | Eigenfrequency | whole model, step `FREQ`, modes 7 to 12 | minimum (or the list form, one value per mode) | **CHECK** units: Hz or eigenvalue (417 Hz = 6.865e6 (rad/s)^2) |
| `R_SE_LC1` | Strain energy | whole model, step `LC1` | sum | |
| `R_SE_LC2a` | Strain energy | whole model, step `LC2a` | sum | |
| `R_SE_LC2b` | Strain energy | whole model, step `LC2b` | sum | |
| `R_SE_LC3a` | Strain energy | whole model, step `LC3a` | sum | |

Strain energy, not compliance: the compliance is C = 2 x ALLSE, so the cap C_i <= 2 C_i,0 (A-020) is the same as **ALLSE_i <= 2 ALLSE_i,0**.

## 5. Objective and constraints (D-042)

| Item | Setting |
|---|---|
| Objective | minimise `R_VOL` |
| Constraint 1 | `R_FREQ` >= 417 Hz for modes 7 to 12 (one bound per mode if Tosca lists them separately). The band includes local modes on purpose (D-056) |
| Constraints 2 to 5 | `R_SE_LCi` <= 2 x ALLSE_i,0, the four reference values from the solid design space on this mesh |

Mode tracking (MAC): off. With a band of six modes all held to the same bound, the order of the modes does not matter (theory part 2, Step 5).

## 6. Geometric restrictions

| Restriction | Setting | Notes |
|---|---|---|
| Frozen area | `FIXED_BODY` and the four `FIXED_ARM` sets | joint bosses, motor pads, FC bosses, plate and GPS frames |
| Member size | minimum 2.5 mm (D-057) | on the 1.2 to 2.0 mm debug mesh this is only about one to two elements across, so it is approximate; it becomes meaningful at 0.8 mm. **CHECK** that member size is available with the general algorithm and frequency responses in 2022 |
| Cyclic symmetry | arms only, section 2 | |
| Demould / overhang | not used in the first run | printability is judged on the result first (D-044) |

## 7. Stop criteria and output

| Item | Setting |
|---|---|
| Maximum design cycles | 30 for the first local run (enough to see the trend; the HPC runs go to convergence) |
| Convergence | defaults |
| Save | every cycle for the first run (small model), so the history can be inspected |
| Results | `TOSCA_POST/*.odb` with the density field; history of `R_VOL`, `R_FREQ`, `R_SE_*` |

Optimization Process: create in the Job module, linked to the model and task; Submit; monitor the `.onf` / status and the Tosca log.

## 8. First run: what to look at, in order

1. **Cycles 1 and 2 (the Tosca smoke test, D-041):** both complete; the inertia relief steps run inside Tosca; the strain energy values of cycle 1 equal the reference ALLSE_i,0 (the design starts solid or at Tosca's initial density, **CHECK** which).
2. **Mode shapes at cycle 1 and every few cycles:** modes 7 to 12 must be frame or real local modes. A mode whose motion sits in grey or void elements is a fake low-density mode: stop and change the mass interpolation setting.
3. **History:** volume should fall; the frequency and strain energy constraints should become active and stay satisfied (feasible at the end). Oscillation: switch the density update to Conservative.
4. **Symmetry:** the four arm density fields must be identical.
5. **Shape:** density iso-surface at 0.3 and 0.5 (Optimization > Smooth / Extract, **CHECK** the 2022 menu name). Note the mass at each threshold against the B allowance (about 13 g of design material, Q-53).
6. **Report back to the main chat:** final volume and mass, final frequencies (modes 7 to 12) and strain energies against the caps, cycle count and run time, peak memory, screenshots of the density field (iso 0.3 / 0.5) from three views, and every CHECK item with its answer.
