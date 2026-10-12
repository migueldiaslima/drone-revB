# Stage 6: v04-B revision 2, gates G6 and G7, report (stop per instruction 6)

From the set-up chat, 2026-10-11 evening. Inputs: `stage6_abaqus_v04B.zip` (revision 2), `claude/stage6_v04B_export_note.md`. Full record: `claude/stage6_build_log_v03B.md` items 34 to 38, DV-22, DV-23.

## Miguel's preference

Miguel (2026-10-11, 22:27): at this moment he prefers to move on with G7b (option A) rather than redesign anything. Decision to be recorded in the main chat.

## Result

| Gate | Result |
|---|---|
| G6 CAE mesh | PASS at both levels (0 errors, warnings 0.00 to 0.04 %) |
| G7a, lid tied at the 5 screw bosses | FAIL: mode 7 389.8 Hz (arm saddle), mode 8 405.1 Hz (lid plate with the battery) |
| G7b, lid tied over the whole seat (bosses plus rim) | PASS: modes 7 to 12 = 449.7 to 654.6 Hz |

Only G7b passes, so H4c is not started (instruction 6). Decision needed in the main chat (brief 9.8).

## Model build (V1) and G6

- Every check of V1 passed against values computed independently from the STEP files: TUB 19 cells (design 40,676.0, fixed 10,496.1 mm^3), LID 7 cells (2,496.6 / 4,599.1), S_FLOOR 2060.58, S_FC_SEAT 113.47, fin tie faces 138.50 each, tub boss tops 5 x 20.23, tub top under the lid 625.98, S_BATT_SEAT 1052.91, S_GPS_SEAT 209.19, joint gaps 0.150 mm at all four corners, RPs at the revision 2 positions, point masses 200.00 g, LC3a p = 56.4 / 2060.58 = 0.027371 MPa.
- Two deviations from the note: DV-22 (lid ties with main = lid pad, secondary = tub boss annulus, no partition: the keel pad is not a separate face and a dia 6 circle there would follow the existing fixed / design edge) and DV-23 (G7b as one tie over the whole seat).
- G6:

| Part | Debug (2.5 / 1.5 / 1.5) | Production 1.0 mm |
|---|---|---|
| TUB | 49,742 C3D10, 19 warnings (0.04 %) | 382,422, 78 (0.02 %) |
| LID | 19,322, 3 (0.02 %) | 63,398, 10 (0.02 %) |
| ARM (x4) | 26,542, 10 (0.04 %) | 80,603, 4 (0.00 %) |
| Total | 175,232 | 768,232 |

Warnings at the known small features: fin roots and fin boss tops, the GPS pocket rim and deck, the tab.

## G7 (nexus, Abaqus 2024, debug mesh, 828,051 variables)

Common to both: mass 332.809 g (expected 332.79, +0.006 %); modes 1 to 6 below 0.001 Hz; no numerical singularity, no zero pivot; support reactions below 1.1e-10 N; untied tie nodes: 172 on the lower fin boss faces (the known joint pattern), 0 on the lid seat, 0 elsewhere.

Mode shapes from `g7_check.py` (share of sum |U|^2 per part; battery and GPS = their RP displacement over the peak). No screenshots: the Abaqus GUI on nexus is not usable.

| Mode | G7a f (Hz) | G7a shape | G7b f (Hz) | G7b shape |
|---|---|---|---|---|
| 7 | **389.8** | arms, saddle (pp+mm vs pm+mp); GPS 0.32 | 449.7 | arms, saddle |
| 8 | **405.1** | lid plate, peak at the plate side edge (-2, 17, 21.5); battery 0.42 | 465.2 | arms in plane |
| 9 | 446.2 | arms, front vs rear; battery 0.31, GPS 0.37 | 477.0 | arms in plane |
| 10 | 463.3 | arms in plane | 483.9 | arms, left vs right |
| 11 | 520.3 | arms in plane | 571.3 | lid plate side edge (0, -17) |
| 12 | 590.0 | lid front tab | 654.6 | lid front tab |
| 13 | 621.5 | GPS deck | 661.7 | arms, umbrella |
| 14 | 776.4 | GPS deck | 865.4 | GPS deck |

| Step | G7a ALLSE (N mm) | G7b ALLSE (N mm) | G7b cap 2 x ALLSE (debug mesh) |
|---|---|---|---|
| LC1 | 0.112757 | 0.108317 | 0.216635 |
| LC2a | 0.122007 | 0.100093 | 0.200186 |
| LC2b | 0.0558645 | 0.0511136 | 0.102227 |
| LC3a | 0.227628 | 0.197021 | 0.394042 |

## Reading

1. The lid connection matters globally, not only locally. With 5 point ties the lid and the 100 g battery on it act as a soft mass on the frame: the first lid mode (battery rocking on the plate, 405 Hz) is inside the band, and it couples into the arm saddle mode, pulling it from 449.7 down to 389.8 Hz. With the seat tied, every mode in the band is an arm mode at 450 Hz or more, and the lid modes start at 571 Hz.
2. This is the situation brief 9.8 anticipated (hand estimates bracketed 417 Hz: 202 to about 600 Hz).
3. What is physically true lies between the two models. Under the static load cases the battery inertia presses the lid down onto the rim (compression, contact closed), and the screws preload it near the bosses; the 5-tie model ignores this contact entirely. The full-seat tie assumes the lid is in contact over the whole 626 mm^2 seat, which needs a flat seat (print flatness) and enough clamping between the screws. Separation is not a mode of the linear model either way.
4. Arm frequencies are lower than v03-B in both models (G7b mode 7 449.7 Hz against 489.9 Hz for the v03-B solid reference): the corners moved out 4.24 mm along each diagonal, and the plate is no longer merged into the body. Still above 417 Hz in G7b, so the optimisation is feasible from cycle 0.
5. Mass in G7: 332.809 g against 332.79 expected (the note's figure, within 0.006 %).

## Options for the main chat (mutually exclusive)

| Option | What | Effect | Cost |
|---|---|---|---|
| A | Model with G7b (lid tied over the seat), justified by the screw clamping and the compressive contact in all four load cases | Tosca can run now; feasible from cycle 0 | Assumes full seat contact: requires a flat seat in print (flatness check of lid and rim) and is unconservative where the lid could lift |
| B | More lid screws so the 5-point model passes (for example on the corner wall pieces or along the front and rear walls) | Keeps the conservative modelling | New geometry, export and G0 to G7 again; each screw adds about 0.35 g and a boss in the corner walls, where space is tight (brief section 9 item 1) |
| C | Deeper fixed lid frame (stiffer plate) | Raises the lid modes in the 5-point model | New geometry; mass on the lid, where it lowers other frequencies |

My recommendation: A, with two conditions recorded as decisions: (1) a flatness requirement for the lid seat and the tub rim at print (for example 0.1 mm, checked with a feeler gauge on the printed parts), and (2) a Stage 7 check on the final design with the 5-tie model, reporting how far the lid modes fall if the seat contact is lost. An intermediate model (ties along the front and rear wall tops only) could narrow the bracket if wanted; about 10 minutes on nexus.

## Also noted (not blocking)

ALLWK differs from ALLSE in every static step of both runs (LC3a: ALLSE 0.197, ALLWK 0.078 in G7b). In v03-B Phase 8 (free-free, inertia relief only) they were equal. Likely cause: since DV-18 the static steps have 3-2-1 supports, and ALLWK counts only the work of the applied loads on displacements measured from the supports, not the work of the inertia relief loads, so it no longer equals ALLSE even though the reactions are zero. The caps use ALLSE, so nothing changes; to confirm, the same comparison on the H0 odb (v03-B with DV-18) should show the same mismatch.

## Ready when the decision is in

- Option A: H4c inputs are written from `revB_v04B_G7b` (debug mesh) and the H4 reference from the 1.0 mm mesh with the same tie (`revB_v04B_m10.cae`); Tosca task re-pointed to the v04-B sets; caps from the H4 reference (D-063).
- Option B or C: new export, then V1 to V3 and G7 again.
