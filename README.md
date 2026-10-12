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

- H4 (v04-B, 1.0 mm mesh, G7b seat tie, member size 2.5 mm) converged at cycle 31.
- Next: TH04 (thresholded check at iso 0.4 with both lid connections, D-082), then the H4 report.

See `CLAUDE.md` for the working rules.
