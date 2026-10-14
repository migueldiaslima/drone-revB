# Sources of chapter 11 (sections 11.1 to 11.3)

Set-up chat, 2026-10-14. Labels used in the comment block at the end of `report/extensive/chapters/11_strength.tex`. Section 11.4 (capacity ordering) is written by the main chat.

| Label | Source | What it gives |
|---|---|---|
| W1 | `docs/stage7_brief.md` (a), (b), (c), (d); journal N-05-03, D-038 | 64 and 28.1 MPa source strengths, x 0.85, S_xy 54.4, S_z 23.9 MPa, FoS 1.5, allowables 36.3 and 15.9 MPa; compression equal to tension; S_z as shear allowable (assumption); build direction +z, tub floor-down; three checks; max principal within 15 % of von Mises at sigma_2 = sigma_1 / 2; centroid values, volume-weighted P99.9, cluster rule (1 mm^3, about 8 elements, on the surface), exclusions |
| W2 | build log items 64, 65; `docs/stage6_v04B_H4_report.md` | final thresholded model: 1.0 mm C3D10, 511,770 of 765,252 elements solid |
| W3 | `docs/stage7_data/stress_TH_r4b_i30_final.txt` (raw output of `scripts/post/stress_th.py`) | 30 tie and coupling surfaces, 78,733 excluded elements (71,564 solid); per part, step and check: P99.9, max, clusters, excluded max; top ten elements with coordinates (arm peaks at (40.0, 47.0, 0.1) and mirror positions, u = (x + y) / sqrt(2) = 61.5 mm; lid peaks at x -17.4 to -18.5, z 22.7 to 23.6; tub LC3a peaks at (+-9.5, +-10, -11.5 to -12.3) and (+-15.1, +-23.1, 9.8)) |
| W4 | build log item 67; `scripts/post/test_stress/` | offline test: 6 parts, surface hot spot passes, 27 mm^3 through-thickness block fails, tie peak excluded, 72 rows equal to an independent computation |
| W5 | `docs/stage7_strength_report.md`; `data/report/stage7_strength.csv` | results table, governing case LID LC3a 1.42 / 2.43 MPa, utilisation 0.04, margin about 25, excluded maxima 2.24 (LID) and 2.11 MPa (TUB) |
| W6 | journal D-036, N-04-06 | LC3a firm landing, n = 23 |
| W7 | journal D-035, D-042 | frequency requirement 417 Hz |
| W8 | `scripts/figures/fig_strength_vm.py` on `stress_TH_r4b_i30_final_LC3a.npz` (written by `stress_th.py` on nexus) | 440,206 checked solid elements (511,770 - 71,564); largest 2.43 MPa (agrees with W3); frame volume-weighted P99.9 0.89 MPa (figure scale); checked TUB solid volume 32,812.9 mm^3 (0.1 % = 32.8 mm^3, cube side 3.2 mm) |

Figure: `report/figures/su_strength_vm_LC3a.png`, from `scripts/figures/fig_strength_vm.py <npz> <png> "landing case"`. It replaces `su_stage7_vm_LC3a.png` in the report (that file has an internal job name in its title and is left in place; Miguel decides whether to delete it).

Arithmetic shown in the text: 0.85 x 64 = 54.4, 54.4 / 1.5 = 36.3; 0.85 x 28.1 = 23.9, 23.9 / 1.5 = 15.9; sqrt(1 - 1/2 + 1/4) = 0.866; 2.43 / 36.3 = 0.067 (largest element) and 1.42 / 36.3 = 0.039 (P99.9, the 4 % and margin about 25).
