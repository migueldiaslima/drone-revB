# Report data (set-up chat, 2026-10-14)

| File | Content | Source |
|---|---|---|
| h4r4_history.csv | H4 rev 4, cycles 0 to 28: design volume (mm^3), f7 to f12 (Hz, Tosca grey model), SE/cap per load case (SE / (2 x SE at cycle 0)), feasible flag as written by `h4_check.py` | `h4_check.py rel` output on nexus (TOSCA.OUT / optimization_report), build log item 50 |
| th_comparison.csv | Tosca cycle 28 and every thresholded check on cycle 28 (TH_r4b, i30, S, L, cA, cB, cAB, i30_final): model mass incl. 205.4 g point masses, f7 to f12, SE/cap, result. TH_r4b_L: only f7 recorded | build log items 50 to 53, 58, 65 |
| stage7_strength.csv | Stage 7 route A, TH_r4b_i30_final: per part (TUB, LID, 4 arms), step (LC1, LC2a, LC2b, LC3a) and check (VM, S33 tension, TSH = sqrt(S13^2 + S23^2)): volume-weighted P99.9, limit, utilisation, maximum, elements above the limit, clusters, excluded (tie / coupling) maximum, result (72 rows) | `docs/stage7_data/stress_TH_r4b_i30_final.txt`, build log items 68, 69 |
| stage7_capacity.csv | Section properties normal to the pp diagonal on the print STLs: table d050 (ARM_pp, u 45 to 55), slot (slot end u 43.74 and u 54), lever (u 45 to 72 with Z / (u_m - u)), fin (TUB fin within abs(w) <= 8 mm, u 25 to 33) | `docs/stage7_data/capacity_r4_iso030.txt`, build log item 69 |

Notes: cycle 0 f7 in the history (444.3 Hz) is Tosca's full-density value; the plain-Abaqus reference job G7b_r4_ref gave 448.70 Hz (item 49). u is measured from the frame centre; motor axis u_m 74.25, bolt line u_j 37.24.
