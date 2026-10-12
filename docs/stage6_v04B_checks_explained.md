# Stage 6: the eight v04-B layout checks, explained

Companion to `claude/stage6_v04B_design_brief.md` section 9. Each check is explained from the basic rule it tests, with the numbers worked step by step, the options, and a verdict. Figures: `check1_plan.png` to `check6_capacitor.png` (sent in the set-up chat, 2026-10-11).

## 0. The rules every check uses

Five rules, all decided earlier in the project. Every check below is one of them applied to one feature.

| Rule | Where it comes from | What it means here |
|---|---|---|
| Prop keep-out | D-024, D-030: prop disc radius 44.45 mm plus a 3 mm margin = 47.45 mm around each motor axis, for z 10 to 21.5 (blades at 13 to 18.5, plus and minus 3) | nothing (frame, cable, connector) may enter that zone. The margin covers blade flex, print tolerance and arm deflection |
| Landing plane | D-036, D-037: the floor bottom (z = -15) is the lowest point of the frame; it is what touches the ground | nothing may hang below it, or it becomes the landing point |
| Tangency | D-054, D-055, F-031: two region boundaries must cross at a clear angle or stay at least one element (1 mm) apart | otherwise thin wedges or strips form that the mesher cannot fill (the v03-B arm failure) |
| Printable wall | D-057: about 3 extrusion lines | a wall thinner than about 1.2 mm cannot be printed reliably |
| Assembly path | F-16, requirement 4 of the redesign | a part must be able to travel from outside to its final place, with every other part already fitted in that step |

Positions use the model axes: x forward, y left, z up, origin at the frame centre, z = 0 on the arm top under the motor. The four motor axes are at (+-49.5, +-49.5).

## 1. FC insertion and the lid boss positions

### What was agreed

The FC is lowered from above into the open tub (lid off), and the lid is screwed to the tub with four bosses at the tub corners plus one on the keel.

### The basic fact: the top of the body is an octagon, not a square

Below z = 10 the body is a 40 x 40 square. Between z = 10 and the rim (z = 21.5) the body is the same square with its four corners cut off (D-030):

    |x| + |y| <= 31.8

Why the corners are cut: at that height the props sweep past. The front-left motor axis is at (49.5, 49.5), which is

    sqrt(49.5^2 + 49.5^2) = 70.0 mm

from the centre, along the diagonal. The keep-out circle around it has radius 47.45 mm, so along the diagonal it reaches in to

    70.0 - 47.45 = 22.55 mm

from the centre. The chamfer line |x| + |y| = 31.8 crosses the diagonal at

    31.8 / sqrt(2) = 22.5 mm

So the chamfer is exactly the prop keep-out. It cannot move outward.

### The numbers

The FC board is 33 x 33 mm. Its corner is at (16.5, 16.5), at a distance from the centre of

    sqrt(16.5^2 + 16.5^2) = 23.3 mm

along the diagonal. The octagon allows 22.5 mm there. The board corner is 0.8 mm outside the body before any clearance is added.

The same test written with the octagon rule: at the board corner

    |x| + |y| = 16.5 + 16.5 = 33.0

against the limit 31.8. With 0.5 mm of clearance all round (an insertion opening of 34 x 34) it is 34.0 against 31.8.

Analogy: a square tray that must pass through an octagonal hole whose flat-to-flat width (40 mm) is larger than the tray, but whose corner-to-corner reach along the diagonals (45 mm) is shorter than the tray's diagonal (46.7 mm). The tray fits in the hole's width but not across its corners.

### What goes wrong

The FC sits below z = 10 in its final position (z -6 to +5), where the body is the full square, so it fits where it lives. It cannot get there: on the way down it must pass through the octagon band (z 10 to 21.5).

To let it pass, the opening must be cut through the band as a 34 x 34 square. Figure `check1_plan.png` shows the consequence: the square opening removes the four chamfer corners completely. What remains of the band are four separate wall pieces, one per side, each 3 mm thick (from 17 to 20 mm out). There is no tub corner left above z = 10 to hold a boss.

### What the default does

- Opening (keep-out K2): 34 x 34 square from z +5 to the rim; the four corners of the band are open.
- Lid bosses: on the front and rear wall pieces, at (+20.25, +7), (+20.25, -7), (-20.25, +7), (-20.25, -7), Ø6, plus the keel boss at (-26, 0).

How each coordinate was chosen:

| Requirement | Value | Check |
|---|---|---|
| Boss outside the opening | inner edge at 20.25 - 3 = 17.25, opening ends at 17.0 | 0.25 mm clear |
| Boss outside the prop keep-out | distance from (20.25, 7) to the motor (49.5, 49.5): sqrt(29.25^2 + 42.5^2) = 51.59; minus the boss radius 3 = 48.59, against 47.45 | 1.14 mm clear |
| Why y = 7 and not further out | at y = 8 the clearance drops to 0.32 mm; at y = 10 the boss enters the keep-out (-1.3 mm) | y = 7 is the furthest position with about 1 mm |
| Clear of the nut access columns (Ø8 at (12.75, 12.75)) | centre distance sqrt(7.5^2 + 5.75^2) = 9.45, needed 4 + 3 = 7.0 | 2.45 mm clear |
| Clear of the strap passage (x -9 to +9) | bosses at x = +-20.25 | clear |

The wall bosses stand 3.25 mm proud of the old wall face (out to x = 23.25). That is allowed: the outer limit there is the prop keep-out, not the old body face, and the table above shows the boss is outside it.

### Options (mutually exclusive)

- **Option A (default): open corners, bosses on the wall pieces.** Straight vertical insertion; nothing to tilt; every screw and nut reachable from above.
- **Option B: keep the corners closed, insert the FC tilted.** If the board is tilted by an angle theta about the y axis, its corners move in to x = 16.5 cos(theta). The corner must satisfy

      16.5 cos(theta) + 16.5 <= 31.8 - 0.5

  so

      cos(theta) <= 0.897,    theta >= 26 deg

  The board would go in tilted by about 26 to 30 deg, then be levelled once below z = 10. With the capacitor lying over the board (10.5 mm tall) and the pigtail wires folded on it, the tilted package is taller and harder to guide; this works against "easy assembly".

### Verdict

The corners as agreed cannot exist together with a vertical insertion; it is a geometric fact, not a tolerance issue. Option A keeps the agreed idea (screwed lid, FC from above) and moves the four bosses about 8 mm from the corners onto the wall pieces.

## 2. The XT30 and the front window

### What was agreed

Only the two pigtail wires leave the tub, through a window in the front wall about 7 x 3.5 mm at board height (y -9 to -2). The pigtail and capacitor are soldered on the bench before the FC goes in.

### The basic fact: the wire fits, the plug does not

| Item | Cross-section |
|---|---|
| Window | 7.0 x 3.5 mm |
| One 18 AWG silicone wire | about Ø2.0 mm (copper Ø1.02 plus insulation) |
| Two wires side by side | about 4.0 x 2.0 mm: fits with 1.5 mm to spare each way |
| XT30 housing (male or female) | about 10.2 x 5.2 mm: wider and taller than the window |

Figure `check2_window.png` shows the three outlines to scale.

### What goes wrong

The pigtail comes with the XT30 on its free end. If it is soldered to the FC on the bench (step 1), the XT30 is on the inside when the FC is lowered, and it must get out through the window. The XT30 is 3.2 mm wider and 1.7 mm taller than the window; tilting does not help (its smallest section, 5.2 mm, is already larger than the 3.5 mm window height).

### Options (mutually exclusive)

- **Option A (default): pigtail with bare ends, XT30 soldered outside.** On the bench, cut the XT30 off the pigtail (or buy a bare pigtail) and solder the wires and the capacitor to the FC. After the FC is screwed down, push the two bare ends out through the window and solder the XT30 on outside the frame, in free air, then heat-shrink. Window and wall unchanged.
- **Option B: window big enough for the XT30**, about 11 x 6 mm. No soldering at the window, but the front wall loses about 2.7 times the area (66 against 24.5 mm^2) at board height, right where the front lid bosses and the front fins load the wall.
- **Option C: window as a slot open to the rim**, closed above by the lid front lip. The wires drop in from above while the FC goes down. The front wall is cut through its whole height (z -2 to 21.5) over 7 mm.

### Verdict

Option A keeps the window as agreed and costs one extra pair of solder joints done outside the frame, which is the easiest place to solder. The XT30 is a wear item that is resoldered from time to time anyway.

## 3. The GPS cable "down beside the keel"

### What was agreed

The GPS sits on the lid deck behind the battery. Its cable goes down beside the keel through a Ø4 hole and enters the bay through a rear-wall hole opposite the antenna.

### The basic fact: the keel already fills the gap between the rear props

The keel was designed in D-056 to fill exactly the corridor between the two rear prop keep-outs at blade height (z 10 to 21.5), and no more. The corridor half-width at a position x behind the body is the distance from the centreline to the keep-out circle. For the rear-left motor at (-49.5, 49.5):

    y_limit(x) = 49.5 - sqrt(47.45^2 - (x + 49.5)^2)

Worked at x = -36:

    x + 49.5 = 13.5
    sqrt(47.45^2 - 13.5^2) = sqrt(2251.5 - 182.3) = 45.49
    y_limit = 49.5 - 45.49 = 4.01 mm

| x (mm) | -40 | -36 | -30 | -25 | -22 | -20 |
|---|---|---|---|---|---|---|
| Corridor half-width, prop sweep + 3 (mm) | 3.0 | 4.0 | 6.2 | 8.9 | 10.8 | 12.3 |
| Keel half-width above z = 10 (mm) | 3.0 | 4.0 | 6.2 | 8.9 | 9.0 | 9.0 |
| Blade tip path, no margin (mm) | 6.1 | 7.2 | 9.6 | 12.4 | 14.6 | 16.3 |

"Beside the keel" therefore means "inside the prop keep-out", everywhere from the GPS to x = -25. Near the body (x -22 to -20) the corridor is wider than the keel by 1.8 to 3.3 mm, but that is not enough for a Ø3 cable with any clearance.

### What goes wrong

Figure `check3_keel.png`: a Ø3 cable laid against the keel side at x = -36 has its outer edge at

    4.0 + 3.0 = 7.0 mm

from the centreline, while the blade tips pass at 7.15 mm. The cable would be 0.15 mm from the blade tips, with none of the 3 mm margin. A loose cable also moves in flight.

The cable has to cross the blade band somewhere, because the GPS is above it (z 24 and up) and the bay is below (the cable enters around z 5). Behind the body, the only place in the blade band that is outside the keep-out is the keel itself.

### What the default does

The same route, but inside the keel: keep-out K9, a Ø4 channel.
- Vertical leg at (x -33, y 0), from the pocket floor (z 21.5) down to z 5. At x = -33 the keel is 10.0 mm wide, so the channel leaves 3 mm of keel on each side.
- Bend radius at least 5 mm, then a horizontal leg at z 5 forward to the rear wall, entering the bay at (x -20, y +4), the side opposite the antenna hole.

Second part of this check, the connector rule. A Ø4 channel passes a cable but not its plugs. The GM10 cable has a small plug at the GPS end and either a plug or bare wires at the FC end. Whichever end is threaded through the channel must fit it:
- if the plug at one end fits through Ø4 (or through a locally enlarged channel, as long as the keel walls stay at least 1.2 mm), the cable can be soldered to the FC on the bench and threaded through afterwards, plug first;
- otherwise the bare FC end is threaded from the GPS pocket down into the bay, and soldered to the FC there, from above, with the lid off (step 11).

### Verdict

The agreed concept stays (down through the keel area, separate rear-wall hole opposite the antenna). The cable runs inside the keel instead of beside it. The GM10 plugs must be measured to decide which end is threaded.

## 4. The antenna hole "beside the keel"

### What was agreed

The antenna coax leaves the bay through a Ø4 hole in the rear wall beside the keel.

### The basic fact: the flat part of the rear wall is narrow, and its edges are tangent lines

Seen from behind (figure `check4_rearface.png`), the body rear face (x = -20) is flat only between y = -10.86 and +10.86. Beyond those lines the face curves into the R5 fillets at the roots of the two rear fins. A fillet meets the flat face tangentially: there is no edge, only a line where the curvature starts.

The keel covers the middle of that flat face, |y| <= 9, from z = 0 up.

So beside the keel, the flat face is a strip from y = 9 to y = 10.86:

    10.86 - 9.0 = 1.86 mm wide

### What goes wrong

- A Ø4 hole does not fit in a 1.86 mm strip. Centred at y = 9.93 it would cut into the keel side by 1.07 mm and into the fillet by 1.07 mm.
- Cutting a hole edge into a region where two surfaces meet tangentially is exactly the F-031 situation. There, a keel side placed 0.14 mm from the fillet tangent line left 9 sliver tetrahedra with quality down to 0.002, and the fix was to keep the keel side 1.86 mm away. A hole edge near that line would bring the problem back.

Why near-tangency breaks the mesh, in one line: near a tangent contact the material between two curves is a wedge whose thickness grows from zero as

    t = d^2 / (2 R)

with d the distance from the contact point and R the radius. With R = 5 mm, the wedge is still only 0.1 mm thick at d = 1 mm. A 1 mm tetrahedron cannot fill a 0.1 mm wedge without becoming a flat sliver.

### What the default does

The hole moves below the keel, where the rear face is flat and free: centre at (y -5, z -3.5). Its top edge is at

    -3.5 + 2.0 = -1.5

which is 1.5 mm below the keel bottom (z = 0): more than one element (1 mm). Its side edges are 3.86 mm from the fillet tangent line at y = -10.86. The coax then runs under the keel to the antenna holder, which is also under the keel, so the path is short.

Open point: the rear-left motor-lead channel also exits this face near the centreline, at z -8 to -3 (its exact y is to be read from the STEP). The hole and that exit must be at least 1 mm apart (check C-7).

### Verdict

The hole stays a Ø4 hole in the rear wall, 7 mm lower than "beside the keel", where it fits with clean edges.

## 5. The antenna V

### What was agreed

The T antenna is bent into a downward V with 90 deg between the two elements, held by a TPU holder screwed under the keel.

### The basic fact: how far a V hangs

The SpeedyBee Nano T antenna is a dipole about 49 to 52 mm across, so each element is about 25 mm long. In a downward V with 90 deg between the elements, each element is 45 deg from the vertical. Its vertical drop is

    drop = L cos(45 deg)

    drop = 25 x 0.707 = 17.7 mm

### What goes wrong

The holder sits on the keel underside, at z = 0 (or about z -1 to -2 with the holder's own thickness). The element tips therefore reach

    z = 0 - 17.7 = -17.7, down to about -20 with the holder

The landing plane is z = -15 (floor bottom). The tips would be 3 to 5 mm below it: on a landing the antenna touches the ground before the frame. Figure `check5_antenna.png` shows it from the side. The ground would bend the elements up into the keel every landing, and in a firm landing (LC3a) pull on the coax and the IPEX plug.

### Options (mutually exclusive)

- **Option A (default): the V lying flat under the keel.** Same 90 deg V, but in a horizontal plane at about z -3, vertex at the holder (x -42, y 0), elements pointing rear-left and rear-right. Tips at about (-59.7, +-17.7, -3).
  - Ground: 12 mm above the landing plane.
  - Props: below z = 10, so outside the blade band.
  - Rear arms: the distance from a tip to the rear arm axis is |x + y| / sqrt(2) = |-59.7 + 17.7| / 1.414 = 29.7 mm; the arm is at most 10.15 mm wide either side of its axis.
  - Radio: both elements horizontal, so when the quad is level and the radio antenna is vertical, the polarisation match is poorer. The 90 deg V keeps one element partly aligned in most attitudes; at 100 mW and normal ranges this is acceptable, but it is a real trade-off.
- **Option B: a V standing vertically on the centreline behind the keel.** Vertex at the rear end of the keel (about x -50, z 5), one element pointing rear-up and one rear-down, each 45 deg from the horizontal.
  - Ground: the lower tip reaches z = 5 - 17.7 = -12.7, 2.3 mm above the landing plane.
  - Props: on the centreline behind the keel the corridor half-width is about 2.0 to 3.2 mm (x -50 to -60), so a 1 mm element on the centreline clears the keep-out by 1.5 to 2.7 mm. Tight, and only if the element stays exactly on the centreline.
  - Radio: better polarisation with a vertical radio antenna.
  - Exposure: the antenna sticks out about 18 mm behind the frame, in the path of a rearward crash.

### Verdict

The downward V as agreed hangs below the landing plane. Option A is the protected and simple default; Option B is better for the radio link but tight against the props and exposed. Miguel chose A (2026-10-11).

## 6. The capacitor cradle

### What was agreed

The capacitor is flipped 180 deg over the FC (option 2), held by a half-pipe on the tub side plus a rib on the lid, with a wall between the capacitor and the nut at the front-right screw. In the discussed position the capacitor cleared that nut stack by about 0.3 mm.

There are two separate problems here, one of assembly and one of printing.

### Problem 1: a tub cradle blocks the FC on its way down

Think of the FC as a tray lowered into a box. On the way down, the board sweeps through every point above its final position, inside its 33 x 33 footprint. Any part of the tub that lies above the board and inside that footprint is in the way.

A half-pipe that carries the capacitor over the board must, by definition, sit above the board and inside its footprint (the capacitor lies at x -6 to +15, y -11 to -0.5, all inside the board's +-16.5). If that half-pipe is part of the tub, the FC cannot be lowered past it. It does not matter how it is attached to the walls.

So the lower cradle has to arrive after the FC: a separate small print, fitted once the FC is screwed down.

### Problem 2: 0.3 to 0.4 mm is not a printable wall

Figure `check6_capacitor.png` is a cut across the FC at the front-right (pm) screw, x = 12.75. On that screw the stack above the board is:

| z from | z to | Item |
|---|---|---|
| +1.6 | +4.1 | anti-loosening nut |
| +4.1 | +5.5 | retainer ear |
| +5.5 | +7.1 | nylon nut |

The nut is about 4 mm across its flats, so its corner reaches y = -12.75 + 2.31 = -10.44. The nearest point of the stack to the capacitor is that top corner, (y -10.44, z 7.1).

In the discussed position the capacitor (Ø10.5, radius 5.25) has its axis at (y -5.75, z 10.25). Distance from the axis to the nut corner:

    d = sqrt((-10.44 + 5.75)^2 + (7.1 - 10.25)^2)

    d = sqrt(22.0 + 9.9) = 5.65 mm

Gap between the capacitor surface and the nut corner:

    5.65 - 5.25 = 0.40 mm

A cradle wall must go in that gap. One extrusion line is about 0.42 mm wide; a wall that prints reliably needs about three lines, 1.2 mm.

### What the default does

- The lower cradle becomes a separate print (half-pipe Ø11 inside, wall 1.2) with an ear on the pm screw, clamped between the anti-loosening nut and the nylon nut, like the receiver cradle on the other side. The lid rib still presses from above.
- The capacitor moves 0.75 mm to +y and 0.75 mm up: axis at (y -5.0, z 11.0). New distance to the nut corner:

      d = sqrt((-10.44 + 5.0)^2 + (7.1 - 11.0)^2)

      d = sqrt(29.6 + 15.2) = 6.69 mm

  Gap 6.69 - 5.25 = 1.44 mm: the 1.2 mm wall fits, with 0.24 mm to spare.
- What the move costs: the capacitor top rises to +16.25 (5.25 mm left to the lid underside, where the rib is); its +y side reaches +0.25, 1.0 mm from the receiver cradle (moved to start at y +1.25). The leads change length by under 1 mm; the bench forming still keeps every bend at least 2 mm from the solder joint.

Order at assembly: FC screwed, pm anti-loosening nut fitted (the capacitor lifted aside on its leads to reach it), cradle ear onto the screw, nylon nut, capacitor pressed into the cradle.

### Verdict

The capacitor stays where it was agreed, flipped over the FC, within 0.75 mm. Its lower support changes from a tub feature (which would block the FC) to a clip-on part like the receiver cradle.

### Decision (Miguel, 2026-10-11)

No retainer at all. Reviewed after this analysis: a clip-on cradle, a lid rib (stops upward and sideways only) and a lid snap clip (also holds from below) were considered. Miguel's flight experience: a capacitor soldered and left floating on its leads works. Rough estimates for this layout (3 g on 0.6 mm leads, 3 to 10 mm free): lead resonance about 66 to 124 Hz, and in LC3a the capacitor would rest on the FC components after about 0.75 mm, its insulated sleeve touching. Accepted as not worth the added parts for this project. The capacitor stays at the discussed position (axis y -5.75, z 10.25), about 2.5 mm above the pm anti-loosening nut; the pm screw is M2 x 20 with no ear and no nylon nut.

## 7. The landing pressure (LC3a)

### What was agreed

Screws come up from below through the four FC bosses, with Ø4.2 x 1.5 mm counterbores for the heads.

### The basic fact: Abaqus applies a pressure, not a force

LC3a pushes the floor up with the ground reaction of a firm landing (N-04-07, load factor 23 on 250 g):

    F = 23 x 0.250 kg x 9.81 m/s^2 = 56.4 N

The model applies it as a pressure p on the floor surface `S_FLOOR` (the 40 x 40 square under the FC). The force Abaqus actually applies is

    F = p x A

so if the area changes and p does not, the force changes. This is the same effect as F-2, where leaving out the four boss discs would have applied 52.4 N instead of 56.4 N.

### The numbers

Each counterbore removes a disc of the floor face:

    A_cb = pi x 2.1^2 = 13.85 mm^2

For four:

    4 x 13.85 = 55.4 mm^2

New floor area:

    A = 1600 - 55.4 = 1544.6 mm^2

With the old pressure the applied force would be

    F = 0.03525 x 1544.6 = 54.4 N

3.5 % low. The pressure that restores 56.4 N:

    p = 56.4 / 1544.6 = 0.036515 MPa

### Verdict

Bookkeeping, not a design problem: read A from the model after the surface is built and set p = 56.4 / A. The FC seat ring area also changes (from 80.9 to 97.9 mm^2, the boss holes go from Ø3.2 to Ø2.2), but that seat only carries a coupling, whose forces do not depend on area.

## 8. Lid modes

### What was agreed

The lid is a separate part, tied to the tub in the model only at the five screw bosses (conservative: it ignores the lid resting on the rim).

### The basic fact: a mass on a spring

Every mode is a mass on a spring:

    f = (1 / 2 pi) sqrt(k / m)

The 100 g battery is the largest mass on the frame, and in v04-B it sits on a 2.5 mm plate. In v03-B that plate was merged into the body (walls and an optimised ceiling under it), so the "spring" under the battery was very stiff. In v04-B, in the model, the plate touches the tub only at the five bosses: the plate between them bends like a beam, and the battery bounces on it.

### Two hand estimates that bracket the answer

Plate as a beam: width 34 mm, thickness 2.5 mm, supported at the front and rear bosses (x = +-20.25, span 40.5 mm), solid (as in the reference job before Tosca removes anything). Its second moment of area:

    I = b t^3 / 12

    I = 34 x 2.5^3 / 12 = 44.3 mm^4

Estimate 1, all the battery mass at mid-span (pessimistic). Stiffness of a simply supported beam under a central load:

    k = 48 E I / L^3

    k = 48 x 5058 x 44.3 / 40.5^3 = 162 N/mm

Frequency with m = 100 g = 1.0e-4 t:

    f = (1 / 2 pi) sqrt(162 / 1.0e-4) = 202 Hz

Estimate 2, the battery weight spread over its 59 mm length, which extends beyond both supports (the overhanging parts lift the middle, so the plate deflects much less on average). A small beam model of this case gives about 1530 N/mm and

    f = about 600 Hz

The real case lies between: the battery is spread (closer to estimate 2), but the plate also bends across its width (the bosses are only 14 mm apart in y while the plate is 34 mm wide) and the battery can rock as well as bounce (closer to estimate 1).

### What goes wrong

The two estimates bracket 417 Hz, so a hand calculation cannot settle it. If the five-tie model puts a battery-on-lid mode below 417 Hz in the solid reference, the Tosca run is infeasible from cycle 0, exactly as the GPS overhang was in Phase 8 (F-012). And it might be a modelling artefact: the real lid rests on the rim along every wall piece, and the screws clamp it down.

### What to do (before Tosca, minutes of computing)

Run the solid reference job twice (gate G7):

| Run | Lid connection | Meaning |
|---|---|---|
| G7a | ties at the five bosses only | lower bound on the lid stiffness |
| G7b | ties at the bosses plus the rim contact faces (tub wall tops to lid underside) | upper bound: lid fully seated |

Then:
- both runs have all of modes 7 to 12 at or above 417 Hz: use G7a (conservative) for Tosca;
- G7a has a lid mode below 417 Hz and G7b does not: the answer depends on how well the lid is seated, which is a design choice. Options (mutually exclusive): (a) model with G7b, justified by the screw clamping, accepted in the main chat; (b) more lid screws so G7a passes, for example two more on the side wall pieces; (c) a deeper fixed lid frame (stiffer plate), then rerun G7a;
- both below 417 Hz: the lid plate itself is too flexible; option (c).

### Verdict

Not decidable by hand. It is the first thing the reference job must answer, and it needs the second run (G7b) added to the gate so the decision is made on numbers.

## Summary

| # | Check | Rule | Default | Your decision needed |
|---|---|---|---|---|
| 1 | FC insertion vs octagon band | assembly path | open band corners, bosses at (+-20.25, +-7) and (-26, 0) | confirmed |
| 2 | XT30 through the window | assembly path | bare-ended pigtail, XT30 soldered outside | confirmed |
| 3 | GPS cable beside the keel | prop keep-out | channel inside the keel; measure the plugs | confirmed |
| 4 | Antenna hole beside the keel | tangency, space | hole below the keel at (y -5, z -3.5) | confirmed |
| 5 | Antenna V | landing plane | horizontal V under the keel (A) | A chosen |
| 6 | Capacitor cradle | assembly path, printable wall | no retainer, capacitor floating on its leads (decided) | none |
| 7 | Floor pressure | load bookkeeping | p = 56.4 / A | none |
| 8 | Lid modes | frequency | reference job with two lid connections (G7a, G7b) | after the run |
