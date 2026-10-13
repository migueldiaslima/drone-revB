# Stage 7 brief: strength check of the print geometry (route A)

Main chat, 2026-10-13, for the set-up chat and Miguel. Time budget about 2 h in total (Miguel). Basis: H4 rev 4 cycle 28 at iso 0.3 with the exact keels and the clean keel cell, model TH_r4b_i30_final (build log items 62 to 65, T-4 PASS), D-015, D-034, D-036, D-038, D-045, D-050, D-064, R-06.

## Route

Route A: stresses from TH_r4b_i30_final (1.0 mm C3D10, 511,770 of 765,252 elements solid, seat tie, D-045 transversely isotropic material, D-064 inertia relief with 3-2-1 supports) in the existing static steps LC1, LC2a, LC2b, LC3a. No remesh of the print STLs (route B, not feasible in the time). Consequence stated in the report: the stresses are those of the element-level thresholded body (staircase surfaces), not of the smoothed print surface; the acceptance rule below is built for that.

## (a) Allowables

Siraya Fibreheart PET-CF, unannealed, design values N-05-03 (D-038): independent strengths (MyTechFun, as provided by Miguel) x 0.85.

| Direction | Source value | Design value (x 0.85) | Allowable / 1.5 |
|---|---|---|---|
| In the layer plane (X-Y), tensile | 64 MPa | S_xy = 54.4 MPa | 36.3 MPa |
| Across layers (Z), layer adhesion | 28.1 MPa | S_z = 23.9 MPa | 15.9 MPa |

The 0.85 knockdown covers scatter and print settings (N-05-03); no further knockdown. Across-layer weakness is handled by the separate Z check in (d), not by a second factor. No compressive or shear allowables exist for this material: compression is taken equal to tension (conservative for FFF, where compression is usually higher), across-layer shear is checked against S_z (assumption, stated).

## (b) Factor of safety

1.5 on the limit loads of LC1, LC2a, LC2b, LC3a (D-015, R-06; LC3a is a design case with FoS 1.5, D-036). Pass: stress x 1.5 <= allowable, i.e. stress <= the last column above.

## (c) Acceptance rule on the thresholded mesh

The staircase surface of the element-level body gives single-element peaks at re-entrant corners that are not in the printed part. Rule, per part (TUB, LID, each ARM) and per load case, over the solid elements only (stiffness factor 1), element-average (centroid) values:

1. **P99.9**: the volume-weighted 99.9th percentile of the checked stress is at or below the allowable / 1.5. Volume-weighted so that the many small surface tets do not set the level.
2. **Clusters**: every element above the allowable / 1.5 is listed with its location; edge-connected groups of such elements are reported as clusters with their volume and the part region (fixed / design, distance to the nearest coupling or tie surface). A cluster passes if its volume is below 1 mm^3 (about 8 elements at 1.0 mm) and it lies on the surface; a larger or through-thickness cluster fails the part regardless of P99.9, because a real hot spot of a few mm^3 at a fin root would hide below the 99.9th percentile (0.1 % of the TUB is about 390 elements).
3. **Excluded from both**: elements touching a coupling surface (S_FC_SEAT, S_GPS_SEAT, S_ANT_PAD, S_BATT_SEAT, motor pad rings) or a tie (fin boss ties, seat tie): distributed-coupling and tie stresses are load-introduction artefacts. Their maximum is reported separately, not judged.
4. **Peaks listed**: the ten highest elements per part and load case (after exclusion) with coordinates, so the report can show where the frame is most loaded.

## (d) Which stress against which allowable

Print orientation: every part is printed with its layers in the global x-y plane (build direction = global z), which is the D-045 material model. The TUB is printed floor-down, on the landing face where the FC screws enter (Miguel, 2026-10-13): build direction = global +z, so S33 is the stress across the layers; the arms are printed flat. Two checks per element:

| Check | Stress | Allowable / 1.5 | Why |
|---|---|---|---|
| In-plane | von Mises (S, Mises) | 36.3 MPa | combined in-plane state; with S_z checked separately, von Mises against S_xy is the practical criterion for a short-fibre FFF material in the layer plane |
| Across layers | S33 tensile (normal to the layers) | 15.9 MPa | layer separation is driven by tension across the layers; compression across layers does not delaminate |
| Across layers, shear | sqrt(S13^2 + S23^2) | 15.9 MPa (assumption: S_z as shear allowable) | interlaminar shear, no measured value |

Maximum principal stress against S_xy is not used as a separate check: in the layer plane (plane stress) it exceeds von Mises by at most 15 % (at sigma_2 = sigma_1 / 2), inside the margin of the check, and across layers S33 is the physically meaningful component. Report all three per part and load case with rule (c).

## (e) Capacity check D-050

Confirmed: geometric, on the print STL `print_ARM_pp_r4_iso030.stl` (arm frame, as restored). Section at the fork exit, u about 50 mm along the arm diagonal from the frame centre (corrected 2026-10-13; after the D-079 shift the fork exit is near u 54), normal to the arm axis; elastic section modulus for up-down bending, Z = I_h / c_max, I_h about the horizontal axis through the section centroid, c_max the largest vertical distance from it. Requirement Z <= 260 mm^3. Report Z for u from 45 to 55 mm in 1 mm steps and the value at the fork exit; the sideways ordering (8.5 x, D-050) is not rechecked.

## (f) Limitations and future work (stated in the report)

| Item | Status |
|---|---|
| LC3b (motor cut from 0.3 m, n = 200, survivability, D-036) | not analysed; the capacity ordering (D-034, D-050) is the design argument that only an arm fails |
| LC4 (arm strike) | not analysed; joint and body sized for 1.5 F_arm by D-034 |
| Five-boss sensitivity (DV-26, D-082 item 3: seat contact lost) | not analysed; TH04a_ni on rev 2 showed the design relies on the seat contact; the flatness requirement (D-082 item 1) carries the risk |
| Bolt bearing (A-022) | not analysed; bearing allowable assumed S_xy; Stage 9 coupon test candidate |
| Fatigue (1P at hover, about 870,000 cycles per hour) | not analysed; stress levels to be compared with the static result |
| Route B (stress on the smoothed print geometry) | not done; route A stresses are element-level |
| Thin areas T-6 (ARM_pp above both limits, LID above the 0.8 mm limit) | slicer check passed; noted as a print-quality risk |
| Retainers (TPU) and the skid | outside the model |

## Output for the main chat

Per part and load case: P99.9 of the three checks against the limits, clusters above the limits, excluded maxima, top-ten peaks with coordinates; D-050 table; one figure of the von Mises field for the governing case. The main chat records the Stage 7 N entries and the verdict.
