# Stage 6: HPC plan for the v03-B optimisation (2026-10-09, rev. after H1)

For the set-up chat. Decisions D-060 to D-066 in `claude/journal_quadcopter.md`, following `claude/stage6_tosca_chain_test_report.md` (F-13: Tosca 2022 refuses inertia relief with the sensitivity-based algorithm) and `claude/stage6_hpc_H1_report.md` (H0 and H1 passed on Abaqus/Tosca 2025).

## Status
| Run | State |
|---|---|
| H0 | Passed (N-06-08): 2025 matches 2022 within 0.001 % after D-064 |
| H1 | Passed: inertia relief accepted by Tosca 2025, volume 74,740 to 60,598 mm^3 in 3 cycles, all constraints satisfied |
| H2 | Next, settings D-065, checks D-066 |
| H3 | After the H2 report |

## Route (D-060)
- Model `revB_v03B`: inertia relief in the four static steps with the D-064 supports, free-free FREQ, absolute strain-energy caps, rotational arm symmetry, start density 1.0.
- CAE 2022 writes the `.inp` and `.par`; the HPC (nemix, Abaqus 2025, Tosca R2025x build R427) runs them. The 2022 `.par` is read without changes except `driver.Solver.AddCallArgs` (DV-17).

## Supports in every static step (D-064, set-up chat DV-18)
- `RP_JNT_pp` U1 U2 U3, `RP_JNT_pm` U1 U3, `RP_JNT_mp` U3; inertia relief kept; FREQ free-free.
- Why: Abaqus 2025 reuses the LC1 factorisation in later static steps, which fails for a free-free model (F-033). Determinate supports make the stiffness matrix non-singular; with balanced loads they carry nothing.
- Check every run: support reactions near zero (H0: below 1.5e-11 N). A reaction above about 1e-6 N means the load set is not balanced: stop and report.

## Run sequence (D-061)

| Run | Mesh | Content | Pass criteria |
|---|---|---|---|
| H0 | 2.5 / 1.5 | plain Abaqus reference job on the HPC version | passed |
| H1 | 2.5 / 1.5 | Tosca smoke test, 3 cycles, with inertia relief | passed |
| H2 | 2.5 / 1.5 | full run (D-065) | constraints satisfied at the end; D-066 checks pass; arm fields identical. First reviewable shape; no member size (C-5) |
| H3 | 1.0 (D-062) | reference job (caps, D-063), then the production run with member size 2.5 mm | same checks as H2 |

## H2 settings (D-065)
| Item | Setting |
|---|---|
| Model and mesh | `revB_v03B` as in H1 (D-064), 2.5 / 1.5 mm |
| Caps | 2 x (0.090893 / 0.069877 / 0.045459 / 0.10466) N mm (D-063; H0 reproduced them) |
| Cycles | maximum 60, Tosca default convergence |
| Member size | none (C-5) |
| Density update | Normal; not changed during the run |
| Save | every 5 cycles plus the last (about 9 GB expected; record the actual figure) |
| Resources | 16 CPUs, memory cap 35 % |
| Expected time | about 3.5 h |

## C-3 checks (D-066)
1. Documentation: how Tosca 2025 eigenfrequency responses treat low-density elements (modified mass interpolation or mass penalty); search the `.par` and the Tosca log for any such setting. Record the answer with its source, or that nothing is stated.
2. At every saved cycle (5, 10, ...), modes 7 to 12 with the density field: a mode whose largest displacements sit in elements of density below 0.3 is spurious. If one appears: record the cycle, frequency and location, stop the run, report.
3. After H2: plain Abaqus frequency job on the final H2 design with elements below density 0.3 removed (fixed regions and point masses unchanged). Compare modes 7 to 12 with Tosca's last cycle. Pass within 5 %. If the thresholded modes are lower by more than 5 %, report: grey elements are credited with stiffness, and H3 needs a change decided in the main chat.

## Production mesh (D-062)
1.0 mm, not 0.8 mm. Tosca needs the minimum member size above twice the element size (C-5): 2.5 mm > 2 x 1.0 mm holds. Go to 0.8 mm only if the H3 shape differs materially from H2 in the joints or keel.

## Caps (D-063)
Always 2 x ALLSE_i,0 from a solid-design-space reference job with inertia relief (and the D-064 supports) on the same mesh as the run. H3: from the 1.0 mm reference job.

## Watch items
- Mode 11 (battery plate front edge, local) fell fastest in H1 (681.8 to 541.0 Hz in 3 cycles); f7 was 11 Hz above the bound at cycle 3, so the frequency band becomes active early. Tosca keeping support under the plate front is the intended outcome.
- LC3a is the closest strain-energy cap (0.80 at cycle 3).
- Mass against the B allowance (about 13 g of design material, Q-53) at iso 0.3 and 0.5.

## H2 report to the main chat
Sheet part 2, section 8 item 6, plus: history of volume, modes 7 to 12 and SE / cap per cycle (table or plot); which constraints are active at the end; the D-066 results (documentation answer, mode check at each saved cycle, thresholded frequencies against Tosca); support reactions; run time and disk used.
