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
| Journal | v0.52 (D-001 to D-082) |
| Build log | items 1 to 42, DV-1 to DV-25 |
| H4 (v04-B, 1.0 mm, G7b seat tie, member size 2.5 mm, caps 2.0 x cycle 0) | converged at cycle 31 (build log item 42) |
| Cycle 31 files | frozen in `/tmp/mdias_H4/TH` on nexus (`c31.odb`, `TO_v04B_H4-Job.inp`, `tosca_distribution.inp`) |

## Open tasks

| # | Task | Owner |
|---|---|---|
| 1 | TH04 (iso 0.4) with both lid connections, D-082 b: `cd /tmp/mdias_H4/TH && bash ~/drone_revB/stage6/scripts/run_TH04.sh 30` (`scripts/hpc/TH04`) | set-up chat |
| 2 | H4 report: history, D-082 b seat densities, T-1 to T-7, restoration at iso 0.4 with fillet pass B | set-up chat |
| 3 | Confirm DV-25 (H4c skipped, relative caps) | main chat |
| 4 | Optional: ALLWK vs ALLSE check on an older odb (G7 report, "Also noted") | set-up chat |
| 5 | Q-58 to Q-60 (GM10 wiring and plugs, FC heat-sink height) | Miguel |

See `CLAUDE.md` for the working rules.
