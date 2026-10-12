# drone-revB

Quadcopter frame rev B (3.5 inch true X, PET-CF, topology-optimised with Abaqus/Tosca). Owner: Miguel Dias de Lima.

## Layout

| Folder | Content |
|---|---|
| `docs/` | All project docs (copies of the claude.ai project "Drone Rework"). `journal_quadcopter.md` is the master record |
| `geometry/v04B/` | Current export, v04-B revision 2: TUB, LID, ARM_xx, KEEPOUTS, COMPONENTS (STEP), reference points, volumes and gate results |
| `geometry/v03B_arms/` | v03-B arm STEPs (D-054 split), kept for reference |
| `scripts/geometry_main/` | Main-chat generators and gates (CadQuery, gmsh, renders) |
| `scripts/cae_v03B/` | Abaqus/CAE 2022 scripts for the v03-B model (R1 to R13) |
| `scripts/cae_v04B/` | Abaqus/CAE 2022 scripts for v04-B (V1 build, V2 mesh, V3 jobs, W1/W2 Tosca task, D1 diagnostics) |
| `scripts/hpc/` | nexus run scripts and checks per run: H0H1, H2, H3ref, H3, G7, H4, threshold, TH04 |
| `scripts/post/` | Post-processing (iso surfaces, cycle checks) |
| `figures/` | Figures used in the docs |

Not in the repo (size): odb, inp, par, cae, stl. Those live on nexus (`/tmp/mdias_*`, `~/drone_revB/stage6`) and on Miguel's laptop.

## Status (2026-10-12)

| Item | State |
|---|---|
| Journal | v0.53 (D-001 to D-085) |
| Build log | items 1 to 45, DV-1 to DV-25 |
| H4 (v04-B rev 2) | converged at cycle 31; TH04b_ni passes, TH04a_ni fails as expected (N-06-17, N-06-18); antenna boss island F-036 |
| v04-B revision 3 (D-084, antenna spine) | exported to `geometry/v04B_r3/`, gates G0 to G5 pass (`docs/stage6_v04B_r3_export_note.md`) |

## Open tasks

| # | Task | Owner |
|---|---|---|
| 1 | Rebuild the model from revision 3, reference job, H4 rerun with D-083 caps; report the cycle 0 ALLSE in N mm | set-up chat |
| 2 | TH at iso 0.4 with the island check (D-085); H4 report: history, seat densities, T-1 to T-7, restoration at iso 0.4 with fillet pass B and SPINE_fixed_v04B_r3.stl | set-up chat |
| 3 | Tub print orientation (floor-down or rim-down, D-082 flatness) | Miguel |
| 4 | Optional: ALLWK vs ALLSE check on an older odb (G7 report, "Also noted") | set-up chat |
| 5 | Q-58 to Q-60 (GM10 wiring and plugs, FC heat-sink height) | Miguel |

See `CLAUDE.md` for the working rules.
