# Stage 6 Phase 8: reference run of revB_v03B (solid design space)

For the main chat. Model `revB_v03B_D055.cae`, job `revB_v03B_ref`, Abaqus/Standard 2022. Full record: `claude/stage6_build_log_v03B.md` (Phases 7R, 8A, 8B; F-11, F-12).

## Model

| Item | Value |
|---|---|
| Geometry | `stage6_abaqus_v03B.zip` (D-054 arms, D-055 BODY fin bosses), all five parts pass the acceptance test |
| Mesh | C3D10, 145,750 elements, 227,412 nodes, 673,860 equations; BODY 2.5 mm with tie faces 1.5 mm, arms 1.5 mm (sheet section 9, laptop debug level); 0 errors, 74 warnings (0.05 %) |
| Mass | 322.1 g (frame 116.7 g + point masses 205.4 g); expected 322.2 g |
| Centre of mass | (-1.14, 0.02, 14.5) mm |
| Run | 5 threads, 242 s wallclock |

## Ties

172 untied secondary nodes, 21 or 22 per tie, all on the lower fin boss faces (z -15 to -11.25): the 10.3 mm^2 per face with no prong opposite (D-055 fin boss outline against the D-054 prong disk clipped at z = -14.5). No untied nodes on the upper bosses or elsewhere. Every joint is connected over the flat-on-flat overlap.

## Frequencies (free-free)

| Mode | f (Hz) | Shape |
|---|---|---|
| 1 to 6 | below 0.002 | rigid body |
| 7 | 365.2 | local: GPS overhang plate bending |
| 8 | 487.6 | global: arms out of plane, tips together (umbrella) |
| 9 | 521.0 | global: saddle |
| 10 | 523.9 | global: saddle, near-equal pair with mode 9 |
| 11 | 566.6 | global: arms |
| 12 | 689.0 | local: GPS overhang and front edge of the battery plate |

## Compliance caps (A-020)

| Load case | C_i,0 = 2 ALLSE (N mm) | Cap 2 C_i,0 (N mm) | Max U (mm) |
|---|---|---|---|
| LC1 | 0.1898 | 0.3796 | 0.024 |
| LC2a | 0.1436 | 0.2873 | 0.021 |
| LC2b | 0.0976 | 0.1952 | 0.016 |
| LC3a | 0.2981 | 0.5962 | 0.057 |

ALLWK = ALLSE in every step. Inertia relief confirmed by the solver; exactly 6 numerical singularity warnings per factorisation (the rigid-body directions, as announced for a model without supports).

These caps come from the debug mesh. A finer mesh is more flexible, so C_i,0 rises slightly; recompute the caps on the mesh Tosca will use.

## Notes

- Coupling formulation (F-11): CAE 2022 writes `*Distributing` with no formulation keyword. The solver defaults to STRUCTURAL and warns that it drops the rotational part because all coupling nodes are on solid elements, so the couplings behave as continuum couplings.

## Decision needed: Q-55

The first elastic mode (365 Hz) is a local mode of the GPS overhang (2.5 mm plate, x -50 to -33, 8 g GPS point mass at z = 28), not a global frame mode. It is above the D-035 minimum (290 Hz) and below the goal (417 Hz).

With the band constraint (modes 7 to 12 at least 417 Hz) it is active from the first iteration. Tosca can only remove material, and the overhang is already at its design-space limit, so the constraint is probably infeasible and would distort the result. The debug mesh has one element through the 2.5 mm thickness (too stiff in bending), so a finer mesh will likely give a lower value.

Options:
- (a) Stiffen the GPS mount in the geometry: thicker or ribbed fixed GPS frame, shorter overhang, or support from below.
- (b) Constrain only global modes and check the GPS mount separately as a component; needs a way to keep local modes out of the band (for example a MAC check against the umbrella and saddle shapes).
- (c) Accept 365 Hz for the GPS mount against the 290 Hz minimum and lower its target.

Also check whether the GPS model (8 g at z = 28) is realistic.

Mode 12 shows the battery plate front edge as well: once Tosca opens windows in the plate, that local mode may drop into the band too.
