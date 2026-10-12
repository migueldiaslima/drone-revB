# Stage 6: HPC runs H0 and H1 (v03-B), short report

For the main chat, after H1 as the HPC plan asks (`claude/stage6_hpc_plan.md`). Written in the set-up chat on 2026-10-09. Full record: `claude/stage6_build_log_v03B.md` (Phase H, DV-17, DV-18, F-14).

## Result

H0 and H1 both pass. The model runs on the HPC with Abaqus/Tosca 2025. Tosca 2025 accepts inertia relief with the sensitivity-based algorithm (the F-032 limit is gone). One model change was needed for the 2025 solver (DV-18). The run is stopped before H2, as the plan asks.

## HPC set-up (DV-17)

| Item | Value |
|---|---|
| Machine | nemix.fe.up.pt: 2 x Xeon Gold 6130 (32 cores), 125 GB RAM, no job scheduler (jobs started from the shell with nohup) |
| Software | Abaqus 2025 (`abq2025`), Tosca Structure R2025x build R427; FlexNet licence server on the machine, 9999 tokens per feature (`standard`, `TOSCA_TOPO`, `TOSCA_INT_ABAQUS`) |
| Storage | `/home` 2.8 TB free, no quota; project folder `~/drone_revB/stage6/{inputs,H0,H1,H2,H3,scripts}` |
| Run settings | 16 CPUs, memory cap 35 %; the only `.par` edit is the `driver.Solver.AddCallArgs` line |

## F-14 and DV-18: supports needed in Abaqus 2025

- **Finding (F-14).** The first H0 run reproduced the mass, the six frequencies and LC1 exactly, but LC2a, LC2b and LC3a gave strain energies of 1e6 to 1e9 N mm.
- **Cause.** Abaqus 2025 reuses the LC1 factorisation for those steps. Abaqus 2022 re-factorised at LC2a and LC2b ('load applied to a DOF without stiffness'). With no supports, the inertia-relief singularity is regularised inside the factorisation, and that is not valid for other load vectors. The solver warned in every step to use statically determinate supports.
- **Fix (DV-18).** 3-2-1 supports in every static step: `RP_JNT_pp` U1 U2 U3, `RP_JNT_pm` U1 U3, `RP_JNT_mp` U3. Inertia relief kept; FREQ stays free-free. This is the arrangement D-041 describes and the one tested locally in T4.
- **Result.** H0 run 2 matches 2022 on every quantity, and the support reactions are below 1.5e-11 N. The supports carry nothing, so the physics is unchanged and the D-063 caps stand.

## H0 (version check)

| Quantity | Abaqus 2025 | 2022 | Difference |
|---|---|---|---|
| Mass | 333.698 g | 333.70 g | -0.001 % |
| Modes 7 to 12 | 489.93 / 521.51 / 524.32 / 573.63 / 681.81 / 749.44 Hz | same | 0.000 % |
| ALLSE LC1 / LC2a / LC2b / LC3a | 0.0908934 / 0.0698767 / 0.0454587 / 0.10466 N mm | 0.090893 / 0.069877 / 0.045459 / 0.10466 | at most 0.001 % |
| Support reactions | below 1.5e-11 N | | |

Run time 2 min (laptop 4 min); peak memory 9 GB.

## H1 (Tosca, 3 cycles, inertia relief)

| Cycle | Volume (mm^3) | f7 | f8 | f9 | f10 | f11 | f12 (Hz) | SE / cap (LC1 / 2a / 2b / 3a) |
|---|---|---|---|---|---|---|---|---|
| 0 | 74,740 | 489.9 | 521.5 | 524.3 | 573.6 | 681.8 | 749.4 | 0.50 / 0.50 / 0.50 / 0.50 |
| 3 | 60,598 | 428.2 | 445.7 | 453.0 | 475.9 | 541.0 | 624.9 | 0.69 / 0.72 / 0.74 / 0.80 |

- **Checks.** Preprocessor accepted the 2022 `.par` and inertia relief; cycle 0 equals H0; volume falls 19 % in 3 cycles; all constraints satisfied.
- **Run.** 14.7 min in total, about 3.5 min per cycle; 2.7 GB on disk.
- **Constraints.** f7 is 11 Hz above the 417 Hz bound, so the frequency band becomes active within one or two cycles. Mode 11 (battery plate front edge) is again the fastest-falling mode. LC3a is the closest strain-energy cap (0.80).
- **Same history as T7.** Volume and frequencies are identical to the local chain test without inertia relief, as expected: no strain-energy constraint is active yet, and the frequency responses do not depend on the static load cases.
- **C-3 still open.** The 2025 log does not name the interpolation used for the frequency responses. To be checked through the mode shapes in H2 (spurious low-density modes).

## Proposed H2 settings (for confirmation)

| Item | Proposal |
|---|---|
| Model and mesh | `revB_v03B` as in H1 (DV-18), 2.5 / 1.5 mm |
| Cycles | maximum 60, Tosca default convergence (D-061) |
| Save | every 5 cycles plus the last (about 690 MB per saved cycle, about 9 GB in total); matches the mode check every 5 cycles |
| Expected run time | about 3.5 h for 60 cycles |
| Checks | constraints at the end; modes 7 to 12 at cycles 5, 10, ... for low-density modes; arm fields identical; mass at iso 0.3 and 0.5 against the B allowance (about 13 g, Q-53) |

## Decisions for the main chat

1. Accept DV-18 (3-2-1 supports with inertia relief in every static step) as the model for H2 and H3, and record F-14.
2. Confirm the H2 settings above.
