# Quadcopter frame rev B: project journal

Journal version: v0.56 (2026-10-13, H4 rev 4 and TH recorded; F-038 grey deck support; keels A and B, D-087, D-088)
Owner: Miguel Dias de Lima. Maintained by Claude, decisions by Miguel.
Rule: after any compaction or new session, resume from Section 1. The journal overrides chat memory. The report may only quote numbers from Section 4.

---

## 1. Current state

- **Stage**: 6 (Topology optimisation), started 2026-10-06: tool choice first (Q-30). Stages 0 to 5 closed.
- **Done**: Stage 5 closed: Siraya Fibreheart PET-CF (D-038), TPU 95A HF skid in a dovetail slide-in (D-039). Feasibility check N-06-01: a fully solid arm corridor reaches 736 Hz (clamped root, X-Y modulus).
- **Next**: H4 rev 4 converged (N-06-21); print fix keels A + B with the keel zone cleaned (D-087, claude/stage6_v04B_r4_keels_export_note.md, geometry/v04B_r4_keels/): set-up chat restores iso 0.4 of cycle 28 with the exact fixed solids (spine, GPS deck, bosses, keels A and B), optional confirmation TH with the exact keels, T-1 to T-7, H4 report. Main chat: TPU skid. Open: tub print orientation (Miguel); Q-60 checked at the first cradle fit; before ordering parts: GM10 compass wiring, GM10 plug sizes (O-a, O-b of the v04-B brief).
- **Project goals (Miguel, 2026-10-03)**: a cheaper printed structure for the same components; assess the limits of FFF printing for a quadcopter frame; use the frame as a full practical case of design, analysis and validation. The Volador carbon frame is a reference point, not a target expected to be beaten (D-011).
- **Deferred to the end**: GPS module choice and flight firmware (ArduPilot recalled, to confirm) (D-007).

### Open questions

| ID | Question | Status |
|---|---|---|
| Q-01 | Printer and filaments | Closed: Bambu Lab P1S; all materials assumed available (D-005, D-006) |
| Q-02 | Does it fly, Blackbox? | Closed: flies on a FlyFishRC Volador VX3.5 carbon frame, not on the printed frame. FC has 8 MB onboard Blackbox flash (datasheet) |
| Q-03 | Firmware and GPS | GPS closed: Flywoo GOKU GM10 Nano V3 with compass (D-076); firmware still deferred (D-007) |
| Q-04 | Rev A files | Closed: none; everything from scratch (D-009) |
| Q-05 | Rev A TO tool | Closed: irrelevant; tool chosen in Stage 6 from what is available |
| Q-06 | Scale | Closed: manufacturer masses used (D-008) |
| Q-07 | Charger IR | Closed: charger is ToolkitRC M4 Pocket; no per-cell IR function found in reviews. IR becomes an assumption (A-004) |
| Q-08 | Flight logs from rev A | Closed: none |
| Q-09 | Motor mount spacing | Closed: 9 x 9 mm, M2 (measured by Miguel) |
| Q-10 | Volador as benchmark | Closed: reference point only (D-011) |
| Q-11 | Stage 9 scope | Closed: test plan only (D-012) |
| Q-12 | Sub-250 g scope | Closed: without payload; A1 speed limit not pursued (D-014) |
| Q-13 | Endurance floor | Closed: not a requirement, performance output (D-018) |
| Q-14 | TWR floor | Closed: not a requirement; output and load input (D-018) |
| Q-15 | Factor of safety | Closed: 1.5 (D-015) |
| Q-16 | Crash philosophy | Closed: bolt-on replaceable arms (D-028) |
| Q-18 | Hover power model | Closed: M3 central, M2 conservative bound (D-020). Note kept: both models overpredict the 91.2 g row, so 18.3 W is likely conservative |
| Q-21 | Two Stage 4 inputs | Closed: battery mount force added (N-02-26); arm root moment held until Stage 3 sets the arm length (D-021) |
| Q-22 | Logged hover flight on the Volador build | Closed: future work, not done in this project (D-022) |
| Q-19 | Watt-density check | Closed: dropped as an invalid method; replaced by a datasheet rating comparison; motor-mount temperature moved to R-09 / Stage 5 (D-023) |
| Q-20 | Crash design speed | Closed: superseded by capacity design (D-034) |
| Q-23 | Layout | Closed: true X (D-024) |
| Q-24 | Battery mount | Closed: top mount on a raised plate (D-025) |
| Q-25 | Prop gap | Closed: 10 mm, wheelbase 140 mm (D-024) |
| Q-26 | Arm joint | Closed: bolt-on replaceable arms; tied-joint fallback (D-028) |
| Q-27 | GPS position | Closed: rear deck with raised pad (D-029) |
| Q-28 | Design space | Closed: confirmed with two changes (D-030) |
| Q-29 | CAD route | Closed: voxel TO domain (A) and reference STEP (B) now, Abaqus model script (C) in Stages 6 and 7, final CAD by Miguel in Fusion after TO (D) (D-031); format of A waits on Q-30 |
| Q-30 | Topology optimisation tool | Closed: Abaqus Tosca main; Fusion generative design fallback; own BESO last, only if time allows (D-040) |
| Q-31 | Component void and access windows | Closed: suggested sizes adopted for now (D-032); USB plug size may be measured later |
| Q-32 | Tool availability | Closed: Tosca available on the local Abaqus 2022 (HPC to confirm, Abaqus 2024/2025); Fusion generative design (Education licence) lists Modal Frequency, Displacement and Buckling limits with Minimize Mass or Maximize Stiffness objectives (screenshot, 2026-10-06) |
| Q-33 | Crash case | Closed: capacity design (D-034); replaces Q-20 |
| Q-34 | Landing case | Closed: thin integrated skid, LC3a design case, LC3b survivability check (D-036) |
| Q-35 | Frequency target | Closed: 290 Hz hard requirement, 417 Hz goal, free-free (D-035) |
| Q-36 | Load-case table | Closed: accepted as tabulated (LC2 idle pair at zero as bounding case) |
| Q-37 | Arm tip corridor height | Closed: z = -6 at the tip kept for now (D-037) |
| Q-38 | Frame material | Closed: Siraya Tech Fibreheart PET-CF (D-038) |
| Q-39 | Nylon moisture knockdown | Closed: not needed, PAHT-CF not selected |
| Q-40 | Poster orientation | Closed: specimens printed flat, rasters at 0 and 90 deg to the specimen axis; the poster shows in-plane raster-angle anisotropy, not across-layer (Z) behaviour |
| Q-41 | Skid attachment | Closed: TPU 95A HF skid in a dovetail slide-in groove with a click-in detent (D-039) |
| Q-42 | TO formulation | Closed: (B) minimise volume subject to modes 7 to 12 at least 417 Hz and one compliance cap per load case (D-042) |
| Q-43 | Compliance cap level | Closed: 2 x the compliance of the fully solid domain for each load case (A-020) |
| Q-44 | Who builds the Abaqus/Tosca model | Closed: Miguel in Abaqus/CAE; scripted model as fallback (D-043) |
| Q-45 | Material model, Poisson's ratio and shear moduli | Closed: A-021 with a G_xz = 700 MPa sensitivity run (D-045) |
| Q-46 | Arm corridor shape in v02 | Closed: envelope A (D-046) |
| Q-47 | Use of the Tosca result | Closed: the smoothed Tosca result is the printed part, not a rebuilt CAD (D-044) |
| Q-48 | Bolt-on joint in a direct-print workflow | Closed: J3 fin and fork (D-047), detail rules D-048 |
| Q-49 | Minimum member size | Closed: 2.5 mm (D-057) |
| Q-50 | Joint bolts: size and material | Closed: steel M3 x 20 (Miguel has no aluminium bolts); 8 bolts 13.2 g, above the 12 g hardware allowance (A-005), tracked in the mass budget (D-049) |
| Q-51 | Capacity rule for up-down bending | Closed: Stage 7 check, arm section modulus at the fork exit at most 260 mm^3 (D-050) |
| Q-52 | Joint mass against R-01 | Closed: B kept with full 1.5 x ordering and bosses-only fixing (D-051), plates and pads partly design (D-052), C built in parallel (D-053) |
| Q-53 | Mass budget of B with joint hardware | Closed: R-01 not met for variant B at 417 Hz; v03-B print set frame 76.8 g, AUW about 282 g (N-06-13), about 45 g of design material against the about 13 g allowance; accepted by Miguel (D-068) |
| Q-54 | Fin bosses of B: apply the D-054 rule to the BODY too | Closed: applied now (D-055) |
| Q-55 | First elastic mode is a local GPS overhang mode (365.2 Hz) | Closed: geometry fix, central keel design region under the GPS overhang (D-056) |
| Q-56 | Mesh for the first Tosca run | Closed: BODY 2.0 / arms 1.2 mm if memory allows, else 2.5 / 1.5 (D-058) |
| Q-57 | Symmetry in the TO | Closed: identical arms (one part x 4 instances, cyclic symmetry restriction); no symmetry for the body (D-059) |
| Q-58 | GM10 Nano V3 compass version: 6 wires (SDA / SCL)? | Open (Miguel, before ordering): if only 4, choose another compass module of similar size and redo the lid pocket |
| Q-59 | GM10 cable plug sizes | Open (Miguel, measure): decides which cable end is threaded through K9 (connector rule, brief 9.3) |
| Q-60 | FC heat-sink and component height under the receiver cradle; PCB position in the grommet groove | Open, checked at the first fit (cannot be measured now, Miguel 2026-10-13): C-6 needs the components under the cradle floor at or below z = +3.8 (0.3 mm under the floor at +4.1); paper test under the floor, floor step if it touches |
| Q-61 | Receiver thickness: PCB edge, maximum over components, with heat shrink | Closed (Miguel, 2026-10-13): PCB 1.0 to 1.25, maximum 4.0 to 4.1 with heat shrink; cradle lip at 4.1, end stop 1.0 |
| Q-62 | Receiver layout: IPEX connector end, solder pad end, button and LED | Closed (Miguel, 2026-10-13): IPEX at the -x end towards +y, pads at the +x end; +y lip starts at x -3.5 |
| Q-17 | Cost reference | Closed: 37.91 EUR, AliExpress listing seen 2026-10-03 (D-017) |


### Open items from the Stage 2 revision (2026-10-05)

| Item | Affects | How to close |
|---|---|---|
| Hover power is extrapolated (A-003) | N-02-07, N-02-10 | Hover with a current log (Blackbox or meter); measured power replaces the model. Largest single gain in certainty. Future work (D-022) |
| Pack internal resistance (A-004) | N-02-19, sagged top speed | Charger or tester with an IR function |
| Drag areas (A-013) | N-02-21, N-02-22 | Stage 3 projected areas |
| Thrust against forward speed (A-014) | N-02-21 | Propeller data against airspeed, or full-throttle flight with GPS speed |
| Motor spin-up time | Dynamic factor for thrust steps (estimated about 1, bound 1.03 for 20 ms rise and a 500 Hz first mode) | Blackbox log of a punch-out |
| Blade chord at 0.75 R (assumed 8 mm) | Reynolds numbers only | Measure a blade |
| Frame damping (assumed 0.02 to 0.05) | Resonant amplification 10 to 25 | Tap test or Blackbox gyro FFT on the built frame |

### Changelog

- 2026-10-13: v0.56: H4 rev 4 and TH results recorded from the set-up chat (build log items 50 to 58, N-06-21); F-038 (deck support grey in Tosca, not caught by the connectivity check); D-087 (keels A + B with the clean keel zone, exact solids with deviations D1 to D4, B gusset to z -2.0 above the K11 opening at z -3.0); D-088 (D-085 extended to stiffness); L-017 (rehearsal plus TH on saved cycles before a long run); N-06-22 (keel solids). Files: claude/stage6_v04B_r4_keels_export_note.md, s07_keels_r4.py, geometry/v04B_r4_keels/.
- 2026-10-13: v0.55: receiver cradle v2 (TPU 95A HF, 0.88 g, Q-61 and Q-62 answered and closed; claude/retainer_rx_cradle_note.md, s07_receiver_cradle.py); Q-60 to be checked at the first fit.
- 2026-10-13: v0.54: F-037 (set-up F-18, build log items 46 and 47: keel lid boss 5 an island in the TUB at iso 0.4, held only by the lid tie; tub behind x -34.5 removed in H4 cycle 31), L-016; D-086 (option D: GPS deck to the TUB, lid ends at the plate, boss 5 deleted, pad links, D-085 stated per part); N-06-20 (revision 4 export, gates G0 to G5 pass). Files: claude/stage6_v04B_r4_export_note.md, geometry/v04B_r4/.
- 2026-10-12: v0.53: H4 (N-06-17) and TH04 (N-06-18) recorded from the set-up chat (build log items 42 to 45); D-082 item 2 closed (TH04b_ni passes; TH04a_ni shows the design relies on the seat contact); F-036 (set-up F-17, antenna boss island), L-015; D-083 (DV-25 confirmed), D-084 (v04-B revision 3: antenna spine, straight T under the K8 exit, K8 R7, K9 moved), D-085 (fixed-region connectivity rule); N-06-19 (revision 3 export, gates G0 to G5 pass); measured: strap 3.25 g, receiver coax 60 to 62 mm, T antenna 52 mm tip to tip, legs dia 1.4, moulding 14 x 7.5 mm. Files: claude/stage6_v04B_r3_F17_note.md, claude/stage6_v04B_r3_export_note.md, f17_antenna_viewer.html.
- 2026-10-11: v0.52: v04-B G6 pass, G7a fail / G7b pass (N-06-16, claude/stage6_v04B_G7_report.md, set-up DV-22, DV-23); D-082 (lid tied over the seat, with flatness requirement, TH04 with both connections, Stage 7 contact-lost check).
- 2026-10-11: v0.51: v04-B revision 2 (D-081: closed corner walls, inward lid bosses on 45 deg supports, fillet passes A and B); N-06-15 updated; revisions 0 and 1 superseded (kept as abaqus_v04B_r0, _r1).
- 2026-10-11: v0.50: v04-B revision 1 after Miguel's review (D-079 46 x 46 body and 148.5 mm wheelbase, D-080 antenna channel, GPS channel, 11 x 7 window, C cutout, GPS pocket at x = -44); D-024 revised; N-06-15 updated; revision 0 export superseded (kept as abaqus_v04B_r0).
- 2026-10-11: v0.49 (cont.): v04-B export generated and gated (N-06-15, claude/stage6_v04B_export_note.md): G0 to G5 pass; 13 implementation changes to brief values listed in the note section 2 for Miguel's confirmation (mostly from the G3 rule: lid bosses at (+-21, +-5) and (-27, 0), FC bosses dia 6.4, USB window to x 9.8, antenna hole at (y -6.5, z -3), GPS deck fully fixed, front boss feet); new gate scripts s06_tangency_audit.py and s06_gmsh_meshtest_loc.py.
- 2026-10-11: v0.49: set-up chat update since H1 recorded (claude/stage6_update_since_H1.md, claude/stage6_v04B_design_brief.md, claude/stage6_v04B_checks_explained.md): H2 stopped at cycle 10 by the D-066 rule; H3 at 1.0 mm on nexus feasible from cycle 28, stopped after cycle 40 (set-up deviations DV-19 resources, DV-20 save every cycle, DV-21 H3 started before the H2 review); D-066 closed; v03-B print set at iso 0.4 (N-06-09 to N-06-14); F-034 (MPI with adjoint sensitivities), F-035 (print set cannot be assembled); D-067 to D-078 (brief section 15, section 9 defaults confirmed, antenna option A); L-011 to L-014; Q-53 closed, Q-58 to Q-60 opened; FC mounting corrected to M2 (Section 2, R-10); A-007, A-025 superseded by D-076.
- 2026-10-09: v0.48: HPC H0 and H1 passed (N-06-08, claude/stage6_hpc_H1_report.md); F-033 (Abaqus 2025 factorisation reuse with free-free inertia relief); D-064 (3-2-1 supports with inertia relief, set-up chat DV-18, accepted), D-065 (H2 settings), D-066 (C-3 checks); claude/stage6_hpc_plan.md updated.
- 2026-10-09: v0.47: chain test results (N-06-07, F-032, L-009); HPC plan D-060 to D-063 (claude/stage6_hpc_plan.md); export note mass line corrected to 333.7 g.
- 2026-10-09: v0.46: Q-49, Q-56, Q-57 closed (D-057 to D-059); Tosca sheet part 2 (claude/stage6_model_setup_part2_tosca.md) and handover 2 (claude/stage6_handover_2_tosca.md) written; fig06_tangency panel b label corrected (strip thickness t = d^2 / 2R, 0.15 mm at 1.34 mm from the contact; no hole involved).
- 2026-10-09: v0.45: D-056 revised to the flared keel (half-width 9, BODY design 42206.2 mm^3, model 333.7 g); F-031; gmsh mesh test added (s06_gmsh_meshtest.py); explanation figure of the tangency failure (fig06_tangency); export note, sheet and handover updated. Watch item for the 0.8 mm mesh: 25 low-quality tets (0.02) at 1.0 mm in existing BODY features (fin fillet end at z = 10, 1 mm waist between fin bosses), not caused by the keel.
- 2026-10-09: v0.44: Phase 8 reference results recorded (N-06-06, F-029, F-030); Q-55 closed by D-056 (GPS keel design region), BODY.step regenerated (passes the acceptance test), A-025 (GPS placeholder); handover and sheet mass figures corrected (322.2 g, 324.7 g with the keel); coupling note added to the sheet.
- 2026-10-08: v0.43: D-055 (fin bosses extended, Q-54 closed); final v03-B export (BODY.step, ARM_xx.step, reference_points.csv unchanged), all five pass the acceptance test; export note claude/stage6_v03B_export_note.md for the set-up chat; N-06-05, Q-53 updated (B allowance about 13.0 g).
- 2026-10-08: v0.42 check: set-up chat files (s06_arm_split_fix_v03B.py, abaqus_v03B_fix/ARM_xx.step) compared with the regenerated generator output: per arm design 8036.9 and fixed 2933.5 mm^3 in both, Boolean differences 0.000 mm^3 both ways, 88 faces each after a general fuse, both pass the acceptance test. The two sets are interchangeable; D-054 stands as recorded.
- 2026-10-08: v0.42: D-054 (arm split rule, from the set-up chat) adopted in the generator; FC boss overlap fixed (F-028); regenerated abaqus_v03B STEPs match the set-up chat's fix volumes (arm design 8036.9, fixed 2933.5 mm^3; body design 34287 mm^3); acceptance test script s06_split_acceptance.py; Q-54 (fin bosses) opened; set-up sheet updated (322.2 g, partitions, tie main/secondary).
- 2026-10-08: v0.41: Abaqus/Tosca set-up and debugging moved to a separate chat in the project (handover: claude/stage6_abaqus_handover.md); set-up sheet mesh guidance revised for the laptop (Ryzen 5 5600H, 16 GB): debug at 2.5 / 1.5 mm, production at 0.8 mm on the HPC.
- 2026-10-08: v0.40: Abaqus inputs for v03-B (s06_abaqus_inputs_v03B.py, abaqus_v03B/: BODY.step, ARM_xx.step, reference_points.csv); model set-up sheet part 1 (project doc claude/stage6_model_setup_part1.md); A-024; Q-53 (B mass budget with joint hardware: correction to the 32.4 g quoted with N-06-05, which ignored the hardware).
- 2026-10-08: v0.39: F-027 (tunnel roof = plate underside), v03 B and C rebuilt.
- 2026-10-08: v0.38: reference v03 B and C (s06_reference_geometry_v03.py, s06_render_v03.py, geometry_v03/, fig06_reference_v03); D-051 to D-053; A-023; F-026; N-06-05; Q-52 closed.
- 2026-10-08: v0.37: reference geometry v02 (s06_reference_geometry_v02.py, geometry_v02/, fig06_reference_v02); gaps checked (fin to prong 0.15 mm, nose 0.5 mm, prong tip to fillet 1.15 mm, no keep-out overlap); F-025 joint mass, Q-52.
- 2026-10-08: v0.36: D-049 (steel M3, fin 10 / prongs 5), D-050 (Stage 7 capacity check); fig06_joint_forces; Q-50, Q-51 closed.
- 2026-10-07: v0.35: J3 first sizing (N-06-04, A-022); Q-50 bolts, Q-51 vertical capacity rule opened.
- 2026-10-07: v0.34: D-048 (J3 detail rules, gap sizing).
- 2026-10-07: v0.33: D-047 (J3 fin and fork); Q-48 closed.
- 2026-10-07: v0.32: joint concepts J1 to J4 (CadQuery STEP + VTK renders, s06_joint_concepts.py, s06_render.py, s06_joint_sheets.py).
- 2026-10-07: v0.31: D-045 (A-021 material model), D-046 (arm envelope A); F-023 resolved (MyTechFun modulus is a secant with seating, chord about 5400 MPa); F-024 joint packaging; Q-49 member size.
- 2026-10-07: v0.30: N-06-03 arm profile study (A, B, C); F-023 MyTechFun flexural modulus; D-044 print the TO result (supersedes D-031 D); Q-45, Q-46 updated; Q-47 closed; Q-48 opened.
- 2026-10-07: v0.29: D-043; F-022 (arm-body contact, holes filled); Q-45 to Q-47 opened; arm taper hand study (N-06-02).
- 2026-10-07: v0.28: D-042 (formulation B), A-020 (caps 2 x solid compliance); Q-42, Q-43 closed.
- 2026-10-07: v0.27: TO theory part 2, Steps 2 to 5 rewritten at slower pace with project impact (frequency, sensitivity with arm example, spurious local modes with numbers, mode switching and repeated modes).
- 2026-10-06: v0.26: part 1 Q&A (equilibrium differentiation, sensitivity with a worked example); Abaqus 2022 inertia relief check (D-041 updated); TO theory part 2 (several load cases, frequency constraint, local modes, mode switching, formulation); Q-42, Q-43 opened.
- 2026-10-06: Stage 6 notes: minimal supports (full), TO theory part 1.
- 2026-10-06: D-040 (Tosca main), D-041 (minimal supports).
- 2026-10-06: Stage 5 closed (D-039 skid); Stage 6 started; N-06-01 feasibility check.
- 2026-10-06: D-038 material (Siraya PET-CF); index derivation; F-021; Q-38 to Q-40 closed.
- 2026-10-06: Stage 5 comparison (N-05-01, N-05-02, A-018, A-019); D-037.
- 2026-10-06: Stage 4 closed; reference STEP v01 built (N-04-13).
- 2026-10-06: D-036 landing; Stage 4 load-case table (N-04-01 to N-04-12).
- 2026-10-06: D-035 frequency target; landing case reworked (thin skid, load factor approach).
- 2026-10-06: D-034 capacity design for crash; Q-34, Q-35 explained.
- 2026-10-06: Stage 3 closed (D-033); Stage 4 started.
- 2026-10-06: D-032 (component void, access windows); Fusion GD modal frequency limit confirmed; Q-32 closed.
- 2026-10-06: Strap moved to one centreline tunnel; D-031 (CAD route); Q-30 (TO tool) opened.
- 2026-10-06: Design space confirmed (D-030: body floor at -15, strap tunnels).
- 2026-10-06: D-028 (bolt-on arms), D-029 (GPS rear deck); design space drafted.
- 2026-10-06: Stage 3 layout decisions D-024 to D-027; Volador heights measured.
- 2026-10-05: Stage 2 closed (Q-19, D-023). Stage 3 started.
- 2026-10-05: Q-18 and Q-21 closed (D-020, D-021, N-02-26); logged hover flight set as future work (D-022).
- Stage 2 revision (2026-10-05): ten corrections from the first-principles revision; see claude/stage2_revision_handover.md.

---

## 2. Fixed inputs

Mass status: **D** = manufacturer datasheet or listing (D-008), **E** = estimate, **TBD** = decided in a later stage.

### Components (as bought, order of 15 Jan 2026)

| Subsystem | Component | Key data | Mass (g) | Status | Source |
|---|---|---|---|---|---|
| FC + ESC | SpeedyBee F405 AIO 40A Bluejay, 3-6S | STM32F405, ICM-42688P gyro, 8 MB Blackbox flash, 4 UARTs + SBUS, ESC 40 A cont. / 45 A (10 s), Bluejay JH-40 48 kHz, 25.5 x 25.5 mm (M2 hardware with soft-mount grommets; earlier written as 3 mm holes, corrected 2026-10-11), 33 x 33 x 8 mm | 13.6 (incl. CNC heat sink) | D | Pyrodrone listing |
| Motors (x4) | T-Motor Pacer P1604 3800 KV | 12N14P, stator 16 x 4 mm, shaft 1.5 mm (prop) / 2 mm (internal), 24 AWG 120 mm leads, idle 0.8 A at 10 V, peak 16.8 A and 277.8 W (10 s), mount 9 x 9 mm M2 (measured by Miguel) | 11.6 each incl. cable, 46.4 total | D | T-Hobby, GetFPV, Rotorama listings |
| Propellers (x4) | Gemfan Hurricane 3520, 3-blade, PC, T-mount 1.5 mm | D = 3.5 in (88.9 mm), pitch 2.0 in | 1.75 each, 7.0 total | D | Pyrodrone listing |
| Battery | Tattu R-Line V5.0 4S 850 mAh 150C, XT30 (2 bought) | 14.8 V nominal, 59 x 30 x 32 mm | 100 | D | Tattu listing (old report Fig. 5) |
| Receiver | SpeedyBee Nano 2.4 GHz ELRS | ESP8285 + SX1281, single T antenna (IPEX1), 100 mW, 10.4 x 18.4 mm | 0.7 + 0.9 antenna = 1.6 | D | GetFPV listing |
| Radio (ground) | Radiomaster Pocket ELRS (FCC), EdgeTX, 2 x 18650 | not in AUW | - | - | Order screenshot |
| Charger (ground) | ToolkitRC M4 Pocket, 80 W, 5 A, USB-C input | no IR measurement found | - | - | Order screenshot, Oscar Liang review |
| Bench safety | XT30/XT60 smoke stopper | not in AUW | - | - | Order screenshot |
| Frame (flying) | FlyFishRC Volador VX3.5 O4 Pro, T700 carbon | wheelbase 160 mm, 127.5 x 148 mm, arms 3.5 mm, plates 2 / 2.5 / 2.5 mm, motor holes 9 x 9 / 12 x 12 (2 mm), stack 20 x 20 / 25.5 x 25.5 (M2) | 70.5 (with TPU parts) | D | FlyFishRC product page |
| Frame (rev B) | to design | - | TBD | TBD | Stage 6 |
| GPS | not bought; choose at the end | - | TBD | TBD | D-007 |
| Hardware and wiring | screws, strap, XT30 pigtail, capacitor | - | 12 +/- 5 | E | A-005 |

### Provisional mass budget (frozen in Stage 1)

| Item | Mass (g) | Status |
|---|---|---|
| Motors | 46.4 | D |
| Propellers | 7.0 | D |
| FC + ESC | 13.6 | D |
| Receiver + antenna | 1.6 | D |
| Battery | 100.0 | D |
| **Fixed subtotal** | **168.6** | D |
| Hardware and wiring | 12 +/- 5 | E |
| GPS | TBD | - |
| Frame | TBD (Volador reference 70.5) | - |

With the Volador frame: 168.6 + 12 + 70.5 = 251 g (no GPS).

### Propulsion data (primary): T-Motor P1604 3800 KV, Gemfan 3520-3

Status: manufacturer test data (rcdrone.top product page, reproducing T-Motor data). Consistent with the official peak figures (16.8 A, 277.8 W).

| Throttle % | Voltage (V) | Current (A) | RPM | Thrust (g) | Power (W) | g/W |
|---|---|---|---|---|---|---|
| 20 | 16.8 | 1.5 | 17311.1 | 91.2 | 25.9 | 3.52 |
| 40 | 16.7 | 4.6 | 25611.5 | 202.2 | 76.6 | 2.64 |
| 60 | 16.7 | 7.7 | 30692.7 | 292.4 | 127.6 | 2.29 |
| 80 | 16.6 | 11.0 | 35219.6 | 380.5 | 182.5 | 2.08 |
| 100 | 16.5 | 16.8 | 40750.1 | 514.1 | 277.8 | 1.85 |

Quality check (Stage 0): thrust / RPM^2 = 3.04 to 3.10 x 10^-7 g/RPM^2 over the whole range (spread 2 %). V x I matches the power column within 3 % (20 % row) and 1 % (others). Electrical power / RPM^3 falls from 5.0 to 4.1 x 10^-12 as load rises, consistent with fixed losses (idle current) weighing more at low load. Lowest data point (91.2 g) is above the hover thrust per motor (about 63 g at 250 g AUW): hover requires extrapolation (A-003).

### Propulsion data (old documents, audit only): "1504 3600 KV", Gemfan 3520-3, 16 V

Kept only to audit the rev A documents (F-014). Not used for rev B.

| Throttle % | RPM | Current (A) | Thrust (g) | Power (W) |
|---|---|---|---|---|
| 10 | 6000 | 0.1 | 8 | 1.6 |
| 20 | 10500 | 0.4 | 30 | 6.4 |
| 30 | 14400 | 0.9 | 61 | 14.4 |
| 40 | 17500 | 1.5 | 95 | 24.0 |
| 50 | 20000 | 2.4 | 137 | 38.4 |
| 60 | 23700 | 3.8 | 188 | 60.8 |
| 70 | 26000 | 5.3 | 234 | 84.8 |
| 80 | 28500 | 7.1 | 298 | 113.6 |
| 90 | 29700 | 8.9 | 323 | 142.4 |
| 100 | 32000 | 12.1 | 418 | 193.6 |

### Measured on the Volador build (Miguel, 2026-10-06, rough)

| Quantity | Value | Note |
|---|---|---|
| Arm top face to lowest point of the prop blades | 13 mm | motor and prop only, frame-independent |
| Arm top face to highest point of the prop blades | 18 to 19 mm | as above |
| Arm top face to battery underside (Volador, two stacked centre plates) | about 23 mm | reference for the rev B battery plate height |
| Battery strap mass (Miguel, 2026-10-12) | 3.25 g | inside the A-005 hardware allowance |
| Receiver coax, receiver plug to the T moulding | 60 to 62 mm | the listing value 79 mm does not apply |
| T antenna | 52 mm tip to tip, legs dia 1.4, moulding 14 (along the legs) x 7 to 7.5 (along the coax) mm, moulding rigid | D-084 |

### Tools

Bambu Lab P1S. Abaqus 2022 (local), Abaqus 2024/2025 (FEUP HPC, batch). Fusion, Inventor. Own BESO code (solid-void and lattice engines, thermal overhang mitigation). Python (NumPy, SciPy, pandas, matplotlib), MATLAB.

---

## 3. Decisions log

| ID | Date | Decision | Options considered | Reasoning | Decided by |
|---|---|---|---|---|---|
| D-001 | 2026-10-03 | Baseline battery: Tattu R-Line V5 4S 850 mAh 150C | Tattu 850 (flown), GNB 1100 LiHV (spreadsheet) | The Tattu is the battery bought and flown. 850 vs 1100 trade redone in Stage 2 | Miguel |
| D-002 | 2026-10-03 | New frame = rev B, designed October 2026. Original printed frame = rev A | - | Keeps results of the two versions separate | Miguel |
| D-003 | 2026-10-03 | Old documents are audit inputs only | - | Prompt rule 1 | Miguel |
| D-004 | 2026-10-03 | File naming scheme (Section 7) | - | Report can be rebuilt from files | Miguel (accepted, no objection) |
| D-005 | 2026-10-03 | Printer: Bambu Lab P1S | - | Available printer | Miguel |
| D-006 | 2026-10-03 | Material selection is an open trade study over all candidate filaments; the chosen one is assumed bought | Restrict to filaments owned; open study | Shows the selection logic in full | Miguel |
| D-007 | 2026-10-03 | GPS module and flight firmware decided at the end of the project | Now; at the end | Not frame-critical; design, optimisation and validation take priority. GPS placement is still reserved in the Stage 3 layout | Miguel |
| D-008 | 2026-10-03 | Component masses = manufacturer quoted values | Weigh; datasheet | Speed; labelled D in the budget | Miguel |
| D-009 | 2026-10-03 | Rev B designed from scratch; no rev A CAD or FEA reused | - | No rev A files exist | Miguel |
| D-010 | 2026-10-03 | Propulsion model built on the T-Motor P1604 3800 KV + Gemfan 3520-3 data; the 1504 3600 KV table is used only to audit the old documents | Keep old table; switch | The P1604 is the motor on the aircraft (F-014), and its data is internally consistent | Miguel (accepted, no objection) |
| D-011 | 2026-10-03 | Volador VX3.5 (70.5 g, T700 carbon, 160 mm wheelbase) is a reference point for mass, stiffness and cost, not a target to beat | No reference; reference; target to beat | Printed thermoplastic cannot match T700 plates on specific stiffness; the comparison quantifies the gap and the cost saving | Miguel |
| D-012 | 2026-10-03 | Stage 9 is a test plan only | Print and fly; test plan only | Time; effort goes to design, optimisation and analysis | Miguel |
| D-013 | 2026-10-03 | Battery internal resistance treated as an assumption with a sensitivity band (A-004); optional later estimate from Blackbox voltage and current during throttle steps | Charger IR (not available); assumption; Blackbox dV/dI | Charger cannot measure it; Blackbox route costs one flight on the Volador build | Miguel (accepted; measure only if fast) |
| D-014 | 2026-10-03 | R-01: AUW < 250 g in flight configuration without payload (GPS placeholder included). Frame budget 61.4 g | With payload (51.2 g budget); without payload; A1 eligibility with 19 m/s firmware limit | The report acknowledges the A1 conditions (MTOM < 250 g and max speed < 19 m/s); the speed limit is not pursued because the study explores full capability; a real operating programme would set the limit in firmware | Miguel |
| D-015 | 2026-10-03 | Factor of safety 1.5 on printed allowables with print-orientation knockdown | - | Conventional aerospace ultimate factor | Miguel |
| D-016 | 2026-10-03 | Arm architecture (replaceable vs unibody) deferred to Stage 3/4; preference for replaceable arms | Decide now; defer | Depends on how tractable the joint is to model and validate (contact, preload, bolt bearing) | Miguel |
| D-017 | 2026-10-03 | Cost reference: Volador VX3.5 at 37.91 EUR (current listing, 2026-10-03) | Paid price (unknown); listing | Market reference for the "cheaper structure" goal | Miguel |
| D-018 | 2026-10-03 | Endurance and thrust-to-weight are aircraft performance outputs, not frame requirements. Endurance is reported with its uncertainty and its sensitivity to frame mass; TWR enters Stage 4 as the manoeuvre load factor | Requirement with floor; output | Both are set by components already fixed (motors, props, battery); the frame acts on them only through mass, which R-01 already controls. Frame mass effect on endurance (about 0.4 min per 10 g) is smaller than the model uncertainty (8 to 11 min), so a floor would neither drive nor discriminate the design | Miguel (after critical review) |
| D-019 | 2026-10-03 | RunCam payload excluded from the rev B baseline (mass, loads, analysis); reported as the next step, done at the end only if time allows | Include now; defer | Keeps the baseline focused on the frame work | Miguel |
| D-020 | 2026-10-05 | Hover power model: M3 (a n^3 + b n) central, M2 (a n^3 + c) conservative bound; M1 and M4 rejected | M1 to M4 | Only M2 and M3 pass the efficiency-trend test; M3 has physical terms and the better fit. Both overpredict the 91.2 g row, so the central value is likely conservative | Miguel |
| D-021 | 2026-10-05 | Battery mount inertial force registered now (N-02-26); arm root bending moment registered in Stage 4 once Stage 3 sets the arm length. Stage 4 uses the full maximum thrust on the arm (0.40 N m at 80 mm) as the design value: the punch-out relief from motor inertia (0.33 N m) does not exist in asymmetric manoeuvres or when the aircraft is restrained | Register both now; register force only | The moment depends on a length not yet designed | Miguel |
| D-022 | 2026-10-05 | Logged hover flight on the Volador build (measured hover power) is future work | Do now; future work | Time; stated in the report as the step that would remove the largest uncertainty (A-003) | Miguel |
| D-023 | 2026-10-05 | Watt-density thermal check (F-006) dropped. Replaced by a rating comparison: hover 18.3 W per motor against the 277.8 W (10 s) peak, about 7 %; full throttle at the rated peak, allowed for 10 s; no continuous rating published. The frame-relevant thermal question, motor-mount temperature against the filament's heat-deflection temperature, goes to R-09 and Stage 5, with an IR-thermometer measurement in the test plan | Drop; drop and replace with rating comparison; build a thermal model | The check uses total power as heat, ignores time and cooling, uses d^2 h as a volume, has unsourced thresholds, and flags the manufacturer's own rated peak as critical (0.271 W/mm^3 for the P1604). A thermal model would need invented inputs | Miguel |
| D-024 | 2026-10-06 | Layout: true X, prop-to-prop gap 10 mm, wheelbase 140 mm (revised by D-079 to 148.5 mm, gap 16.1 mm) | True X; squashed X (1.1: +24 % arm stiffness, 1.2: +54 %); H | Shortest arms for a given gap (required stiffness scales with free length cubed); four identical arms, one spare fits all; squashed X's advantages (camera field of view, roll/pitch tuning) do not apply to the baseline | Miguel |
| D-025 | 2026-10-06 | Battery top-mounted on a raised plate, underside at about 23 mm above the arm top face (Volador reference), clearing the prop blades (13 to 18.5 mm) by about 4.5 mm | Bottom mount (140 mm); top mount, low plate (156 mm); top mount, raised plate (140 mm) | CG near the thrust plane (estimated +21 mm against a blade plane at 13 to 18.5 mm): little translation-rotation coupling, same behaviour upright and inverted; punch-out load goes into the plate in compression; frame bottom takes landings; Miguel's preference. Roll inertia is within about 4 % of bottom mount at equal wheelbase, so inertia does not decide. Cost: taller centre body; GPS needs a position off the battery | Miguel |
| D-026 | 2026-10-06 | Structural direction: 3D printed centre body, topology-optimised to carry the battery plate and stack to the arm roots; tall, narrow, tapered arms (truss or ribbed section chosen in Stage 6); moulding-style ribbed features where they help Stage 8; arm joint still open (D-016, Q-26) | Plate sandwich; one-piece frame; printed body with bolt-on arms; truss arms; ribbed shell; carbon-tube hybrid; ducts | Puts printing where it is strong (3D nodes, tall sections); keeps download low (narrow arms); supports the frequency-driven sizing and the injection-moulding discussion | Miguel |
| D-027 | 2026-10-06 | Perimeter ring between motors considered and rejected; recorded as an alternative in the report | Inner ring; outer ring (prop guard); root gussets | The ring adds no stiffness to the umbrella mode (all corners move together, the ring translates) and only adds mass there, so it lowers that frequency; it stiffens saddle, rocking and in-plane scissor modes. Inner members sit under both prop discs for about 89 of 99 mm: about 2.2 times the arm download per mm of width. An outer guard avoids download but weighs an estimated 20 to 30 g against a 61.4 g frame budget and answers no requirement. Root gussets remain available as a local feature | Miguel |
| D-028 | 2026-10-06 | Bolt-on replaceable arms: arm root clamped in a centre-body pocket, two bolts into heat-set inserts. Fallback if contact modelling becomes a time sink: tied joint in Abaqus plus hand calculation of bolt bearing and clamp friction. Closes D-016 | One-piece frame; bolt-on arms | Defined failure location (R-07), one-part repair fitting all four positions (R-13), joint design is core airframe work; cost is joint modelling and an arm-root joint at the peak moment | Miguel |
| D-029 | 2026-10-06 | GPS on a rear deck with a raised pad at battery-plate height; battery XT30 lead exits at the front | Rear mast; rear deck; front | Compact and robust; keeps the compass away from the battery lead; front kept free for the future camera (R-02). Module and mass still deferred (D-007) | Miguel |
| D-030 | 2026-10-06 | Design space confirmed (Stage 3 notes table), with two changes raised by Miguel: (1) centre body floor moved from z = -12 to z = -15, level with the arm bottoms; (2) battery strap runs across the battery width (along y), through one tunnel in the top of the centre body on the centreline (x = 0); two tunnels at x = +/-15 were drawn first and dropped because the upper body is chamfered there (y <= 16.8 at x = 15), which put the strap exit about 4 mm from the blade edge, inside the 3 mm clearance convention | Floor at -12 or -15; strap along the length (slots in the plate) or across the width (tunnels) | (1) The arm-root moment must pass into the body over the full arm height; the lowest fibres are the most effective in bending (stiffness grows with height cubed), so a body 3 mm shallower than the arm would waste them and concentrate load at the clamp edge. (2) Straps normally wrap the short dimension (as on the Volador); a strap under the plate edge would hang into the 3 mm blade clearance, while a tunnel through the body keeps it out of the prop sweep | Miguel |
| D-031 | 2026-10-06 | CAD and model route: (A) voxel design domain written as Abaqus .inp with element sets, from the same parameters as fig03; (B) CadQuery STEP of non-design features and keep-outs for Fusion; (C) Abaqus model script for Stages 6 and 7; (D) final clean CAD by Miguel in Fusion after TO | Miguel models everything in Fusion; generated geometry plus Miguel's final CAD | One parameter set drives figures, TO domain and reference geometry, so they cannot drift; the final CAD stays Miguel's work for the portfolio | Miguel |
| D-032 | 2026-10-06 | Add to the design space: a component and wiring void above the FC (about 32 x 32 mm, z 6 to 18), a USB-C access window (about 12 x 8 mm) on the FC port side, and a wire channel at each body corner towards the arms (about 5 x 5 mm). All sizes are editable parameters, confirmed with Miguel before use | Leave the space above the FC as design space; add voids | Without them the optimiser fills the space needed for the receiver, capacitor and wiring; the voids also make the two-panel layout explicit | Miguel (suggested sizes adopted) |
| D-033 | 2026-10-06 | TO tool chosen at the start of Stage 6, after Stage 4 (frequency target, load cases) and Stage 5 (material) | Decide now; decide at Stage 6 | Both inputs change the answer: if a stiffness-optimised design meets the frequency target, frequency support matters less; E and density set every frequency | Miguel |
| D-034 | 2026-10-06 | Crash case by capacity design: the arm is the weakest link; the arm joint and the centre body are sized for 1.5 times the arm's own failure load (at the arm tip). Kinetic energy at top speed (114 J) is reported only to show that failure in a full-speed crash cannot be avoided | Size for a crash speed; capacity design | A crash speed gives arbitrary forces (hundreds to thousands of newtons over millimetres); capacity design guarantees where failure occurs (R-07) whatever the impact | Miguel |
| D-035 | 2026-10-06 | Frequency requirement (R-08): first free-free elastic mode at least 290 Hz (1.2 x hover 1P) as the hard requirement; goal 417 Hz (geometric middle of hover 1P and 3P). Stage 6 runs the optimisation at 417 Hz first and relaxes towards 290 Hz only if the mass budget is exceeded; a short sweep (290 / 350 / 417 Hz) gives a mass-versus-frequency curve for the report | 20 % margins only; centred target only; hard floor plus goal | The middle halves the response at hover 1P (amplification 1.5 against 3.2 at 3 % damping) and gives room for modelling error (printed E +/- 20 % means frequency +/- 10 %), but needs about twice the stiffness of the 290 Hz design | Miguel |
| D-036 | 2026-10-06 | Landing: thin sacrificial skid surface (1 to 2 mm) integrated in the centre-body floor, no energy-absorbing pad. LC3a firm landing (1.5 m/s onto grass, s = 10 mm, n = 23) is a design case with FoS 1.5; LC3b motor cut from 0.3 m onto hard ground (s = 3 mm, n = 200) is a survivability check in which only an arm may fail (capacity order, D-034) | Thick TPU pad with 0.3 m / 5 mm design drop; thin skid with load-factor cases | Ground bearing stress is negligible; what loads the structure is the deceleration of each mass; frequency-sized arms carry even the n = 200 case at low stress (about 8.5 MPa for an 8 x 10 mm solid section) | Miguel |
| D-037 | 2026-10-06 | Arm corridor bottom rises from z = -15 at the root to z = -6 at the tip (9 mm ground clearance level, about 12 deg tilt before a tip touches), parameter arm_tip_zmin | Keep; change | Makes the body the landing point (D-036) | Miguel |
| D-038 | 2026-10-06 | Frame material: Siraya Tech Fibreheart PET-CF (15 % carbon fibre), printed unannealed. Design values: independent strengths (MyTechFun, as provided by Miguel) and TDS moduli, each multiplied by 0.85: E_xy 5058 MPa, E_z 2890 MPa, S_xy 54.4 MPa, S_z 23.9 MPa (layer adhesion), density 1.30 g/cm^3 | Bambu PAHT-CF, Bambu PET-CF, ASA, PETG-CF; manufacturer data only vs independent tests | Best cost/performance: frequency index 13.9 (X-Y, TDS), passes the heat gate unannealed (HDT 86.7 C at 0.45 MPa), 40 EUR/kg against 90 EUR/kg for Bambu PET-CF; independent tests show manufacturer across-layer strengths are optimistic (PAHT-CF 64 MPa on the TDS against 20 MPa measured), so PAHT-CF loses its main advantage. Prints at 280 to 300 C on the P1S (TDS range 280 to 320 C), hardened nozzle | Miguel |
| D-039 | 2026-10-06 | Skid: separate TPU 95A HF part sliding into a dovetail groove in the centre-body floor, retained by a click-in detent; no screws. Fallback: PET-CF skid integrated in the floor | Dovetail slide-in; snap pins; glue; integrated PET-CF | Landing loads press the skid onto the floor; scraping loads act along the floor, which the dovetail carries; replaceable without tools; TPU impact and abrasion resistance | Miguel |
| D-040 | 2026-10-06 | TO tool: Abaqus Tosca (local Abaqus 2022; HPC 2024/2025 for heavy runs) as the main optimiser, with the eigenfrequency constraint (290 Hz hard, 417 Hz goal); Fusion generative design as fallback if Tosca set-up stalls; Miguel's BESO (stiffness only) as the last task, only if time allows | Tosca; Fusion GD; nTop; own BESO | Documented frequency constraint with mode tracking; the same Abaqus model is reused in Stage 7, so optimisation and validation agree; nTop skipped for learning time | Miguel |
| D-041 | 2026-10-06 | Free-flying load cases are solved with balanced loads and minimal (3-2-1) supports: inertial forces (load factor x mass, plus angular terms in LC2) applied as loads so that the load set is in equilibrium, and six single restraints on three non-collinear nodes in non-design regions to remove rigid-body motion. Reaction forces must come out near zero, as a check. Abaqus inertia relief, which computes the balancing accelerations automatically, is used in the static steps (Abaqus 2022: listed in Miguel's local documentation; *INERTIA RELIEF is not among Tosca's non-supported keywords; a two-iteration smoke test confirms it before the main runs); modal analyses use no supports (free-free) | Clamp the body; minimal supports with balanced loads; inertia relief | A clamp adds stiffness and carries load that does not exist in flight, and the optimiser would route material to it; statically determinate supports remove rigid-body motion without carrying load | Miguel |
| D-042 | 2026-10-07 | TO formulation (B): minimise design volume subject to (1) free-free modes 7 to 12 each at least 417 Hz (290 / 350 Hz in the sweep) and (2) one compliance cap per static load case (LC1, LC2a, LC2b, LC3a), C_i <= 2 C_i,0 (A-020). LC3b and LC4 are Stage 7 checks, not optimisation cases | (A) minimise compliance at fixed volume with a frequency constraint; (B) | States the real goal (lightest frame meeting the frequency goal, D-035); one limit per case removes the load-case weighting problem; the sweep is three runs differing only in the frequency bound; the mode band handles mode switching and the symmetric pairs | Miguel |
| D-043 | 2026-10-07 | The Abaqus/Tosca model is built by Miguel in Abaqus/CAE from a step-by-step set-up sheet, keeping the replay file; a scripted model (Abaqus Python, noGUI) is the fallback if time runs short or many automated runs are needed | CAE by hand; script by Claude | Miguel wants to go through the whole process; Tosca set-up lives mostly in the CAE Optimization module; scripts cannot be tested in Claude's workspace | Miguel |
| D-044 | 2026-10-07 | The printed frame is the smoothed Tosca result (iso-surface STL), not a CAD rebuilt from it; exact non-design features (motor pads and holes, FC bosses, battery plate, joint, skid groove) are restored by mesh booleans with the reference geometry; Stage 7 validates the final STL geometry; supports accepted where needed, with Tosca member-size (and, if available in 2022, overhang) restrictions. Supersedes D-031 (D) | Rebuild clean CAD in Fusion; print the TO result | A manual rebuild loses much of the organic load path and is not necessarily more printable; FFF prints an STL directly; supports cost little material | Miguel |
| D-045 | 2026-10-07 | Material model for Stage 6 and 7: transversely isotropic Siraya PET-CF, build direction = global z: E_xy 5058, E_z 2890 MPa, nu 0.35, G_xy 1873, G_xz = G_yz 1070 MPa (A-021); one sensitivity run with G_xz 700 MPa | Isotropic E_xy; isotropic E_z; transversely isotropic | Arms bend in the layer plane, joints and body walls load across layers; no measured nu or G for the material (TDS, MyTechFun) | Miguel |
| D-046 | 2026-10-07 | Arm design envelope (reference v02): top face at z = +10 from the root to the motor keep-out (3 mm under the lowest blade), step down to the motor pad with the step face pulled back from the keep-out by the fillet radius (R 3); root width up to 20 mm, 10 mm at the pad, corridor blended tangentially into the pad flange; screw-head, shaft-clip and motor-wire clearances kept free under the pad | Flat top z = 0 (C); ramp (B); flat z = +10 (A) | Depth governs bending stiffness (h^3): for the same frequency profile A needs 2.7 g per arm against 5.7 g for C (N-06-03); Tosca carves the profile inside the envelope | Miguel |
| D-047 | 2026-10-07 | Arm-to-body joint: J3 fin and fork. Vertical fin on each body corner, forked arm root straddling it, two horizontal M3 bolts through prong, fin and prong into a heat-set insert in the far prong; joint geometry non-design in the TO model, tied. Refines D-028 (pocket replaced by fin and fork) | J1 corner pocket; J2 socket pocket; J3 fin and fork; J4 lap joint | Fits beside the FC (F-024); the deep fin continues the deep arm section (D-046) into the body; bolts in shear and inserts loaded along the layer plane; bolts reachable from the side below the props | Miguel |
| D-048 | 2026-10-07 | J3 detail rules: slot end a full semicircle and fin nose rounded, with a 0.5 mm gap at the nose; fin root fillets R 5 (vertical axes) with prong tips rounded to clear them by 0.5 mm; fin sides and inner prong faces flat and parallel with 0.15 mm gap per side, closed by bolt preload; spot faces for the bolt heads with at least 3 mm under the head. Non-design: fin with fillets and nose, inner prong faces with at least 3 mm wall, bolt bosses and seats; design (Tosca): prong outer shape, fork-to-arm transition, body around the fin | Tight fit on all mating faces; gaps sized by function | Load goes through bolts and clamped side faces only, so the load path is defined; the side gap only has to allow assembly and is closed by preload, while the nose and fillet gaps must never close under print tolerance stack-up (about +/- 0.2 mm per part), bolt-hole play (3.2 mm hole on a 3 mm bolt) and joint deflection | Miguel |
| D-049 | 2026-10-08 | J3 sizing: steel M3 x 20 bolts, two per arm stacked vertically (spacing s = 13 mm, edge distance 6 mm), fin 10 mm, prongs 5 mm (fork 20 mm wide), insert in the far prong. Bolt force limit 1632 N (fin bearing), up-down moment capacity 21,216 N mm (N-06-04) | M2.5 / M3 / M4; fin 8 / prongs 6 or fin 10 / prongs 5; steel, titanium, aluminium | Fin and prongs balanced in bearing when t_fin = 2 t_prong; M3 gives margin over the expected arm; steel is what Miguel has (mass 13.2 g for 8 bolts, over A-005) | Miguel |
| D-050 | 2026-10-08 | Capacity ordering for up-down bending (moment from vertical tip forces) checked in Stage 7: the optimised arm's section modulus at the fork exit (u about 50 mm, depth about 20 mm) must not exceed 260 mm^3; if it does, M4 bolts or a larger bolt spacing | Enforce now by geometry; check in Stage 7 | The TO arm is unknown until Stage 6 ends; sideways ordering already 8.5 x | Miguel |
| D-051 | 2026-10-08 | Repairable variant B keeps the 1.5 x capacity ordering in both directions (D-034, D-050) with the D-049 joint sizes; only dia 12 bolt bosses are fixed (full fin and prong thickness); the rest of the fin and prongs is design space bounded by the D-048 shapes. Stage 7 adds a check: fin-root section modulus (up-down) at least 390 mm^3 (1.5 x the arm limit), else a fixed band at the fin root. Insert holes from the outer face of the far prong, 3 mm short M3 insert, 2 mm shoulder (bolt preload pushes the insert against the shoulder) | Relax the up-down ordering (slim joint); keep full ordering | A joint that can fail before the arm in a vertical hit breaks the body, which defeats repairability; bearing needs only the bosses | Miguel |
| D-052 | 2026-10-08 | Partial fixing of interfaces: battery plate = 3 mm perimeter frame plus the strap band (x +/- 9 mm) fixed, interior design; GPS pad = 3 mm frame fixed, interior design; motor pads = dia 6 screw bosses and a dia 16 to 20.8 motor contact ring fixed, rest design | Fully fixed plates and pads; partial | Plates are not primary structure but have local functions; pad material sits at the arm tip where mass costs frequency most | Miguel |
| D-053 | 2026-10-08 | One-piece variant C built in parallel (same envelope, no joint, one design region); Tosca set-up and runs on B first, C as a second run for the repairability cost comparison | Build C later; now | Same model with the joint region changed; cheap to keep ready | Miguel |
| D-054 | 2026-10-08 | Arm design/fixed split for the TO model (supersedes the boss shape of D-051): each prong boss pair is one dia 12 cylinder along the bolt axis through the full fork width, clipped by the arm envelope; the upper boss is extended over its 12 mm width up to the arm top (z = +10); one tool set splits the envelope (fixed = envelope AND tools, design = envelope MINUS tools), so design and fixed faces coincide. Envelope, joint, holes, slot, pad and keep-outs unchanged. Acceptance test: after a general fuse no face below 0.5 mm^2 or narrower than 0.3 mm (s06_split_acceptance.py): arms pass (smallest 2.5 mm^2, narrowest 0.4 mm). +0.35 g fixed per arm, +1.41 g in total | Bosses bounded by the prong planes (D-051); through-fork bosses with top extension; D-shaped bosses to the prong tip (+0.80 g per arm); frozen prong root (+0.88 g per arm) | The D-051 split met the slot-end semicircle tangentially and the upper boss touched the arm top, leaving 3 um crescents and 0.15 mm strips that Abaqus could not mesh (set-up chat F-8, F-9); the extension above the upper bolt is the 6 mm edge-distance material of D-049 | Set-up chat proposal, accepted in the main chat |
| D-055 | 2026-10-08 | D-054 rule applied to the BODY fin bosses: dia 12 bosses extended over their 12 mm width to the fin top (z = +10, upper boss) and bottom (z = -15, lower boss). Final v03-B export: all five files pass the acceptance test (BODY smallest face 8.04 mm^2, narrowest 0.80 mm). +0.93 cm^3 = +1.21 g fixed | Keep the tangent fin bosses (BODY meshed at 1.5 / 1.0 mm with warnings); extend now | One split rule for the whole model; avoids a likely meshing failure at the 0.8 mm production mesh; cheaper before the Tosca set-up than after | Miguel |
| D-056 | 2026-10-09 (rev. same day) | GPS mount: keel design region under the GPS overhang, block x = -50 to -19, y = +-9, z = 0 to 21.5, with the rear prop keep-outs cut from it: above z = 10 it fills the corridor between the rear prop keep-outs (4.1 mm wide at the GPS end, 18 mm near the body), below z = 10 the full 18 mm. Half-width 9 keeps it 1.86 mm clear of the fin root fillet tangent lines (y = +-10.86); bottom at z = 0 keeps 3 mm above the rear-left motor-wire exit. The 417 Hz band (modes 7 to 12) stays unchanged and applies to local modes as well | (a) stiffen the GPS mount in geometry: 3 mm keel, flared keel (Miguel's proposal); (b) constrain global modes only (MAC filtering, feasibility in Tosca unconfirmed); (c) accept 365 Hz for the GPS mount | Makes the local GPS mode something Tosca can size; the flare puts width where the root moment is largest (as at the arm roots) and adds torsional stiffness; all of it is design space, so Tosca trims it; the GPS mount also sees the 1P sweep (241 to 679 Hz) in flight | Miguel (flare), Claude (implementation) |
| D-057 | 2026-10-09 | Minimum member size 2.5 mm in Tosca (6 lines of 0.42 mm with a 0.4 mm nozzle, or 4 of 0.625 mm with a 0.6 mm nozzle); approximate on the debug mesh (one to two elements across), meaningful at the 0.8 mm HPC mesh | 2.5 mm; larger | Printability of FFF members (Miguel) | Miguel |
| D-058 | 2026-10-09 | First Tosca run local and fast, to prove the chain: BODY 2.0 mm (tie faces 1.2), arms 1.2 mm if the data-check memory estimate stays under about 10 GB, else the Phase 8 mesh (2.5 / 1.5); 30 cycles; production runs at 0.8 mm on the HPC | Debug mesh; finer local mesh; HPC only | 16 GB laptop (13.9 GB visible); Phase 8 at 0.68 M equations took 4 min and about 11 GB | Miguel |
| D-059 | 2026-10-09 | Identical arms in the TO: one arm part instanced four times (rotations 0, -90, +90, 180 deg about z) plus a Tosca cyclic symmetry restriction on the arm design sets; no symmetry on the body. Verified: ARM_pp rotated reproduces ARM_pm / mp / mm exactly (Boolean difference 0.0000 mm^3) | Identical arms; free arms | One arm design fits all four positions (R-13, repairability); the load cases and the GPS are not symmetric, so the body stays free | Miguel |
| D-060 | 2026-10-09 | Optimisation runs with inertia relief move to the HPC (Abaqus/Tosca 2024 or 2025), using the .inp and .par written by CAE 2022; the no-inertia-relief chain-test model is kept only as a record. Confirm the HPC Tosca licence and that the 2022 .par reads cleanly | Run locally without inertia relief (3-2-1 supports); HPC with inertia relief | Tosca 2022 refuses inertia relief with the sensitivity-based algorithm (F-032); supports would carry the unbalanced thrust and distort the shape | Miguel (Claude recommendation) |
| D-061 | 2026-10-09 | HPC run sequence: H0 reference job (version check against the local 2022 results, 0.5 %), H1 Tosca 3-cycle smoke test with inertia relief, H2 full run at 2.5 / 1.5 mm (max 60 cycles, first reviewable shape, no member size), H3 production | Straight to production; staged | Each stage isolates one risk (version, inertia relief in Tosca, convergence and modes, mesh) before the expensive run | Miguel (Claude recommendation) |
| D-062 | 2026-10-09 | Production mesh 1.0 mm with member size 2.5 mm (Tosca needs the minimum above twice the element size, C-5); 0.8 mm only if H3 differs materially from H2 in the joints or keel. Supersedes the 0.8 mm figure in D-057 / D-058 | 0.8 mm; 1.0 mm | About half the elements of 0.8 mm for each of 40 to 60 cycles; 2.5 elements across the thinnest member | Miguel (Claude recommendation) |
| D-063 | 2026-10-09 | Strain-energy caps always 2 x ALLSE_i,0 from a solid-design-space reference with inertia relief on the same mesh as the run: H1 / H2 use 2 x (0.090893 / 0.069877 / 0.045459 / 0.10466) N mm if H0 reproduces them; H3 from a 1.0 mm reference | Fixed caps; per-mesh caps | Mesh refinement makes the model more flexible, so caps from a coarser mesh would be too tight | Miguel (Claude recommendation) |
| D-064 | 2026-10-09 | Every static step (LC1, LC2a, LC2b, LC3a; later LC3b, LC4 in Stage 7) uses inertia relief plus 3-2-1 supports on the arm joint reference points: RP_JNT_pp U1 U2 U3, RP_JNT_pm U1 U3, RP_JNT_mp U3; FREQ stays free-free. Every run reports the support reactions as a check (H0: below 1.5e-11 N). Adopts set-up chat DV-18 for H2, H3 and Stage 7 | Inertia relief alone (free-free static steps); supports added | Abaqus 2025 reuses the LC1 factorisation in the later static steps, which is not valid for a free-free model regularised inside the factorisation (F-033); with determinate supports the stiffness matrix is non-singular, the reuse is correct and the solver's own warning is answered. The supports carry nothing (reactions 1e-11 N against 20 N of thrust), so stresses, strain energies and the D-063 caps are unchanged; this is the arrangement D-041 described from the start | Miguel (Claude recommendation) |
| D-065 | 2026-10-09 | H2 settings: model revB_v03B with D-064, mesh 2.5 / 1.5 mm, caps as D-063, maximum 60 cycles with Tosca default convergence, no member size, density update Normal; results saved every 5 cycles plus the last; 16 CPUs, memory cap 35 %. Settings are not changed during the run; if the history oscillates or a constraint stays violated, the run is reported and the change decided in the main chat | Save every cycle; every 5; every 10 | Every 5 matches the C-3 mode check (D-066) and keeps disk modest (about 690 MB per save in H1, about 9 GB expected; 2.8 TB free); about 3.5 min per cycle, about 3.5 h for 60 cycles | Miguel (Claude recommendation) |
| D-066 | 2026-10-09 | C-3 (mass interpolation for the frequency responses) closed by evidence rather than by the log: (1) look up in the Tosca 2025 documentation how eigenfrequency responses treat low-density elements and search the .par and Tosca log for any interpolation or mass-penalty setting; record what is found, or that nothing is stated; (2) at every saved cycle, for modes 7 to 12, check where the motion sits: a mode whose largest displacements lie in elements of density below 0.3 is spurious; (3) after H2, a plain Abaqus frequency job on the H2 design with elements below density 0.3 removed (point masses and fixed regions unchanged), modes 7 to 12 compared with Tosca's last cycle. Pass: no spurious mode at any saved cycle and the thresholded modes within 5 % of Tosca's. Thresholded lower by more than 5 %: grey elements are credited with stiffness, so H3 needs a stronger penalty or a higher bound; reported to the main chat | Trust the default; change the setting blind; check by evidence | The setting is not in the 2025 log; a spurious mode would show as motion in grey or void material (theory part 2, Step 4); the thresholded job is also the first estimate of the printable design's real frequencies, which H3 and Stage 7 need anyway | Miguel (Claude recommendation) |
| D-067 | 2026-10-11 | v03-B print set (H3 cycle 40, iso 0.4, smoothed, fixed interfaces restored; frame 76.8 g) recorded as the v03-B structural result; not built, because it cannot be assembled (F-035) | Build it; record only | The structure meets every constraint once thresholded (N-06-12), but no component can be installed | Miguel |
| D-068 | 2026-10-11 | R-01 (AUW < 250 g) not met for variant B at 417 Hz (AUW about 280 g); accepted. Mass for assembly features accepted. The D-035 sweep (350 / 290 Hz) and variant C are not run now | Relax the frequency goal; variant C; accept | At 417 Hz the design space needs about three times the B allowance of design material (N-06-13); Miguel: 250 g is not achievable with this concept | Miguel |
| D-069 | 2026-10-11 | D-066 closed: (1) Tosca's interpolation measured from the *SCALESTIFFNESS / *SCALEMASS tables (mass linear in density, stiffness about 0.19 x density at low density rising to density^3 near 1: grey material penalised, void regions protected); (2) the flagged modes are the arm bending modes with grey material at the motor seats, not spurious void modes; (3) the thresholded designs at iso 0.3 and 0.5 pass every constraint and are stiffer than Tosca predicted (N-06-12) | - | Measured in H3 (claude/stage6_update_since_H1.md section 6) | Miguel (set-up chat evidence) |
| D-070 | 2026-10-11 | From H4 on, the D-066 mode check is a reported diagnostic, not a stop rule; acceptance is the thresholded job at the print iso level (TH04): f7 >= 417 Hz, every SE <= cap, reactions < 1e-6 N. Supersedes the D-066 stop rule | Keep the stop rule; diagnostic plus thresholded acceptance | The rule detects grey material in a mode, not a spurious mode; it stopped H2 and would have stopped H3 at cycle 20 on designs that pass once thresholded (L-011) | Miguel |
| D-071 | 2026-10-11 | Print iso level 0.4 | 0.3; 0.4; 0.5 | Halves the thin-wall surface share of iso 0.5 for 5.4 g; its frequencies lie between TH05 and TH03, which both pass (N-06-14); TH04 is run on v04-B (T-4) | Miguel |
| D-072 | 2026-10-11 | v04-B architecture: topology-optimised open tub (rim at z = 21.5) plus a removable lid (battery plate and GPS deck as one printed part), five M2 countersunk screws into heat-set inserts; in the model tub and lid are tied only at the screw bosses (G7a), with a second reference run including the rim contact (G7b) to decide the lid connection | Access windows in the walls; lid | Windows large enough for the 33 x 33 FC would remove most of a wall; a lid gives a vertical insertion path and a straight tool path to every screw and pad, and keeps the plate one stiff part | Miguel |
| D-073 | 2026-10-11 | Component retention by designed seats and separate retainers, no glue or tape: receiver cradle clamped on the pp and mp FC screws; GPS cap with two screws; antenna holder screwed under the keel; capacitor floating on its soldered leads with no retainer (Miguel's flown builds; in LC3a it may rest on the FC components, insulated sleeve) | Glue and tape; tub-fixed cradles; separate retainers | Requirements of the redesign (claude/stage6_update_since_H1.md section 9); a tub-fixed capacitor cradle would block the FC insertion (brief 9.6) | Miguel |
| D-074 | 2026-10-11 | FC soft-mounted on through-bosses: M2 button-head screws from below in 1.5 mm counterbores (floor flush for the skid), damping rings and grommets, anti-loosening nuts on all four screws, nylon nuts over the cradle ears (pp, mp); FC rotated (USB-C on -y, battery pads at +x), with Betaflight board alignment and motor remap, checked in the 3D tab and with a props-off motor test | Blind bosses with screws from above; through-bosses | The v03-B blind bosses had no screwdriver line (F-035); nuts are held from above through the open bay | Miguel |
| D-075 | 2026-10-11 | Capacitor flipped 180 deg over the FC (option 2); pigtail through a 7 x 3.5 front window with bare ends, XT30 soldered on outside after the FC is seated, mated XT30 on the lid front lip | Window sized for the XT30 (11 x 6); slot open to the rim; bare-ended pigtail | The XT30 (10.2 x 5.2) cannot pass a 7 x 3.5 window; soldering outside is the easiest joint and keeps the front wall intact (brief 9.2) | Miguel |
| D-076 | 2026-10-11 | GPS: Flywoo GOKU GM10 Nano V3 with compass (12 x 17 x 5, 2.6 g, listing) in a lid deck pocket, CG at (-40, 0, 26.5); cable through a channel inside the keel; closes D-007 for the GPS (firmware still deferred); supersedes A-007 and A-025. Compass version wiring to confirm before ordering (Q-58) | 8 g placeholder; GM10 Nano V3 | Light, small, with compass; the lighter module also raises the GPS deck mode | Miguel |
| D-077 | 2026-10-11 | v04-B layout defaults of brief section 9, confirmed: (1) open upper corners of the tub for the FC insertion prism K2, lid bosses on the front and rear wall pieces plus one on the keel; (2) XT30 soldered after threading (D-075); (3) GPS cable inside the keel (beside the keel is inside the prop keep-out); (4) antenna coax hole below the keel at (y -5, z -3.5) (beside the keel is a 1.86 mm strip at the fin fillet tangent line); (5) antenna option A, a 90 deg V lying horizontally under the keel (a downward V hangs below the landing plane); (6) capacitor with no retainer (D-073); (7) LC3a pressure from the new floor area, p = 56.4 N / A(S_FLOOR); (8) lid modes decided by G7a and G7b | Per item, in claude/stage6_v04B_checks_explained.md | Each default follows from the prop keep-out, landing plane, tangency, printable wall or assembly-path rule | Miguel |
| D-078 | 2026-10-11 | Design-space rule added to D-032: every component has an insertion path, a tool path and a cable path as keep-outs, and each is checked by a sweep in the clash test (gate G5) | - | F-035: the v03-B design space defined where components sit, not how they get there, so Tosca filled every assembly path | Miguel |
| D-079 | 2026-10-11 | Centre body 46 x 46 (half-width 23) with the FC bay +-20.5, 4 mm from the FC to the inner walls on every side; every corner (fin, joint, arm, motor) moved out 3 mm in x and 3 mm in y, so the J3 joint and the arms stay exactly as v03-B. Motor axes at (+-52.5, +-52.5); wheelbase 148.5 mm, adjacent prop gap 16.1 mm. Revises D-024 (140 mm, 10 mm gap) | 40 x 40 body with 1 to 2 mm margin; bigger body with shorter arms; bigger body with the motors moved out | 1 mm margin forces tight bends at the solder joints; moving the motors keeps the arms, the joint and the arm-to-motor geometry unchanged and moves the props away from the body and battery. Costs: LC2b moment +6 % (lever 52.5 mm), motor share of roll / pitch inertia +12 %, a few grams of design space | Miguel |
| D-080 | 2026-10-11 | v04-B details after review: (1) antenna coax through the keel at receiver height, dia 3.5 channel from (y +3.5, z 7) to the keel underside at (-38, +3.5), antenna boss at (-44, 0), holder pocket for the 14 x 7.5 x 4 T junction; (2) GPS channel on the -y side (bay entry y -3.5, z 5); (3) pigtail window 11 x 7, the complete pigtail with its XT30 female passes through (replaces the bare-end option of D-075); (4) lid tab with a Volador-style C cutout, XT30 female standing on the tab, battery plugging in from above; zip-tie slots and plate wire slot removed; (5) GPS pocket 4 mm rearward (CG at x = -44), deck and keel to x = -54, for the keel lid boss at (-30, 0) | Shared GPS / antenna hole; hole below the keel | Miguel's review of the revision 0 export; separate holes keep each channel sized to its plug and avoid a tangent branch in the keel | Miguel |
| D-081 | 2026-10-11 | v04-B revision 2: (1) octagonal corner walls restored above z = 10 (2.5 mm, the FC still drops in with 0.96 mm at its corners), with a 45 deg bay-corner transition between z about 6 and 10 so the walls are continuous and the 4 mm margin at board level is kept; (2) wall lid bosses moved towards the corners and 2.5 mm into the bay on 45 deg design supports, front (21, +-9.5), rear (-21, +-5), keel (-30, 0); (3) fillets pass A in the model (keel root R2, bay corners R2, window corners R0.75, strap notch R1, lid tab root R2, deck root R3, C cutout pocket R0.8), pass B at restoration (R0.5 outside edges, R1 inside edges where walls are at least 2.5 mm) | Bosses exactly in the corners (only 3.5 mm between the FC corner and the prop margin along the diagonal); open corners; fillets everywhere in the model | Only inside corners concentrate stress; fillets that would cross a design/fixed boundary or leave sub-1 mm faces were dropped after the gates (bay floor edge, C cutout entry corners) | Miguel |
| D-082 | 2026-10-11 | v04-B optimisation runs (H4c, H4) model the lid tied to the tub over the whole seat (G7b: bosses plus rim, 626 mm^2), with three conditions: (1) print requirement: lid underside and tub rim flat within 0.1 mm, checked with a feeler gauge on the printed parts before assembly; (2) after H4, the thresholded check (TH04) is run with both lid connections, G7b and the five boss ties (G7a), and the seat densities are reported; (3) Stage 7 reports how far the lid and arm modes fall with the seat contact lost (five ties only) on the final design | (A) G7b model; (B) more lid screws; (C) deeper fixed lid frame | G7a fails (389.8 Hz arm saddle coupled to the battery-on-lid mode at 405.1 Hz); G7b passes (449.7 to 654.6 Hz). In all four static cases the battery inertia presses the lid onto the rim and the screws preload it, so full contact is the realistic state when the seat is flat; B and C need new geometry and gates. Miguel prefers to move on | Miguel (set-up chat recommendation) |
| D-083 | 2026-10-12 | DV-25 confirmed: H4 caps set relative, ALLSE <= 2.0 x cycle 0; cycle 0 of a solid-start run (DV-13) on the production mesh with the seat tie is the D-063 / A-020 reference, so no separate H4_ref job; H4c not repeated | H4c restart plus H4_ref before H4; relative caps | Same cap by definition (2 x solid compliance, same mesh, tie, loads and supports); H4c was a rehearsal and its first 10 cycles had shown the seat and lid behaviour. The cycle 0 ALLSE values in N mm are still to be reported by the set-up chat for N-06-17 | Miguel |
| D-084 | 2026-10-12 | F-036 fix, v04-B revision 3: (1) straight T receiver antenna (the moulded junction cannot bend), moulding vertical, stem up, directly under the K8 exit, legs along y at z -5.75, held by a TPU 95A holder (C-clips on both legs, snap lips, peg, one M2 x 5 screw into an M2 x 3 insert); (2) K8 rerouted: z 6.5, one R7 bend (6 x the coax OD, I-PEX), exit at (-49, +3.5); (3) antenna spine replaces the antenna boss (TUB fixed): sleeve 1.5 mm around K8 from the bay face to the exit, pad in the keel underside with insert boss and locating hole, web continuing the rear lid boss (-21, +5) down to the sleeve; (4) K9 and the lid GPS hole moved 1.5 mm to -y, no fixed material around K9; (5) antenna, holder and GPS cap masses moved out of the RP_FC lump to RP_ANT and RP_GPS | L1 bridge to the keel lid boss; conduit around both channels; antenna on the GPS cap (coax 74 mm route against 62 mm measured); flat T under the keel (R2 coax bend, C-9 2.6 mm) | The chain antenna to rear lid boss is fixed throughout, so the mount cannot be cut loose (F-036); coax bends >= R7; C-9 5.49 mm on the real arms; 35 geometry checks and gates G0 to G5 pass (N-06-19). Cost 1.54 g of fixed material; a new H4 is required | Miguel |
| D-085 | 2026-10-12 | Design-space rule added to D-078: every fixed solid either touches another fixed solid or carries a load, tie or mass that needs a solid path; any other fixed solid gets a fixed link. Checked at export (G1 floating fixed solids, now fixed-to-fixed) and after every thresholding (island check) | - | F-036: the antenna boss touched only design material and carried nothing, so Tosca was free to isolate it | Miguel |
| D-086 | 2026-10-13 | F-037 fix, v04-B revision 4 (option D): (1) the GPS deck (plate x -54 to -32.5, y +-9, z 21.5 to 24, pocket rim, two cap bosses with M2 inserts) moves from the LID to the TUB and sits on the keel; S_GPS_SEAT and RP_GPS move with it; (2) the LID ends at the plate (x -32), 0.5 mm gap to the deck, no tie between them; (3) keel lid boss 5 at (-30, 0) deleted, the lid is clamped by the four wall bosses; (4) each lid screw pad joined to the plate frame by a fixed link 4.5 mm wide, so the LID fixed region is one cell; (5) K9 runs up through the keel and the deck to the pocket floor; (6) D-085 stated per part: each fixed solid is kept by a load, mass or fixed link within its own part; exception: the wall bosses 1, 2, 4 are kept only through the seat tie (held in H4 cycle 31 at iso 0.3 and 0.4, build log item 46) and are covered by the per-part island check after H4 | (A) link boss 5 to the keel or wall with fixed material; (B) accept iso 0.3 locally at boss 5; (C) keep the deck on the lid and add a fixed lid-to-tub path | With the deck on the TUB the GPS mass needs a tub path (D-085 met by a mass on the part), the lid carries no cable and no part of the design relies on the lid holding tub material; the deck rear is no longer cantilevered from the lid. Seat tie area 625.98 to 363.23 mm^2; full-density mass -0.09 g; gates G0 to G5 pass (N-06-20). A new H4 is required | Miguel (proposed; set-up chat and main chat recommend) |
| D-087 | 2026-10-13 | F-038 fix, print geometry of the rev 4 tub: the keel zone behind the rear wall (x -54 to -23, abs(y) <= 9, z 0 to 21.5) is cleaned of all design material and the GPS deck is carried by two fixed parts: (A) twin tapered keels hanging from the deck underside, plan between abs(y) 4.6 and the deck edge (9) or the prop sweep + 3 mm, flaring into the rear wall, depth z_bot = 21.5 - 11.5 (0.6 t + 0.4 t^2), t = (x + 50) / 28, from x -46; (B) a 2 mm web under the antenna sleeve (y 2.5 to 4.5) from x -36.9 to the wall, continued as a 45 deg gusset down the outside of the rear wall to z -2.0, 1 mm above the K11 motor-lead opening (z -8 to -3). Exact solids differ from the TH shapes only for printability and mesh quality (D1 to D4 in the keels export note) and hold more material except two pieces thinner than one element. No new H4 | (S) full side webs forced solid, +2.11 g; (L) local iso 0.15; new H4 with the keel as fixed | TH_r4b_cAB passes every requirement (f7 428.4 Hz, LC3a 0.94 x cap) at 1.1 g less than S; L fails (380.6 Hz); B alone does not reach the deck (cB 7.8 Hz) but braces the spine (f12 458.5 to 529.6 Hz). Shapes by Miguel, checked in Fusion (build log item 56) | Miguel (set-up chat and main chat recommend) |
| D-088 | 2026-10-13 | D-085 extended from connectivity to stiffness: a fixed part that carries a mass or a load gets either a fixed load path to the main structure or a design corridor narrow enough that the optimiser must form a defined member in it; checked after every thresholding by TH (modes and caps), not only by the island check | Connectivity check alone (D-085) | F-038: the GPS deck was connected at iso 0.3 to 0.5 (D-085 met) and still failed TH at 146.8 Hz, because its support in Tosca was a wide grey block (densities below 0.15) that no threshold keeps | Miguel (set-up chat recommendation) |

---

## 4. Numbers register

Only numbers in this table may appear in the report. ID format N-SS-nn (SS = stage).

| ID | Quantity | Value | Units | Method / script / file | Uncertainty | Version |
|---|---|---|---|---|---|---|
| N-00-01 | Fixed component mass (motors, props, FC, receiver, battery) | 168.6 | g | Sum of datasheet values, Section 2 | datasheet tolerance, not quantified | rev B build |
| N-00-02 | P1604 + 3520 thrust coefficient (thrust / RPM^2) | 3.04 to 3.10 x 10^-7 | g/RPM^2 | Manufacturer table, Stage 0 check | 2 % spread | data |
| N-02-01 | Thrust constant k | 3.088 x 10^-7 | g/RPM^2 | LSQ through origin, s02_sizing.py | max residual 1.5 % (1.46 %, at the 20 % row) | data |
| N-02-02 | Thrust coefficient C_T | 0.1425 | - | T = C_T rho n^2 D^4 | as N-02-01 | data |
| N-02-03 | Arm download fraction (8 mm arm) | 3.0 | % of rotor thrust | F/T = Cd kappa^2 w L / 4A (A-012) | band 2.2 to 3.9 % (kappa 1.2 to 1.6) | rev B |
| N-02-04 | Hover thrust per motor at 250 g | 64.4 | g | AUW/4 / (1 - N-02-03) | +/- 1 g | rev B |
| N-02-05 | Hover RPM | 14440 | RPM | N-02-01 | +/- 1 % | rev B |
| N-02-06 | Hover 1P / 3P | 241 / 722 | Hz | RPM/60 | +/- 1 % | rev B |
| N-02-07 | Hover electrical power per motor | 18.3 | W | M3 model | M2 20.2, M3 18.3 (M1 12.6 and M4 15.2 rejected) | rev B |
| N-02-08 | Hover total power / current | 74 / 5.0 | W / A | 4 x N-02-07 + 1 W avionics, at 14.8 V | as N-02-07 | rev B |
| N-02-09 | Hover throttle (bench mapping) | 14 | % | power-law RPM vs throttle | indicative only (A-006) | rev B |
| N-02-10 | Hover endurance at 250 g | 8.2 | min | 80 % of 850 mAh at 3.70 V/cell | band 6.6 to 9.0 min | rev B |
| N-02-11 | Endurance sensitivity to mass | -0.036 | min/g | finite difference at 250 g | about +/- 15 % | rev B |
| N-02-12 | Endurance sensitivity to arm width (4 arms) | -0.035 | min/mm | via N-02-03, exact 1/(1 - f) download form (s02_sizing.py v2) | as A-012 | rev B |
| N-02-13 | Endurance with Volador frame (259.1 g) | 7.8 | min | as N-02-10 | band as N-02-10 | reference |
| N-02-14 | Chain efficiency P_ideal / P_elec on bench | 0.265 to 0.331 | - | momentum theory / data, 91 to 514 g | data | data |
| N-02-15 | Implied figure of merit at full throttle | 0.535 | - | P_ideal / (K_t (I - I0) omega) | depends on K_t = 1/Kv (ideal) | data |
| N-02-16 | Max thrust per motor (loads basis) | 5.04 | N | datasheet, 16.5 V | conservative upper bound | loads |
| N-02-17 | Max motor reaction torque | 0.040 | N m | K_t (16.8 - 0.8 A) | momentum cross-check 0.036 to 0.048 | loads |
| N-02-18 | Max load factor n_z (loads basis) | 8.2 | g | 4 T_max / W at 250 g | conservative (no sag) | loads |
| N-02-19 | TWR with sag | 5.4 to 7.3 | - | R_pack 20 to 40 mOhm, V_oc 15.2 to 16.8 V | A-004 | rev B |
| N-02-20 | Max 1P / 3P | 679 / 2038 | Hz | 40750 RPM | datasheet | rev B |
| N-02-21 | Top speed | 30 (109 km/h) | m/s | tilt balance, linear C_T(J) (A-013, A-014) | band 27 to 36 m/s; about 28 m/s with sag | rev B |
| N-02-22 | Kinetic energy at top speed | 114 | J | 0.5 m V^2 | band up to 160 J | loads |
| N-02-23 | ESC margin / battery C margin | 2.4 / 1.9 | - | 40/16.8 A; 127.5/67.2 A | C-rating is a marketing value | rev B |
| N-02-24 | Endurance with GNB 1100 LiHV (88 g, 238 g AUW) | 11.4 | min | as N-02-10, 3.8 V/cell | information only | trade |
| N-02-25 | Tip speed / Mach at max RPM; disk loading at hover thrust | 190 / 0.55; 102 | m/s; N/m^2 | geometry; T_hover / A at 64.4 g (hover v_i 6.45 m/s, ideal power 4.1 W per motor) | exact | rev B |
| N-02-26 | Inertial force on the battery mount, punch-out | 8.1 | N | n_z x m_batt x g = 8.2 x 0.100 x 9.81 (s02_sizing.py v2) | conservative (no sag) | loads |
| N-04-01 | LC1 punch-out: thrust and torque per motor | 5.04 / 0.040 | N / N m | N-02-16, N-02-17 | conservative (no sag) | loads |
| N-04-02 | LC1 load factor; battery, FC + receiver, GPS, motor inertial forces | 8.2; 8.06, 1.23, 0.65, 1.11 | -; N | s04_loads.py | as N-02-18 | loads |
| N-04-03 | LC1 arm root moment, design (no inertia credit, 41.7 mm free length) | 210 | N mm | T_max x L | L from Stage 3 design space | loads |
| N-04-04 | LC2a diagonal pair at full thrust: net yaw torque; vertical load factor | 0.080; 4.1 | N m; - | s04_loads.py | idle pair at zero (bounding) | loads |
| N-04-05 | LC2b adjacent pair at full thrust: pitch/roll moment about the centre | 0.50 | N m | 2 T_max x 49.5 mm | as above | loads |
| N-04-06 | LC3a firm landing load factor (1.5 m/s, s = 10 mm) | 23 | - | n = 2 h / s | A-017 | loads |
| N-04-07 | LC3a battery, motor inertial forces; ground reaction | 22.5, 3.1; 56 | N | s04_loads.py | A-017 | loads |
| N-04-08 | LC3a arm root moment (motor inertia) | 129 | N mm | s04_loads.py | A-017 | loads |
| N-04-09 | LC3b survivability load factor (0.3 m, s = 3 mm) | 200 | - | n = 2 h / s | A-017 | loads |
| N-04-10 | LC3b battery, motor inertial forces; ground reaction | 196, 27; 491 | N | s04_loads.py | A-017 | loads |
| N-04-11 | LC3b arm root moment (motor inertia) | 1125 | N mm | s04_loads.py | A-017 | loads |
| N-04-12 | Frequency requirement / goal (first free-free elastic mode) | 290 / 417 | Hz | D-035 | - | requirement |
| N-04-13 | Volumes: body design domain; one arm corridor; non-design (plate, GPS pad, motor pads, FC bosses) | 28.39; 4.38; 12.14 | cm^3 | s04_reference_geometry.py (CadQuery) | exact for the v01 geometry | rev B |
| N-05-01 | Frequency merit index E^(1/3)/rho, X-Y (Z): PLA 11.2 (10.4), PLA-CF 11.5 (10.6), PETG HF 9.5 (9.0), PETG-CF 10.8 (8.8), ASA 12.8 (12.2), PET-CF 13.0 (10.0), PAHT-CF 14.8 (12.2), PPA-CF 18.2 (13.0) | see value | MPa^(1/3) cm^3/g | s05_materials.py, Bambu TDS (dry) | TDS scatter 5 to 10 % on E | data |
| N-05-02 | Arm mass for the same frequency, relative to PLA (X-Y): PAHT-CF 0.76, PET-CF 0.86, ASA 0.87, PETG-CF 1.04, PETG HF 1.18 | see value | - | m ~ rho E^(-1/3) at fixed width | as N-05-01 | data |
| N-05-03 | Design values, Siraya PET-CF (x 0.85): E_xy, E_z; S_xy, S_z; density | 5058, 2890; 54.4, 23.9; 1.30 | MPa; MPa; g/cm^3 | s05_materials.py v2; Siraya TDS (moduli, unannealed, ASTM D638); MyTechFun (strengths) | knockdown 0.85 covers scatter and print settings; layer adhesion governs across layers | data |
| N-06-01 | First bending frequency of a fully solid arm corridor (10 mm wide, height 15 to 6 mm, 41.7 mm free length, tip mass 13.75 g, clamped root): E_xy 5058 MPa / E_z 2890 MPa; solid arm mass | 736 / 557 Hz; 5.7 g | Hz; g | Euler-Bernoulli beam FE (60 elements), design values N-05-03 | upper bound: rigid body and joint, no battery coupling | rev B |
| N-06-02 | Arm hand study (Timoshenko beam, tip mass 13.75 g, depth 15 to 6 mm, E_xy 5058, G 1070 MPa): uniform 10 mm 687 Hz, 5.7 g; root width 16 tapering to 10: 798 Hz (+16 %), 7.6 g, in-plane stiffness x2.8; uniform 13.5 mm: 791 Hz, 7.7 g; root depth 25 tapering to 6 at width 10: 1157 Hz (+68 %), 8.4 g. Shear share of tip deflection 13 %; G 700 / 1500 MPa gives 665 / 700 Hz | see quantity | Hz; g | stage6/s06_arm_taper.py (energy method) | clamped root, single arm | rev B |
| N-06-03 | Arm top-face profiles (width 10, bottom -15 to -6, motor keep-out edge 30.2 mm from the root, energy method, G 1070): C (top z = 0) 687 Hz, 5.7 g; B (ramp z = +10 to 0 at the motor edge) 999 Hz, 7.7 g; A (z = +10 flat to the motor edge, then 0) 1277 Hz, 9.6 g; square-root profile at the mass of B 1027 Hz. Width for 687 Hz: C 10.0 mm (5.7 g), B 4.6 mm (3.5 g), A 2.8 mm (2.7 g) | see quantity | Hz; g | stage6/s06_arm_profiles.py | clamped root, single arm, solid sections | rev B |
| N-06-04 | J3 joint first sizing (two bolts stacked vertically, spacing 13 mm, edge distance 6 mm, bearing allowable S_xy): M3 with fin 8 / prongs 6: bolt force limit 1306 N, vertical moment capacity 16,973 N mm; M3 with fin 10 / prongs 5: 1632 N, 21,216 N mm, so arm section modulus at the fork exit at most 260 mm^3 for the 1.5 x ordering; lateral ordering 8.5 x; LC1 bolt force 12 N | see quantity | N; N mm; mm^3 | stage6/s06_joint_sizing.py | fin bearing governs in all cases; friction ignored | rev B |
| N-06-05 | Reference v03 fixed and design material (solid, PET-CF 1.30 g/cm^3), final v03-B export 2026-10-08 (D-054, D-055, F-028): B fixed 31.6 g (fin bosses 11.4, prong bosses 11.9, plate frame 3.4, GPS frame 0.5, motor pads 3.3, FC bosses 1.0), design domain 85.2 g solid (96.7 g with the D-056 flared keel), frame 116.8 g solid (128.3 g with the keel), model total 322.2 g (Phase 8: 322.1 g; 333.7 g with the keel) with 205.4 g of point masses; C fixed 8.3 g, design domain 118.4 g solid; B joint hardware 13.2 g bolts + about 2 g inserts; R-01 allowance for B design material about 13.0 g (Q-53) | see quantity | g | stage6/s06_reference_geometry_v03.py, abaqus_v03B/, claude/stage6_v03B_export_note.md | before optimisation | rev B |
| N-06-06 | Phase 8 reference run, v03-B solid design space (debug mesh 145,750 C3D10, BODY 2.5 mm, arms 1.5 mm): free-free modes 7 to 12 = 365.2 (local GPS) / 487.6 / 521.0 / 523.9 / 566.6 / 689.0 (local) Hz; compliance C_i,0 = 2 ALLSE = 0.1898 / 0.1436 / 0.0976 / 0.2981 N mm (LC1 / LC2a / LC2b / LC3a), caps 0.380 / 0.287 / 0.195 / 0.596 N mm; max U 0.024 / 0.021 / 0.016 / 0.057 mm; rigid modes < 0.002 Hz; mass 322.1 g | see quantity | Hz; N mm | claude/stage6_phase8_reference_results.md | debug mesh, before D-056; recompute on the Tosca mesh | rev B |
| N-06-07 | Local model with D-056 keel, D-059 arms, 2.5 / 1.5 mm (149,305 C3D10, 10.5 GB, 236 s per analysis; 2.0 / 1.2 needed 20.8 GB): mass 333.70 g; modes 7 to 12 = 489.9 umbrella / 521.5, 524.3 saddle / 573.6 arms / 681.8 local plate front edge / 749.4 mixed Hz; ALLSE_i,0 = 0.090893 / 0.069877 / 0.045459 / 0.10466 N mm (LC1 / LC2a / LC2b / LC3a; LC3a 30 % lower than Phase 8, keel supports the plate rear); inertia relief vs 3-2-1: reactions < 2.4e-11 N, ALLSE identical | see quantity | Hz; N mm | claude/stage6_tosca_chain_test_report.md | debug mesh | rev B |
| N-06-08 | HPC version check and Tosca smoke test (nemix, Abaqus 2025 / Tosca R2025x build R427, 16 CPUs, D-064 supports): H0 mass 333.698 g, modes 7 to 12 489.93 / 521.51 / 524.32 / 573.63 / 681.81 / 749.44 Hz, ALLSE 0.0908934 / 0.0698767 / 0.0454587 / 0.10466 N mm (at most 0.001 % from the local 2022 values), reactions below 1.5e-11 N, 2 min, 9 GB; H1 3 cycles with inertia relief: volume 74,740 to 60,598 mm^3, modes 7 to 12 at cycle 3 428.2 / 445.7 / 453.0 / 475.9 / 541.0 / 624.9 Hz, SE / cap 0.69 / 0.72 / 0.74 / 0.80, about 3.5 min per cycle, 2.7 GB | see quantity | g; Hz; N mm; mm^3 | claude/stage6_hpc_H1_report.md | debug mesh | rev B |
| N-06-09 | H2 (2.5 / 1.5 mm, nemix, 32 threads, DV-19, DV-20): stopped at cycle 10 by the D-066 mode rule, not converged; cycle 10 f7 to f12 407.3 / 417.0 / 418.2 / 419.7 / 456.3 / 486.3 Hz, LC3a strain energy 1.24 x cap; about 3.8 min per cycle, 11 GB | see quantity | Hz; min | claude/stage6_hpc_H2_report.md, claude/stage6_update_since_H1.md | not converged | rev B |
| N-06-10 | H3 reference (1.0 mm, 723,474 C3D10, 3.19 M variables, nexus, 671 s on 64 threads, 80 GB): mass 333.69 g; f7 to f12 486.66 / 517.87 / 520.97 / 568.67 / 673.31 / 742.66 Hz (-0.6 to -1.3 % against 2.5 / 1.5); ALLSE 0.0919015 / 0.0709504 / 0.0461905 / 0.106569 N mm (+1.1 to +1.8 %); H3 caps 0.183803 / 0.141901 / 0.0923811 / 0.213138 N mm; reactions below 3.7e-10 N | see quantity | g; Hz; N mm | claude/stage6_update_since_H1.md section 4 | mesh converged within 1.3 % (frequency), 1.8 % (strain energy) | rev B |
| N-06-11 | H3 cycle 40 (1.0 mm, member size 2.5 mm, Tosca 2024, 54 threads): f7 to f12 417.8 / 419.7 / 420.5 / 427.3 / 487.1 / 521.2 Hz; SE / cap 0.98 / 1.00 / 1.00 / 1.00 (active: f7, LC2a, LC2b, LC3a); feasible from cycle 28; about 14 min per cycle | see quantity | Hz | claude/stage6_update_since_H1.md section 5 | stopped by hand, slow volume decrease (about -0.8 % per cycle) | rev B |
| N-06-12 | Thresholded cycle 40 (plain Abaqus, near-air below the iso value): TH05 (iso 0.5) 437,027 solid elements, model mass 277.2 g, f7 to f12 438.3 / 446.1 / 450.8 / 456.5 / 515.6 / 547.4 Hz, SE / cap 0.86 / 0.86 / 0.92 / 0.93; TH03 (iso 0.3) 457,918 elements, 281.3 g, 449.5 / 462.5 / 465.8 / 488.2 / 544.8 / 574.9 Hz, SE / cap 0.77 / 0.76 / 0.82 / 0.84; reactions below 1.5e-9 N | see quantity | g; Hz | threshold_job.py, claude/stage6_update_since_H1.md section 6 | f7 +4.9 % (iso 0.5) and +7.6 % (iso 0.3) above Tosca | rev B |
| N-06-13 | Print set v03-B (cycle 40, iso 0.4, 6 Taubin iterations, fixed solids restored, trimmed to the envelope): body 35,062 mm^3 = 45.58 g, arm 6,011 mm^3 = 7.81 g (x 4), frame 76.8 g, AUW about 282 g with 205.4 g of point masses; iso 0.5 frame 71.2 g, iso 0.4 76.6 g before restoration | see quantity | mm^3; g | iso_mt.py, revB_v03B_BODY_c40_iso040.stl, revB_v03B_ARM_c40_iso040_print4.stl | not assemblable (F-035) | rev B |
| N-06-14 | Wall thickness of the cycle 40 surfaces: ray method median / surface share below 1.2 mm: arm iso 0.5 3.09 mm / 5.1 %, arm iso 0.4 3.28 / 2.7 %, body iso 0.5 2.52 / 7.3 %, body iso 0.4 2.77 / 3.7 %; sphere method surface share below 0.8 / 1.2 / 2.0 / 2.5 mm: arm iso 0.5 0.9 / 3.8 / 23 / 43 %, arm iso 0.4 0.8 / 2.2 / 15 / 37 %, body iso 0.5 0.2 / 2.3 / 10 / 23 %, body iso 0.4 0.1 / 1.0 / 5 / 15 %; material volume below 1.2 mm 0.4 to 1.2 % | see quantity | mm; % | claude/stage6_update_since_H1.md section 7 | sphere voxels 0.1 mm (arm), 0.25 mm (body) | rev B |
| N-06-15 | v04-B export revision 2 (claude/stage6_v04B_export_note.md): TUB design / fixed 40,676.1 / 10,496.1 mm^3, LID design / fixed 2,496.6 / 4,599.1 mm^3, arms unchanged (4 x 8,036.9 / 2,933.5, moved 3 mm in x and y); frame solid design space 132.79 g (fixed 34.88 g); point masses 200.0 g; expected model mass 332.79 g; wheelbase 148.5 mm; new hardware about 7.1 g (estimate, within A-005); gates G0 to G5 pass, C-6 open (Q-60) | see quantity | mm^3; g | stage6/s06_geometry_v04B.py, s06_gates_v04B.py, abaqus_v04B/ | before optimisation | rev B |
| N-06-16 | v04-B revision 2 reference (debug mesh 175,232 C3D10, 828,051 variables; 1.0 mm mesh 768,232 elements, G6 0 errors): mass 332.809 g; G7a (5 boss ties) modes 7 to 12 389.8 (arm saddle) / 405.1 (lid plate with battery) / 446.2 / 463.3 / 520.3 / 590.0 Hz; G7b (seat tied) 449.7 / 465.2 / 477.0 / 483.9 / 571.3 / 654.6 Hz; G7b ALLSE LC1 / LC2a / LC2b / LC3a 0.108317 / 0.100093 / 0.0511136 / 0.197021 N mm (debug-mesh caps 2 x ALLSE); reactions below 1.1e-10 N | see quantity | g; Hz; N mm | claude/stage6_v04B_G7_report.md | debug mesh; H4 caps from the 1.0 mm reference | rev B |
| N-06-17 | H4 (v04-B rev 2, 1.0 mm, 768,232 C3D10, member size 2.5 mm, caps 2.0 x cycle 0, D-083, nexus 60 threads): cycle 0 volume 75,520 mm^3, f7 to f12 445.4 / 462.0 / 473.6 / 480.7 / 567.7 / 649.0 Hz; stop condition after cycle 31 (8 h 32 min, about 16 min per cycle): volume 32,709 mm^3 (-56.7 %), f7 to f12 416.4 / 417.1 / 417.7 / 418.6 / 501.2 / 504.5 Hz, SE / cycle 0 = 1.59 / 1.41 / 1.63 / 2.10 (LC1 / LC2a / LC2b / LC3a); iso 0.3 / 0.5 kept volume incl. fixed 62,126 / 60,675 mm^3 | see quantity | mm^3; Hz | set-up build log item 42 | cycle 0 ALLSE in N mm to be reported (caps); at Tosca's stop LC3a 5 % over and f7 0.6 Hz under | rev B |
| N-06-18 | TH04 (H4 cycle 31 thresholded at iso 0.4, antenna boss island set to air): model mass 279.7 g, main frame 79.82 g at iso 0.4; TH04b_ni (seat tie) f7 to f12 426.8 / 432.4 / 436.3 / 436.6 / 520.0 / 525.1 Hz, SE / cap 0.73 / 0.66 / 0.76 / 0.98, PASS; TH04a_ni (five boss ties) 192.1 (GPS deck) / 314.1 (lid edge) / 348.9 / 382.8 / 429.0 / 474.3 Hz, SE / cap 0.86 / 0.89 / 1.00 / 1.52, FAIL; reactions below 3.5e-9 N | see quantity | g; Hz | set-up build log items 43 to 45 | TH04a_ni mode 7 below the 290 Hz minimum: the design relies on the seat contact (D-082 items 1 and 3 cover it) | rev B |
| N-06-19 | v04-B revision 3 export (claude/stage6_v04B_r3_export_note.md): TUB design / fixed 39,368.8 / 11,711.1 mm^3 (rev 2: 40,676.1 / 10,496.1), antenna spine 1,327.7 mm^3 in the TUB (1.54 g more fixed material than rev 2); point masses 199.58 g (RP_FC 22.91, RP_GPS 4.23, RP_ANT 2.24); gates G0 to G5 pass; C-9 antenna to arms 5.49 mm; TPU antenna holder 0.94 g | see quantity | mm^3; g; mm | s06_geometry_v04B.py rev 3, s06_f17_spine.py, geometry/v04B_r3/ | before optimisation | rev B |
| N-06-20 | v04-B revision 4 export (claude/stage6_v04B_r4_export_note.md): TUB design / fixed 39,538.5 / 12,796.3 mm^3, 17 fixed cells incl. GPS deck 1,218.56 mm^3; LID design / fixed 2,357.0 / 3,417.1 mm^3, one fixed cell; S_GPS_SEAT 209.19 mm^2 on the TUB; seat tie tub side 363.23 mm^2 (rev 3: 625.98), lid side 2,314.02 mm^2 (rev 3: 2,740.84); S_BATT_SEAT 1,056.00 mm^2; full-density mass 332.16 g expected (rev 3: 332.25); point masses 199.58 g unchanged; gates G0 to G5 pass | see quantity | mm^3; mm^2; g | s06_geometry_v04B.py rev 4, geometry/v04B_r4/ | before optimisation | rev B |
| N-06-21 | H4 rev 4 (TO_v04B_r4_H4, 765,252 C3D10, member size 2.5 mm, caps 2.0 x cycle 0, 60 threads): stop after cycle 28 (7 h 34 min, about 15.5 min per cycle); cycle 0 ALLSE LC1 / LC2a / LC2b / LC3a 0.1095564 / 0.1022435 / 0.0520785 / 0.2020444 N mm; volume 74,242 to 33,100 mm^3 (-55.4 %); cycle 28 f7 to f12 416.7 / 417.2 / 418.4 / 423.7 / 461.7 / 496.5 Hz, SE / cycle 0 1.58 / 1.40 / 1.60 / 2.02. Rev 2 H4 cycle 0 ALLSE (for N-06-17) 0.1096321 / 0.1018434 / 0.05185425 / 0.1993932 N mm. TH at iso 0.4 (seat tie): TH_r4b 281.3 g, f7 146.8 Hz (GPS deck), LC3a 1.20 x cap, FAIL; TH_r4b_i30 (iso 0.3) 162.3 Hz, FAIL; TH_r4b_S (side webs) 283.4 g, f7 430.7 Hz, LC3a 0.93, PASS; TH_r4b_L (local iso 0.15) f7 380.6 Hz, FAIL; with the keel zone cleaned: cA 282.2 g, f7 420.7 Hz, LC3a 0.95, PASS; cB f7 7.8 Hz, FAIL; cAB 282.3 g, f7 to f12 428.4 / 430.2 / 434.8 / 437.8 / 455.6 / 529.6 Hz, SE/cap 0.72 / 0.65 / 0.75 / 0.94, PASS; island check per part at iso 0.3 and 0.4: bosses 1 to 4, GPS deck and LID connected | see quantity | N mm; mm^3; g; Hz | set-up build log items 46, 50 to 58 | TH on the element shapes of keels_r4.py; restoration with the exact solids (N-06-22) | rev B |
| N-06-22 | Keels A and B, exact solids (claude/stage6_v04B_r4_keels_export_note.md): A 2 solids 1,315.1 mm^3 = 1.71 g (TH element shape 1,149.4 mm^3), B 105.7 mm^3 = 0.14 g incl. 20.9 mm^3 inside the sleeve and the wall gusset; K11 opening top on the rear wall face at y 2.5 to 4.5: z -3.0; gusset to z -2.0; G2 and G3 pass (0 wedges, 0 strips) | see quantity | mm^3; g; mm | s07_keels_r4.py, geometry/v04B_r4_keels/ | exact | rev B |
| N-00-03 | Actual component spend, order of 15 Jan 2026 (FC, motors, 2 batteries, props, receiver) | 153.77 | EUR | Order screenshots | exact | rev A build |

---

## 5. Assumptions register

| ID | Assumption | Why acceptable | Effect if wrong | Status |
|---|---|---|---|---|
| A-001 | The T-Motor P1604 + 3520 table represents our motors and props on our ESC | Same motor and prop; data internally consistent (N-00-02) | Hover, endurance and load numbers scale with it | Open, bounded in Stage 2 |
| A-002 | (old table) Power column is electrical power at a constant 16.0 V | Power / current = 16.0 exactly on every row | Audit only | Closed (audit only) |
| A-003 | Below 91.2 g per motor, thrust follows T = k n^2 with k from N-00-02, and power is extrapolated with a model fitted to the table | k is constant within 2 % over 20 to 100 %; the fit is checked against momentum theory in Stage 2 | Hover RPM, current and endurance shift; quantified in Stage 2 | Open |
| A-004 | Battery internal resistance: assumed value with a sensitivity band (no measurement) | No IR function on the charger | Voltage sag and full-throttle thrust shift | Open, value set in Stage 2 |
| A-005 | Hardware and wiring 12 +/- 5 g | Screws, strap, XT30 pigtail, capacitor; not itemised by any manufacturer | AUW +/- 2 % | Open |
| A-007 | GPS + compass module placeholder mass 8 g until the module is chosen (D-007) | Typical small M10 GPS with compass | Frame budget shifts by the difference | Superseded by D-076 (GM10 Nano V3, 2.6 g, listing) |
| A-008 | Air density 1.225 kg/m^3 (ISA sea level) | Braga at about 190 m: density about 2 % lower | Power +1 %, thrust at given RPM -2 % | Accepted |
| A-009 | Avionics power 1.0 W (band 0.5 to 1.5) | FC, receiver, GPS at 5 V | Endurance +/- 0.1 min | Accepted |
| A-010 | Usable capacity 80 % (band 75 to 85 %) | Landing reserve, cell protection | Endurance +/- 6 % | Accepted |
| A-011 | Mean cell voltage under hover load 3.70 V (band 3.6 to 3.8) | Nominal LiPo plateau | Endurance +/- 3 % | Accepted |
| A-012 | Arm download: Cd 1.2, wake speed 1.4 v_i at the arm (band 1.2 to 1.6), blocked length R - 5 mm | Flat-plate drag in the near wake; wake accelerates from v_i at the disc to 2 v_i far downstream | Hover power +/- 1 %; arm-width cost N-02-12 | Open, revisit with Stage 3 geometry |
| A-013 | Drag areas: front 0.0025 m^2 (band 0.0015 to 0.0035), top 0.0090 m^2 (band 0.006 to 0.012); drag area = front cos(theta) + top sin(theta) | Projected areas of battery, stack, motors and arms with Cd about 1 | Top speed band 27 to 36 m/s | Open, revisit with Stage 3 geometry |
| A-014 | Thrust falls linearly with axial advance ratio, zero at J0 = 1.1 p/D (band 1.0 to 1.25); RPM held at the full-throttle value | First-order propeller behaviour; no prop data versus airspeed | Top speed +/- 15 % | Accepted (limitation stated) |
| A-015 | Arm root at 23 mm from the centre (FC board corner); arm modelled as a cantilever from a rigid body with a 13.75 g tip mass (motor 11.6, prop 1.75, screws 0.4 g) | First-order sizing only; Stage 7 FEA replaces it | Free length and required stiffness shift | Open (Stage 3 CAD) |
| A-016 | One battery strap up to 16 mm wide (tunnel 18 x 3 mm), with a grip pad on the plate | One strap is common on 3.5 in builds; the punch-out load goes into the plate in compression, so the strap only holds the battery in negative g and crashes | Slot size changes; no structural effect at this stage | Open |
| A-017 | Stopping distance at landing: grass 10 to 15 mm, hard ground about 3 mm (local crushing, body and battery-mount compliance) | Order-of-magnitude values; no measurement | Load factor scales with 1/s | Open |
| A-018 | Motor-mount design temperature 60 C; R-09 gate: HDT at 0.45 MPa at least 70 C | Motor base temperatures after hard flights are not measured; 10 C margin; IR-thermometer check in the test plan (D-023) | Materials near 70 C (PETG HF 69, PETG-CF 74) move across the gate | Open |
| A-019 | Bambu TDS properties (dry, 100 % infill, X-Y and Z specimens) represent printed frame material | Same printer family and filaments; FEA uses solid sections | Lower infill, moisture (nylons) and print settings reduce properties; knockdowns set in Stage 7 | Open |
| A-020 | Compliance cap per load case C_i <= 2 C_i,0 (C_i,0 from the fully solid design domain) is a sufficient stiffness floor while strength is unchecked | No stiffness requirement exists; caps stand in for strength until Stage 7 | Stage 7 stresses exceed allowables: tighten the cap (for example 1.5) and rerun | Open (Miguel, 2026-10-07; checked in Stage 7) |
| A-021 | Siraya PET-CF is transversely isotropic with nu = 0.35 and G_xz = G_yz = E_z / (2 (1 + nu)) = 1070 MPa, G_xy = E_xy / (2 (1 + nu)) = 1873 MPa | No measured values (TDS, MyTechFun); FFF literature gives nu 0.2 to 0.4; shear is 13 % of arm tip deflection, G 700 to 1500 MPa moves frequency by -3 / +2 % (N-06-02) | Frequency error of a few per cent, inside the D-035 margin | Open (sensitivity run in Stage 6) |
| A-022 | Bearing allowable at bolt holes in the fin and prongs = S_xy (54.4 MPa) for forces along the layer plane | No bearing data for the material; confined bearing in FFF is usually above the tensile strength, so this is conservative | Joint heavier than needed, or (if bearing is lower, e.g. holes printed across layers) joint capacity overestimated | Open (Stage 9 test candidate: bolt bearing coupon) |
| A-023 | Battery support ribs in the optimised plate closer than about 15 mm do not point-load the soft-pack battery in a landing | Rule of thumb, no test | Battery damage in hard landings | Open (check on the TO result in Stage 7 / 8) |
| A-024 | Other hardware and wiring (strap, FC screws, wires, antenna) 12 g (A-005) lumped at the FC reference point; B joint hardware (bolts and inserts, 3.8 g per corner) modelled as separate point masses; motor and prop CG 8.5 mm above the pad | No itemised hardware list yet; the joint hardware is known from D-049 | Mass and CG errors of a few grams; small effect on frequency | Open |
| A-025 | GPS placeholder 8 g with CG at z = 28 (4 mm above the pad top, A-007) is a conservative stand-in for a small M10-class module (module and mass to be chosen, D-007) | Small GPS modules for this class are a few grams to about 8 g and some 6 to 9 mm thick (to confirm on the chosen part) | Local GPS-mount frequency and CG; a lighter module raises the local frequency (f ~ 1/sqrt(m)) | Superseded by D-076 (GM10 Nano V3 2.6 g, CG at (-40, 0, 26.5) on the lid deck) |
| A-006 | Throttle % from a manufacturer bench does not map to throttle % on our ESC; hover is stated as thrust, RPM and current, with throttle only as an estimate | Two benches give 20 % = 10500 RPM and 20 % = 17311 RPM (F-018) | Hover throttle quoted wrongly | Open |

---

## 6. Figures register

ID format figSS_topic. Vector PDF for the report, PNG for preview.

| ID | Shows | Generated by | Status |
|---|---|---|---|
| fig02_propulsion_fit | Thrust vs RPM (fit and data); electrical power models near hover | s02_sizing.py | Done |
| fig02_efficiency_chain | P_ideal / P_elec vs thrust: data and four models (rejection test) | s02_sizing.py | Done |
| fig03_design_space | Plan view and diagonal section: design regions, non-design regions, keep-outs | s03_design_space.py | Draft |
| fig03_strap_section | Section at x = 0: strap path through the centre-body tunnel | s03_strap_section.py | Draft |
| fig04_reference_geometry | Rendered reference geometry: design domains, non-design features, prop discs | s04_render_check.py | Done |
| fig05_material_map | Frequency index (X-Y and Z) against HDT, with gates | s05_materials.py | Done |
| fig05_strength_check | TDS against MyTechFun strengths (in-plane and across layers) for PAHT-CF and two PET-CF grades | s05_materials.py v2 | Done |
| fig02_endurance_mass | Hover endurance vs AUW, central and band; Volador point | s02_sizing.py | Done |

---

## 7. Files inventory

### Naming scheme (D-004)

| Type | Pattern | Example |
|---|---|---|
| Python script | sSS_topic.py (SS = stage) | s02_sizing.py |
| Figure | figSS_topic.pdf + .png | fig02_hover_point.pdf |
| Data table | dSS_topic.csv | d01_mass_budget.csv |
| CAD | revB_frame_vNN.f3d / .step | revB_frame_v01.step |
| Abaqus model | revB_<model>_vNN.cae / .inp | revB_static_v01.inp |
| Abaqus job | jSS_<case>_vNN | j07_landing_v01 |
| Journal | journal_quadcopter.md, version line at top | v0.7 |

### Inventory

| File | Version | Purpose | Status |
|---|---|---|---|
| Drone_Build_-_Design_Report.pdf | 2025-12-26 | Rev A component and sizing report | Audit input |
| Performance_Build_Excel.xlsx | sheet "Datasheet" | Rev A sizing spreadsheet | Audit input |
| bought_list.zip (Items_1 to Items_4.png) | screenshots | Orders of 15 Jan 2026 (Items 1, 2); current listings of Volador frame and Radiomaster Pocket (Items 3, 4, prices ignored) | Source of component identity |
| beso-topology-optimisation (GitHub, public) | read 2026-10-06 | Miguel's BESO framework, candidate TO tool (Q-30) | Reference |
| bambulabpetcfdatasheet.pdf, Fibreheart_PET-CF_Filament_TDS.pdf | provided 2026-10-06 | Bambu PET-CF TDS V3.0; Siraya Fibreheart PET-CF TDS | Input for Stage 5 |
| posterfinalmiguelatualizado_1.pdf | IJUP 2024 | PLA (Filament PM) on Bambu Lab X1-Carbon: tensile and Charpy at 0 and 90 deg, layer height 0.1 to 0.3 mm, layer width 0.4 to 0.8 mm; Abaqus models of three orientations | Input for Stage 5 |
| writing_style_guide.md | - | Writing rules for the report | Reference |
| s02_sizing.py | v2 (2026-10-05) | Stage 2 sizing: fits, hover, endurance, top speed, load hand-off. v2: exact download form, disk loading at hover thrust, battery mount force and arm root moment outputs. v1 kept as s02_sizing_v1.py | Done |
| stage2_revision_handover.md (project doc) | 2026-10-05 | Record of the ten corrections from the first-principles revision | Reference |
| Revision doc "Quadcopter rev B: sizing model from first principles" (https://claude.ai/code/artifact/afdb9982-8b85-415b-a50d-37df14156189) | rev 34 | Chapters 0 to 10, appendices A and B, references; derivations behind every Stage 2 number | Reference |
| Propeller Inflow Explorer (https://claude.ai/artifact/WHp9dq1HRSok2n6t88CjQT) | - | Interactive illustration of revision doc section 8.5 | Reference |
| s03_design_space.py | v3 (2026-10-06) | Stage 3 design space schematic | Draft |
| s03_strap_section.py | v1 (2026-10-06) | Strap path section | Draft |
| s04_loads.py, d04_load_cases.csv | v1 (2026-10-06) | Stage 4 load-case table | Done |
| s04_reference_geometry.py, revB_params_v01.json | v1 (2026-10-06) | Parametric reference geometry (CadQuery) | Done |
| revB_design_body_v01.step, revB_design_arms_v01.step, revB_nondesign_v01.step, revB_keepout_v01.step, revB_reference_v01.step | v01 | Design domains, non-design features, keep-outs (STEP, for Fusion and Stage 6) | Done |
| s04_render_check.py | v1 | Visual check render | Done |
| s05_materials.py, d05_materials.csv | v2 (2026-10-06) | Stage 5 material comparison with sources | Done |
| d02_results.csv, s02_output.txt | v2 | Stage 2 numeric output | Done |
| stage2_fundamentals_context.md | v1 | Context file for the parallel theory-revision chat | Done |
| journal_quadcopter.md | v0.7 | This file (also in the Drone Rework project) | Live |

---

## 8. Stage notes

### Stage 0: Set-up

Read the rev A report and spreadsheet in full and reproduced the spreadsheet chain in Python. All audit figures in the project prompt reproduce: AUW 212.8 g, hover 11416 RPM, 35.2 W total, 2.31 A total, 22.8 min, "hover throttle" 12.7 %, TWR 7.86, tip speed 149.0 m/s (Mach 0.434), all computed on the 1504 3600 KV table.

The order history of 15 January 2026 then showed that the aircraft uses T-Motor P1604 3800 KV motors, a SpeedyBee Nano ELRS receiver (single antenna) and the SpeedyBee F405 AIO 40A, so both old documents describe a propulsion set and a receiver that were never installed. Manufacturer test data for the P1604 with the same Gemfan 3520-3 prop was found and checked: the thrust coefficient is constant within 2 % from 20 to 100 % throttle, where the old table varies by a factor of 1.8. With datasheet masses, the fixed components weigh 168.6 g; with the Volador carbon frame now flying, the AUW is about 251 g before a GPS. At that weight, hover needs about 63 g per motor, below the lowest test point of 91.2 g, so the hover point will be extrapolated and its uncertainty stated (A-003).


### Stage 1: Requirements and baseline (draft, 2026-10-03)

Masses for budgeting: fixed components 168.6 g (N-00-01), hardware 12 g (A-005), GPS placeholder 8 g (A-007), RunCam Split 4 V3 10.2 g (RunCam store). Frame budget = 250 g minus the rest: 61.4 g without payload, 51.2 g with payload.

Preliminary hover endurance (Stage 0 check, not a register number): at 250 g, 14200 RPM per motor and 14 to 20 W per motor depending on the extrapolation model, giving 8 to 11 min with 80 % of 850 mAh at 15.2 V. Stage 2 narrows this.

| ID | Requirement | Proposed value | Rationale | Verification |
|---|---|---|---|---|
| R-01 | Maximum take-off mass | < 250 g in flight configuration with GPS, without payload; frame budget 61.4 g (D-014) | EU open category A1 for privately built UAS: MTOM < 250 g and max speed < 19 m/s (Reg. (EU) 2019/947, as published by AESA); lower mass also lowers every load case | Mass budget (analysis); weighing (test plan) |
| R-02 | Payload | Not in the rev B baseline. Adding the RunCam Split 4 V3 (10.2 g, 25.5 x 25.5 mm) to mass, loads and analysis is the stated next step if time allows (D-019) | Future HD recording, carried over from rev A goals | Mass budget, CAD interface check |
| R-03 | (removed, D-018) Thrust-to-weight | Output only; used as manoeuvre load factor in Stage 4 | Control authority for manoeuvres, gusts and recovery; 2 is the usual minimum for controllable flight, freestyle builds sit at 5 to 10 (practice, not a standard) | Analysis (Stage 2) |
| R-04 | Maximum speed | Not a requirement; A1 speed condition acknowledged, not pursued (D-014) | Speed drives drag and crash energy, not frame sizing at this scale | Analysis (Stage 2) |
| R-05 | (removed, D-018) Hover endurance | Output only, with uncertainty and frame-mass sensitivity | Usable mission time with margin below the 8 to 11 min preliminary estimate | Analysis (Stage 2); flight test plan |
| R-06 | Strength | No failure and no permanent deformation under limit loads; factor of safety 1.5 on printed allowables including print-orientation knockdown (D-015) | 1.5 is the conventional aerospace ultimate factor (CS-25.303 / FAR 25.303), borrowed here as a convention | FEA (Stage 7) |
| R-07 | Crash behaviour | In an arm strike, the arm fails before the centre body; the failed part is a single replaceable print; architecture deferred (D-016) | Protects the stack and battery mount; repair cost limited to one part | Analysis (Stage 4, optional explicit); test plan |
| R-08 | Stiffness and frequency | First elastic mode separated from hover 1P (about 241 Hz) and hover 3P (about 722 Hz) by a margin set in Stage 4; motor tilt under maximum thrust below a limit set in Stage 4 | Resonance near the excitation dwell frequency feeds the gyro and the control loop; motor tilt couples thrust into yaw and roll | Modal FEA, Campbell diagram (Stage 7); Blackbox FFT (test plan) |
| R-09 | Temperature | Structure keeps its properties at the motor-mount temperature (value assumed in Stage 5; IR-thermometer measurement in the test plan, D-023) | Motors heat the mounts; PLA softens near 55 to 60 C | Material selection (Stage 5) |
| R-10 | Interfaces | Motors 9 x 9 mm M2 (x4); FC 25.5 x 25.5 mm (M2, soft-mounted); RunCam Split 25.5 x 25.5 mm; battery 59 x 30 x 32 mm with strap; 3.5 in props with tip clearance set in Stage 3; receiver antenna and GPS positions reserved | Fixed by bought components | CAD inspection (Stage 3) |
| R-11 | Manufacturing | Prints on the P1S (256 x 256 x 256 mm build volume) in one plate; no supports inside functional holes; print time and material cost stated per frame | DFM | Slicer estimate (Stage 8) |
| R-12 | Cost | Frame material cost well below the Volador reference, 37.91 EUR (D-017) | Project goal: cheaper structure | Slicer estimate and filament price (Stage 8) |
| R-13 | Repairability | Broken arm replaced without reprinting the centre body and without desoldering, if the architecture allows (Stage 3) | Field repair, lower cost per crash | CAD review (Stage 3) |

### Stage 2: Sizing rebuild (2026-10-04)

**Propulsion model.** Thrust follows T = k n^2 with k = 3.088 x 10^-7 g/RPM^2 (C_T = 0.1425); the largest residual over the five test points is 1.5 % (1.46 %, at the 20 % row: fit 92.5 g against 91.2 g measured). Electrical power was fitted with four models: pure n^3 (M1), n^3 plus a constant (M2), n^3 plus a linear term (M3) and n^3 plus linear plus constant (M4). Only M4 fits all five points within about 1 %; M1, M2 and M3 miss the lowest point by 16, 12 and 8 %. Hover (64 g per motor) lies below the lowest point, so the models diverge where it matters: 12.6 to 20.2 W per motor.

**Model selection.** Momentum theory gives the ideal power at each test point. The ratio P_ideal / P_elec, which is the product of figure of merit, motor efficiency and ESC efficiency, falls steadily from 0.331 at 514 g to 0.265 at 91 g, because fixed losses weigh more at light load and figure of merit drops at low Reynolds number. A valid extrapolation must continue that fall. M1 holds the ratio constant at 0.32 and M4 turns upward below 90 g; both were rejected. M3 (aerodynamic n^3 plus a speed-proportional loss term) is the central model, with M2 as the conservative bound.

**Hover and endurance.** At 250 g with 3 % arm download, each motor produces 64.4 g at 14440 RPM and draws 18.3 W; the aircraft draws 74 W (5.0 A). Hover endurance is 8.2 min, with a band of 6.6 to 9.0 min across the accepted models, usable capacity, cell voltage, avionics load and download. Each gram of frame costs 0.036 min, and each millimetre of arm width costs 0.035 min through download, so 1 mm of arm width is worth about 1.0 g (0.96 g) of frame mass. With the Volador frame the endurance is 7.8 min.

**Loads hand-off.** The datasheet maximum of 5.04 N per motor at 16.5 V is the loads basis; with pack sag the usable thrust-to-weight falls from 8.2 to between 5.4 and 7.3. The maximum reaction torque is 0.040 N m from K_t (I - I0), matched by momentum theory with a figure of merit of 0.45 to 0.60 (0.036 to 0.048 N m) and implying a figure of merit of 0.535 at full throttle. The same K_t method fails at 20 % throttle, where it predicts less shaft power than the ideal power: the bench records battery current, which equals motor phase current only at full duty.

**Top speed.** A tilt-angle force balance with thrust falling linearly with axial advance ratio gives 30 m/s (109 km/h) at 64 deg pitch, with a band of 27 to 36 m/s from the drag-area and propeller assumptions and about 28 m/s with sag. The pitch-speed figure (34.5 m/s) is an asymptote of zero thrust, not a flight speed. The old range table and its "optimal 35 km/h, 13 km" result are withdrawn without replacement: forward-flight rotor power needs propeller data versus airspeed that is not available.

**Corrections to the old report's theory (F-013).**
- KV and current: for the same propeller and RPM, shaft power is the same. A lower-KV winding draws less current at a higher voltage; for the same stator rewound, winding resistance scales with 1/Kv^2, so copper loss at equal torque does not change. KV matches the RPM range to the pack voltage.
- PWM and saturation: the ESC switches at tens of kHz and the winding inductance averages the voltage. Magnetic saturation is an iron limit at high current that reduces torque per amp; PWM does not maintain it.
- Stator size: torque scales with r^2 L to first order at constant air-gap shear stress. The P1604 stator gives (16/15)^2 = 1.14 times the torque of a 1504 at equal height and shear stress.
- TCXO: a temperature-compensated oscillator corrects drift electronically; temperature regulation is the OCXO principle. The bought receiver data sheet does not state a TCXO.
- Low pitch and laminar flow: at a Reynolds number of about 27,000 at 75 % radius (64.4 g hover, assumed 8 mm chord) the boundary layer is transitional for any pitch. Lower pitch reduces blade angle, which lowers the stalled fraction of the blade in static thrust.
- Diversity and battery shadowing: the bought receiver has one antenna; the true-diversity argument does not apply.

### Stage 3: Architecture and design space (in progress, 2026-10-05)

**Inputs.** Motor P1604: 20.8 mm diameter x 15.5 mm height (Progressive RC listing), 9 x 9 mm M2 mount. Prop disc radius R = 44.45 mm. FC board 33 x 33 mm. Battery 59 x 30 x 32 mm.

**Wheelbase geometry (true X).** Adjacent motors are W / sqrt(2) apart, so the prop-to-prop gap g sets W = sqrt(2) (D + g): 132.8, 139.9 and 146.9 mm for g = 5, 10 and 15 mm. At W = 140 mm each prop disc overlaps the battery's corners in plan view (motor axis 39.9 mm from the corner, disc radius 44.45 mm), so a top-mounted battery must either sit above the blade plane or the wheelbase must grow to at least 155.6 mm (3 mm clearance). Measured on the Volador: blades between 13 and 18.5 mm above the arm top face, battery underside at about 23 mm. Rev B uses a raised plate at the same height (D-025), so W stays at 140 mm. The Volador clears in plan as well (estimated 5 to 8 mm, from its 160 mm wheelbase).

**Battery position and flight dynamics.** Roll inertia was estimated with lumped masses, I = sum m_i ((y_i)^2 + (z_i - z_CG)^2) + sum I_own. At equal wheelbase (140 mm) the bottom mount gives about 240 and the top mount about 250 x 10^-6 kg m^2 (4 %); an earlier comparison that also changed the wheelbase (156 mm) showed 18 %, almost all from the motors moving outward. Wheelbase dominates roll inertia because the motors are the outermost masses. A low CG gives no pendulum stability on a fixed-pitch multirotor (thrust is fixed to the body). The CG offset from the rotor plane couples translation into rotation through rotor drag; the raised top mount puts the CG at about +21 mm, close to the blade plane.

**Arm stiffness (first-order).** Arm as a cantilever from a rigid centre body with the motor, prop and screws as a 13.75 g tip mass. The first bending frequency f requires EI = (2 pi f)^2 m_tip L^3 / 3, so required stiffness grows with free length cubed. Tip deflection under maximum thrust depends only on f: delta = F / (m_tip (2 pi f)^2) = 0.11 mm at 290 Hz, so the frequency requirement, not deflection, sizes the arm. For an 8 mm wide solid arm, 50 mm free length, 290 Hz needs a section 7 to 11 mm tall for E = 8 to 2 GPa; 600 Hz needs 12 to 18 mm; above hover 3P (870 Hz with 20 % margin) needs 15 to 23 mm. Height costs mass but not download (download scales with width, N-02-12), so printed arms favour tall, narrow or truss sections.

**Arm free length.** With the arm root at about 23 mm from the centre (FC board corner, A-015), free length is about 47 mm at W = 140 mm and 55 mm at W = 156 mm: the top mount needs (55/47)^3 = 1.6 times the bending stiffness for the same frequency.

**Design space (draft, 2026-10-06, s03_design_space.py, fig03_design_space).** Coordinates: origin at the frame centre, z = 0 on the arm top face (motor seat), x forward, y left, z up; mm.

| Region | Type | Definition |
|---|---|---|
| Centre body, lower | Design | Square x, y in [-20, 20], z in [-15, 10] (floor level with the arm bottoms, D-030) |
| Centre body, upper | Design | Same square chamfered to x + y <= 31.8 (diagonal radius 22.5, inside the blade band), z in [10, 21.5] |
| Battery plate | Non-design | 64 x 34 x 2.5, z in [21.5, 24]; top face is the battery seat (battery underside at 24 mm, 5.5 mm above the blade tops) |
| Strap tunnel | Non-design (void) | One tunnel 18 mm (along x) x 3 mm high through the top of the centre body, directly under the plate, on the centreline x = 0, running along y (z from 18 to 21): the strap wraps across the battery width. At the strap's edge (x = 9) the prop keep-out starts at |y| = 24.8, so the strap clears it by more than 3 mm (D-030, A-016) |
| Arm corridors (x4) | Design (separate part, D-028) | Along each diagonal from r = 28.3 (body corner) to r = 70.0 (motor axis), width 10 (download, N-02-12), z in [-15, 0] |
| Arm clamp | Interface | Arm root engages a body corner pocket; two vertical bolts into heat-set inserts; engagement length set in Stage 6 |
| Motor pads (x4) | Non-design | Diameter 24, z in [-3, 0], 4 x M2 holes on 9 x 9 mm, central clearance hole for the shaft clip, wire exit |
| FC | Keep-out | 33 x 33, z in [-6, 6], on four bosses at (+/-12.75, +/-12.75) down to the body floor |
| GPS pad | Non-design | x in [-50, -30], y in [-10, 10], at plate height; module TBD (D-007) |
| Prop sweep | Keep-out | Cylinder of radius 47.45 (44.45 + 3) around each motor axis, z in [10, 21.5] (blades 13 to 18.5, +/-3) |
| Motors | Keep-out | Cylinder diameter 20.8 + clearance, z in [0, 15.5] |
| Component void | Keep-out | About 32 x 32, z in [6, 18], above the FC (receiver, capacitor, wiring) (D-032) |
| USB-C window | Keep-out | About 12 x 8 on the FC port side (side fixed with the FC orientation) (D-032) |
| Wire channels (x4) | Keep-out | About 5 x 5 at each body corner towards the arm (D-032) |

Free arm length with this body is 41.7 mm (body corner at 28.3 mm), shorter than the 47 mm assumed in the first-order stiffness estimate. Lower body and FC sit below z = 10 and may extend under the inner edge of the prop discs; the upper body stays inside the free square between the discs.

**Centre body: domain and expected result (2026-10-06).** The design space is the envelope the optimiser may use, not the final shape. With the battery plate (fixed) on top and a floor at z = -15, the expected result is two panels joined by perimeter structure around a hollow centre (FC keep-out, plus the component void of Q-31). Whether the perimeter becomes posts, walls or diagonal webs is the optimiser's answer: posts alone resist racking shear only in bending (weak, as with standoffs), walls and diagonals carry it in-plane, and a closed perimeter is much stiffer in torsion (Bredt: J = 4 A^2 t / perimeter) than open posts. Comparing the result with Miguel's two-panel-and-posts expectation is a report point.

**BESO framework (repository read 2026-10-06).** migueldiaslima/beso-topology-optimisation: solid-void driver (beso_main.py, 4242 lines) running in Abaqus Python; objective from element strain energy (SENER) over weighted mechanical steps; sensitivity filtering; soft-kill void material (MAT_VOID, E = 1.0); connectivity and checkerboard repair; LPBF thermal printability checks (overhang via an Abaqus thermal step); lattice engine with Gibson-Ashby TPMS properties; checkpoint/resume. No eigenfrequency response. Extension route: BESO frequency formulation (Huang and Xie) with a frequency step, modal strain and kinetic energy per element, a void density ratio to avoid spurious local modes, and mode tracking; estimated several days of development and testing. The LPBF overhang logic does not transfer directly to FFF rules.

**Abaqus versions.** Models are built in Abaqus 2022 locally; the FEUP HPC runs 2024 and 2025. Input files (.inp) written by an older version run on newer solvers; output databases (.odb) written by a newer version cannot be opened by an older one. Plan: send .inp files to the HPC and post-process there, or extract results to CSV with a Python script run in the same version.

**TO tool survey (preliminary).**

| Tool | Frequency in the optimisation | Notes |
|---|---|---|
| Own BESO | No (extension possible) | Known code; compliance only today; good comparison run |
| Abaqus Tosca | Yes: eigenfrequency design responses (DYN_FREQ) as constraints on stiffness or mass objectives; mode tracking documented | Same Abaqus models as Stage 7; licence to confirm (Q-32) |
| Fusion generative design | Yes: Modal Frequency appears as a limit in Miguel's version (screenshot 2026-10-06), alongside Displacement and Buckling; the earlier web search (a drone case with modal analysis after generation) was out of date. How the limit is defined (which modes, boundary conditions) still to check in Fusion's help | Easiest set-up; additive manufacturing constraints built in; less control over the formulation |
| nTop | Yes: natural frequency response as objective or constraint | Strong for implicit and lattice geometry; learning time (Miguel not an expert) |

**Landing loads (2026-10-06).** Energy balance for a contact that behaves like a spring: m g h = 0.5 F_peak s, so the peak load factor on every mass is n = F_peak / (m g) = 2 h / s, with h the equivalent drop height (h = v^2 / 2g for a descent speed v) and s the stopping distance. The ground bearing stress under the body is small (294 N over 40 x 40 mm is 0.18 MPa); what loads the structure is the deceleration of each mass: the battery presses on the plate with n m_b g, and each motor loads its arm tip with n m_tip g even when only the body touches the ground.

| Scenario | h_eq (m) | s (mm) | n | Battery (N) | Motor at arm tip (N) | Arm root moment (N mm) |
|---|---|---|---|---|---|---|
| Normal landing, 1.0 m/s, grass | 0.051 | 15 | 6.8 | 7 | 0.9 | 38 |
| Firm landing, 1.5 m/s, grass | 0.115 | 10 | 23 | 22 | 3.1 | 130 |
| Motor cut at 0.3 m, grass | 0.30 | 10 | 60 | 59 | 8.1 | 340 |
| Motor cut at 0.3 m, hard ground | 0.30 | 3 | 200 | 196 | 27 | 1133 |

Full thrust gives 212 N mm at the arm root. For scale, an 8 x 10 mm solid arm section (section modulus 133 mm^3) would see 8.5 MPa in the worst case, well below the strength of the candidate filaments: arms sized for frequency are likely strong enough for landings. The spring model gives peak = 2 x average; real grass and plastic crushing dissipate energy, so it is conservative. Stopping distances are assumptions (A-017).

### Stage 4: Loads (2026-10-06)

| Case | Description | Loads | Treatment |
|---|---|---|---|
| LC1 | Punch-out, all motors at full thrust | 5.04 N + 0.040 N m per motor pad; n = 8.2 on battery (8.06 N), FC + receiver (1.23 N), GPS (0.65 N), motors (1.11 N each) | Inertia relief; FoS 1.5; DF 1.0 (bound 1.03); arm design moment 210 N mm without inertia credit (D-021) |
| LC2a | Diagonal pair at full thrust, other pair at zero | 5.04 N on two diagonal pads; net yaw torque 0.080 N m; vertical n = 4.1 | Inertia relief (linear and angular accelerations); FoS 1.5; loads the saddle shape |
| LC2b | Adjacent pair at full thrust, other pair at zero | 5.04 N on two adjacent pads; pitch/roll moment 0.50 N m; vertical n = 4.1 | Inertia relief; FoS 1.5; loads the rocking shape |
| LC3a | Firm landing, 1.5 m/s onto grass | n = 23: battery 22.5 N, motors 3.1 N, FC 3.4 N, GPS 1.8 N; skid reaction 56 N | Design case, FoS 1.5 |
| LC3b | Motor cut from 0.3 m onto hard ground | n = 200: battery 196 N, motors 27 N, FC 30 N, GPS 16 N; skid reaction 491 N | Survivability: only an arm may fail (D-034, D-036) |
| LC4 | Arm strike (crash) | Arm tip failure load F_arm, worst of vertical, lateral and axial | Joint and body sized for 1.5 F_arm (D-034); F_arm from arm sizing |
| FREQ | First free-free elastic mode | at least 290 Hz (hard), goal 417 Hz | Point masses for battery, FC, GPS, motors; six rigid-body modes skipped (D-035) |

Masses: tip mass 13.75 g per arm (A-015), battery 100 g, FC + receiver 15.2 g, GPS 8 g (A-007), hardware 12 g distributed (A-005), AUW 250 g. Prop imbalance (about 0.18 N at hover 1P for an assumed 2 mg at 40 mm) and fatigue (about 870,000 cycles per hour at hover 1P) are noted but not design cases at the stress levels expected; Stage 7 checks fatigue only if stresses come out higher than expected.

**Reference geometry (2026-10-06).** s04_reference_geometry.py (CadQuery 2.8) writes the design domains, non-design features and keep-outs as STEP from one parameter set (revB_params_v01.json), checked visually in fig04_reference_geometry. Volumes (N-04-13): body domain 28.39 cm^3 after keep-outs, each arm corridor 4.38 cm^3 (17.52 cm^3 for four), non-design 12.14 cm^3; 58.1 cm^3 in total, about 70 to 75 g if fully solid at an assumed 1.2 to 1.3 g/cm^3 (densities set in Stage 5). Against the 61.4 g frame budget this allows roughly 80 % of the design domains to be filled, so the mass budget is not expected to bind; the frequency requirement and the mass objective will set the result. New parameter: arm corridor bottom rising to z = -6 at the tip (Q-37). Battery plate overhangs the body by 12 mm in x and the GPS pad cantilevers about 18 mm behind the plate; both checked in Stage 7 (GPS pad: about 7 MPa in LC3b for a 2.5 mm plate, hand estimate).

### Stage 5: Material selection (2026-10-06)

**Data.** Bambu Lab technical data sheets for PLA Basic, PLA-CF, PETG HF, PETG-CF, ASA, PET-CF, PAHT-CF and PPA-CF (dry state, ISO 527/178/179/75/1183, 100 % infill, separate X-Y and Z specimens), plus TPU 95A HF for flexible parts; sources in d05_materials.csv.

**Merit index.** Frequency drives the arms (Stage 3). With arm width limited by download and height free: k = 3 E I / L^3, I = b h^3 / 12, m = rho b h L; a fixed k needs h ~ E^(-1/3), so m ~ rho E^(-1/3). The index to maximise is E^(1/3) / rho (Ashby, stiffness-limited beam of fixed width).

**Merit index, derived step by step.**

Step 1, what the arm must do. Frequency sizes the arm (Stage 3, D-035). With the motor and prop as a tip mass m_tip on a cantilever of free length L, the first bending frequency is

    f = (1 / 2 pi) sqrt(k / m_tip)

so a frequency target fixes the arm's tip stiffness:

    k = (2 pi f)^2 m_tip

The target and the tip mass are fixed, so k is fixed. Every material must reach the same k.

Step 2, how the arm makes that stiffness. For a cantilever loaded at its tip,

    k = 3 E I / L^3

and for a rectangular section of width b and height h,

    I = b h^3 / 12

Substituting:

    k = E b h^3 / (4 L^3)

Step 3, what is fixed and what is free. L is set by the layout (Stage 3). The width b is held small, because every millimetre of width costs endurance through download (N-02-12). The height h is free: it costs mass but no download. So each material reaches the required k by choosing its own height. Solving Step 2 for h:

    h = (4 k L^3 / (E b))^(1/3)

With k, L and b fixed, h grows as E^(-1/3): a stiffer material needs a shallower arm, but only by the cube root.

Step 4, what that costs in mass. The arm's mass is

    m = rho b h L

Substituting h from Step 3:

    m = rho b L (4 k L^3 / (E b))^(1/3)

Everything except rho and E is the same for every material, so

    m ~ rho E^(-1/3)

Step 5, the index. The lightest arm comes from the material with the smallest rho E^(-1/3), which is the same as the largest

    M = E^(1/3) / rho

This is Ashby's index for a stiffness-limited beam whose width is fixed and whose height is free. Two consequences: density counts fully while modulus counts only through its cube root (a material twice as stiff makes an arm only 21 % shallower), and the index changes with the constraint (a beam free to scale in both width and height would use E^(1/2) / rho). The index assumes a solid rectangular section and frequency set by the tip mass; the optimised truss or ribbed section changes absolute masses but not the ranking for these arms.

**Gates.** R-09 heat: HDT at 0.45 MPa at least 70 C (A-018) removes PLA (57), PLA-CF (55) and PETG HF (69). P1S printability removes PPA-CF (nozzle 280 to 310 C against the P1S maximum of 300 C, and a 50 to 80 C heated chamber the P1S lacks). All carbon-fibre grades need a hardened steel nozzle.

**Ranking of the survivors.**

| Rank | Material | Index X-Y (Z) | Arm mass vs PLA | UTS Z (MPa) | Impact Z (kJ/m^2) | HDT (C) | Water (%) | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | PAHT-CF | 14.8 (12.2) | 0.76 | 64 | 13.3 | 194 | 0.88 | Best index, best across-layer strength and impact; dry-state data; drying 80 C 8 to 12 h; hardened nozzle |
| 2 | ASA | 12.8 (12.2) | 0.87 | 31 | 4.9 | 100 | 0.45 | Low density, nearly isotropic stiffness; brittle across layers; styrene fumes; warping |
| 3 | PET-CF | 13.0 (10.0) | 0.86 | 38 | 4.5 | 205 (annealed) | 0.37 | Stiff in-plane, weak across layers; heat resistance relies on annealing (Tg 75 C), which can distort parts |
| 4 | PETG-CF | 10.8 (8.8) | 1.04 | 38 | 10.7 | 74 | 0.30 | Easy to print; marginal on the heat gate; heaviest for the frequency target |

**Anisotropy.** Across-layer (Z) values are 46 to 87 % of in-plane for stiffness, 50 to 90 % for strength and 10 to 52 % for impact energy. Miguel's IJUP poster (PLA, Bambu X1C, specimens printed flat, rasters at 0 and 90 deg to the specimen axis; Q-40) measures in-plane raster-angle anisotropy: modulus 2660 to 3530 MPa at 0 deg against 2660 to 3000 MPa at 90 deg, strength 40 to 59 MPa against 30 to 43 MPa, Charpy energy 0.36 to 0.91 J against 0.08 to 0.28 J (read from the poster figures). Even within a layer, loading across the rasters cuts impact energy by roughly 3 to 5 times; across layers (TDS Z values) the loss is of the same order. Impact across rasters and layers is the weakest property of every printed material, which steers print orientation (Stage 8) and the crash weak link (D-034).

**Independent data and final choice (2026-10-06).** Manufacturer data sheets may present their materials favourably, so the shortlist was checked against MyTechFun's standardised tests (tensile in-plane and layer adhesion; values as provided by Miguel, source https://mytechfun.com/video/425 for the Siraya test):

| Material | TDS X-Y (MPa) | MyTechFun X-Y (MPa) | TDS Z (MPa) | MyTechFun layer adhesion (MPa) |
|---|---|---|---|---|
| PAHT-CF (Bambu) | 88 | 67.4 | 64 | 20 |
| PET-CF (Bambu, TDS V3.0) | 74 | 69 | 35 | 28.5 |
| PET-CF (Siraya Fibreheart) | 74 | 64 | 35 | 28.1 |

PAHT-CF's TDS across-layer strength (64 MPa) is three times the independent value (20 MPa); the PET-CF grades agree within about 20 %. Siraya Fibreheart PET-CF (TDS, unannealed): E_xy 5950 MPa, E_z 3400 MPa, density 1.3 g/cm^3, HDT 86.7 C at 0.45 MPa (176 C annealed), water absorption 0.5 %, frequency index 13.9 (X-Y) and 11.6 (Z), 40 EUR/kg. Its moduli were measured to ASTM D638 and Bambu's to ISO 527, so the 26 to 57 % higher Siraya moduli may partly reflect method and specimen differences. Design values (D-038, N-05-03) take the independent strengths and the TDS moduli with a 0.85 knockdown. fig05_strength_check compares TDS and independent strengths.

Correction (F-021): the first comparison used Bambu PET-CF TDS V2 (tensile 76 / 38 MPa); Miguel's TDS V3.0 gives 74 / 35 MPa, now used.

**Cost.** At 20 to 100 EUR/kg, a frame of about 60 g costs roughly 1 to 6 EUR in filament for any candidate, against the 37.91 EUR Volador reference (R-12); cost does not discriminate between the candidates.

### Stage 6: Topology optimisation (started 2026-10-06)

**Tool.** Abaqus Tosca (D-040). Fusion generative design as fallback; Miguel's BESO last, only if time allows.

#### Minimal supports for a free-flying structure (D-041), explained in full

*Context.* The frame flies: nothing holds it. Every static load case (LC1, LC2a, LC2b, LC3a, LC3b) must be analysed without inventing supports that do not exist in flight, because the optimiser builds load paths towards supports.

*Step 1, the static problem.* A static finite element analysis solves

    K u = F

with K the stiffness matrix, u the nodal displacements and F the loads. The solver must invert K.

*Step 2, why a free body breaks it.* A body with no supports can translate in three directions and rotate about three axes without deforming. These six rigid-body motions cost no force, so K has six directions of zero stiffness and is singular: it cannot be inverted, and the solver stops or returns meaningless displacements.

*Step 3, the physical side.* In a punch-out the thrust (20.2 N) exceeds the weight (2.45 N), so the aircraft accelerates upward. It is not in static equilibrium, and a static solver has no way to represent that acceleration directly.

*Step 4, d'Alembert's principle.* Newton's law for any part of mass m is

    F_applied = m a

Moving the right-hand side across,

    F_applied - m a = 0

so if each part is given an extra force -m a (the inertial force, opposite to the acceleration), every part is in equilibrium and the accelerating aircraft can be analysed as a static structure. For LC1 the totals are

    up:   4 x 5.04 = 20.2 N
    down: n_z m g = 8.2 x 0.250 x 9.81 = 20.2 N

where the downward total is gravity plus the inertial forces. Each part's share is applied where its mass sits: battery on its seat (8.06 N), FC on its bosses, GPS on its pad, motors on their pads, and the frame's own material as a body load at 8.2 g. The load set then sums to zero force and zero moment: it is balanced. In LC2, where only two motors push, the aircraft also gains an angular acceleration alpha, and the inertial force on a mass at position r from the centre of gravity becomes -m (a + alpha x r), so it varies from point to point.

*Step 5, why balance is not enough.* Even with balanced loads the model can still float, so K is still singular. The rigid-body motion must be removed without adding any force that does not exist in flight.

*Step 6, 3-2-1 supports.* Exactly six single restraints on three nodes that do not lie on one line:
- node A fixed in x, y and z (removes the three translations);
- node B fixed in two directions (removes two rotations);
- node C fixed in one direction (removes the last rotation).
Six restraints for six rigid-body motions, each removed once: the support is statically determinate.

*Step 7, why these supports do not change the answer.* (1) The loads are already balanced, so the supports have nothing to react: their reaction forces are zero, and a zero force changes no stress. (2) With exactly six restraints there is no redundancy, so the frame can stretch, bend and twist freely; the supports only fix where the deformed shape sits in space. The stresses and strains are those of free flight.

*Step 8, the built-in check.* The solver reports the reaction forces. If they are not close to zero, the load set is not balanced (a mass, a factor or a direction is wrong). Every static run is checked this way.

*Step 9, why not clamp the body.* A clamp adds stiffness and carries load that do not exist in flight. Stresses near it are wrong, and topology optimisation, which is very sensitive to supports, treats the clamp as ground and builds load paths into it instead of between the arm roots and the battery plate.

*Step 10, inertia relief.* Abaqus can do Steps 4 to 6 automatically: from the model's own mass distribution it computes the rigid-body linear and angular accelerations that balance the applied thrusts, applies the matching inertial forces at every node, and uses internal reference supports that carry no load. It is most useful for LC2 (angular acceleration). Inertia relief in Abaqus 2022 with Tosca: supported according to Miguel's local documentation, and *INERTIA RELIEF does not appear on Tosca's list of non-supported Abaqus keywords (which covers mesh-generation keywords such as *NGEN and *ELGEN, and *PARAMETER). Tosca reads the solver's element results, so a static step with inertia relief is just another load case to it. No public page states the combination positively, so a two-iteration smoke test is run first (see the check below). The manual balanced-load method stays as the fallback and as the hand check for LC1 and LC3a.

*Step 11, placement and modal analyses.* Support nodes are placed in non-design regions (for example the FC bosses), so any local disturbance stays out of the design region. Modal (frequency) analyses need no supports at all: a free-free eigenvalue extraction returns the six rigid-body modes at 0 Hz and the elastic modes after them.

#### Topology optimisation theory, part 1: stiffness

*The question.* Given a design domain, loads and supports, where should a limited amount of material go to make the structure as stiff as possible?

*Design variables.* The domain is meshed into elements; each element e gets a density x_e between 0 (void) and 1 (solid). The optimiser changes these numbers.

*Material interpolation (SIMP).* An element's stiffness is tied to its density by

    E_e = x_e^p E_0,    p = 3 (typical)

while its mass is proportional to x_e. At x_e = 0.5 an element costs half the mass but gives only 0.5^3 = 1/8 of the stiffness, so intermediate densities are poor value and the optimiser is pushed towards 0 or 1. BESO (Miguel's code) works directly with 0/1 elements and a soft void material; the logic below is the same.

*Objective: compliance.* Stiffness under a load is measured by the compliance

    C = F^T u = u^T K u

which is the work done by the loads, equal to twice the stored strain energy. A stiffer structure deflects less under the same load, so its compliance is lower. Maximising stiffness means minimising C.

*Constraint: volume.* The material allowed is limited by

    V(x) = sum_e x_e v_e <= V*

with v_e the element volume and V* the allowed volume (often written as a volume fraction of the domain).

*Sensitivity, derived.* The optimiser needs to know how C changes when one element's density changes. Start from compliance and equilibrium:

    C = F^T u,    K u = F

The loads do not depend on x_e, so

    dC/dx_e = F^T du/dx_e

Differentiating the equilibrium equation:

    (dK/dx_e) u + K (du/dx_e) = 0

so

    du/dx_e = - K^-1 (dK/dx_e) u

Substituting, and using K symmetric so that F^T K^-1 = u^T:

    dC/dx_e = - u^T (dK/dx_e) u

Only element e depends on x_e, and with SIMP dK/dx_e = p x_e^(p-1) k_0 (k_0 the solid element stiffness), so

    dC/dx_e = - p x_e^(p-1) u_e^T k_0 u_e

The sensitivity is negative (adding material always stiffens) and proportional to the element's strain energy. Elements with high strain energy are the valuable ones; removing material where strain energy is low costs little stiffness. BESO's sensitivity number is the element strain energy for the same reason.

*Update loop.* (1) Solve the FE model; (2) compute sensitivities; (3) filter them; (4) update densities: increase where |dC/dx_e| per unit volume is high, decrease where low, keeping V(x) = V* (optimality-criteria or MMA updates); (5) repeat until the layout stops changing.

*Filtering.* Without it, two artefacts appear: checkerboards (alternating solid and void elements that the element formulation rates as artificially stiff) and mesh dependence (a finer mesh produces finer members, so the answer never converges). A sensitivity filter replaces each element's value with a distance-weighted average over neighbours within a radius r_min, with weights w = r_min - d. This removes checkerboards and imposes a minimum member size of about r_min. For FFF, members thinner than about three extrusion widths print poorly, so with a 0.4 mm nozzle r_min is about 1.5 to 2 mm; Tosca also offers a member-size manufacturing restriction.

#### Part 1 questions and answers (Miguel, 2026-10-06)

*Q1. How is the equilibrium equation differentiated, and why is the right-hand side zero?*

Equilibrium holds for every design, so it holds as x_e changes:

    K(x) u(x) = F

Both sides are functions of x_e, so their derivatives are equal:

    d/dx_e [K u] = dF/dx_e

The left side is a product of two things that both change with x_e (the stiffness matrix, and the displacements that respond to it). The product rule gives

    d/dx_e [K u] = (dK/dx_e) u + K (du/dx_e)

The right side is zero because the loads do not depend on the design: thrust, battery weight and inertial forces of the components are the same whatever the frame layout. (The frame's own inertial load in a load-factor case does depend on x_e; Tosca includes that term, and it is small here because the frame is a quarter of the mass.) So

    (dK/dx_e) u + K (du/dx_e) = 0

In words: if element e stiffens, the displacements must change by exactly the amount that keeps the internal forces equal to the same external loads.

*Q2. How do we get from du/dx_e to the final sensitivity, step by step, with an example?*

Step A, isolate du/dx_e. Move the first term across and multiply by K^-1:

    du/dx_e = - K^-1 (dK/dx_e) u

Step B, substitute into dC/dx_e = F^T du/dx_e:

    dC/dx_e = - F^T K^-1 (dK/dx_e) u

Step C, replace F^T K^-1 by u^T. From K u = F, transposing both sides,

    F^T = (K u)^T = u^T K^T = u^T K

because K is symmetric (K^T = K: the force at node i from a unit displacement at node j equals the force at j from a unit displacement at i, Maxwell-Betti). Multiplying on the right by K^-1,

    F^T K^-1 = u^T

so

    dC/dx_e = - u^T (dK/dx_e) u

This is the penultimate step. It still contains the full matrices.

Step D, localise. The global matrix is assembled from element matrices, each depending only on its own density:

    K = sum_i K_i(x_i)

Differentiating with respect to x_e, every term with i not equal to e is constant, so

    dK/dx_e = dK_e/dx_e

K_e is zero everywhere except at the degrees of freedom of element e, so the product u^T (dK_e/dx_e) u only picks up the displacements of that element's nodes, u_e:

    u^T (dK_e/dx_e) u = u_e^T (dK_e/dx_e) u_e

Step E, apply SIMP. K_e = x_e^p k_0, so dK_e/dx_e = p x_e^(p-1) k_0, and

    dC/dx_e = - p x_e^(p-1) u_e^T k_0 u_e

This is the last step. Reading it: u_e^T k_0 u_e is twice the strain energy the element would hold if it were solid with its current deformation; p x_e^(p-1) is the penalisation factor (3 for a solid element, 0.75 at x_e = 0.5); the minus sign says that adding material lowers compliance.

*Worked example (two springs in series).* A wall, spring 1, node 1, spring 2, node 2, with a load F = 10 N at node 2. Solid spring stiffness k_0 = 100 N/mm, p = 3, densities x_1 = 1 and x_2 = 0.5, so

    k_1 = 1^3 x 100 = 100 N/mm,    k_2 = 0.5^3 x 100 = 12.5 N/mm

Global stiffness and load:

    K = [ k_1 + k_2   -k_2 ]      F = [ 0 ]
        [ -k_2         k_2 ]          [ F ]

Solving, u_1 = F/k_1 = 0.1 mm and u_2 = u_1 + F/k_2 = 0.9 mm, so

    C = F^T u = 10 x 0.9 = 9.0 N mm

Localisation for spring 2: dK/dx_2 = (dk_2/dx_2) [1 -1; -1 1], and

    u^T [1 -1; -1 1] u = (u_2 - u_1)^2

which is the elongation of spring 2 squared: only its own nodes appear. The sensitivities:

    dC/dx_1 = - 3 x 1^2 x 100 x (0.1)^2 = -3.0 N mm
    dC/dx_2 = - 3 x 0.5^2 x 100 x (0.8)^2 = -48 N mm

Check by finite difference (x_2 from 0.5 to 0.501): C falls by 0.0478 N mm, slope -47.8, matching -48 to first order. The weak spring is sixteen times more valuable per unit of material: the optimiser adds material where the structure strains most, which is exactly what the formula says.

#### Abaqus 2022 inertia relief check (2026-10-06)

- Miguel's local Abaqus 2022 documentation indicates that inertia relief is supported with Tosca.
- Tosca's documented list of non-supported Abaqus keywords (SIMULIA Tosca Structure user guide, Abaqus documentation) contains mesh-generation keywords (*ELCOPY, *ELGEN, *NCOPY, *NFILL, *NGEN, *NMAP) and *PARAMETER only; *INERTIA RELIEF is not on it.
- No public source was found that states the combination explicitly, so it is confirmed by a smoke test: LC1 with inertia relief, two Tosca iterations; pass if the run completes, the reported reference-node reactions are near zero and the element strain energies match a balanced-load 3-2-1 run of the same case within a few per cent.
- Inertia relief applies to static steps. The frequency step needs nothing: free-free extraction (D-035).

#### Topology optimisation theory, part 2: several load cases and frequency

*Step 1, several load cases.* Each static case i (LC1, LC2a, LC2b, LC3a) has its own compliance C_i = F_i^T u_i. LC3b and LC4 are not optimisation cases: they are survivability and capacity checks in Stage 7 (D-034, D-036). The cases must be combined into one problem, in one of two ways.

Weighted sum:

    C_w = sum_i w_i C_i

Simple, and the sensitivity is the same weighted sum of the individual sensitivities. The weakness is scale: C grows with the square of the load, so LC3a (n = 23 against 8.2 for LC1, a load ratio of 2.8, squared about 8) dominates with equal weights. The usual fix is to normalise each case by its value in the starting (fully solid) design, C_i / C_i,0, and then weight.

Min-max:

    minimise  max_i C_i

The design is driven by whichever case is currently worst, so no case is neglected and no weights are needed. Because a maximum has corners where it cannot be differentiated, it is solved in bound form: minimise a new variable beta subject to C_i <= beta for every i.

*Step 2, what a frequency constraint is.*

Why the project cares: the motors excite the frame at 1P (241 Hz at hover) and 3P (722 Hz). A frame natural frequency near either resonates, and the gyro reads the vibration as rotation. D-035 therefore asks for the first elastic natural frequency to be at least 290 Hz, goal 417 Hz, and in Stage 6 this becomes an optimisation constraint computed from the mesh.

One mass on one spring. Newton's law for a mass m on a spring k:

    m x'' = - k x

so

    m x'' + k x = 0

Trying x(t) = A sin(wt), whose second derivative is

    x''(t) = - w^2 A sin(wt)

and substituting:

    - m w^2 A sin(wt) + k A sin(wt) = 0

Dividing by A sin(wt):

    k = m w^2

so

    w^2 = k / m,    f = w / (2 pi)

At the natural frequency the spring force (k x) equals exactly the force needed to accelerate the mass back and forth (m w^2 x). Stiffness raises f, mass lowers it.

The arm with numbers (N-06-01, solid arm, clamped root, 736 Hz): moving mass = motor and prop 13.75 g + about a quarter of the arm's 5.7 g, m = 15.1 g; the bending stiffness that gives 736 Hz is k = 323,000 N/m.

The whole frame. The same balance with matrices:

    K phi = lambda M phi,    lambda = w^2

K is the static stiffness matrix, M the mass matrix (how much mass each node carries), phi the mode shape (how far each node moves relative to the others). At a natural frequency the elastic forces of the deformed shape (K phi) equal the inertia forces of that shape oscillating (w^2 M phi). Only certain shape/frequency pairs satisfy this: the modes (umbrella: four tips up together while the centre moves down; saddle: one diagonal pair up, the other down; twisting: arms swinging in plane). The lowest elastic one must be at least 417 Hz.

Rayleigh quotient. Multiplying K phi = lambda M phi on the left by phi^T:

    phi^T K phi = lambda phi^T M phi

so

    lambda = (phi^T K phi) / (phi^T M phi)

This is k/m with the mode shape as the weighting: the numerator counts stiffness only where the mode bends material (arm roots and joint, in the umbrella mode); the denominator counts mass only where the mode moves it (motors and outer arms). 417 Hz is reached by stiffness where the arms bend and lightness where they move.

Rigid-body modes. Free-free, the frame translates and rotates without bending: for these six shapes phi^T K phi = 0, so lambda = 0. They are modes 1 to 6 at 0 Hz; the first elastic mode is mode 7.

Normalisation. A mode fixes the pattern, not the size (2 phi is also a solution). The convention phi^T M phi = 1 fixes the size; nothing physical changes.

*Step 3, how material changes the frequency.*

Why the project needs it: every iteration the optimiser needs, for each element, the sign and size of the frequency change if material is added there.

One mass on a spring. Start from

    lambda = k / m

A little material changes k by dk and m by dm. Quotient rule:

    d lambda = (m dk - k dm) / m^2

and with k / m = lambda:

    d lambda = (dk - lambda dm) / m

dk (added stiffness) pushes the frequency up; lambda dm (added mass) pushes it down, and it is multiplied by lambda itself, so mass costs more the higher the frequency already is.

Two places to add 0.1 g on the arm (m = 15.1 g, k = 323,000 N/m, 736 Hz):
- Case A, at the root (bends, hardly moves). Illustrative assumption: k rises 5 %, no moving mass added. dk = 16,100 N/m, dm = 0, d lambda = 16,100 / 0.0151 = +1.07e6 (rad/s)^2: 736 to 754 Hz.
- Case B, at the tip by the motor (moves, hardly bends). dk = 0, dm = 0.0001 kg, d lambda = -21.4e6 x 0.0001 / 0.0151 = -0.14e6 (rad/s)^2: 736 to 733.6 Hz.
Same material, opposite effect; only its place in the mode shape differs.

General formula. Write the eigenproblem as

    (K - lambda M) phi = 0

and differentiate with respect to x_e (product rule; K, M, lambda and phi all change):

    (dK/dx_e - (d lambda/dx_e) M - lambda dM/dx_e) phi + (K - lambda M) (dphi/dx_e) = 0

Multiply on the left by phi^T. Because K and M are symmetric,

    phi^T (K - lambda M) = ((K - lambda M) phi)^T = 0

so the term with dphi/dx_e (the expensive mode-shape change) vanishes, leaving

    phi^T (dK/dx_e) phi - (d lambda/dx_e) phi^T M phi - lambda phi^T (dM/dx_e) phi = 0

With phi^T M phi = 1:

    d lambda/dx_e = phi^T (dK/dx_e - lambda dM/dx_e) phi

Localising as in part 1, with SIMP stiffness and mass linear in density (dK_e/dx_e = p x_e^(p-1) k_0, dM_e/dx_e = m_0):

    d lambda/dx_e = phi_e^T ( p x_e^(p-1) k_0 - lambda m_0 ) phi_e

It is d lambda = (dk - lambda dm)/m element by element: the first term is Case A (stiffness weighted by the element's deformation in the mode), the second Case B (mass weighted by its motion).

Difference from compliance: compliance sensitivity is always negative, so only the volume limit stops the optimiser filling the domain. Frequency sensitivity has either sign: the optimiser removes material that moves but does not bend (outer arms, around the motor pads) even without a volume limit, producing arms deep at the root and tapering towards the motor.

Impact on the project: the point masses (battery, FC, GPS, motors; D-035) must be in the model or the frequency is wrong; modes 1 to 6 are excluded; the frequency constraint shapes the design, not only checks it.

*Step 4, spurious local modes.*

Why the project cares: if the solver reports fake low modes, the constraint "modes 7 to 12 at least 417 Hz" acts on them instead of on the real umbrella and saddle modes.

Where they come from. SIMP never deletes elements: "void" elements stay in the mesh with a small minimum density (order 0.001) and keep a little stiffness and a little mass. Treat one such element, or a cluster of them, as a small mass on a spring:

    k_e = x^3 k_0,    m_e = x m_0

Its own natural frequency follows from w^2 = k / m:

    w_e^2 = (x^3 k_0) / (x m_0) = x^2 (k_0 / m_0)

so

    f_e = x f_e,solid

A near-void region vibrates at x times the frequency it would have if solid.

Numbers (order of magnitude). A 20 mm solid PET-CF feature has a local frequency of about c / (2L), with c = sqrt(E / rho) = sqrt(5058e6 / 1300) = 1970 m/s:

    f_solid = 1970 / (2 x 0.020) = 49,000 Hz

At x = 0.01 the same region of near-void elements vibrates at 490 Hz; at x = 0.001, at 49 Hz. The solver sorts modes by frequency, so the 49 Hz local modes become modes 7, 8, 9 ...: they push the real umbrella mode out of the constrained band, and the optimiser tries to raise them by adding material to the voids (from Step 3, raising x raises their k/m), filling the design with grey material or failing to converge.

Fix: modified mass interpolation. Below a threshold density (0.1) the mass is made to fall faster than the stiffness, for example (Du and Olhoff 2007)

    m_e = x m_0                 for x > 0.1
    m_e = c x^6 m_0             for x <= 0.1

with c chosen so the two branches meet at x = 0.1:

    c (0.1)^6 = 0.1,  so  c = 1e5

The stiffness-to-mass ratio below the threshold is then

    k_e / m_e = x^3 k_0 / (1e5 x^6 m_0) = 1e-5 x^(-3) (k_0 / m_0)

which grows as x falls: at x = 0.001 it is 1e4 times the solid ratio, so the local frequency is 100 times the solid one and the fake modes move far above 417 Hz. At x = 0.1 both branches give 0.01 (k_0 / m_0), so there is no jump. This mass is only an optimisation device: near-void elements are removed in the final design, whose mass is computed from solid material.

Impact on the project: confirm in the Abaqus 2022 Tosca documentation how Tosca treats low-density elements in eigenfrequency optimisation; in any case, plot modes 7 to 12 at iteration 1 and every few iterations: a mode whose motion sits in grey or void regions is spurious and the setting must be changed before trusting the run.

*Step 5, mode switching and repeated modes.*

Why the project cares: a frequency constraint written on the wrong mode makes the optimisation zigzag and can leave the real first mode unconstrained.

Mode numbering. The solver numbers modes by ascending frequency, not by shape. "Mode 7" is whichever elastic shape is currently lowest.

Switching, with an illustrative example. Iteration 10: umbrella (vertical bending, set by arm depth, I ~ b h^3) at 380 Hz is mode 7; in-plane arm swing (set by arm width, I ~ h b^3) at 450 Hz is mode 8. A constraint on mode 7 makes the optimiser deepen the arm roots and, to save volume, narrow them. Iteration 11: umbrella 430 Hz, in-plane 410 Hz: the in-plane mode is now mode 7. The optimiser widens and shallows the arms; the umbrella drops back below 417 Hz. The history zigzags and may never settle.

Remedy 1, a band. Constrain modes 7 to 12 together, each at least 417 Hz. Whichever shape is lowest is always inside the band, so swapping order changes nothing. D-035 asks for the first elastic mode of any shape, so the band is exactly the requirement.

Remedy 2, tracking by shape. When one specific shape has its own target, it is followed between iterations by the modal assurance criterion

    MAC(a, b) = (phi_a^T M phi_b)^2 / ((phi_a^T M phi_a)(phi_b^T M phi_b))

1 for the same shape, 0 for unrelated shapes: at each iteration the constraint is attached to the new mode with MAC closest to 1 against the previous umbrella shape. Not needed here, since every elastic mode has the same target.

Repeated modes. The true X has 90 deg symmetry: the mode with the front pair up and the rear pair down is the mode with the left pair up and the right pair down, rotated 90 deg, so both have the same frequency (the 64 x 34 mm battery plate breaks the symmetry slightly, giving a near-equal pair). With two equal frequencies, any mix of the two shapes is also a mode, so phi is not unique and the Step 3 formula, which uses one phi, has no unique value; as the two frequencies cross, their sensitivities jump. Constraining both members of the pair (the band again) avoids chasing one of them.

Impact on the project: the frequency step extracts about 20 modes; the constraint applies to modes 7 to 12; after each run, the band is checked to contain the umbrella, the saddle pair and the first in-plane mode, and mode 12 should sit clearly above 417 Hz so no relevant mode is outside the band.

*Step 6, which formulation.* Two candidates for this frame:

(A) Stiffness at fixed mass:

    minimise   C (weighted or min-max over LC1, LC2a, LC2b, LC3a)
    subject to V <= V*,   f_k >= 417 Hz for modes 7 to 12

(B) Mass at fixed performance:

    minimise   V
    subject to f_k >= 417 Hz for modes 7 to 12,   C_i <= C_i,cap for each load case

B states what the project wants (the lightest frame that meets the frequency goal, D-035) and gives each load case its own limit, so the weighting problem of Step 1 disappears. Its difficulty is the caps: there is no stiffness requirement in the requirements list, so C_i,cap is a stand-in for strength, set relative to the fully solid domain (proposed 2 x C_i,0, Q-43) and checked against stresses in Stage 7. A needs a volume fraction instead, chosen by a sweep. The budget leaves room: the design domain is 45.9 cm^3 (59.7 g solid) and the non-design parts 12.1 cm^3 (15.8 g), so the 61.4 g frame budget allows up to about 76 % of the design domain; frequency, not the budget, will set the mass. In Tosca, frequency constraints need the general (sensitivity-based) topology algorithm; the faster condition-based algorithm handles only stiffness with a volume constraint (to confirm in the 2022 documentation).

*Step 7, the frequency sweep.* D-035 asks for a mass-versus-frequency curve (290 / 350 / 417 Hz). With B this is direct: rerun with the frequency bound at 290, 350 and 417 Hz and record the mass. Each point is one optimisation, so the 417 Hz run comes first, then the two cheaper ones.

#### Joint concepts (2026-10-07, Q-48)

Local frame: u along the arm, v across, z up; body corner at u = 28.3 mm. M3 bolts and heat-set inserts shown; dimensions are first guesses. Files: stage6/joints/J1 to J4 .step, fig06_joint_J1 to J4 .png.

- J1, corner pocket and plug (D-028 as first drawn): the plug (u 13.4 to 28.3, z -13 to +7) runs through the FC space; the floor under the pocket is 2 mm, too thin for an insert. Does not fit (F-024).
- J2, pocket in a corner socket: a socket block (u 22 to 40, 18.2 mm wide, z -15 to +10) is added to the body; pocket 12.2 x 15 mm tall, 16 mm deep; two vertical M3 x 25 bolts from the top into inserts in a 6 mm floor. Root moment carried as a contact couple between pocket roof and floor over the pocket length; bolts clamp and hold the plug in. Arm root starts at u = 40 (free length about 30 mm).
- J3, fin and fork: an 8 mm vertical fin on the body corner (u 24 to 41, z -15 to +8); the arm root is 20 mm wide with a slot that straddles the fin; two horizontal M3 bolts through prong, fin and prong into an insert in the far prong. Root moment carried by the bolts in shear plus clamp friction; the deep fin continues the deep arm section into the body.
- J4, lap joint: a 4 mm arm flange slides into a recess in the underside of the body floor (u 10 to 28.3); two M3 bolts from below into short inserts in the floor; the arm root is cut to sit against both corner faces. Lightest and shortest bolts, but the inner bolt is in tension when thrust lifts the arm (inserts pulled across layers), and the recess conflicts with the skid groove (D-039).

---

## 9. Audit findings

Status: **V** = verified, **C** = corrected (new number referenced), **O** = open, **R** = resolved.

### Component identity (from order history)

| ID | Document | Finding | Status |
|---|---|---|---|
| F-014 | Report, spreadsheet | **Wrong motor.** Both documents size the aircraft on a "1504 3600 KV" (report Fig. 4 shows Darwin FPV 1504 motors). The motors bought and flown are T-Motor P1604 3800 KV: 16 x 4 mm stator, 11.6 g, peak 16.8 A and 277.8 W. Every propulsion number in both documents (TWR, hover, speed, endurance, ESC margin, stator-size and KV reasoning) refers to a motor not on the aircraft | V, rebuild in Stage 2 on D-010 |
| F-015 | Report 3.5 | **Wrong receiver.** Report describes ESP32-PICO, dual SX1280, true diversity, TCXO. Bought: SpeedyBee Nano 2.4 GHz ELRS, ESP8285 + SX1281, single T antenna, 0.7 g. The true-diversity argument and the "battery shadow" diversity solution do not apply | V, rewrite |
| F-016 | Report 3.1, project prompt | FC named "SpeedyBee F405 Mini AIO". Bought: SpeedyBee F405 AIO 40A Bluejay, 25.5 x 25.5 mm, 13.6 g (the F405 Mini is a different 20 x 20 product). Report claims "4-6 UARTs"; the board has 4 full UARTs + SBUS | V, rename |
| F-017 | Report, prompt | Motor mount: P1604 listings disagree (12 x 12 M2 on T-Hobby, 9 mm M2 on Rotorama). Measured by Miguel: 9 x 9 mm M2 | R |
| F-009 | Report BOM | Stated total 191.94 EUR does not match its own lines (205.03 EUR). Actual order totals: FC 52.70, motors (P1604, 4 pcs) 43.26, batteries (2 pcs) 38.29, props 5.74 + 2.69, receiver 11.09: 153.77 EUR. Charger 31.42 and smoke stopper 3.98 bring it to 189.17 EUR. Radio and Volador frame not from orders | R |
| F-010 | Report, spreadsheet | Motor mass 9.1 g (report) and 37.8 g labelled "9.2 g each" (spreadsheet; 4 x 9.2 = 36.8). Actual motor: 11.6 g, 46.4 g total | R |
| F-011 | Report Fig. 2 | Wiring figure is the SpeedyBee generic diagram (TBS Crossfire, SBUS receiver, VTX, LED strip); not the as-built wiring | V, replace |

### Spreadsheet

| ID | Finding | Status |
|---|---|---|
| F-001 | Inconsistent baseline: GNB 1100 LiHV (88 g), 50 g PET-CF frame, AUW 212.8 g, TWR 7.86; report uses Tattu 850, 250 g, TWR 6.7 | V, fix in Stage 1/2 |
| F-002 | Hover from power laws calibrated at 100 % (thrust ~ n^2 D^3 p, power ~ n^3 D^4 p): 11416 RPM, 35.2 W, 22.8 min. Even on its own (wrong-motor) table, interpolation gives 12.4 W per motor at the spreadsheet's 212.8 g (14.8 W at 250 g), so the law (8.8 W per motor) underestimates hover power by about 30 %. Standard form: T = C_T rho n^2 D^4 | C (N-02-07, N-02-10) |
| F-003 | "Hover Throttle %" = hover thrust / max thrust (12.7 %): a thrust fraction, not a throttle position | C (N-02-09, A-006) |
| F-004 | Cruise from pitch speed (V = n x pitch); demands 761 W at 97 km/h. Range table and "optimal 35 km/h, 13 km" depend on it | C: top speed N-02-21; range table withdrawn |
| F-005 | Internal resistance from 1200 / (mAh x C), unverifiable source; uses 60C/120C (GNB values) | C (A-004, N-02-19) |
| F-006 | Watt-density thermal thresholds (0.2, 0.25 W/mm^3) unsourced | R: dropped (D-023) |
| F-007 | Old bench table: thrust / RPM^2 rises from 2.2 to 4.1 x 10^-7 across the range; 90 to 100 % predicts 375 g, table says 418 g; power column = 16.0 V x current | V, moot after D-010 (audit note only) |
| F-019 | Battery voltage 15.2 V used for all current calculations, while the bench data is at 16 V (old table) or 16.5 to 16.8 V (P1604 table) | C (A-011) |

### Report

| ID | Finding | Status |
|---|---|---|
| F-008 | Hover current 1.5 A per motor at 62.5 g gives 6.8 min; its own table gives 0.93 A | C (N-02-10) |
| F-020 | GNB 1100 LiHV mass of 88 g in the spreadsheet: verified on the Pyrodrone listing (62 x 33 x 25 mm, 15.2 V LiHV, 60C/120C). Claude's suspicion in Stage 0 was wrong | R |
| F-021 | Stage 5 (own work) | Bambu PET-CF values first taken from TDS V2 (76 / 38 MPa); Miguel's TDS V3.0 gives 74 / 35 MPa | C (s05_materials.py v2) |
| F-022 | Stage 4 (own work) | Reference STEP v01: (1) the arm corridors start at r = body_half x sqrt(2) = 28.3 mm with a root face normal to the diagonal, which touches the 40 x 40 body only along its vertical corner edge: zero overlap volume (checked in CadQuery), so arms and body are not connected in a mesh; (2) the arm corridor fills the motor centre hole and the inner M2 hole (117 mm^3), which were cut only from the motor pad. Spotted by Miguel in Fusion | C (reference geometry v02) |
| F-023 | Stage 6 (MyTechFun data, Siraya PET-CF, as provided by Miguel) | MyTechFun's flexural modulus (3742 MPa) is the secant from zero at 1.25 kg: E = F L^3 / (4 b h^3 d) with span 50 mm, 10 x 4 mm bar, d = 0.16 mm. The load-deflection points are not proportional (seating at the supports and loading nose, 0.01 mm reading resolution). A chord between 1.25 and 2.5 kg (strain 0.0015 to 0.0026, close to the ISO 178 chord of 0.0005 to 0.0025) gives 5443 MPa; 2.5 to 10 kg gives 6089 MPa; shear adds only 3.6 % at span/depth 12.5. Consistent with the TDS (5600 MPa flexural); design E_xy 5058 MPa confirmed, no extra Stage 7 check. Creep negligible (0.86 to 0.87 mm at 10 kg; ring 12.12 to 12.16 against a 15.4 to 17.2 average) | R (resolved) |
| F-024 | Stage 6 (own work) | The D-028 pocket cannot sit at the body corner: the FC (33 x 33 mm, z -6 to 6) reaches r = 23.3 mm along the diagonal, the body corner is at r = 28.3 mm, leaving about 5 mm of pocket depth at FC height; the component void sits above. A joint concept study is needed before reference v02 | Open |
| F-025 | Stage 6 (own work) | Reference v02 (J3 per D-047 to D-049): non-design material 35.9 cm^3 = 46.6 g solid (fins 15.1 g, prongs 15.8 g, plate, GPS pad, FC bosses and motor pads 15.8 g), leaving 14.8 g of the 61.4 g frame budget (D-014) for all design material (body and four arms); joint hardware 13.2 g bolts + about 2.8 g inserts against a 12 g allowance for all hardware (A-005). R-01 (AUW < 250 g) at risk with J3 as sized | Open (Q-52) |
| F-026 | Stage 6 (own work) | v01 and v02 motor wire channels run along the arm axis at z -8 to -3 through the body corner, i.e. through the J3 fin and its lower bolt boss. v03 moves them off axis (local v = 9.5 to 14.5, outside the fin and its fillets) | C (reference v03) |
| F-027 | Stage 3/4 parameters (own work) | Strap tunnel roof at z = 21 while the plate underside is at z = 21.5 (plate top 24, 2.5 mm thick) left a 0.5 mm body sliver over the tunnel: below the 2.5 mm member size, unprintable and harmful to the mesh, with no function (the plate height is set by the prop keep-out top at 21.5). Tunnel roof raised to 21.5 so the fixed strap band forms the roof; tunnel 3.5 mm tall | C (reference v03 rebuilt; body design B 89.1 g, C 119.6 g solid; fixed masses unchanged) |
| F-028 | Stage 6 generator (own work), found in the set-up chat | (1) v03-B arm split by prong planes left tangent slivers at the slot end and arm top; arms could not be meshed (fixed by D-054). (2) The FC boss cylinders were not subtracted from body_design: 0.79 cm^3 counted twice in the frame mass and 0.29 g of design plugs in the FC screw holes (build log DV-2, DV-3); generator now removes them. Expected model mass 322.2 g (frame 116.8 g), not 323.5 g | C (generator v03 rev 2026-10-08, D-054) |
| F-029 | Stage 6 Phase 8 (set-up chat) | Reference run of the solid design space: mode 7 (365.2 Hz) is a local bending mode of the GPS overhang plate, not a frame mode; global modes 8 (umbrella) 487.6 Hz, 9 and 10 (saddle pair) 521.0 / 523.9 Hz, 11 566.6 Hz; mode 12 (689.0 Hz) local, GPS overhang plus battery plate front edge. Fixed by D-056 | C (D-056) |
| F-030 | Stage 6 Phase 8 (set-up chat F-11) | CAE 2022 writes *Distributing without a formulation keyword; the solver uses STRUCTURAL and, with all coupling nodes on solid elements, drops the rotational part, so the couplings act as continuum couplings. Moments still pass through as force couples; no model change | R (noted in the set-up sheet) |
| F-031 | Stage 6 (own work, raised by Miguel) | First flared-keel candidate (half-width 11) met the fin root fillets 0.14 mm from their tangent line on the body rear face, the same near-tangency mechanism as the D-051 arm split (F-028): the face-size test passed but an independent gmsh mesh test found 9 sliver tets (quality 0.002) at (-20, +-11, 9 to 11). Half-width reduced to 9 (1.86 mm clear): no slivers, quality equal to the baseline. New permanent check: s06_gmsh_meshtest.py alongside the face test; it reproduces the old D-051 failure (81 slivers, quality 0.001) and passes all D-054 arms | C (D-056 rev.) |
| F-032 | Stage 6 set-up chat (F-13), lesson for D-041 | Tosca 2022 stops with 'Inertia relief is not allowed for sensitivity-based topology optimization'; the 2023 to 2025 documentation lists it as supported with 3D elements and Abaqus sensitivities. The 2026-10-06 check relied on the list of unsupported keywords, which does not show this limit. The 3-cycle chain test without inertia relief confirmed the rest: Hz units, start density 1.0, sensitivities on all steps, rotational arm symmetry, constraint handling; mode 11 (battery plate front edge) fell fastest (681.8 to 541 Hz in 3 cycles) | R (D-060) |
| F-033 | Stage 6 HPC (set-up chat F-14) | First H0 run on Abaqus 2025 with free-free inertia relief: mass, frequencies and LC1 exact, but LC2a, LC2b and LC3a strain energies of 1e6 to 1e9 N mm. Abaqus 2025 reuses the LC1 factorisation in the later static steps (2022 re-factorised); the inertia-relief singularity is regularised inside that factorisation, which is not valid for other load vectors; the solver warned in every step to add statically determinate supports. A version check against the 2022 reference caught it | R (D-064) |
| F-034 | Stage 6 HPC (set-up chat F-15) | First H2 start failed in cycle 0: Abaqus 2025 does not support adjoint sensitivities with inertia relief, nor with the eigenvalue step, in MPI mode, and at 32 cores across two sockets it chose MPI (threads at 16 cores). Fix: mp_mode=threads in the .par solver arguments only (the optimization command line rejects it) | R (set-up chat DV-19) |
| F-035 | Stage 6 (set-up chat F-16), v03-B print set | The print set cannot be assembled: the FC bay is closed on every side (openings only the USB window, the strap tunnel, 4 x 4 lead passages and 1 to 3 mm corner slits; roof closed by the fixed plate and an optimised ceiling); the FC cannot be inserted from any side (design material 607 to 861 mm^3 in each direction); the FC boss holes are blind with no screwdriver line; no passage for the battery lead, GPS cable or receiver antenna. Cause: the design space defined where components sit (D-032 voids) but not how they get there, and Tosca filled every assembly path | C (v04-B redesign, D-072 to D-078) |
| F-036 | Stage 6 (set-up chat F-17), H4 cycle 31 | The fixed antenna boss (dia 5.4 x 6.5 at (-44, 0), 0.15 g) touched only design material and carried no load or mass in the model (the antenna and holder were lumped at RP_FC), so Tosca removed the keel material around it; thresholded at iso 0.4 it was a loose part with six rigid-body modes on air (TH04 modes 7 to 12 at 45 to 200 Hz) | C (D-084, D-085) |
| F-037 | Stage 6 (set-up chat F-18), H4 cycle 31, TUB elements only, no tie proximity | Keel lid boss 5 (-30, 0) is an island in the TUB at iso 0.4 (141.4 mm^3 shell, 3.78 mm from the main tub) and joined only by a chain of single elements between 0.3 and 0.4; all tub material behind x -34.5 removed. The boss carried the lid tie, so the lid held it and TH04 (with tie proximity) did not see it; the GPS deck on the lid was cantilevered from the lid | C (D-086) |
| F-038 | Stage 6 (set-up chat), H4 rev 4 cycle 28 | The fixed GPS deck (RP_GPS 4.23 g) was connected to the tub at every threshold (D-085 met) but its support in Tosca was a wide block of grey keel material, mostly below 0.15 density, that carried it at 461.7 Hz in the optimiser and vanished at any threshold from 0.3 to 0.5; thresholded, the deck hung on two thin front straps (TH 146.8 Hz). The connectivity check measures topology, not stiffness | C (D-087, D-088) |
| F-012 | 2300 KV rejection scales loaded RPM linearly with voltage; "TWR > 4" target unsourced. The KV comparison is moot for the P1604 but the KV-selection reasoning is rewritten in Stage 2 | O |
| F-013 | Theory to correct or remove: lower KV draws less current for the same load; TCXO "mechanically regulates" temperature; low pitch "ensures laminar flow"; PWM "maintains magnetic saturation", 4500 KV "exceeds saturation"; torque ~ r^2 as a law (first-order only: T ~ r^2 L at constant airgap shear stress) | O, Stage 2 |
| F-018 | Throttle % is bench-specific: 20 % = 10500 RPM on the old table and 17311 RPM on the P1604 table. Throttle percentages cannot be carried between data sets | V, A-006 |

Kept after check (recompute on P1604 data in Stage 2): tip speed method, disk loading, battery C-rating check, ESC margin method, T ~ D^4 n^2 and P ~ D^5 n^3 (report 3.4.2), 36 % disk-area gain of 3.5 in over 3 in.

---

## 10. Lessons and surprises

| ID | Stage | Note |
|---|---|---|
| L-001 | 0 | The spreadsheet and the report miss the hover current in opposite directions (2.3 A vs 6.0 A total, against 3.7 A from their own table), so their endurance figures (22.8 and 6.8 min) differ by a factor of 3.4 |
| L-002 | 0 | Both rev A documents were sized on a motor that was never bought. The error survived because each document was checked against the other and neither against the order history. Rev B traces every component to its purchase record and datasheet |
| L-003 | 0 | The real motor's data has a constant thrust coefficient (2 % spread), while the table used in rev A varied by a factor of 1.8: a quick C_T check flags suspicious manufacturer data before any model is built on it |
| L-005 | 1 | Endurance and thrust-to-weight looked like natural requirements but the frame barely moves them: they belong to the components, and the frame acts only through mass. Requirements were kept to what the frame controls: mass, strength, stiffness, crash behaviour, interfaces, manufacturing, cost |
| L-006 | 2 | Motor torque from K_t times bench current works at full throttle and fails at low throttle (it predicts less shaft power than the ideal power). The bench logs battery current, and under PWM the motor phase current is larger by roughly 1/duty |
| L-007 | 2 | The preliminary 8 to 11 min endurance band shrank to 6.6 to 9.0 min once a physical test (the efficiency chain must fall at light load) rejected the two optimistic fits, including the one with the best fit to the data |
| L-008 | 2 | Arm width costs endurance through download: 1 mm of width on four arms costs as much as about 1.0 g (0.96 g) of mass. Stiff wide arms are not free, which feeds the Stage 3 and Stage 6 trade |
| L-009 | 6 | Software capability claims are confirmed by running a minimal case, not by reading feature lists: the unsupported-keyword list said nothing about inertia relief in sensitivity-based Tosca, and the limit only surfaced when the job was submitted (F-032) |
| L-010 | 6 | A solver upgrade can change numerical behaviour without changing any input: the same .inp gave correct LC1 and wrong later steps on Abaqus 2025. Running the reference job on the new version before the optimisation (H0) found it in two minutes instead of after a 3.5 h run |
| L-011 | 6 | A rule written to detect one failure (spurious void modes) also fired on a legitimate state (grey arm tips in bending modes). The thresholded job, which measures the printable part directly, was the decisive test and should have been the acceptance test from the start |
| L-012 | 6 | A design space must contain assembly paths, not only component volumes: every component needs an insertion path, a tool path and a cable path as keep-outs (D-078) |
| L-013 | 6 | Check the identity of every input file (solid count, volumes) before use: the first BODY.step used for the restoration was an older export (23 solids instead of 14) |
| L-014 | 6 | Tosca odbs are flattened to one instance (PART-1-1); scripts that look for assembly sets in them must search instance sets |
| L-015 | 6 | A fixed region is only kept by the optimiser if it carries something or touches other fixed material; check fixed-region connectivity at export and islands after every thresholding (F-036) |
| L-016 | 6 | A tie to another part can hold a fixed solid as well as its own part can: the optimiser then removes the material on one side. Check islands per part without tie proximity, and give each fixed solid a reason to be kept within its own part (F-037) |
| L-017 | 6 | Before a long optimisation run, do a coarse rehearsal and a TH on its saved cycles: a threshold failure such as F-038 shows within hours, not after an 8 h production run. Grey support under a fixed mass is visible in the rehearsal densities |
| L-004 | 0 | The aircraft is overpowered for hover: about 63 g per motor needed against 514 g available (TWR about 8.2 at 251 g). Hover sits below the lowest manufacturer test point |
