# Stage 6: concepts explained (topology result to printed part)

Reference notes from the set-up chat, 2026-10-10. Written so the reasoning behind the Stage 6 decisions can be read again later without the chat. Numbers refer to run H3 (1.0 mm mesh, member size 2.5 mm, Tosca 2024 on nexus), cycles 32 to 40. Related records: `claude/stage6_build_log_v03B.md` (Phase H), `claude/stage6_hpc_H2_report.md`.

## 1. The density field

**What Tosca optimises.** The design space is divided into small tetrahedral elements (about 527,000 design elements in H3). Tosca does not choose "material / no material" per element directly, because a yes/no choice cannot be improved step by step with gradients. It gives every element a number between 0.001 and 1, the relative density (`MAT_PROP_NORMALIZED` in the odb):
- 1 = fully solid;
- 0.001 = effectively empty (never exactly 0, so the stiffness matrix stays solvable);
- in between = "grey".

**Why grey exists and why Tosca avoids it.** A continuous number lets Tosca compute sensitivities and move the design gradually. Grey is not a real material, so the optimiser is made to dislike it through a penalty. In textbook SIMP with penalty 3:
- stiffness of an element = rho^3 x solid stiffness;
- mass (and volume cost) = rho x solid.

At rho = 0.5 an element costs 50 % but gives 12.5 % of the stiffness: a bad deal, so the optimiser pushes elements towards 0 or 1. (Tosca 2024 actually used a softened version, section 9.)

**The field.** Taken together, the numbers form a field, a value at every point, like height on a terrain map: high ground (near 1) is where material wants to be, low ground (near 0) is where it does not, slopes are the grey transition zones.

## 2. The iso level

**Iso surface.** "Iso" means equal. On a map an iso line (contour line) joins points of equal height. In 3D the iso surface at level c joins all points where the density equals c. It is a closed skin separating:
- inside: density >= c, kept as material;
- outside: density < c, removed.

**Why a lower c keeps more.** Flood the terrain to a water level c; everything above the water is printed. A low level (0.3) leaves more land dry, including lower slopes; a high level (0.5) floods them.

1D example, a row of seven elements across a wall:

| Element | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| rho | 0.001 | 0.2 | 0.4 | 0.9 | 1.0 | 0.6 | 0.1 |
| kept at iso 0.3 | no | no | yes | yes | yes | yes | no |
| kept at iso 0.5 | no | no | no | yes | yes | yes | no |

The wall is 4 elements thick at 0.3 and 3 at 0.5; element 3 is the grey one that the choice of cut decides. H3 cycle 33: printed frame 82.5 g at iso 0.3 against 72.2 g at iso 0.5.

## 3. Density-weighted volume and the volume-preserving cut

**What Tosca counts.** Volume objective = sum of (rho x element volume) (`R_VOL`). A 1 mm^3 element at rho 0.4 counts 0.4 mm^3. This is the amount of material behind Tosca's reported frequencies and strain energies.

**What the printed part has.** After the cut every kept element is fully solid: printed volume = sum of the full volumes of kept elements.

**When they match.** In the 1D example (1 mm^3 each): weighted = 3.2 mm^3; iso 0.3 keeps 4 mm^3 (more than Tosca counted: grey turned solid); iso 0.5 keeps 3 mm^3 (close). The cut where printed volume equals the weighted volume is the volume-preserving cut.

**H3.** Smoothed iso 0.5 frame 55,554 mm^3 minus fixed regions 24,353 mm^3 = about 31,200 mm^3 of design material; Tosca `R_VOL` at cycle 32 = 31,208 mm^3. Iso 0.5 is about volume-preserving for this design: the faithful translation of Tosca's result into a real part. Equal volume does not guarantee equal stiffness or frequency (material moved from grey to solid), hence the thresholded validation runs.

## 4. Smooth iso surface (marching tetrahedra, `iso_mt.py`)

Tosca stores one density per element, a staircase field. Cutting it element by element (`iso_stl.py`) gives jagged faces and loose fragments (the first "cloud" STLs). The smooth surface is built as Tosca's own smoothing does:
1. **Average to nodes.** Each corner node gets the mean density of the elements around it.
2. **Interpolate in each tetrahedron.** With values at its 4 corners the density varies linearly inside it (like FE shape functions): a continuous field.
3. **Crossing points.** On each tet edge with one end above c and one below, the surface crosses at t = (c - rho_a) / (rho_b - rho_a). Example: 0.8 and 0.2 with c = 0.5 gives t = 0.5, halfway.
4. **Connect.** A cut tetrahedron has 3 or 4 crossed edges: a triangle or a quadrilateral (two triangles). Neighbours share edges and crossing points, so the triangles join into one closed skin.
5. **Caps.** Where material reaches the outer boundary of the design space, the boundary faces are added and trimmed at the crossing line.
6. **Light smoothing.** A few Taubin iterations remove facet noise without shrinking (volume change about 3 %).

## 5. Separation between solid and empty

**Meaning.** In a histogram of design-element densities, a well-separated result has two tall peaks (near 0 and near 1) and few elements in the middle; grey appears only as a thin band where they meet (the filter always blurs an edge over 1 to 2 elements). A poorly separated result has a broad middle hump: whole regions at 0.3 to 0.6 that never decided.

**Why it matters.** With poor separation the cut level decides the topology (members appear or vanish between 0.3 and 0.5), no cut is a faithful version of the design, and Tosca's numbers (which credit grey at reduced stiffness) do not transfer to the part. Typical causes: unconverged run, weak penalty, a constraint that rewards grey, or a member size that forbids thin features except as grey.

**H3 cycle 33 (about 527,000 design elements):**

| Density | Share of design |
|---|---|
| below 0.3 | about 47 % |
| 0.3 to 0.5 | about 5 % |
| 0.5 and above | about 48 % |

About 95 % of elements are clearly decided. Iso 0.3 and 0.5 give the same topology (body plus four connected arms, same sections); only wall thickness changes (+14 % volume). The remaining grey sits mainly in thin arm walls.

## 6. Minimum member size

**The problem.** Density optimisation favours very thin features (one-element struts, lace-like plates): mesh dependent and not manufacturable. `GR_MS` asks for a minimum thickness of 2.5 mm (D-057).

**Why not a hard rule.** During the run there are no walls, only densities; a wall exists only after a cut. The restriction must act on the numbers.

**How it works (filter family).** The density used for stiffness and mass is a weighted average of the design values within a radius R around each element. A thin solid wall gets smeared into a grey band after averaging, and grey is a bad deal under the penalty, so thin walls are unattractive; a wall about 2R thick keeps rho near 1 in its middle. The radius must span several elements (C-5: member size > 2 x element size). A filter alone blurs rather than forbids: a strongly wanted thin feature survives as a grey band. Firm minimum sizes in the literature add a projection step that sharpens the filtered field. Tosca does not publish its exact algorithm.

**Why the STL can still be thinner.**
- The cut level: a 2.5 mm grey band with peak 0.6 becomes a thinner wall at iso 0.5 (only the part above 0.5 survives).
- Bands whose peak is below the cut disappear or leave holes.
- Smoothing moves surfaces by tenths of a millimetre.

So the member size is approximate in the density field and not guaranteed in the STL: it must be checked on the geometry.

**Measured (ray casting into the wall from each surface point, cycle 33):**

| Part, cut | Median wall | thinner than 1.0 mm | 1.5 mm | 2.0 mm | 2.5 mm |
|---|---|---|---|---|---|
| Body, iso 0.5 | 2.7 mm | 2.4 % | 9.3 % | 22 % | 40 % |
| Body, iso 0.3 | 3.2 mm | 0.8 % | 2.3 % | 10 % | 29 % |
| Arm, iso 0.5 | 3.2 mm | 2.9 % | 9.3 % | 20 % | 32 % |
| Arm, iso 0.3 | 3.8 mm | 1.1 % | 2.5 % | 6 % | 17 % |

(Shares of surface area; rays near edges overstate thinness; the body includes fixed parts thin by design.) For FFF with a 0.4 mm nozzle, below about 1.2 mm is fragile. Options: iso 0.3, an intermediate cut (0.4), or local thickening of walls below a limit.

## 7. Iso 0.3 against iso 0.5: what the validation compares

**Frequency basics.** f = (1 / 2 pi) sqrt(k / m) per mode: rises with the stiffness resisting the mode shape, falls with the moving mass. Extra mass alone lowers it; extra material brings stiffness too.

**What the cut does to an element.** Above the cut, grey becomes solid: mass x 1/rho but stiffness x (1/rho)^p, much more (at rho 0.4 with SIMP: mass x2.5, stiffness x15.6). Below the cut, grey disappears: mostly dead weight leaves (40 % of the mass but a few % of the stiffness). Both directions tend to raise k/m against Tosca's grey accounting, except where removed grey was a load path.

**Consequence.** Iso 0.3 is heavier (+10 g) but its extra walls become many times stiffer, and most of the moving mass is the fixed components (about 205 of 280 g). Expected: iso 0.3 gives equal or higher frequencies and lower strain energies than iso 0.5, both at or above Tosca unless a load path breaks.

**Two different comparisons.**
- Validation (real part against requirements): exact for whichever geometry is analysed; iso 0.3 is validated as accurately as iso 0.5.
- Correspondence (real part against Tosca): measures how far the part is from the optimised design; iso 0.5 (volume-preserving) is closest, iso 0.3 is a slightly over-built version.

**Verdict.** Tosca's 417 Hz is a prediction for a grey model that cannot be built. Choose the cut from validation results: the lightest cut that meets the frequency target, the stiffness caps and printable wall thickness. Both cuts are run (TH03, TH05).

## 8. The mode check that stopped H2 (D-066 item 2)

**What it guarded against.** Spurious local modes: in near-empty regions, plain SIMP gives stiffness rho^3 and mass rho, so k/m falls as rho^2 and a patch of "air" vibrates on its own at a very low frequency. Such modes enter the eigenvalue list as modes 7, 8, ..., the frequency constraint reacts to them, and material is added in nonsense places.

**How it was measured (`h2_modecheck.py`, `cyclecheck.py`).** For each mode 7 to 12: take the nodes moving at least 80 % of the maximum displacement (peak region); count those touching only elements below density 0.3; flag the mode if more than half do.

**What happened.** H2 cycle 10 flagged modes 8 to 10 (417 to 420 Hz); H3 flagged modes 9 and 10 at cycle 20 and all six at cycle 30. These were the arm bending modes: smooth, maxima at the motor seats, frequencies continuous with the history, peak regions of thousands of nodes at mean density 0.2 to 0.45. True spurious modes are low-frequency blobs in near-void (rho about 0.001) pockets. The check was too blunt: in an arm mode the largest motion is at the outer arm, which is exactly where the optimiser had made thin grey walls. A false alarm for spurious modes; it pointed correctly at grey material carrying part of the 417 Hz, which the thresholded runs (TH03, TH05) quantify.

**If the smooth surface had failed.** The first fragmented STL was a display artefact (element faces). A fragmented smooth surface would have meant a poorly separated or checkerboarded field, needing a formulation change (stronger penalty, projection, discrete update, larger filter) and a rerun.

## 9. Tosca 2024 interpolation, measured (D-066 item 1)

**Two factors per element.** Abaqus builds two matrices for a vibration problem: stiffness K (resists deformation) and mass M (resists acceleration). Tosca 2024 writes, every cycle, a table of per-element factors (`tosca_distribution.inp`): `*SCALESTIFFNESS` for K and `*SCALEMASS` for M, applied to the solid PET-CF material. Both come from the same single density rho through two interpolation functions; the second number on each row is a derivative used for sensitivities (inferred). Fixed elements have factor 1.

**Measured on H3 cycle 40 ("Optimization product default"):**

| rho | Stiffness factor | rho^3 (textbook) | Mass factor | Stiffness / mass |
|---|---|---|---|---|
| 0.001 | 2.00e-4 | 1e-9 | 1.0e-5 | 20 |
| 0.01 | 1.97e-3 | 1e-6 | 0.0100 | 0.20 |
| 0.05 | 9.39e-3 | 1.25e-4 | 0.0500 | 0.19 |
| 0.1 | 0.0181 | 0.0010 | 0.100 | 0.18 |
| 0.2 | 0.0368 | 0.0080 | 0.200 | 0.18 |
| 0.3 | 0.0627 | 0.0270 | 0.300 | 0.21 |
| 0.4 | 0.1024 | 0.0640 | 0.400 | 0.26 |
| 0.5 | 0.1625 | 0.1250 | 0.500 | 0.33 |
| 0.6 | 0.2496 | 0.2160 | 0.600 | 0.42 |
| 0.8 | 0.5312 | 0.5120 | 0.800 | 0.66 |
| 1.0 | 1 | 1 | 1 | 1 |

**Reading.**
- Mass is linear in rho (mass = volume cost), except at the minimum density 0.001, where it is reduced 100 times.
- Stiffness is not rho^3: at low density it is about 0.19 x rho (linear), rising towards rho^3 near 1 (equivalent SIMP exponent about 1.7 at 0.1, 2.3 at 0.3, 2.6 at 0.5, 2.8 at 0.8).
- Void protection: k/m no longer tends to zero in near-empty regions (about 0.19 of solid, and 20 at rho 0.001), so "air" cannot form low-frequency blobs. This is why no true spurious modes appeared.
- Grey is still penalised: k/m stays below 1 for every intermediate density (0.18 to 0.66), so grey is always worse value than solid. The penalty is softer than textbook SIMP (at 0.5: 16 % stiffness instead of 12.5 %).

**Does the protection tempt the optimiser towards grey?** No: the objective is volume, counted linearly in rho regardless of the mass factor; near-void elements give almost no stiffness (2e-4 at 0.001) so their high k/m is harmless rather than useful; and in the intermediate range k/m < 1 everywhere. The measured separation (95 % decided) confirms it.
