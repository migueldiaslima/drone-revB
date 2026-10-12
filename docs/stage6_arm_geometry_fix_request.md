# Stage 6: arm STEP split fix (v03-B), for decision in the main chat

From the Abaqus set-up chat. Supersedes the first version of this note (2026-10-08 evening), whose diagnosis and suggested fixes were incomplete: raising the arm top to z = 10.3 would enter the prop keep-out (D-046, arm top = 3 mm under the lowest blade), a smaller boss would leave a 0.2 mm design sliver over the boss and change D-051, and the slot itself was not the cause.

## What the design intent produces (no error in the decisions)

All three geometric facts below follow directly from accepted decisions; each is correct on its own, the problem is only how the design/fixed split meets them.

| Fact | Comes from | Value |
|---|---|---|
| Slot end is a full semicircle tangent to the flat inner prong faces | D-048 (fin sides and prong faces flat and parallel, slot end a full semicircle) | slot half-width 5.15 = semicircle radius 5.15, centre 34.35 mm along the diagonal |
| Upper Ø12 prong boss reaches exactly the arm top | D-049 (edge distance 6 mm) with D-051 (Ø12 bosses fixed) and D-046 (arm top z = +10 under the prop keep-out) | boss axis z = 4, radius 6, top z = 10 |
| Bolt hole passes the slot-end tangent line | D-049 bolt line at 33 mm, slot-end centre at 34.35 mm | Ø3.2 hole reaches 34.6 mm, 0.25 mm past the tangent line |

## Why the arms cannot be meshed

`ARM_FIXED` holds the prong bosses as Ø12 disks between the prong planes (5.15 to 10.15 mm from the arm axis). Their inner boundary is therefore the plane at 5.15 mm, which beyond the slot-end tangent line runs inside the solid arm and meets the slot semicircle tangentially. With the facts above this leaves, per arm:

| Feature | Size | Cause |
|---|---|---|
| 4 crescents | 0.0058 mm^2, 3 um wide | the bolt hole cuts the thin design lip between the slot semicircle and the boss plane, 0.25 mm past the tangent line |
| 2 strips | 0.069 mm^2, 0.15 mm tall | design material between the upper boss circle and the arm top, where the circle is tangent to the top |
| zero-angle wedge | along the slot-end tangent lines | design lip between the boss plane and the slot semicircle |

Abaqus/CAE 2022 results: ARM_mm meshed only with clusters at these features (78,858 elements); ARM_mp fails at every global or local seed from 1.0 to 0.1 mm except a 0.55 mm global seed (387,289 elements for one arm, warnings all along the tangent lines). Repair small faces (0.4 mm tolerance edges), remove faces (deleted the design cell) and virtual topology (crescents untouched) did not help. Post-processing tests with a larger slot radius, a larger boss radius or a slot-tool recut created new thin faces. BODY meshed (140,463 C3D10, 0 errors, 0.37 % warnings) and is not part of this request.

## Proposed fix: change only how the fixed bosses are cut

Arm envelope, bolt line, holes, inserts pockets, slot, fin interface, motor pad and all keep-outs unchanged. Only the design/fixed split changes:

1. Each prong boss pair becomes one Ø12 cylinder along the bolt axis through the full fork width, clipped by the arm envelope (so the thin lip next to the hole at the slot end is fixed, and the boss boundary is the cylinder, not the prong plane).
2. The upper boss is extended upward over its 12 mm width to the arm top (a "tombstone" outline: Ø12 below the axis, straight sides up to z = 10), so its boundary crosses the top face at right angles instead of touching it. Structurally this is the 6 mm edge-distance material above the upper bolt (D-049), which carries the bolt bearing load towards the top edge.
3. Motor pad unchanged.
4. `fixed = envelope AND tools`, `design = envelope MINUS tools`, with the same tools for both, so design and fixed faces coincide exactly.

Tested in the set-up chat on the v03-B STEPs (script `s06_arm_split_fix_v03B.py`, output `abaqus_v03B_fix/ARM_xx.step`, sent to Miguel):

| Per arm | Before | After |
|---|---|---|
| Design volume | 8307.9 mm^3 (10.80 g) | 8036.9 mm^3 (10.45 g) |
| Fixed volume | 2662.5 mm^3 (3.46 g) | 2933.5 mm^3 (3.81 g) |
| Total | 10970.4 mm^3 | 10970.4 mm^3 (envelope unchanged) |
| Acceptance (general fuse; no face < 0.5 mm^2, none narrower than 0.3 mm) | 6 failing faces, smallest 0.0058 mm^2 / 3 um | pass; smallest face 2.5 mm^2, narrowest 0.4 mm |

Remaining narrow feature (by design, not a defect): the prong tip sits at 26.5 mm along the diagonal (D-048 tip clearance) while the Ø12 boss and the extended upper boss start at 27 mm, so a 0.5 mm design strip remains along the prong tip (top-face edge 0.5 mm; same 0.5 mm gap existed before around the boss circles). It is 170 times wider than the removed crescents, not tangent, and passes the acceptance test. Alternatives checked to remove it: extending the bosses to the prong tip (D-shaped bosses, +0.80 g per arm, leaves a 1 mm band between the bosses) or freezing the whole prong root end (+0.88 g per arm); both cost about 3.2 to 3.5 g in total and were not adopted.

Mass effect: fixed material +0.35 g per arm, +1.41 g in total (variant B fixed 29.0 to 30.4 g, N-06-05); design material in the arms 43.2 to 41.8 g solid. Q-53 (B design allowance about 15.6 g) shrinks by the same 1.4 g.

## Requested in the main chat

1. Decide whether to accept the new fixed-boss rule (proposed decision record: through-fork Ø12 bolt bosses, upper boss extended to the arm top; supersedes the boss shape in D-051 for the TO model; +1.41 g fixed).
2. If accepted: record it (decision, N-06-05 and Q-53 numbers), and adopt the same rule in the generator for variant C and any later export. The set-up chat imports the provided `abaqus_v03B_fix` STEPs now; a regenerated set from the main chat is welcome but not required for v03-B.
3. For later (variant C and future exports): same envelope rule for BODY (the upper fin bosses also reach z = 10 and appear to have the same tangency; BODY meshed, but its verify warnings cluster at the fin bosses) and subtract the FC boss holes from `body_design` (DV-2).
