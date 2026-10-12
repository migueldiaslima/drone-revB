# Stage 6: Tosca chain test and the inertia relief limit of Abaqus 2022 (v03-B)

For the main chat. Written in the set-up chat on 2026-10-09 after handover 2 steps 1 to 7. Full record: `claude/stage6_build_log_v03B.md` (Phases T1 to T7, DV-10 to DV-16, F-13, CHECK items C-1 to C-7).

## Summary

- Steps 1 to 6 of handover 2 are done and pass.
- Tosca 2022 rejects inertia relief with the sensitivity-based (general) algorithm (F-13). The local 30-cycle run is therefore not possible.
- A 3-cycle chain test without inertia relief, on 3-2-1 supports, showed every other part of the setup working.
- The first optimisation with inertia relief has to run on the HPC with Abaqus 2023 or later.

## Model state (handover steps 1 to 5)

| Item | Result |
|---|---|
| BODY (D-056 keel) | design 42,206.1 mm^3 (1 cell), fixed 12,597.9 mm^3; seats and tie faces unchanged |
| Arms (D-059) | one part `ARM`, four instances rotated 0 / -90 / +90 / 180 deg; all 8 joint gaps 0.150 mm; generic surface names (DV-10) |
| Mesh (D-058) | target 2.0 / 1.2 mm needed 20.8 GB (memory to minimise I/O); fallback 2.5 / 1.5 mm used: 149,305 C3D10, 10.5 GB, 236 s per full analysis |
| Mass | 333.70 g (expected 333.7 g) |
| Modes 7 to 12 | 489.9 umbrella / 521.5, 524.3 saddle pair / 573.6 arms / 681.8 local (battery plate front edge) / 749.4 mixed Hz; GPS mode gone from the band (D-056 works) |
| ALLSE_i,0 | 0.090893 / 0.069877 / 0.045459 / 0.10466 N mm (LC1 / LC2a / LC2b / LC3a); caps 2 x these. LC3a fell 30 % from Phase 8 because the keel supports the rear of the plate |
| Inertia relief smoke test (D-041) | LC1 with inertia relief plus 3-2-1 supports: reactions below 2.4e-11 N (net thrust 20.16 N), ALLSE equal to the free run (0.000 %) (DV-11) |

## Tosca task (handover step 6, CHECK items)

| # | Answer |
|---|---|
| C-1 | The 90 deg arm pattern is 'Rotational symmetry' in CAE ('Cyclic symmetry' is a translational repeat); applied to the four `DESIGN_ARM` sets across four instances; works (identical arm density fields) (DV-12) |
| C-2 | General algorithm required for frequency; inertia relief needs Abaqus sensitivities and, in 2022, is refused (F-13) |
| C-3 | Interpolation left at 'product default' (Tosca switches to PEDE with a dynamic step, per the documentation); not named in the 2022 log: open |
| C-4 | Frequencies in Hz (cycle 0 values equal the reference frequencies) |
| C-5 | Member size needs a minimum above twice the element size; 2.5 mm is not meaningful on 2.5 / 1.5 mm elements; left out of the local test (Q-T1, DV-15), for the 0.8 mm HPC mesh |
| C-6 | Default start density is 0.5 when volume is the objective; set to 1.0 so cycle 0 is the solid reference (DV-13); confirmed |
| C-7 | Results are combined and extracted from the Optimization Process Manager ('Results', 'Extract...') |

Frequency responses: one 'Eigenfrequency from modal analysis' response per mode (7 to 12, Range lower = upper), each constrained >= 417 Hz; one response over the range would sum the frequencies.

## F-13: inertia relief in Tosca 2022

The Tosca 2022 preprocessor stops with 'Inertia relief is not allowed for sensitivity-based topology optimization'. The Tosca documentation for 2023, 2024 and 2025 says 'Inertia relief is supported only during optimization using 3D elements and Abaqus sensitivities'. The 2026-10-06 check behind D-041 relied on the list of unsupported keywords, which does not show this limit.

Consequence: optimisation runs with inertia relief need Abaqus 2023 or later (the HPC has 2024/2025). D-041 itself (inertia relief as the load balance) is confirmed in Abaqus (smoke test); only its use inside Tosca 2022 fails.

## Chain test without inertia relief (DV-16)

Copy model `revB_v03B_NOIR`: inertia relief removed, 3-2-1 supports in the four static steps only (FREQ stays free-free), strain energy caps as 2.0 times the cycle 0 value, 3 cycles. Completed in 17 min.

| Cycle | Volume | f7 | f8 | f9 | f10 | f11 | f12 (Hz) | SE / SE0 (LC1 / 2a / 2b / 3a) |
|---|---|---|---|---|---|---|---|---|
| 0 | 1.000 | 489.9 | 521.5 | 524.3 | 573.6 | 681.8 | 749.4 | 1.00 / 1.00 / 1.00 / 1.00 |
| 3 | 0.809 | 428.2 | 445.7 | 453.0 | 475.9 | 541.0 | 624.9 | 1.38 / 1.47 / 1.37 / 1.60 |

- Works: Abaqus sensitivities for all five steps; Hz; solid start; rotational symmetry (four identical arm fields); constraint handling (all satisfied, f7 near the bound).
- First material to go: battery plate windows, GPS pad, keel (density about 0.64 at cycle 3).
- Mode 11 (battery plate front edge, local) falls fastest: 681.8 to 541 Hz in 3 cycles. It will likely be the first band constraint to become active, and should make Tosca keep support under the plate.
- Not testable in 3 cycles: spurious low-density modes (no element below 0.64 yet). Check modes 7 to 12 every few cycles on the HPC.
- The shapes are not meaningful (unbalanced 20 N thrust reacted at the supports).

## For the HPC run (decisions for the main chat)

1. Abaqus/Tosca 2023 or later: the run uses `revB_v03B` as is (inertia relief, absolute caps). CAE 2022 writes the `.inp` and `.par` (Optimization Process > Write Files); the HPC runs them with its newer version.
2. First HPC run: the same 2.5 / 1.5 mesh, 3 cycles, as the inertia relief smoke test inside Tosca (sheet section 8 item 1); then the full run to convergence.
3. Production mesh 0.8 mm with member size 2.5 mm (C-5), and the caps recomputed on that mesh (a reference job there first).
4. Watch item: the battery plate front-edge mode (mode 11) as the first active frequency constraint.
5. Documentation: export note mass line reads '324.7 g with the D-056 keel'; 333.7 g is correct.
