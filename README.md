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

## Status (2026-10-13)

| Item | State |
|---|---|
| Journal | v0.56 (D-001 to D-088) |
| Build log | items 1 to 58, DV-1 to DV-26 |
| H4 (v04-B rev 2) | converged at cycle 31; TH04b_ni passes, TH04a_ni fails as expected (N-06-17, N-06-18); antenna boss island F-036 |
| v04-B revision 3 (D-084, antenna spine) | exported to `geometry/v04B_r3/`, gates G0 to G5 pass (`docs/stage6_v04B_r3_export_note.md`); boss 5 island in H4 cycle 31 (F-037) |
| v04-B revision 4 (D-086, GPS deck on the TUB, four lid bosses) | exported to `geometry/v04B_r4/`, gates G0 to G5 pass (`docs/stage6_v04B_r4_export_note.md`) |
| H4 (v04-B rev 4) | converged at cycle 28; TH at iso 0.4 fails on the GPS deck (F-038); keels A + B with the keel zone cleaned pass (TH_r4b_cAB, N-06-21) |
| Keels A and B (D-087) | exact solids in `geometry/v04B_r4_keels/` (`docs/stage6_v04B_r4_keels_export_note.md`) |
| Receiver cradle | v2 in `geometry/retainers/` (`docs/retainer_rx_cradle_note.md`) |

## Open tasks

| # | Task | Owner |
|---|---|---|
| 1 | Restoration of H4 rev 4 cycle 28 at iso 0.4 with the clean keel zone and the exact fixed solids (spine, deck, keels A and B); optional confirmation TH with the exact keels | set-up chat |
| 2 | T-1 to T-7 and the H4 report | set-up chat |
| 3 | Tub print orientation (floor-down or rim-down, D-082 flatness) | Miguel |
| 4 | Optional: ALLWK vs ALLSE check on an older odb (G7 report, "Also noted") | set-up chat |
| 5 | Q-58, Q-59 (GM10 wiring and plugs); Q-60 at the first cradle fit | Miguel |
| 6 | TPU skid plate, GPS cap | main chat |

See `CLAUDE.md` for the working rules.
