# Stage 6: v04-B export note, revision 2 (46 x 46 body, 148.5 mm wheelbase, closed corners, fillets)

From the main chat, 2026-10-11. It replaces revisions 0 (40 x 40 body) and 1 of the same day; both are kept in the main chat (`abaqus_v04B_r0`, `abaqus_v04B_r1`). Read with `claude/stage6_v04B_design_brief.md`. Decisions D-067 to D-081 are in `claude/journal_quadcopter.md` (v0.51). Gates G0 to G5 all pass. Package: `stage6_abaqus_v04B.zip`.

## 0. Revision 2 changes (Miguel, 2026-10-11, D-081)

| # | Change | Detail |
|---|---|---|
| 1 | Octagonal corner walls restored above z = 10 | The bay above z = 10 follows the outer octagon with 2.5 mm corner walls (inner chamfer \|x\| + \|y\| <= 34.36). The FC still drops straight in: its corners clear the inner corner walls by 0.96 mm (C-1). Between z about 6 and 10 the bay corners rise at 45 deg from the R2 rounded corners to the corner walls, so the walls are continuous; at board level (z -6 to 6) the 4 mm margin and the corners are unchanged |
| 2 | Wall lid bosses moved towards the corners and into the bay | Front pair at (21, +-9.5), rear pair at (-21, +-5), keel boss (-30, 0). Each wall boss stands 2.5 mm into the bay (inner edge at x = +-18, 1.5 mm from the FC path) on a 45 deg design support (z 11.5 to 15.5) that Tosca can shape into an inclined overhang; below it the bay is back to +-20.5. Closer to the corners is not possible: along the diagonal only 3.5 mm separate the FC corner from the prop margin, and the front pair is limited by the nut-access columns (1.9 mm) and the inner corner (1.4 mm); the rear pair stays 1 mm inside the keel sides. The design feet of revision 1 are gone |
| 3 | Fillets, pass A (in the model) | Keel root to rear wall, vertical edges and underside edge, R2. Bay vertical corners (below the 45 deg transition) R2. Pigtail and USB window corners R0.75. Strap notch bottom corners R1. Lid: tab root R2, GPS deck root R3, C cutout pocket corners R0.8 |
| 4 | Fillets dropped after the gates | Bay floor edge R1: its remnant beside the motor-lead passages was 0.59 mm thick. C cutout entry corners R0.5: they left 0.6 mm flats. USB window R0.5 raised to R0.75 (a 0.5 mm fillet puts its neighbouring faces 0.71 mm apart). These outside corners and the floor edge are left to pass B |
| 5 | Fillets, pass B (at restoration T-5, on the final printed STL) | R0.5 on every remaining outside edge; R1 on inside edges wherever the wall is at least 2.5 mm thick; then Stage 7 checks the stresses on that geometry |


## 1. What changed from revision 0 (Miguel, 2026-10-11)

| # | Change | Reason |
|---|---|---|
| 1 | Body 46 x 46 (half-width 23), FC bay +-20.5: 4 mm from the FC to the inner walls on every side (D-079) | Room for the soldered wires; with 1 mm the joints were stressed |
| 2 | Every corner moved out 3 mm in x and 3 mm in y, i.e. 4.24 mm along each diagonal: fins, fin bosses, arms, motors, prop sweep, motor-lead passages. Motor axes at (+-52.497, +-52.497); wheelbase 148.5 mm (D-024 revised) | Joint, arm and arm-to-motor geometry stay exactly as v03-B; the arms are the same parts, only moved |
| 3 | One FC bay prism +-20.5 from z -6 to the rim | Replaces K1 / K2 and removes the 0.5 mm step at z = 5 |
| 4 | Antenna coax goes through the keel at receiver height: dia 3.5 channel entering the bay at (y +3.5, z 7), straight back to x -33, R5 bend down, out through the keel underside at (-38, +3.5) (D-080) | The receiver sits at z 5.5 to 9.5 with its antenna lead at its -X end. The old hole below the keel forced the coax past the FC edge. Dia 3.5 passes the IPEX plug |
| 5 | GPS cable channel moved to the -y side: vertical leg at (-38.2, -1.5), enters the bay at (y -3.5, z 5) | Makes room for the antenna channel; 1.5 mm between the two channels |
| 6 | Antenna boss moved to (-44, 0); holder pocket 14.4 x 7.9 x 4 for the T junction (14 x 7.5 x 4, measured) | 2.5 mm from the antenna channel exit |
| 7 | Pigtail window 11 x 7 (y -10 to 1, z -1.8 to 5.2); the complete pigtail with its XT30 female passes through | Two 3 mm wires (measured) did not fit 7 x 3.5; XT30 female 10.25 x 5.25 |
| 8 | Lid tab: Volador-style C cutout (2.6 mm entry from the tab front edge, 6.4 x 3.4 pocket at x 35.8 to 39.2). The XT30 female stands upright on the tab over the pocket; the battery plugs in from above. Wire slot and zip-tie slots removed | Miguel's design (Volador top plate) |
| 9 | Pigtail route: out of the window, up near the body (x 28.5 to 33), forward just under the plate one wire behind the other (y +-1.75), into the pocket from below | Keeps the wires out of the prop sweep + 3 mm between the front props |
| 10 | GPS pocket 4 mm further back: inside x -52.8 to -35.2, deck x -54 to -30, keel to x = -54, GPS CG (-44, 0, 26.5) | Room for the keel lid boss at (-30, 0) with a standard dia 6 pad: 1.0 mm from the rim, countersink 2.1 mm from the rim |
| 11 | Lid bosses (+-24.5, +-5) and (-30, 0), all pads dia 6 | superseded in revision 2: (21, +-9.5), (-21, +-5), (-30, 0) |
| 12 | USB window 13 x 8 (x -1.1 to 11.9, z -2 to 6) | The wall is now 6.5 mm from the board edge, so the plug overmold reaches the wall; the window is 0.5 mm larger than the assumed 12 x 7 overmold all round; 1.0 mm above the mm motor-lead passage |

Kept from revision 0: FC bosses dia 6.4 with dia 4.2 counterbores, GPS deck fully fixed, GPS cap bosses dia 5.4 at y +-9.3 with through holes, antenna boss dia 5.4 x 6.5, lead zone of the capacitor (K4, now to x = 17.5 as in the brief).

## 2. Files

| File | Bodies (solids) | Volume (mm^3) | sha256 (first 16) |
|---|---|---|---|
| TUB.step | TUB_DESIGN (1), TUB_FIXED (18) | 40,676.1 / 10,496.1 | a07acc90122aa853 |
| LID.step | LID_DESIGN (2), LID_FIXED (5) | 2,496.6 / 4,599.1 | a2b31ddad8171e71 |
| ARM_pp / pm / mp / mm.step | ARM_DESIGN, ARM_FIXED (6 solids per file) | 8,036.9 / 2,933.5 each | v03-B arms moved by (3 sx, 3 sy, 0) |
| KEEPOUTS_v04B.step | K1, K3 to K12 (K2 merged into K1) | | 426971baec1c01d6 |
| COMPONENTS_v04B.step | 39 named dummies | | b27e40bdc088c4ed |
| reference_points_v04B.csv | point masses and coupling surfaces | | |
| v04B_volumes.json, gates_v04B.json, gates_v04B_log.txt | volumes of every region, gate results | | |
| fig06_v04B_export.png | tub, lid, bay contents, assembly | | |

- **TUB_FIXED (18 solids).** 8 fin bosses, 4 FC bosses, 5 lid bosses, 1 antenna boss.
- **LID_FIXED (5 solids).** 1 connected solid (plate frame and strap band, GPS deck, rim, cap bosses, keel pad, tab) plus the 4 wall screw pads.
- **LID_DESIGN (2 solids).** The two plate interiors.
- **Arms in the model.** Same part as before, now instanced at the moved positions: each corner moved by (+-3, +-3, 0) in addition to the 0 / -90 / +90 / 180 deg rotations, so the joint gaps (0.150 mm) and ties are unchanged.

## 3. Gates G0 to G5

| Gate | Result |
|---|---|
| G0 file identity | PASS. Every body matches v04B_volumes.json. Each ARM file, moved back by (-3 sx, -3 sy, 0), is identical to the v03-B arm (Boolean difference 0.000 mm^3) |
| G1 Boolean bookkeeping | PASS. Design AND fixed = 0; exported XOR independent recomputation = 0.000 mm^3; every keep-out AND part = 0 (arms too); no floating fixed solid |
| G2 face test | PASS. TUB: 271 faces, smallest 2.95 mm^2, narrowest 0.65 mm. LID: 86 faces, 2.75 mm^2, 0.76 mm (the narrowest faces are fillet strips; all above the 0.5 mm^2 / 0.3 mm limits) |
| G3 tangency audit | PASS. Only the known v03-B features: 16 fin-nose wedges, 8 fillet-end strips (0.106 mm), moved with the corners. No flag from the new corner walls, bosses, wedges or fillets. LID: no flags |
| G4 gmsh mesh test | PASS. Details below |
| G5 clash and clearances | PASS. No interference; all of C-1 to C-9 meet their requirement except C-6, which depends on a board measurement (Q-60) |

G4 mesh test results:

| Part | 1.5 mm | 1.0 mm |
|---|---|---|
| TUB | 136,496 tets, min gamma 0.1265, 0 below 0.05 | 304,369 tets, min 0.0227, 25 below 0.05: the same 25 as v03-B BODY, at the same fin features moved with the corners |
| LID | min 0.136 | min 0.249, 0 below 0.05 |

### G3 feature table

Columns: faces of the part on the feature; smallest interior angle where it meets another face; smallest distance to a face of the same solid it does not touch.

| Part | Feature | Faces | Min angle (deg) | Min distance (mm) |
|---|---|---|---|---|
| TUB | K1 FC bay (+-20.5, corner walls, 45 deg corner transition) | 33 | 45 | 1.38 |
| TUB | K3 screw holes and counterbores | 12 | 90 | 1.0 |
| TUB | K6 pigtail window (R0.75 corners) | 8 | 90 | 1.06 |
| TUB | K7 USB window (R0.75 corners) | 8 | 90 | 1.0 (to the mm motor-lead passage) |
| TUB | K8 antenna channel | 3 | 90 | 1.5 (to K9) |
| TUB | K9 GPS channel | 3 | 82.9 | 1.5 (to K8) |
| TUB | K10 strap notches (R1 corners) | 10 | 90 | 1.41 |
| TUB | K11 motor-lead passages | 20 | 45 | 1.0 |
| TUB | FC bosses dia 6.4 | 16 | 90 | 1.1 (counterbore ring) |
| TUB | Lid bosses | 35 | 48.2 | 1.38 (to the inner corner) |
| TUB | Antenna boss and insert holes | 5 / 12 | 90 | 1.1 |
| TUB | Boss support wedges (45 deg) | 20 | 90 | 1.38 |
| LID | Screw pads, holes and countersinks | 18 / 10 | 90 | 1.1 |
| LID | GPS cap bosses | 2 | 90 | 1.1 |
| LID | GPS hole | 1 | 90 | 1.0 |
| LID | C cutout (R0.8 pocket corners) | 3 | 90 | 1.13 |
| LID | Front tab | 4 | 90 | 2.6 |
| LID | Pocket rim | 8 | 90 | 1.1 |
| LID | Plate frame inner edge | 28 | 90 | 1.1 |

### G5 clearances

| # | Check | Required | Measured |
|---|---|---|---|
| C-1 | FC (33 x 33) plus capacitor swept from the seat past the rim, to TUB | >= 0.25 | 0.96 at the corner walls (4.0 to the flat walls; 1.0 down to the boss tops, where the grommets seat) |
| C-2 | Lid bosses and their supports to the FC path / nut columns / prop sweep + 3 | 0.25 / 1.0 / 1.0 | 1.5 / 1.87 / 2.85 |
| C-3 | Pigtail to ARM_pm / pm fin and front bosses / window edges | 1.0 / 1.0 / > 0 | 7.8 / 1.9 / 0.3 |
| C-4 | XT30 on the tab / pigtail to prop sweep + 3 | outside | 2.9 / 4.3 |
| C-5 | Capacitor to pm lock nut / receiver cradle / lid | >= 1.0 | 2.7 / 1.75 / 6.0 |
| C-6 | Cradle floor to FC parts | >= 0.3 | 0.3 only if the parts under the cradle stay at or below z +3.8 (Q-60): open |
| C-7 | Rear-wall openings: antenna to motor-lead passage / antenna to GPS / GPS to motor-lead passage | >= 1.0 | 8.3 / 3.5 / 6.9 |
| C-8 | USB plug to ARM_pm / to TUB | 0.5 / > 0 | 3.2 / 0.5 |
| C-9 | Antenna V to rear arms / z range / prop sweep | >= 5; above -12, below 10 | 15.4 / z -2.6 to -1.4 / 11.4 |
| | Lid placement: lid to bay contents | > 0 | 6.0 (capacitor) |

## 4. Mass and model data

| Item | Volume (mm^3) | Solid mass (g) |
|---|---|---|
| TUB design / fixed | 40,676.1 / 10,496.1 | 52.88 / 13.64 |
| of which fixed: fin bosses, FC bosses, lid bosses, antenna boss | 8,755.2 / 961.0 / 667.3 / 112.7 | 11.38 / 1.25 / 0.87 / 0.15 |
| LID design / fixed | 2,496.6 / 4,599.1 | 3.25 / 5.98 |
| Arms, 4 x (design / fixed) | 4 x (8,036.9 / 2,933.5) | 41.79 / 15.25 |
| Frame, solid design space | 102,149.6 | 132.79 (fixed 34.88, design 97.91) |
| Point masses | | 200.0 (battery 100, FC 27.2, GPS 2.6, motors 4 x 13.75, joint hardware 4 x 3.8) |
| **Expected model mass (G7)** | | **332.79 g** |

New hardware (estimates from the dummy volumes, retainers as solid dummies), counted against A-005: receiver cradle 0.87, GPS cap 0.84, antenna holder 1.36, 5 lid screws 0.87, 8 inserts 1.33, 6 nuts 1.11, 3 screws 0.69; total about 7.1 g.

| Item | Value |
|---|---|
| RP_MOT_xx | (+-52.5, +-52.5, 8.5) |
| RP_JNT_xx | (+-26.335, +-26.335, -2.5) |
| RP_GPS | (-44, 0, 26.5), 2.6e-6 t; S_GPS_SEAT = pocket floor, about 209.2 mm^2 (fixed) |
| RP_BATT, RP_FC | unchanged positions; S_BATT_SEAT = lid plate frame and strap band tops (z = 24); S_FC_SEAT = 4 rings dia 6.4 / 2.2 = 113.47 mm^2 |
| S_FLOOR | 46 x 46 minus 4 counterbores = 2060.58 mm^2; LC3a p = 56.4 / A = 0.027371 MPa (read A from the model) |
| Lid ties TIE_LID_1..5 | Main = tub boss top annulus dia 6 / 3.2. Secondary = lid pad bottom, partitioned at dia 3.2 so it matches the main annulus |
| G7b rim contact | TUB faces at z = 21.5 under the lid: about 626 mm^2 |
| D-064 supports | at RP_JNT_pp, _pm, _mp (moved with the joints) |
| LC2b | the pitch / roll moment arm grows from 49.5 to 52.5 mm (+6 %); the loads are applied at the moved motor RPs, nothing else changes |

## 5. Open items

| # | Item |
|---|---|
| C-6 / Q-60 | FC parts under the cradle floor must stay at or below z +3.8 (4.7 mm above the PCB top): measure |
| Q-58, Q-59 | GM10 compass wiring and plug sizes |
| USB plug | the window assumes an overmold up to 12 x 7 centred on the connector; a larger plug needs a slimmer cable |
| C cutout fit | print a test coupon of the keyhole (2.6 mm entry, 6.4 x 3.4 pocket) with the real wires before the lid |
| Lid modes | G7a / G7b (brief 9.8) |

## 6. Scripts (in the package)

| Script | What it does |
|---|---|
| `s06_geometry_v04B.py` | Generator, revision 1; imports the v03 generator for the fins and the arm local geometry |
| `s06_gates_v04B.py` | G0 to G5 |
| `s06_tangency_audit.py` | G3 |
| `s06_gmsh_meshtest_loc.py` | gmsh mesh test with the location of every tet below gamma 0.05 |
| `s06_split_acceptance.py` | Face test |
| `s06_render_v04B.py` | The figure sheet |
