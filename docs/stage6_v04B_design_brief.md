# Stage 6: v04-B design brief (assemblable frame), for the main chat

From the Abaqus set-up chat, 2026-10-11. Part B of `claude/stage6_update_since_H1.md` (part A explains why: F-16, the v03-B print set cannot be assembled). This brief is the full specification for the v04-B geometry export, the model changes and the checks. It records what was agreed with Miguel, gives every dimension that was fixed, and marks clearly the few points where checking the agreed layout while writing this brief found a conflict (section 9): for each, a default is given so the generator can proceed, and Miguel confirmed all section 9 defaults and antenna option A on 2026-10-11; the main chat records them. Each section 9 item is explained step by step, with figures, in `claude/stage6_v04B_checks_explained.md`.

Conventions as before: mm, x forward, y left, z up, origin at the frame centre, z = 0 on the arm top under the motor; corners pp (+x+y), pm (+x-y), mp (-x+y), mm (-x-y). Model units N, mm, tonne.

## 1. What stays and what changes

| Item | v04-B |
|---|---|
| Arms (D-046 to D-054, D-059) | unchanged: same ARM_xx.step, same joint, same fixed bosses |
| Fin bosses, joint ties (D-055) | unchanged |
| Body envelope (D-030, D-056 keel) | unchanged as an outer limit; new keep-outs and fixed regions inside it |
| Battery plate and GPS deck | move from the body into a separate lid part |
| Body | becomes an open tub (rim at z = 21.5) |
| Components | each gets a designed seat and retainer; no glue, no tape |
| GPS | Flywoo GOKU GM10 Nano V3 with compass (2.6 g) replaces the 8 g placeholder (A-007, A-025) |
| FC mounting | through-bosses, screws from below, soft-mount grommets, nuts from above |
| Formulation (D-042), loads, material, frequency goal 417 Hz, caps rule (D-063), supports (D-064) | unchanged |

## 2. Architecture

1. **Tub.** The centre body, open at the top. Topology-optimised as before (floor sandwich, walls, fins, keel, joint). New: through FC bosses with counterbores, five lid-screw bosses with heat-set inserts, an antenna-holder insert boss under the keel, an internal GPS cable channel in the keel, and the keep-outs of section 6.
2. **Lid.** One printed part: the battery plate (64 x 34 x 2.5, z 21.5 to 24, as D-025) and the GPS deck behind it (x -50 to -30, y +-10, same thickness), joined. Fixed: plate perimeter frame 3 mm and strap band x +-9 (D-052), deck frame 3 mm, GPS pocket rim and cap bosses, five countersunk screw pads, the front lip (XT30 groove and zip-tie slot). Design: plate and deck interiors (as D-052).
3. **Joint lid to tub.** Five M2 countersunk screws into M2 heat-set inserts in tub bosses: four on the front and rear walls, one on the keel (positions in section 9, item 1). The lid rests on the tub rim at z = 21.5.
4. **Retainers (separate small prints, PETG or TPU, not in the TO model):** receiver cradle, GPS cap, antenna holder.
5. **Model.** Tub and lid are separate parts, tied only at the five screw bosses (conservative: the rim contact is ignored). Section 10.

Why a lid, not access windows: windows large enough for the FC (33 x 33) in a side wall would remove most of a wall; a removable lid gives a vertical insertion path, a straight tool path to every screw and solder pad, and keeps the battery plate as one stiff part.

## 3. Components and data

| Component | Data used | Source / status |
|---|---|---|
| FC SpeedyBee F405 AIO 40A | board 33 x 33, total height 8 incl. heat sink; mounting 25.5 x 25.5, holes at (+-12.75, +-12.75); M2 hardware with soft-mount grommets 6.6 mm tall, damping rings 1.0 mm | listing; M2 (not M3 as the journal's component table says: correct Section 2 of the journal) |
| FC pads | battery pads on the front edge (+x after rotation): "-" at y = -8.7, "+" at y = -4.5 | Miguel's drawing |
| FC USB-C | on the -y edge at x = +5.4 | Miguel's photo |
| XT30 pigtail | 7 cm, 18 AWG pair (about 2 mm per wire) | kit |
| Capacitor | 470 uF 35 V, design envelope Ø10.5 x 21 | kit |
| Receiver SpeedyBee Nano ELRS | 10.4 x 18.4, 4 mm thickness allowance; T antenna (dipole about 49 to 52 mm across, coax about 79 mm), IPEX-1 | GetFPV listing |
| GPS Flywoo GOKU GM10 Nano V3 with compass | 12 x 17 x 5, 2.6 g | Flywoo listing; the page lists 4 pins: confirm the compass version has SDA / SCL (6 wires) before ordering (item 14) |
| Battery | 59 x 30 x 32, 100 g, XT30 lead at the front (D-029) | unchanged |
| Lid hardware | 5 x M2 countersunk (ISO 10642) M2 x 6, 5 x M2 heat-set inserts (length about 3 to 4 mm) | to buy; insert hole size from the insert maker |
| FC screws | button head (ISO 7380, head about Ø3.5 x 1.1): M2 x 20 at pm and mm, M2 x 22 at pp and mp (section 4) | head must sit within the 1.5 mm counterbore so the floor stays flush for the skid (D-039) |

FC orientation: USB-C on the -y side, battery pads facing +x (front). This is not the board's default orientation: set the Betaflight board-alignment yaw to the angle between the board's arrow and +x, and remap the motors in the Motors tab; check with the 3D model tab and a props-off motor direction test.

## 4. FC stack (soft mount, screws from below)

| z from | z to | Item |
|---|---|---|
| -15.0 | -13.5 | counterbore Ø4.2 x 1.5 from the floor bottom (screw head) |
| -15.0 | -6.0 | FC boss Ø6, through hole Ø2.2 (fixed region; was blind Ø3.2) |
| -6.0 | -5.0 | damping ring 1.0 |
| -5.0 | +1.6 | grommet 6.6 with the PCB in its groove (PCB about -2.5 to -0.9: confirm on the part) |
| +1.6 | +4.1 | anti-loosening nut (all four screws) |
| +4.1 | +5.5 | ear of a retainer (receiver cradle, pp and mp only) |
| +5.5 | +7.1 | nylon nut (pp, mp, pm) |

Screw tips (head bearing face at -13.5): M2 x 20 reaches +6.5, M2 x 22 reaches +8.5 (at least 1 mm above the nylon nut). The pm and mm screws carry only the anti-loosening nut: M2 x 20 (tip +6.5), or M2 x 18 (tip +4.5, flush plus 0.4) if the tip needs to stay low.

FC keep-out (board, components, grommets): 35 x 35 (x, y +-17.5), z -6 to +5.

## 5. Component seats and retainers

### 5.1 Receiver cradle (separate print)

- U section open at both ends (receiver wires and the IPEX lead leave through the ends), inside 11 (y) x 19 (x) x 4.5 deep, walls 1.2, floor 1.4, snap lips along both side walls, end stops 1 mm high.
- Position: centred on x = 0, outer y +1.25 to +14.65 (inside +2.45 to +13.45), floor z +4.1 to +5.5, top about +11.
- Two ears (1.4 thick) on the pp and mp screws, clamped between the anti-loosening nut and the nylon nut.
- Check C-6: the FC components under the floor footprint (x +-9.5, y +1.25 to +14.65) must be below +4.1; if the heat sink reaches higher there, the floor steps up (ear stays at +4.1 to +5.5); 10 mm of height are free to the lid.

### 5.2 Capacitor (option 2: flipped 180 deg over the FC, confirmed)

- Soldered on the bench to the battery pads together with the pigtail; leads formed on the bench so that no bend starts within 2 mm of the solder joint or of the capacitor body (Miguel's requirement: no bending at the joint).
- Lies along x over the board at the discussed position: body x -6 to +15, y -11 to -0.5, z +5 to +15.5 (axis y -5.75, z +10.25). No retainer (Miguel, 2026-10-11): it floats on its soldered leads, as in his flown builds. Clearance to the pm anti-loosening nut (top +4.1): about 2.5 mm.
- Lead zone (no material, no retainer): x +13 to +17.5, y -10.5 to +0.5, z -1 to +16.5.
- No cradle and no lid rib. Accepted consequence: in a hard landing the capacitor can move down about 0.75 mm onto the FC components (insulated sleeve).

### 5.3 Battery lead (pigtail and XT30)

- Front window in the tub front wall: 7 (y) x 3.5 (z), y -9 to -2, z -2 to +1.5 (board height). Only the two wires pass.
- Outside run: forward low (z about -2 to +2), moving to y about 0, then rising at x +25 to +30 with bend radius 10 to 13 to the XT30 at the front of the lid. Keep-out (no tub material): x 20 to 31, y -10 to +3, z -3 to +3 (low run) and x 24 to 31, y -3 to +3, z 0 to 24 (riser).
- The mated XT30 pair sits on the lid front lip (above z = 21.5), in a guide groove, held by a zip tie through a slot in the lip.
- Clearances already checked in the discussion: the low run clears the pm arm (which occupies y <= -11.6 for x >= 11.6 below z = 10) by about 1 mm when angled; the riser at |y| <= 2 is inside the prop corridor (prop sweep + 3 mm reaches |y| = 8.86 at x = 25, 6.24 at x = 30, 4.32 at x = 35, for z 10 to 21.5). An XT30 (about 10.2 mm wide) must not sit at blade height beyond x = 28: at x = 30 its edges would be 1.1 mm from the corridor limit, at x = 32 0.3 mm. Hence the XT30 is on the lid lip, above z = 21.5.
- Threading: section 9, item 2.

### 5.4 (removed)

The lid clamp rib was dropped with the capacitor cradle (Miguel, 2026-10-11).

### 5.5 USB-C

- Window in the -y wall, 12 (x) x 7 (z): x -0.6 to +11.4, z -1.5 to +4.5.
- Plug path outside the wall, along -y, 12 x 7 section to y = -40 (no frame material). Its front edge (x = 11.4) is 0.2 mm short of the pm arm region (x >= 11.6): check C-8 with the real cable plug.

### 5.6 Receiver antenna

- Coax leaves the bay through a Ø4 hole in the rear wall (x = -20), centred y = -5, z = -3.5 (1.5 mm below the keel bottom edge, z = 0); section 9, item 4 explains why not beside the keel.
- Holder: TPU, one M2 screw into an insert boss in the keel underside at (x -42, y 0), boss Ø5 from z 0 to 5 (fixed region inside the keel; keel half-width below z = 10 is 9, so 6.5 mm clear of the keel sides).
- T antenna bent into a V of 90 deg included angle. Plane of the V: horizontal under the keel, elements pointing rear-left and rear-right (section 9, item 5).

### 5.7 GPS

- Pocket on the lid deck for the GM10 Nano: inside 12.6 (y) x 17.6 (x), long side along x, centred at (x -40, y 0). The pocket floor is the deck itself (z 21.5 to 24, 2.5 mm, not cut); rim walls 1.2 mm from z 24 to 26.5. Module on the deck top: CG at about (-40, 0, 26.5).
- Retainer: TPU cap with a window over the ceramic antenna, two M2 screws into inserts in two rim bosses (Ø5, z 21.5 to 26.5) beside the pocket at y about +-9.5. The deck may widen locally above z = 21.5 for these bosses (there is no prop keep-out above z = 21.5). No lid feature may reach below z = 21.5 outside the tub opening (it would hit the keel).
- Cable: hole Ø4 in the pocket floor at (x -33, y 0), then an internal channel down the keel and forward into the bay through a separate rear-wall hole opposite the antenna (section 9, item 3).
- Compass: keep the module's arrow along +x; the XT30 and battery lead are at the front (D-029), 70 mm away.

### 5.8 Battery strap

- D-030 path kept: one strap up to 16 mm wide, across y at x = 0, over the battery and under the lid strap band.
- Strap passage: notches 18 (x) x 3.5 (z) in the top of both tub y walls, x -9 to +9, z 18 to 21.5, closed above by the lid band (the "lid slots" of the discussion). Across the open bay the strap runs under the band at z 18 to 21.5: no retainer or rib may enter x +-9, z 18 to 21.5 (the receiver top is +11 and the capacitor top +16.25, both below).
- Anti-slip pad on the plate top.

### 5.9 Motors and motor leads

- Motors, pads and the arm wire channels unchanged.
- The leads enter the bay through the passages at the foot of each wall (z -6 to -3): these must be continuous 5 x 5 keep-outs from the arm channel exit to the bay (check C-7), and the leads are soldered to the FC corner pads from above after the FC is seated.

## 6. Tub regions

### 6.1 Keep-outs (voids cut from the tub envelope; nothing may be generated inside)

| # | Keep-out | Extent | Purpose |
|---|---|---|---|
| K1 | FC stack | x, y +-17.5, z -6 to +5 | board, components, grommets |
| K2 | FC insertion prism | x, y +-17, z +5 to +21.5 (the rim) | lowering the FC from above with the lid off; section 9, item 1 |
| K3 | Screw holes and counterbores | Ø2.2 through the four FC bosses; Ø4.2 x 1.5 from z -15 | screws from below |
| K4 | Retainers and components above the FC | receiver cradle box x +-9.5, y +1.25 to +14.65, z +4.1 to +11.5; capacitor Ø11.5 cylinder (0.5 mm clearance), axis (y -5.75, z 10.25), x -6.5 to +15.5; lead zone of 5.2 | inside K2 anyway; listed so that the clash check covers them |
| K5 | Nut access columns | Ø8 at (+-12.75, +-12.75), z +1.6 to +21.5 | fingers or tweezers for the nuts |
| K6 | Pigtail window and outside path | 5.3 | battery lead |
| K7 | USB window and plug path | 5.5 | USB-C |
| K8 | Antenna hole | Ø4 along x through the rear wall at (y -5, z -3.5) | coax |
| K9 | GPS cable channel | Ø4: vertical leg at (x -33, y 0) from z 21.5 to 5, bend R >= 5, horizontal leg at z 5 to the rear-wall hole at (x -20, y +4) | GPS cable; section 9, item 3 |
| K10 | Strap passage | x +-9, z 18 to 21.5, through both y walls | strap |
| K11 | Motor-lead passages | 5 x 5, continuous from each arm channel into the bay | motor leads |
| K12 | Prop sweep, motors, arm clearances | unchanged (D-046) | |

### 6.2 Fixed regions in the tub

| Region | Shape | Note |
|---|---|---|
| Fin bosses (8) | unchanged (D-055) | |
| FC bosses (4) | Ø6, z -15 to -6, minus K3 | was blind |
| Lid bosses (5) | Ø6, z 15.5 to 21.5, insert hole per maker (about Ø3.2 x 4.5) | positions in section 9, item 1 |
| Antenna-holder boss | Ø5, z 0 to 5 at (-42, 0) in the keel | |

The old battery plate frame, strap band and GPS frame leave the body: they are now lid regions.

### 6.3 Design region

Tub design = old body design envelope (D-056, keel included) minus the keep-outs and the fixed regions. The upper body z 10 to 21.5 keeps its chamfered outline (|x| + |y| <= 31.8).

## 7. Lid regions

| Region | Type | Content |
|---|---|---|
| Plate frame 3 mm, strap band x +-9 | fixed | as D-052, now on the lid (battery seat `S_BATT_SEAT`) |
| Deck frame 3 mm | fixed | as D-052 |
| GPS pocket rim, cap bosses | fixed | 5.7 (GPS seat `S_GPS_SEAT` = pocket floor) |
| Screw pads (5) | fixed | Ø6 discs through the 2.5 mm plate with Ø3.8 x 90 deg countersinks, coaxial with the tub bosses |
| Front lip | fixed | XT30 groove and zip-tie slot, at the plate front edge (x = +32), above z = 21.5 |
| Plate and deck interiors | design | as D-052 |

## 8. Assembly sequence and space check at each step

| Step | Action | Space check (what must be true) |
|---|---|---|
| 1 | Bench: solder the pigtail (bare ends, no XT30 yet) and the capacitor to the battery pads; form the capacitor leads and lay the capacitor over the board (option 2); solder the receiver wires; solder the GPS cable at the FC end only if its GPS-end plug passes K9 (section 9, item 3) | lead bends at least 2 mm from the joints |
| 2 | Bolt the four arms (motors fitted), feed the motor leads through K11 into the bay | lid off |
| 3 | Damping rings on the four boss tops | |
| 4 | Lower the FC with the grommets fitted, pigtail wires folded up over the board, receiver loose on its wires | board plus capacitor (top +15.5) pass down K2 (34 x 34); nothing protrudes into K2; the corners of K2 at z 10 to 21.5 are open (section 9, item 1) |
| 5 | Push the four screws up from below; anti-loosening nuts from above (lift the capacitor aside on its leads for the pm nut) | K5 free; screws reach the bosses from below with the tub on its back or held on edge |
| 6 | Solder the motor leads to the FC corner pads | iron reaches every corner pad from above through K2 |
| 7 | Receiver cradle onto the pp and mp screws, nylon nuts; receiver into the cradle | |
| 8 | Lay the capacitor back in place over the FC (no retainer) | capacitor clear of the pm nut and the receiver cradle |
| 9 | Push the pigtail ends out through the front window; solder the XT30 outside (section 9, item 2); heat-shrink | window 7 x 3.5 passes two 18 AWG wires side by side |
| 10 | Antenna: IPEX end in from outside through K8 to the receiver; V into the holder; holder screwed under the keel | IPEX plug (about Ø2) passes Ø4 |
| 11 | GPS cable: from the lid pocket down K9 into the bay; solder to the FC if not done in step 1; plug into the GPS | slack in the bay so the lid can be lifted and set aside |
| 12 | Lid on, five countersunk screws | no lid feature hits a retainer, a nut or the capacitor |
| 13 | GPS into its pocket, cap and two screws; battery, strap, XT30 mated on the lid lip, zip tie | |

Maintenance: battery and strap off, five lid screws out, lid lifted and laid aside on the GPS cable; everything in the bay is then reachable from above.

## 9. Points found while checking the agreed layout for this brief (defaults adopted)

Each item: what was agreed, what the check found, the default used in this brief, alternatives. Confirm in the main chat; none changes the architecture.

1. **Lid boss positions and the FC insertion path.**
   - Agreed: four lid bosses at the tub corners plus one on the keel; FC lowered from above through a large opening.
   - Found: the FC board is 33 x 33, so its corners lie on the diagonal at 23.3 mm from the centre, while the upper body (z 10 to 21.5) is chamfered to |x| + |y| <= 31.8 (22.5 mm on the diagonal, set by the prop keep-out). A 34 x 34 insertion prism therefore cuts through all four upper corners: above z = 10 the tub walls become four separate wall segments (3 mm thick, x or y from 17 to 20) and there is no corner left for a boss.
   - Default: open corners (K2) and four bosses Ø6 on the wall segments, centred at (+20.25, +7), (+20.25, -7), (-20.25, +7), (-20.25, -7), plus the keel boss at (-26, 0). The wall bosses stand 3.25 mm proud of the old wall faces (x up to 23.25), which is allowed: the envelope limit there is the prop keep-out, not the old body face. Checks done: inner boss edge at |x| = 17.25, 0.25 mm clear of K2 (|x| <= 17); 1.14 mm outside the prop sweep + 3 mm; centres 9.45 mm from the nut column axes (needs 7.0); clear of the strap passage (x +-9) and the windows. Keel boss: keel width at x = -26 about 16 mm (prop corridor +-8), countersink 2.1 mm from the GPS pocket rim, under the battery rear end (flush countersunk; the battery is off before the lid comes off).
   - Alternative: FC inserted tilted about 30 deg (its projection then clears the chamfer), keeping closed corners; rejected as default because the capacitor over the board and the folded pigtail make tilting awkward, against requirement 1 (easy assembly).
2. **XT30 through the front window.** An XT30 housing (about 10.2 x 5.2) does not pass a 7 x 3.5 window. Default: the pigtail is bench-soldered with bare ends, pushed out through the window after the FC is seated, and the XT30 is soldered on outside (step 9). Alternatives: window 11 x 6 (passes the XT30, weakens the front wall more), or a slot open to the rim, closed by the lid lip (wall cut over its full height).
3. **GPS cable "down beside the keel".** Above z = 10 the keel already fills the corridor between the rear prop sweeps (+3 mm): at x = -36 the corridor is +-4.0 and the keel is the same width; at x = -22 the gap between the keel side (y = 9) and the sweep is 1.8 mm. A cable beside the keel at blade height would sit inside the prop keep-out. Default: the same route inside the keel (K9), entering the bay through its own rear-wall hole at (y +4, z 5), opposite the antenna. Connector rule: every opening a connector must pass during assembly is sized for that connector, or the cable is threaded bare-ended and soldered afterwards; measure the GM10 cable plugs and either enlarge K9 locally (keel walls must stay >= 1.2 mm) or solder the FC end in place (step 11).
4. **Antenna hole "beside the keel".** Below z = 10 the gap between the keel side (y = 9) and the fin-root fillet tangent line on the rear face (y = 10.86) is 1.86 mm, too narrow for a Ø4 hole and a near-tangency hazard (F-031 type). Default: below the keel, centre (y -5, z -3.5), 1.5 mm from the keel bottom edge. Check: >= 1 mm from the rear-left motor-lead exit (z -8 to -3 near the centreline) (C-7).
5. **Antenna V downward.** A 90 deg V of two 25 mm elements hanging below the keel (z = 0) drops 17.7 mm, so its tips reach about z -18 to -20, below the landing plane (floor bottom z = -15): the antenna would touch the ground first. Options (mutually exclusive): A (default) the same V in the horizontal plane under the keel, vertex at the holder (-42, 0, about -3), tips at about (-60, +-18, -3), 29.7 mm from the rear arm axes, 12 mm above the landing plane, below the props; poorer polarisation match with a vertical radio antenna when level. B a vertical V on the centreline behind the keel (vertex about (-50, 0, 5), elements rear-up and rear-down at 45 deg): lower tip at z -12.7, 1.5 to 2.7 mm clear of the prop keep-out only if exactly on the centreline, better polarisation, exposed about 18 mm behind the frame. Miguel chose A (2026-10-11).
6. **Capacitor retention.** A tub-fixed cradle would block the FC insertion, and a clip-on cradle on the pm screw needed the capacitor moved and a 1.2 mm wall in a 0.4 mm gap. Decision (Miguel, 2026-10-11): no retainer at all; the capacitor floats on its soldered leads at the discussed position, as in his flown builds. The pm screw carries only the anti-loosening nut (M2 x 20).
7. **Floor pressure in LC3a.** The four counterbores remove 4 x 13.85 = 55.4 mm^2 from `S_FLOOR` (was 1600 mm^2 including the boss discs, F-2). To keep the 56.4 N ground force: p = 56.4 / A(S_FLOOR) = 56.4 / 1544.6 = 0.036515 MPa (was 0.03525); read A from the model and recompute.
8. **Lid modes.** The plate was merged into the body; now it is tied at five points and carries the 100 g battery. Hand estimates of the battery-on-lid mode (plate 34 x 2.5, supports at x = +-20.25, solid): 202 Hz with the battery mass at mid-span, about 600 Hz with the battery weight spread over its 59 mm length; they bracket 417 Hz, so the reference job decides. Gate G7 is run twice: G7a with ties at the five bosses only, G7b with ties at the bosses plus the rim contact faces. Both pass: Tosca uses G7a. Only G7b passes: (a) model with G7b, justified by the screw clamping (main chat decision), or (b) more lid screws, or (c) a deeper fixed lid frame, then rerun G7a. Both fail: (c). The lighter GPS (2.6 g instead of 8 g) raises the deck mode by about 1.75 for the mass part alone.

## 10. Abaqus / Tosca model changes (set-up chat)

| Item | v03-B | v04-B |
|---|---|---|
| Parts | BODY, ARM (x4 instances) | TUB, LID, ARM (x4 instances) |
| Design sets | DESIGN_BODY, DESIGN_ARM | DESIGN_TUB, DESIGN_LID, DESIGN_ARM; `DESIGN_ALL` = all three |
| Fixed sets | FIXED_BODY | FIXED_TUB, FIXED_LID |
| `S_BATT_SEAT` | body top z = 24, plate frame and band | same faces, on LID |
| `S_GPS_SEAT` | GPS frame ring z = 24 | pocket floor (deck top inside the rim) on LID |
| `S_FC_SEAT` | 4 boss rings, 80.92 mm^2 | 4 rings Ø6 / Ø2.2, 97.89 mm^2 |
| `S_FLOOR` | 1600 mm^2 | 40 x 40 square minus counterbores, about 1544.6 mm^2; LC3a pressure recomputed (9.7) |
| RP_GPS | (-40, 0, 28), 8.0e-6 t | (-40, 0, 26.5), 2.6e-6 t |
| RP_FC | 27.2 g | 27.2 g (receiver lumped here as before); retainers and new screws counted against the 12 g hardware allowance (A-005), itemised in the export note |
| Lid ties (new) | | `TIE_LID_1..5`: main = tub boss top annulus (z 21.5), secondary = lid pad bottom annulus; coincident faces, position tolerance 0.1 mm, adjust off. Expected: 0 untied secondary nodes |
| Joint ties, couplings, supports (D-064), steps, loads | | unchanged |

Caps (D-063): recomputed from the v04-B solid reference on each mesh used.

## 11. Verification gates (no export or run passes a gate with a failure)

The meshing failures of v03-B came from boundaries that touched tangentially or nearly so (F-8, F-10, F-028, F-031). Every new feature here (bosses, holes, windows, channels, notches, rim, counterbores) is a new boundary, so each one is checked, not only the files as a whole.

| Gate | Check | Pass |
|---|---|---|
| G0 | File identity: solid count and names, design and fixed volumes of every STEP against the export note | exact match (the wrong BODY.step of 2026-10-10 would have been caught here) |
| G1 | Boolean bookkeeping: design + fixed = envelope minus keep-outs, per part; design AND fixed = 0; every keep-out AND (design OR fixed) = 0; every fixed solid touches the design solid of its part | differences < 0.01 mm^3; no floating fixed solid |
| G2 | Face test (`s06_split_acceptance.py`, general fuse of all solids per file) | no face < 0.5 mm^2, none narrower than 0.3 mm |
| G3 | Tangency audit: for every new feature, the minimum distance to every other region boundary and the crossing angle where they meet; table in the export note | distance >= 1.0 mm (one production element) or crossing angle >= 30 deg; listed pairs at least: lid bosses vs wall faces, chamfer faces and K2; FC boss and counterbore vs floor faces; K8 vs keel bottom, fillet tangent lines (y +-10.86) and motor-lead exits; K9 vs keel side faces; K10 notches vs wall tops and the chamfer; antenna boss vs keel faces; USB and pigtail windows vs floor, wall ends and fin fillets; lid pads vs the lid frame and pocket rim |
| G4 | gmsh mesh test (`s06_gmsh_meshtest.py`, fragment as Abaqus merge, linear tets) at 1.5 and 1.0 mm, on TUB and LID | 1.5 mm: no tet below quality 0.05; 1.0 mm: no new low-quality tets compared with v03-B (25 tets of 0.02 at known BODY features), each tet below 0.05 located and explained |
| G5 | Assembly clash: component dummies (FC stack, receiver and cradle, capacitor, nuts, screw heads, pigtail path, XT30, USB plug, antenna and holder, GPS and cap, battery, strap) against TUB, LID, the four ARM STEPs, the prop sweep + 3 mm and each other; plus the insertion of step 4 (FC with capacitor swept down K2) and lid placement | no interference; minimum clearances reported (C-1 to C-9) |
| G6 | Abaqus/CAE mesh at the debug (2.5 / 1.5) and production (1.0) sizes | 0 errors, warnings < 1 % (v03-B had 0.05 %); unprojected mid-side nodes only on curved faces |
| G7 | Reference job (solid design space) on the debug mesh, run twice (G7a: lid tied at the five bosses; G7b: bosses plus rim contact faces, 9.8), then on 1.0 mm with the chosen connection | mass as computed from the STEPs plus point masses (+-0.1 %); modes 1 to 6 < 1 Hz; modes 7 to 12 identified by shape (screenshots), no local lid or GPS mode below 417 Hz (9.8); ALLWK = ALLSE; reactions < 1e-6 N; joint ties as Phase 8 (172 untied secondary nodes at 2.5 / 1.5, lower fin faces only); lid ties 0 untied; caps = 2 x ALLSE |

Clearance checks for G5:

| # | Check | Required |
|---|---|---|
| C-1 | FC plus capacitor through K2 | >= 0.25 mm all round |
| C-2 | Lid bosses to K2, K5 and the prop sweep + 3 | >= 0.25 / 1.0 / 1.0 mm |
| C-3 | Pigtail low run to the pm arm and fin | >= 1 mm |
| C-4 | XT30 and riser to the prop sweep + 3 | outside |
| C-5 | Capacitor to the pm nut, the receiver cradle and the lid | >= 1 mm |
| C-6 | Receiver cradle floor to the FC components | >= 0.3 mm (measure the board) |
| C-7 | K8, K11 and the motor-lead exits | >= 1 mm apart |
| C-8 | USB plug to the pm arm | >= 0.5 mm with the real plug |
| C-9 | Antenna V to the rear arms, the ground plane z = -15 and the rear props | arms >= 5 mm, above z = -12, below z = 10 |

## 12. Runs (set-up chat, after G0 to G7)

| Run | Machine | Mesh | Settings | Purpose | Time |
|---|---|---|---|---|---|
| R4 ref | laptop or nexus | 2.5 / 1.5 | plain Abaqus | G7, caps for H4c | minutes |
| H4c | nexus, Tosca 2024 | 2.5 / 1.5 | as H2 (no member size: 2.5 mm is not above twice the element size, C-5), max 60 cycles, save every 10 + last | shape and convergence of the new space, lid modes during the run | about 1.5 h |
| H4 ref | nexus | 1.0 | plain Abaqus | caps for H4 | about 12 min |
| H4 | nexus, Tosca 2024 | 1.0 | as H3: member size 2.5 mm on `DESIGN_ALL`, start density 1 (DV-13), rotational symmetry on the arms, max 60 cycles, save every 10 + last, threads (`mp_mode=threads` in AddCallArgs; never on the optimization command line, F-15), memory 80 %, run in `/tmp` | production | about 10 h (40 cycles x about 14 min) |

During H4c and H4: the mode check (`cyclecheck.py`) and the reactions are reported at each saved cycle as diagnostics, not as stop rules (decision 4).

Post-processing of the final cycle (same chain as v03-B):

| # | Step | Pass |
|---|---|---|
| T-1 | Freeze the final cycle (input, distribution, odb) before any pruning | files present |
| T-2 | Separation table (share below 0.3, 0.3 to 0.5, at or above 0.5) | reported |
| T-3 | Iso surfaces at 0.3, 0.4, 0.5 (`iso_mt.py`, 6 Taubin iterations), masses | closed, manifold |
| T-4 | Thresholded jobs TH03, TH04, TH05 (`threshold_job.py`, all `*...RESPONSE` blocks stripped) | TH04: f7 >= 417 Hz, every SE <= cap, reactions < 1e-6 N |
| T-5 | Restoration at iso 0.4 (D-044) with the v04-B STEPs, tub and lid separately | one manifold piece per part; restored and trimmed volumes reported |
| T-6 | Wall thickness, both methods | surface below 0.8 mm <= 1 %, below 1.2 mm <= 3 % (v03-B iso 0.4: body 0.1 / 1.0 %, arm 0.8 / 2.2 %); every thin spot located |
| T-7 | Final assembly clash: G5 repeated on the restored STLs | no interference; every keep-out empty |

## 13. Mass (estimate)

| Item | Change |
|---|---|
| v03-B frame (print set) | 76.8 g |
| GPS 8 g placeholder to GM10 Nano 2.6 g | -5.4 g |
| Retainers (receiver, GPS cap, antenna holder), lid screws, inserts, longer FC screws and nylon nuts, lid split (pads, bosses) | about +3 to +4 g |
| Net | roughly neutral: frame plus hardware about 75 to 79 g, AUW about 280 g |

R-01 not met (decision 2).

## 14. To send back with the export

1. `TUB.step` (`TUB_DESIGN`, `TUB_FIXED`), `LID.step` (`LID_DESIGN`, `LID_FIXED`), `ARM_xx.step` (unchanged, G0 confirms), `reference_points_v04B.csv`.
2. `KEEPOUTS_v04B.step` (K1 to K12 as named solids) and `COMPONENTS_v04B.step` (dummies of G5), for the clash checks.
3. Export note: volumes, G1 to G5 results, tangency table, clearance table C-1 to C-9, mass table, expected model mass.
4. Generator and test scripts.

## 15. Decisions proposed for the main chat

| # | Proposed decision |
|---|---|
| 1 | v03-B print set (H3 cycle 40, iso 0.4, restored; frame 76.8 g) recorded as the v03-B structural result; not built, because it cannot be assembled (F-16) |
| 2 | R-01 (AUW < 250 g) not met for variant B at 417 Hz; accepted by Miguel (about 280 g); mass for assembly features accepted. D-035 sweep and variant C not run now |
| 3 | D-066 closed: item 1 measured interpolation; item 2 flags are grey arm bending modes, not spurious; item 3 thresholded designs pass and are stiffer than Tosca predicted |
| 4 | From H4 on: the mode check is a reported diagnostic, not a stop rule; acceptance is the thresholded job at the print iso level (TH04) |
| 5 | Print iso level 0.4 |
| 6 | v04-B architecture: optimised open tub plus removable lid (plate and GPS deck), five M2 countersunk screws into heat-set inserts; tub and lid tied only at the screw bosses in the model |
| 7 | Component retention by designed seats and separate retainers, no glue or tape: receiver cradle on the FC screws; capacitor floating on its leads, GPS cap, antenna holder |
| 8 | FC soft-mounted on through-bosses, screws from below (counterbores), nuts from above; FC rotated (USB -y, pads +x), board alignment and motor remap in Betaflight |
| 9 | Capacitor flipped 180 deg over the FC (option 2); pigtail through a front window, XT30 on the lid lip |
| 10 | GPS: Flywoo GOKU GM10 Nano V3 with compass (2.6 g) in a lid pocket; closes D-007 for the GPS (firmware still deferred), replaces A-007 / A-025 |
| 11 | The section 9 defaults (open upper corners and wall bosses; XT30 soldered after threading; GPS cable inside the keel; antenna hole below the keel; horizontal antenna V; capacitor with no retainer; LC3a pressure from the new floor area) |
| 12 | Design-space rule added to D-032: every component has an insertion path, a tool path and a cable path as keep-outs, and each is checked by a sweep in the clash test |

Journal records also proposed: F-16 (assembly), lessons L-a to L-d of the update, numbers N-06-09 to N-06-14, correction of the journal's FC hole size (M2), A-005 itemised hardware list after the export.

## 16. Open items

| # | Item |
|---|---|
| O-a | GM10 Nano V3 compass version: confirm 6 wires (SDA / SCL) before ordering; if only 4, choose another compass module of similar size and redo the pocket |
| O-b | Measure the GM10 cable plugs (connector rule, 9.3) |
| O-c | Measure the FC heat-sink height under the receiver cradle (C-6) and the PCB position in the grommet groove |
| O-d | Lid tie modelling if a lid mode is active (9.8) |
