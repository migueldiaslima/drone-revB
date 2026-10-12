# Stage 6 handover: Abaqus/Tosca set-up chat (v03-B)

Purpose of this chat: build, debug and run the v03-B Abaqus model and then the Tosca task, keeping the main project chat free of debugging. Results and decisions come back to the main chat as a short summary; the journal (`claude/journal_quadcopter.md`) stays the master record and is updated from the main chat.

## Read first
- `claude/stage6_model_setup_part1.md`: the step-by-step model sheet (parts, material, sets, point masses, ties, steps, loads, mesh, checks).
- `claude/journal_quadcopter.md`, Stage 6 notes and decisions D-040 to D-053, assumptions A-020 to A-024, findings F-022 to F-027, open questions Q-49 and Q-53.

## Fixed context (do not reopen here)
- Frame rev B, 3.5 inch true X, 140 mm wheelbase; material Siraya PET-CF, transversely isotropic (D-045): E 5058 / 5058 / 2890 MPa, nu 0.35, G 1873 / 1070 / 1070 MPa, density 1.30e-9 t/mm^3.
- Variant B, repairable: J3 fin-and-fork joint, steel M3 x 20 bolts, Ø12 bosses fixed, ties between boss faces (D-047 to D-051). Variant C (one-piece) is the second run, later (D-053).
- Free-flying model: no boundary conditions; inertia relief in the static steps; free-free frequency step (D-041).
- Load cases: LC1, LC2a, LC2b, LC3a as in the sheet (N-02-16, N-02-17, N-04). LC3b and LC4 are Stage 7 checks.
- Formulation for Tosca (part 2, later): minimise volume; modes 7 to 12 at least 417 Hz; compliance caps C_i <= 2 C_i,0 from the solid reference run (D-042, A-020); member size about 2.5 mm (Q-49); freeze load regions.
- Units mm, N, tonne, s. Abaqus/CAE 2022 locally; HPC 2024/2025 for production runs.

## Files (from the main chat, stage6_abaqus_v03B.zip)
BODY.step, ARM_pp/pm/mp/mm.step (design and fixed solids per part), reference_points.csv (point masses, rotary inertia, coupling surfaces, loads).

## Working rules
- Miguel builds the model by hand in CAE (D-043); scripts only as a fallback.
- One step at a time; explain the physics and the effect on the project of each setting; label assumptions; never invent values.
- Note every deviation from the sheet (for example an import option or inertia relief route that CAE 2022 does not offer) and why.
- No em dashes; direct headings; derivations as phrased steps with formulas on their own lines.

## What to bring back to the main chat
1. Model status and any deviations from the sheet.
2. Reference run (solid design space): element and node count, total mass (expected 322.2 g for the D-055 export, 333.7 g with the D-056 GPS keel), frequencies and shapes of modes 7 to 12, ALLSE per static step (C_i,0 = 2 x ALLSE), warnings.
3. Inertia relief smoke test result (LC1 vs a 3-2-1 supported run).
4. Later: Tosca part 2 results (mass history, final frequencies, compliances, the extracted shape).
