# Sources of the numbers in report/extensive/chapters/08_optimisation_model.tex

Labels S1 to S14 are used in the comment block at the end of the chapter. Kept outside the report folder so that internal IDs and file names do not travel with the Overleaf zip.

| Label | Source |
|---|---|
| S1 | journal numbers register N-06-20 (revision 4 export); `docs/stage6_v04B_r4_export_note.md`; arms N-06-15 |
| S2 | `docs/stage6_model_setup_part1.md` sections 2 (material), 6 (ties); material model D-045, A-021 |
| S3 | build log item 49 (V1r4 checks, G6 production mesh 765,252, warnings, G7b_r4_ref mass, modes, reactions, untied nodes); `docs/stage6_v04B_H4_report.md` "Model and reference job" |
| S4 | `docs/stage6_hpc_H2_report.md` "H3 reference (1.0 mm) and caps" (mesh convergence); `docs/stage6_tosca_chain_test_report.md` (inertia relief smoke test 0.000 %, 2.4e-11 N; local refusal F-13) |
| S5 | build log line on member size ("minimum member size must exceed twice the average element size"), chain test report C-5 |
| S6 | `geometry/v04B_r4/reference_points_v04B.csv` (masses, positions, seats); total 199.58 g also build log item 49 |
| S7 | `docs/stage6_v04B_G7_report.md` (G7a 389.8 / 405.1 Hz, G7b 449.7 Hz, lid modes 571.3 Hz); D-082 (flatness 0.1 mm) |
| S8 | `docs/stage6_model_setup_part1.md` section 8 (loads); journal N-02-16, N-02-17, N-04-01, N-04-06, N-04-07; `scripts/cae_v04B_r4/V1r4_build.py` line 280 and 512 (S_FLOOR 2060.58 mm^2, LC3a 0.027371 MPa); net thrust 20.16 N journal Stage 4 line |
| S9 | `docs/stage6_hpc_H1_report.md` (F-14, DV-18: 1e6 to 1e9 N mm without supports, agreement 0.001 %, smoke test -19 %) |
| S10 | build log item 50; journal N-06-21; `docs/stage6_v04B_H4_report.md` "H4 run" (cycle-0 strain energies, caps, history, saved cycles, cyclecheck cycle 28, 259,292 elements, iso 0.3 / 0.5 kept volumes); c28.odb size 2,970,437,784 bytes (nexus ls, 2026-10-13) |
| S11 | `docs/stage6_hpc_H2_report.md` (F-15 threads, mode-check rule 0.8 / 0.3, grey arms 0.2 to 0.35) |
| S12 | `data/report/h4r4_history.csv` (cycle-by-cycle values: 444.3 Hz cycle 0, 421.2 Hz cycle 4, volume steps 1,633 to 3,464 mm^3 per cycle in cycles 0 to 14, 325.1 Hz cycle 15, SE/cap 1.06 at cycles 17 to 19) |
| S13 | build log item 65, `docs/stage6_v04B_H4_report.md` "T-4 on the print geometry" (431.0 Hz) |
| S14 | figure run on the final thresholded model (2026-10-14): `export.log` (30 tie and coupling surfaces, 12 reference-point node sets, element counts per part); figures `su_th_setup.png` and `su_iso_snapshots.png` from `scripts/figures/fig_th_figs.py` and `fig_iso_snapshots.py` (PR #44) on `th_figs.npz` and the iso 0.3 STLs of cycles 0, 10, 20, 28 |

Computed in the text: nu31 = 0.35 x 2890 / 5058 = 0.20; 259,292 / 765,252 = 33.9 %; 63,912 - 61,947 = 1,965 mm^3, x 1.30e-3 g/mm^3 = 2.6 g; 417^2 = 1.7e5 Hz^2.
