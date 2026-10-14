# Quadcopter rev B: sizing model from first principles

Oct 4, 2026 · @Miguel Lima

## Chapter 0: The goal

The frame cannot be designed until we know what the rest of the aircraft does to it. The sizing model exists to produce those numbers from the parts already bought.

### The situation

The motors, propellers, battery, flight controller and receiver are bought and fixed. Only the frame is open. It must be 3D printed and keep the aircraft under 250 g.

The frame produces no thrust and stores no energy. It only carries. So every number that drives its design comes from somewhere else: from the propulsion system, the battery and the way the aircraft flies.

### What the frame designer needs

| Question the frame designer asks | Model output | Used in |
| --- | --- | --- |
| How heavy can the frame be? | Mass budget and hover point | R-01, Stage 3 |
| How hard does each motor pull on its arm? | Maximum thrust per motor | Stage 4 loads |
| How hard does each motor twist its arm? | Maximum motor reaction torque | Stage 4 loads |
| How hard are the battery and stack pressed into their mounts in a violent manoeuvre? | Load factor | Stage 4 loads |
| How hard can the aircraft hit something? | Top speed and kinetic energy | Stage 4 crash case |
| At which frequencies is the frame shaken? | Rotor frequencies at hover and full throttle | Stage 4 stiffness targets, Stage 7 modal analysis |
| What does each gram, or each millimetre of arm width, cost? | Endurance and its sensitivity to mass and arm width | Stage 3 and Stage 6 trades |
| Is the bought hardware consistent? | ESC and battery current margins | Sanity check |

### The two operating points

Almost everything comes from two conditions:

- **Hover**: the aircraft holds still in the air. This is where it spends most of its time, so it sets **performance**: power, current, endurance, and the frequency at which the rotors shake the frame most of the time.
- **Full throttle**: the motors push as hard as they can. This sets the **loads**: the largest forces and torques the frame must carry.

Forward flight is a third, smaller piece: it gives the top speed, which sets the crash energy.

### The chain

Each chapter answers one question and hands its result to the next:

1. Mass: how much the aircraft weighs, so how much thrust it needs (Chapter 1).
2. Thrust to speed: how fast each propeller must spin to make that thrust (Chapter 2).
3. Speed to minimum power: the least power physics allows for that thrust (Chapter 3).
4. Minimum to real power: where the extra power is lost, in the propeller, motor and ESC (Chapter 4).
5. Real hover power: estimated outside the test data (Chapter 5).
6. Power to flight time: battery energy divided by power, and what a gram of frame costs (Chapter 6).
7. Full throttle: forces, torques and load factor for the structure (Chapter 7).
8. Forward flight: top speed and crash energy (Chapter 8).
9. Spinning to shaking: the vibration frequencies (Chapter 9).
10. Summary of outputs passed to the next stages (Chapter 10).

### What we have to work with

- **Datasheet masses** of every bought part (decision D-008).
- **Propeller geometry**: diameter 3.5 in (0.0889 m), pitch 2.0 in, 3 blades.
- **Manufacturer bench test** of the same motor with the same propeller: five rows of throttle, voltage, current, RPM, thrust and electrical power.

A bench test (thrust stand) clamps the motor on a load cell, spins the propeller at fixed throttle steps and records the thrust, the speed, and the battery voltage and current. It is the only measured propulsion data we have. Everything in the model is either read from this table or derived from physics and checked against it.

Numbers in this document match the journal numbers register (N-02-xx). Where an assumption enters, it is named with its register ID (A-0xx).

## Chapter 1: Keeping it in the air

To hover at 250 g, each rotor must produce 64.4 g of thrust: a quarter of the weight, plus 3 % to cancel the push of its own air jet on the arm below it.

### How a quadcopter flies

A quadcopter has four fixed-pitch propellers. The blades can't change angle, so the **only** thing the flight controller can change is how fast each motor spins.

- **Up and down**: all four motors speed up or slow down together.
- **Tilt (pitch and roll)**: the motors on one side spin faster than the other side, and the aircraft leans.
- **Moving sideways or forward**: the aircraft leans, so part of the thrust points horizontally.
- **Turning (yaw)**: two propellers spin clockwise and two counter-clockwise, so their reaction torques cancel. Speeding up one pair and slowing the other leaves a net torque that turns the aircraft.

Consequence for the frame: every force on it comes from rotor speed. If we know how thrust and torque depend on speed, we know the loads.

### Mass, weight and grams of thrust

| Symbol | Name | What it is | Unit |
| --- | --- | --- | --- |
| m | Mass | Amount of matter; doesn't depend on gravity | kg |
| g | Gravitational acceleration | 9.81 m/s^2 at the Earth's surface | m/s^2 |
| W | Weight | Force of gravity on the mass, W = m g | N |
| T | Thrust | Upward force from one rotor | N, or "g" in bench tables |

Drone data quotes thrust in grams. It means **gram-force**: the weight of a 1 g mass, 9.81 x 10^-3 N. It is a convenient unit because hover thrust in gram-force equals the aircraft mass in grams. Tables keep grams; any physics formula uses newtons.

### The mass budget

The aircraft mass is fixed by the 250 g limit (requirement R-01, from the EU open category A1 rule for privately built drones). Everything except the frame is known, so the frame gets what is left.

| Item | Mass (g) | Source |
| --- | --- | --- |
| Motors (4) | 46.4 | Datasheet |
| Propellers (4) | 7.0 | Datasheet |
| Flight controller and ESC | 13.6 | Datasheet |
| Receiver and antenna | 1.6 | Datasheet |
| Battery | 100.0 | Datasheet |
| **Fixed components** | **168.6** | N-00-01 |
| Screws, strap, wiring, capacitor | 12 | Estimate, A-005 |
| GPS placeholder | 8 | Estimate, A-007 |
| **Frame budget** | **61.4** | 250 minus the rest |
| **Total** | **250** | Design point |

The model is evaluated at 250 g, the heaviest allowed weight. This is the worst case for endurance and for every load that scales with mass.

### Hover: the first estimate

In hover nothing accelerates, so the vertical forces cancel (Newton's first law). If the four rotors carried the weight equally and nothing else acted:

```latex
4T = W = m g
```

m = 0.250 kg, so W = 2.45 N and T = W / 4 = 0.613 N per rotor, which is **62.5 g**. This is the value in the original context file.

### Arm download

The first estimate misses one force. A propeller makes thrust by throwing air downwards. The arm sits directly under the propeller, inside that jet. The jet hits the arm like wind hitting a plate and pushes it down. This downward force is called **download**.

The rotor's thrust is unchanged, but part of it is spent fighting its own jet. The aircraft feels rotor thrust minus download. So the rotor must produce slightly more than a quarter of the weight.

**Variables**

| Symbol | Name | What it is | Our value |
| --- | --- | --- | --- |
| F\_d | Download | Downward force of the jet on one arm | N |
| f | Download fraction | F\_d / T | 3.0 % |
| C\_d | Drag coefficient | How strongly a shape resists a flow hitting it; about 1.2 for a flat strip broadside to the flow | 1.2 (A-012) |
| w | Arm width | Width of the arm seen from above | 8 mm (assumed, Stage 3 sets it) |
| L | Blocked length | Length of arm under the disk, R minus 5 mm hidden by the motor | 39.5 mm (A-012) |
| A | Disk area | Area swept by the propeller, pi D^2 / 4 | 6.21 x 10^-3 m^2 |
| rho | Air density | 1.225 kg/m^3 at sea level, 15 C | A-008 |
| v\_i | Induced velocity | Speed of the air passing through the propeller disk | Chapter 3 |
| kappa | Wake factor | Speed of the jet at the arm divided by v\_i | 1.4 (band 1.2 to 1.6) |

**Step 1: drag on the arm.** The force of a flow on a flat plate is the dynamic pressure times the plate area times C\_d:

```latex
F_d = \tfrac{1}{2} \rho V^2 C_d \, w L
```

**Step 2: the jet speed V.** Chapter 3 shows that the air passes through the disk at v\_i and keeps accelerating below it, reaching 2 v\_i far downstream. It also shows that v\_i^2 = T / (2 rho A). The arm sits just below the disk, so the jet there is between v\_i and 2 v\_i. We take V = kappa v\_i with kappa = 1.4, and carry 1.2 to 1.6 as the uncertainty.

**Step 3: substitute.**

```latex
F_d = \tfrac{1}{2} \rho \kappa^2 \frac{T}{2 \rho A} C_d \, w L \quad\Rightarrow\quad f = \frac{F_d}{T} = \frac{C_d \, \kappa^2 \, w L}{4A}
```

Density and thrust cancel. The download fraction depends only on how much of the disk the arm blocks (w L / A), the arm's shape (C\_d) and the jet speed factor (kappa). It is the same percentage at hover and at full throttle.

**Step 4: numbers.**

f = 1.2 x 1.4^2 x (0.008 x 0.0395) / (4 x 6.21 x 10^-3) = **3.0 %** (N-02-03). With kappa = 1.2 it is 2.2 %, with kappa = 1.6 it is 3.9 %.

**Step 5: corrected hover thrust.** Each rotor must satisfy T - F\_d = W / 4, so T (1 - f) = W / 4:

```latex
T = \frac{W}{4\,(1 - f)}
```

T = 62.5 / 0.970 = **64.4 g = 0.632 N** per rotor (N-02-04).

### Where the two values come from

| Value | Source | Includes download? |
| --- | --- | --- |
| 62.5 g | Context file, written before Stage 2 | No |
| 64.4 g | Journal, Stage 2 (N-02-04) | Yes, 3 % |

From here on every number uses 64.4 g.

Correction: the journal writes N-02-04 as AUW / 4 x (1 + f). The exact form is AUW / 4 / (1 - f). At f = 3 % both give 64.4 g, so the register value stands; the formula should be corrected.

### Why download matters to the frame

Download makes arm width a design variable with a cost. A wider arm is stiffer but blocks more of the jet, so each rotor works harder and the battery drains faster. Chapter 6 puts a number on it: 1 mm of extra width on all four arms costs about as much flight time as 0.9 g of extra frame mass.

### Next

Hover thrust per rotor: 64.4 g. The next question is how fast the propeller must spin to make it.

## Chapter 2: How fast the propeller must spin

The propeller must spin at 14,440 RPM to make 64.4 g. This comes from one law, thrust proportional to speed squared, checked against the bench data.

### The question

The flight controller sets motor speed. We know the thrust we need. We need the link between the two: thrust as a function of speed.

We can't calculate it from blade geometry: the blades are small, twisted and curved, and their airflow is hard to predict. Instead we find the **form** of the law from physics and the **constant** from the bench data.

### The propeller is a rotating wing

Each blade section is a small wing. A wing in a flow makes lift:

```latex
L = \tfrac{1}{2} \rho V^2 S \, C_L
```

L is lift (N), V the air speed over the wing (m/s), S its area (m^2), C\_L the lift coefficient (depends on shape and angle, not on size or speed). Lift is dynamic pressure, 0.5 rho V^2, times area times a shape factor.

On a propeller, the speed of a blade section is omega x r: it grows from zero at the hub to the maximum at the tip. The lift of all the sections, added up and pointing along the shaft, is the thrust.

Scaling argument: every speed on the blade is proportional to the tip speed, which is proportional to n D. Every area is proportional to D^2. So:

```latex
T \propto \rho \, (nD)^2 \, D^2 = \rho \, n^2 D^4
```

Double the speed: 4 times the thrust. Double the diameter at the same speed: 16 times.

### Variables

| Symbol | Name | What it is | Unit | Our value |
| --- | --- | --- | --- | --- |
| T | Thrust | Axial force of one propeller | N | 0.632 hover |
| n | Rotational speed | Revolutions per second, RPM / 60 | rev/s | 240.7 hover |
| omega | Angular speed | 2 pi n | rad/s | 1512 hover |
| D | Diameter | Tip to tip | m | 0.0889 |
| R | Radius | D / 2 | m | 0.0445 |
| rho | Air density |  | kg/m^3 | 1.225 |
| V | Axial speed | Speed of the aircraft along the shaft axis; zero in hover | m/s | 0 |
| mu | Dynamic viscosity | Air's resistance to shearing | Pa s | 1.81 x 10^-5 |
| nu | Kinematic viscosity | mu / rho | m^2/s | 1.48 x 10^-5 |
| a | Speed of sound |  | m/s | 343 |
| c | Blade chord | Width of the blade, leading to trailing edge | m | about 0.008 at 0.75 R (assumed, to measure) |
| C\_T | Thrust coefficient | Thrust made dimensionless; a property of the propeller shape | - | 0.1425 |

### Making the scaling argument rigorous: Buckingham pi

**What the theorem says** (Buckingham, 1914). If a physical law involves k variables built from r base dimensions, it can be rewritten as a law between k - r dimensionless groups.

**Step 1: what can thrust depend on?** We study one specific propeller, the Gemfan 3520, with its own shape: airfoil, twist, how the chord changes along the blade, number of blades, and pitch-to-diameter ratio. The shape doesn't change during the analysis, so these are **not variables**: they are fixed, and their effect is built into the unknown function f. That is why they don't appear in the list. What remains are the quantities that can change between operating conditions:

T = f(rho, n, D, V, mu, a)

Why keep D if our propeller has a fixed diameter? Because all the shape parameters above are ratios or angles (pitch / D, chord / D, twist). "Same shape" therefore describes a whole family of geometrically similar propellers of any size, and D is the one length that says how big it is. The law we derive holds for that whole family; for our propeller D is simply a known constant.

**Step 2: count.** 7 variables. Base dimensions: mass M, length L, time t, so r = 3. That leaves 4 groups.

**Step 3: pick repeating variables** that together contain M, L and t: rho (contains M), D (contains L), n (contains t).

**Step 4: build the thrust group.** Find exponents so that T / (rho^x n^y D^z) has no units. T has units kg m s^-2, rho kg m^-3, n s^-1, D m.

- Mass: 1 = x
- Time: -2 = -y, so y = 2
- Length: 1 = -3x + z, so z = 4

```latex
C_T = \frac{T}{\rho \, n^2 D^4}
```

The same method with the other variables gives:

| Group | Formula | Meaning |
| --- | --- | --- |
| C\_T | T / (rho n^2 D^4) | Thrust coefficient |
| J | V / (n D) | Advance ratio: how far the propeller moves forward per turn, in diameters |
| Re | rho n D^2 / mu | Reynolds number: inertia against viscosity |
| M | n D / a | Mach number: speed against the speed of sound |

**Step 5: the result.**

```latex
C_T = f(J, \, Re, \, M)
```

The theorem does not give f. It only says: if J, Re and M stay the same, C\_T stays the same. Then thrust follows T = C\_T rho n^2 D^4 exactly.

### Do J, Re and M stay the same?

**J.** In hover V = 0, so J = 0. A bench test is also at V = 0. The bench data describes hover directly.

**Mach number.** The fastest part of the blade is the tip, at V\_tip = pi D n.

| Point | RPM | Tip speed (m/s) | Tip Mach |
| --- | --- | --- | --- |
| Hover | 14,440 | 67 | 0.20 |
| Full throttle | 40,750 | 190 | 0.55 |

Below about 0.3 air behaves as incompressible. Up to about 0.6 to 0.7 at the tip, compressibility effects are small. Hover is far from them; full throttle is near the start of the range where they begin.

**Reynolds number.** It measures whether viscosity matters. At high Re, the boundary layer on the blade is thin and the wing works well. At low Re, the boundary layer is thick, separates early and drag rises: the blade makes less lift for more drag.

The Buckingham form, rho n D^2 / mu, is a valid group but no part of the blade actually sees it. Aerodynamicists use the blade section version, at 75 % radius as a representative station:

```latex
Re_{0.75} = \frac{\omega \, (0.75R) \, c}{\nu}
```

| Point | RPM | Re at 0.75 R |
| --- | --- | --- |
| Hover | 14,440 | about 27,000 |
| Lowest bench point (20 %) | 17,311 | about 33,000 |
| Full throttle | 40,750 | about 77,000 |

These use an assumed chord of 8 mm. Re is proportional to RPM, so the ratios are exact even if the chord changes: the bench data spans a factor of 2.35 in Re, and hover sits 1.2 times below the lowest point.

This is low: airfoils lose performance quickly below about 100,000. So of the three groups, Re is the only one that can make C\_T at hover differ from the bench.

### Why T / RPM^2 must be constant if C\_T is constant

The bench table gives thrust and RPM, not C\_T. So we need a test of "C\_T is constant" that uses only those two columns.

Start from the definition of C\_T, rearranged for thrust:

```latex
T = C_T \, \rho \, n^2 D^4
```

Now look at which factors can change between the five rows of the table:

- D: same propeller in every row, so fixed.
- rho: same bench, same air, same session. We assume it doesn't change between rows.
- C\_T: constant if the law holds. This is what we want to test.
- n: changes from row to row. It is the only thing the throttle changes.

So if the law holds, the product C\_T rho D^4 is one fixed number. Call it K:

```latex
T = K \, n^2
```

The table uses RPM, not rev/s. Since RPM = 60 n, n^2 = RPM^2 / 3600, and:

```latex
T = \frac{K}{3600} \, \mathrm{RPM}^2 = k \, \mathrm{RPM}^2 \quad\Rightarrow\quad \frac{T}{\mathrm{RPM}^2} = k
```

k is just K / 3600, kept in bench units (grams and RPM). The logic also works backwards: D and rho don't change between rows, so if T / RPM^2 changes from row to row, C\_T must be changing. Computing T / RPM^2 for each row is therefore a direct test of C\_T, and it doesn't even need the value of rho.

### The test

For each row: square the RPM, then divide the thrust by it. First row: 17,311.1^2 = 2.997 x 10^8, and 91.2 / 2.997 x 10^8 = 3.043 x 10^-7 g/RPM^2.

| Throttle | RPM | RPM^2 | Thrust (g) | k = T / RPM^2 (g/RPM^2) |
| --- | --- | --- | --- | --- |
| 20 % | 17,311 | 2.997 x 10^8 | 91.2 | 3.043 x 10^-7 |
| 40 % | 25,612 | 6.560 x 10^8 | 202.2 | 3.083 x 10^-7 |
| 60 % | 30,693 | 9.420 x 10^8 | 292.4 | 3.104 x 10^-7 |
| 80 % | 35,220 | 1.240 x 10^9 | 380.5 | 3.068 x 10^-7 |
| 100 % | 40,750 | 1.661 x 10^9 | 514.1 | 3.096 x 10^-7 |

How to read it:

- **Size of the variation**: smallest 3.043, largest 3.104, mean 3.079 (all x 10^-7). The range is 2 % of the mean. Thrust itself changes by a factor of 5.6 over the same rows.
- **No trend**: the values go up, up, down, up. A Reynolds effect would show as a steady drift with RPM (k rising or falling row after row). This looks like measurement scatter instead.
- **Comparison**: on the old table used in rev A, the same ratio varied by a factor of 1.8 (audit item F-007). That is what a broken law, or bad data, looks like.

Conclusion: C\_T is constant within 2 % over the tested range, and Re (which changes by a factor of 2.35 over these rows) has no visible effect.

### Fitting one value of k

**Why fit.** The model needs one number for k, but the five rows give five slightly different values. We want the single k that makes the curve T = k RPM^2 pass as close as possible to all five measured points at once.

**What "close" means.** For each row i, the error (called the residual) is the measured thrust minus the thrust the curve predicts:

```latex
e_i = T_i - k \, \mathrm{RPM}_i^2
```

We can't make all five errors zero with one k, so we need a single number that measures the total misfit, then choose k to make it as small as possible.

**Least squares.** The usual measure is the sum of the squared errors:

```latex
S(k) = \sum_{i=1}^{5} e_i^2 = \sum_{i=1}^{5} \left(T_i - k \, \mathrm{RPM}_i^2\right)^2
```

Why squares: a plain sum would let positive and negative errors cancel; squares are always positive, punish large errors more than small ones, and give a smooth function of k that can be minimised with calculus. This is the standard least squares method (Gauss, Legendre).

**Through the origin.** The curve has no constant term: T = k RPM^2, not T = k RPM^2 + b. Physically, a propeller at zero speed makes zero thrust, so the curve must pass through the point (0, 0). We impose that instead of letting the fit add an offset with no physical meaning.

**Finding the minimum.** Write x\_i = RPM\_i^2 to shorten the algebra. S(k) = sum (T\_i - k x\_i)^2 is a parabola in k that opens upwards, so its minimum is where the slope is zero:

```latex
\frac{dS}{dk} = \sum_i 2\,(T_i - k x_i)(-x_i) = 0
```

Divide by -2 and expand:

```latex
\sum_i T_i x_i - k \sum_i x_i^2 = 0 \quad\Rightarrow\quad k = \frac{\sum_i T_i \, x_i}{\sum_i x_i^2}
```

**The numbers, row by row.**

| Throttle | x = RPM^2 | T (g) | T x | x^2 |
| --- | --- | --- | --- | --- |
| 20 % | 2.9967 x 10^8 | 91.2 | 2.7330 x 10^10 | 8.980 x 10^16 |
| 40 % | 6.5595 x 10^8 | 202.2 | 1.3263 x 10^11 | 4.3027 x 10^17 |
| 60 % | 9.4204 x 10^8 | 292.4 | 2.7545 x 10^11 | 8.8744 x 10^17 |
| 80 % | 1.24042 x 10^9 | 380.5 | 4.7198 x 10^11 | 1.53864 x 10^18 |
| 100 % | 1.66057 x 10^9 | 514.1 | 8.5370 x 10^11 | 2.75749 x 10^18 |
| **Sum** |  |  | **1.7611 x 10^12** | **5.7036 x 10^18** |

k = 1.7611 x 10^12 / 5.7036 x 10^18 = **3.088 x 10^-7 g/RPM^2** (N-02-01).

**Why not just average the five ratios?** The average is 3.079 x 10^-7. Least squares gives more weight to the high-thrust rows, because their x is large. The two differ by 0.3 %, which changes the hover RPM by 0.15 %. Either choice is fine; least squares is the standard one.

**Checking the fit.** Put k back into T = k RPM^2 and compare with the measurements. Error = (predicted - measured) / measured.

| Throttle | Measured (g) | Predicted (g) | Error |
| --- | --- | --- | --- |
| 20 % | 91.2 | 92.5 | +1.46 % |
| 40 % | 202.2 | 202.5 | +0.17 % |
| 60 % | 292.4 | 290.9 | -0.52 % |
| 80 % | 380.5 | 383.0 | +0.66 % |
| 100 % | 514.1 | 512.7 | -0.27 % |

The largest error is 1.46 %, at the lowest point. The register rounds it to 1.4 %; 1.5 % is the correct rounding.

### Converting k to C\_T

k is in bench units. To get the dimensionless C\_T, undo each unit choice in turn.

**Step 1: grams to newtons.** 1 g of thrust is 9.81 x 10^-3 N:

k = 3.0877 x 10^-7 x 9.81 x 10^-3 = 3.0290 x 10^-9 N/RPM^2

**Step 2: RPM to rev/s.** T = k RPM^2 = k (60 n)^2 = 3600 k n^2, so the coefficient on n^2 is K = 3600 k:

K = 3600 x 3.0290 x 10^-9 = 1.0904 x 10^-5 N/(rev/s)^2

**Step 3: divide by rho D^4.** From T = C\_T rho D^4 n^2, C\_T = K / (rho D^4). D^4 = 0.0889^4 = 6.246 x 10^-5 m^4, and rho D^4 = 1.225 x 6.246 x 10^-5 = 7.652 x 10^-5 kg m:

C\_T = 1.0904 x 10^-5 / 7.652 x 10^-5 = **0.1425** (N-02-02)

**Unit check.** N/(rev/s)^2 divided by kg m is (kg m s^-2)(s^2) / (kg m) = no units, as a coefficient must be. ("Revolutions" are a count, not a unit.)

The value of rho enters only here. The bench air density isn't known, so this step uses the standard 1.225 kg/m^3 (assumption A-008). The test of constancy above didn't need it.

k and C\_T carry the same information. k is convenient with bench data; C\_T can be compared with other propellers and used at another air density.

### Hover speed

Invert T = k RPM^2:

```latex
\mathrm{RPM}_h = \sqrt{\frac{T_h}{k}} = \sqrt{\frac{64.4}{3.088 \times 10^{-7}}} = 14{,}440
```

**14,440 RPM**, or 240.7 rev/s (N-02-05). Without download (62.5 g) it would be 14,230 RPM.

**This is an extrapolation.** Hover is 1.2 times below the slowest bench point in speed (and Re). Since k showed no trend over a factor of 2.35 in Re, a further step of 1.2 is unlikely to change it much. That is a reasonable inference, not a proof, so it is recorded as assumption A-003 with an uncertainty of about 1 % on the hover RPM.

### Side note: ground effect

Close to the ground the jet can't spread freely, the air through the disk slows down, and the propeller makes more thrust for the same power. A classic estimate for a single rotor (Cheeseman and Bennett, 1955), with z the rotor height above the ground:

```latex
\frac{T_{IGE}}{T_{OGE}} = \frac{1}{1 - \left(R / 4z\right)^2}
```

At z = R (44 mm) the gain is 7 %; at z = 2R it is 2 %. It matters only at take-off and landing, so it is not a sizing case.

### Next

Hover speed: 14,440 RPM. It gives the hover vibration frequency (Chapter 9). The next question is how much power this costs. The bench table has a power column, but it is electrical power, which includes motor and ESC losses. Chapters 3 to 5 separate the physics from the losses.

## Chapter 3: The least power physics allows

No rotor of this size can make 64.4 g of thrust with less than 4.1 W. This floor comes from conservation of mass, momentum and energy alone, and every real power number must sit above it.

### The question

Chapter 2 gave the speed. The next question is power, because power sets current, and current sets flight time. But Chapter 2 can't answer it: the law P = C\_P rho n^3 D^5 has an unknown C\_P, and the bench power column is electrical power, which mixes the propeller with motor and ESC losses.

So we first ask a simpler question: ignoring every loss, what is the minimum power needed to make this thrust with a rotor of this size? That minimum gives:

1. A **floor**: any estimate below it is impossible.
2. A **yardstick**: real power divided into ideal power measures how good the system is.
3. The **form** of the power law: how power grows with thrust and mass.

### The physical idea

To push the aircraft up, the rotor must push air down. Newton's third law: the force on the air equals the force on the rotor.

- **Thrust** is the rate at which the rotor gives downward momentum to the air: mass of air per second times the speed given to it.
- **Power** is the rate at which it gives kinetic energy to the air: half the mass per second times that speed squared.

Momentum grows with speed, energy with speed squared. So the cheap way to make thrust is to move a lot of air slowly. A large rotor touches more air, so it can move it more slowly for the same thrust. That is why big rotors hover efficiently, and the whole chapter is this idea made exact.

### The model: the actuator disk

The propeller is replaced by an **actuator disk**: an infinitely thin disk with the same area as the propeller, which raises the pressure of the air passing through it. It has no blades, so it can only represent what any rotor must do, not how a particular one does it.

**Assumptions**, each one a reason the real rotor needs more power:

1. The pressure jump and the air speed are **uniform** over the disk. (Real blades load the air unevenly.)
2. **No swirl**: the air is not set spinning. (A real propeller twists its wake, and that rotation is wasted energy.)
3. **No tip losses**: no air leaks around the blade tips. (Real tips shed vortices.)
4. **No viscosity**: no friction drag on the blades. (For small propellers this is the largest real loss.)
5. Incompressible, steady flow, in **hover**: the air far above the rotor is at rest.
6. One **isolated** rotor: the other three rotors and the frame are ignored here.

### Variables

| Symbol | Name | What it is | Unit | Hover / full throttle |
| --- | --- | --- | --- | --- |
| T | Thrust | Force from one rotor | N | 0.632 / 5.04 |
| A | Disk area | Area swept by the propeller, pi D^2 / 4 | m^2 | 6.21 x 10^-3 |
| rho | Air density |  | kg/m^3 | 1.225 |
| v\_i | Induced velocity | Speed of the air as it passes **through** the disk, caused by the rotor | m/s | 6.45 / 18.2 |
| w | Wake velocity | Speed of the air **far below** the rotor, once the jet is fully developed | m/s | 12.9 / 36.4 |
| m\_dot | Mass flow | Mass of air passing through the disk each second | kg/s | 0.049 / 0.139 |
| p\_inf | Ambient pressure | Pressure far from the rotor | Pa | cancels out |
| p\_1, p\_2 | Disk pressures | Pressure just above and just below the disk | Pa | cancels out |
| P\_ideal | Ideal power | Minimum power to make T | W | 4.1 / 91.8 |
| DL | Disk loading | Thrust per disk area, T / A | N/m^2 | 102 / 812 |

### Derivation

Follow the air that ends up passing through the disk. It forms a tube (a streamtube) that is wide far above the rotor and narrow far below it. Four stations along it:

| Station | Where | Air speed | Pressure |
| --- | --- | --- | --- |
| 0 | Far above | 0 | p\_inf |
| 1 | Just above the disk | v\_i | p\_1 |
| 2 | Just below the disk | v\_i | p\_2 |
| 3 | Far below, in the wake | w | p\_inf |

Two things in this table need justifying. The speed is the same at 1 and 2 because the disk is infinitely thin: the same mass per second passes through the same area, so it can't change speed across it. The pressure at 3 is back to ambient because far below, the jet is surrounded by still air at p\_inf, and a free jet can't hold a different pressure from the air around it.

**Step 1: mass conservation.** The mass of air crossing the disk each second is density times area times speed:

```latex
\dot m = \rho A v_i
```

**Step 2: momentum.** Newton's second law applied to the air: force equals rate of change of momentum. The air starts at rest (station 0) and leaves at w (station 3), so each second the rotor gives it m\_dot times w of momentum:

```latex
T = \dot m \, (w - 0) = \rho A v_i \, w
```

**Step 3: Bernoulli above the disk.** Bernoulli's equation (pressure plus 0.5 rho V^2 is constant along a streamline) holds wherever no energy is added. Between stations 0 and 1 nothing adds energy:

```latex
p_\infty = p_1 + \tfrac12 \rho v_i^2
```

**Step 4: Bernoulli below the disk.** Between 2 and 3 nothing adds energy either:

```latex
p_2 + \tfrac12 \rho v_i^2 = p_\infty + \tfrac12 \rho w^2
```

Bernoulli can't be applied **across** the disk, from 1 to 2, because that is where the rotor adds energy. That is why it is used twice, once on each side.

**Step 5: the pressure jump.** Subtract Step 3 from Step 4. The v\_i terms and p\_inf cancel:

```latex
p_2 - p_1 = \tfrac12 \rho w^2
```

The thrust is that pressure difference acting on the disk area:

```latex
T = (p_2 - p_1) A = \tfrac12 \rho A w^2
```

**Step 6: combine.** Steps 2 and 5 are two expressions for the same thrust:

```latex
\rho A v_i w = \tfrac12 \rho A w^2 \quad\Rightarrow\quad w = 2 v_i
```

The air reaches half of its final speed at the disk. The other half is gained below it, as the pressure falls from p\_2 back to ambient. This is the result used in Chapter 1 for arm download: the arm, just under the disk, sits in air moving between v\_i and 2 v\_i.

**Step 7: thrust in terms of v\_i.** Put w = 2 v\_i into Step 2:

```latex
T = 2 \rho A v_i^2 \quad\Rightarrow\quad v_i = \sqrt{\frac{T}{2 \rho A}}
```

**Step 8: power.** Power is the kinetic energy given to the air each second. The air leaves at w, so:

```latex
P_{ideal} = \tfrac12 \dot m \, w^2 = \tfrac12 (\rho A v_i)(2 v_i)^2 = 2 \rho A v_i^3 = T \, v_i
```

(The last step uses T = 2 rho A v\_i^2 from Step 7.) Substituting v\_i from Step 7:

```latex
P_{ideal} = T \, v_i = \frac{T^{3/2}}{\sqrt{2 \rho A}}
```

**Side result: the wake contracts.** The same mass flow passes through the disk at v\_i and the far wake at 2 v\_i, so the wake area is A / 2 and its radius is R / sqrt(2), about 0.71 R.

### Reading the result

- **P\_ideal = T v\_i**: power is thrust times the speed of the air through the disk. Less v\_i for the same thrust means less power.
- **Disk loading.** Dividing Step 7 by A: v\_i = sqrt(DL / 2 rho). Thrust and area enter only as their ratio, T / A. Watts per newton of thrust equal v\_i in m/s. Low disk loading means efficient hover.
- **Power against thrust**: P \~ T^1.5. Twice the thrust needs 2.83 times the power.
- **Power against size**: P \~ 1 / sqrt(A) \~ 1 / D at fixed thrust. A bigger propeller needs less power. (Chapter 2's scaling law gives the same 1 / D dependence when speed is eliminated between thrust and power.)
- **Power against air density**: P \~ 1 / sqrt(rho). Hot or high air costs more power.

### Numbers

2 rho A = 2 x 1.225 x 6.207 x 10^-3 = 0.01521 kg/m.

**Hover**, T = 64.4 g = 0.632 N:

- v\_i = sqrt(0.632 / 0.01521) = **6.45 m/s**
- w = 12.9 m/s
- m\_dot = 1.225 x 6.207 x 10^-3 x 6.45 = 0.049 kg/s, about 40 litres of air per second through each rotor
- P\_ideal = 0.632 x 6.45 = **4.1 W** per rotor, 16.3 W for the aircraft
- DL = 0.632 / 6.207 x 10^-3 = **102 N/m^2**

**Full throttle**, T = 514.1 g = 5.04 N:

- v\_i = sqrt(5.04 / 0.01521) = **18.2 m/s**
- P\_ideal = 5.04 x 18.2 = **91.8 W**
- DL = **812 N/m^2**

8 times the thrust needs 22.5 times the ideal power, because 7.98^1.5 = 22.5.

Correction: earlier messages and register entry N-02-25 give hover v\_i = 6.35 m/s, P\_ideal = 3.9 W and DL = 99 N/m^2. Those are for 62.5 g, without download. With the register's own hover thrust (N-02-04, 64.4 g) the values are 6.45 m/s, 4.1 W and 102 N/m^2.

### The same calculation for every bench row

This is what Chapters 4 and 5 use. For each row, the ideal power for its thrust:

| Throttle | Thrust (N) | v\_i (m/s) | P\_ideal (W) | P\_elec measured (W) |
| --- | --- | --- | --- | --- |
| 20 % | 0.895 | 7.67 | 6.9 | 25.9 |
| 40 % | 1.984 | 11.42 | 22.7 | 76.6 |
| 60 % | 2.868 | 13.73 | 39.4 | 127.6 |
| 80 % | 3.733 | 15.67 | 58.5 | 182.5 |
| 100 % | 5.043 | 18.21 | 91.8 | 277.8 |

The real system needs 3 to 4 times the ideal power. Chapter 4 explains where the rest goes.

### Where the theory breaks down

| Assumption | Reality | Effect |
| --- | --- | --- |
| Uniform inflow | Inflow is stronger outboard, weak near the hub | More induced power |
| No swirl | The wake rotates | Wasted kinetic energy |
| No tip loss | Tip vortices shrink the effective disk | More induced power |
| No viscosity | Blade friction drag, large at low Reynolds number | Profile power, the largest loss for small propellers |
| Isolated rotor | Four rotors and a frame | Download (Chapter 1) and rotor interaction |
| Hover | Climb, descent, forward flight | Different flow; in fast descent the rotor meets its own wake (vortex ring state) and the theory has no valid solution |

### Next

Ideal hover power: 4.1 W per rotor. The real number is several times larger. Chapter 4 breaks the gap into propeller, motor and ESC losses.

## Chapter 4: Where the real power goes

**Where we are.** Chapter 3 gave the least power physics allows: 4.1 W per rotor in hover, 91.8 W at full throttle. The bench shows the battery supplying 3 to 4 times more. This chapter explains the gap, but only as far as the frame needs it.

The frame needs three things from it:

1. **The torque each motor puts on its arm.** It is a load case for Stage 4.
2. **Why efficiency falls at light load.** Chapter 5 needs this to estimate hover power.
3. **Why the bench current at part throttle can't be used to compute torque.** This is the second half of the chapter.

The deeper mechanisms (how the motor makes torque, how the ESC switches) are in Appendix A for reference.

### 4.1 Three converters in a row

Power travels from the battery to the air through three devices in series:

- The **ESC** (electronic speed controller) takes power from the battery and feeds it to the motor at the right level.
- The **motor** turns that electrical power into torque on the shaft.
- The **propeller** turns the shaft power into a downward jet of air.

Each one loses part of what it receives. If we call the fraction each passes on its efficiency, the power that finally reaches the air in the ideal, useful form is the battery power multiplied by all three:

```latex
P_{ideal} = P_{elec} \times \eta_{ESC} \times \eta_m \times \mathrm{FoM}
```

Here P\_elec is the electrical power drawn from the battery, eta\_ESC and eta\_m are the ESC and motor efficiencies, and FoM is the propeller's efficiency, called figure of merit (4.2).

The bench gives P\_elec. Chapter 3 gives P\_ideal for each row. So we can measure the **product** of the three efficiencies, although not each one on its own:

| Throttle | Thrust (g) | P\_ideal (W) | P\_elec (W) | Product P\_ideal / P\_elec |
| --- | --- | --- | --- | --- |
| 20 % | 91.2 | 6.9 | 25.9 | 0.265 |
| 40 % | 202.2 | 22.7 | 76.6 | 0.296 |
| 60 % | 292.4 | 39.4 | 127.6 | 0.309 |
| 80 % | 380.5 | 58.5 | 182.5 | 0.320 |
| 100 % | 514.1 | 91.8 | 277.8 | 0.331 |

(N-02-14.) Keep one thing from this table: **the product falls steadily as the load falls.** Section 4.6 explains why, and Chapter 5 relies on it.

### 4.2 The propeller's share: figure of merit

The figure of merit is the propeller's efficiency:

```latex
\mathrm{FoM} = \frac{P_{ideal}}{P_{shaft}}
```

P\_shaft is the mechanical power the motor delivers to the propeller shaft. P\_ideal is the minimum from Chapter 3. So FoM is the share of the shaft power that does the one useful thing: pushing air straight down, evenly over the disk. A perfect propeller would have FoM = 1.

The rest of the shaft power is lost in four ways, each one an assumption of Chapter 3 that the real propeller breaks:

- **Blade friction drag.** The blades are dragged through the air and lose energy to friction. For small propellers this is the biggest loss.
- **Uneven inflow.** The blades push the air harder near the tips than near the hub. Uneven pushing costs more energy than even pushing for the same thrust.
- **Swirl.** The propeller sets the wake spinning, and that rotation is wasted energy.
- **Tip losses.** Air leaks around the blade tips from the high-pressure side to the low-pressure side.

**Typical values.** Full-size helicopter rotors reach 0.7 to 0.8. Small propellers like ours reach 0.4 to 0.6 (literature range, not measured for our propeller). The difference is mostly friction drag: at our low Reynolds number (about 27,000, Chapter 2) the blade airfoil works poorly, as explained in Chapter 2.

Appendix A.1 derives the friction-drag power from first principles.

### 4.3 The motor in one idea: torque is proportional to current

Inside the motor, permanent magnets sit next to coils of copper wire. When current flows through the coils, the magnetic field pushes on them, and that push turns the shaft. More current gives a proportionally larger push.

So the torque on the shaft is proportional to the current through the motor:

```latex
\tau = K_t \, I
```

Here tau is the torque (N m), I is the current (A), and K\_t is the **torque constant** (N m per A). K\_t depends only on how the motor is built: its magnets, its size and how many turns of wire it has. For a given motor it is a fixed number.

The datasheet doesn't give K\_t directly. It gives **Kv**, so we need the link between the two.

### 4.4 Where K\_t comes from: the Kv on the label

**A motor is also a generator.** If you spin a motor by hand, the magnets moving past the coils produce a voltage. This voltage, called the **back-EMF** E, is proportional to the speed of rotation. It is present whenever the motor turns, including when it is driving the propeller.

**What Kv means.** Connect a motor with no propeller to a battery. It speeds up until the voltage it generates almost equals the battery voltage. At that point there is almost no voltage left to push current through the coils, so there is almost no torque, and the motor stops accelerating. The no-load speed is therefore set by the voltage. Kv is that relation: RPM per volt of generated voltage. Our motor is 3800 Kv. In equation form, the generated voltage at a given speed is:

```latex
E = \frac{\mathrm{RPM}}{K_v}
```

**The same relation in SI units.** Physics formulas use rad/s, not RPM. Written with the angular speed omega, the relation becomes a simple proportionality with a constant we call K\_e:

```latex
E = K_e \, \omega
```

To find K\_e from Kv, we convert RPM to rad/s. One revolution is 2 pi radians and one minute is 60 seconds, so:

```latex
\omega = \frac{2\pi}{60} \, \mathrm{RPM} \qquad \text{which means} \qquad \mathrm{RPM} = \frac{60}{2\pi} \, \omega
```

Putting this RPM into the label relation E = RPM / Kv:

```latex
E = \frac{60}{2\pi K_v} \, \omega
```

This has exactly the form E = K\_e omega. So the constant in front of omega is K\_e:

```latex
K_e = \frac{60}{2\pi K_v}
```

**Why K\_t equals K\_e.** Think of an ideal motor with no losses. All the electrical power it converts becomes mechanical power. Electrical power is voltage times current, and the voltage being converted is E. Mechanical power is torque times angular speed. So:

```latex
E \, I = \tau \, \omega
```

Now replace E with K\_e omega (from above) and tau with K\_t I (from 4.3):

```latex
K_e \, \omega \, I = K_t \, I \, \omega
```

The I and omega appear on both sides and cancel, leaving K\_e = K\_t. The two constants are the same number: one describes the motor seen as a generator (volts per rad/s), the other the motor seen as a torque producer (N m per amp). Therefore:

```latex
K_t = \frac{60}{2\pi K_v}
```

**Our number.** With Kv = 3800:

```latex
K_t = \frac{60}{2\pi \times 3800} = 2.513 \times 10^{-3} \ \text{N m/A}
```

Each amp through the motor produces 2.5 mN m of torque.

### 4.5 Internal losses: the no-load current

Not all of the torque K\_t I reaches the propeller. Part of it is used up inside the motor, mainly by:

- **Bearing friction** and air drag on the spinning bell.
- **Magnetic losses in the stator iron.** The iron core is magnetised back and forth thousands of times per second and warms up a little each time.

The datasheet measures these losses by spinning the motor **without a propeller**. Then there is no load on the shaft, so all the current drawn goes into internal losses. That current is the **no-load current** I\_0. For our motor it is 0.8 A, measured at 10 V.

The model treats this as a slice of the current that never reaches the shaft: the first I\_0 amps only cover the internal losses, and the rest makes useful torque. So the torque formula of 4.3 becomes:

```latex
\tau = K_t \, (I - I_0)
```

**At what speed was I\_0 measured?** At 10 V with no load, the motor spins at roughly Kv x 10 V, a little below 38,000 RPM because some voltage is still lost in the wires; about 37,000 RPM. That is close to full throttle (40,750 RPM). Since these losses grow with speed, I\_0 = 0.8 A is a fair value near full throttle, and too high for hover.

### 4.6 Full-throttle torque: the number for Stage 4

**The calculation.** At 100 % throttle the bench measured 16.8 A. Taking away the 0.8 A spent on internal losses leaves 16.0 A of useful current:

```latex
\tau = K_t \, (I - I_0) = 2.513 \times 10^{-3} \times (16.8 - 0.8) = 0.040 \ \text{N m}
```

This is the maximum torque each motor applies to the propeller (N-02-17).

**Why we can use the bench current here.** At full throttle the ESC connects the battery straight to the motor, so the current measured at the battery is the motor current. At part throttle this is no longer true, which is the subject of the second half of this chapter.

**A check with power.** If the torque is right, the shaft power must make sense. The angular speed at 40,750 RPM is:

```latex
\omega = \frac{2\pi}{60} \times 40{,}750 = 4267 \ \text{rad/s}
```

So the shaft power is:

```latex
P_{shaft} = \tau \, \omega = 0.040 \times 4267 = 172 \ \text{W}
```

The battery supplies 277.8 W, so the motor and ESC together pass on 172 / 277.8 = 0.62 of it. The propeller's figure of merit is then:

```latex
\mathrm{FoM} = \frac{P_{ideal}}{P_{shaft}} = \frac{91.8}{172} = 0.535
```

(N-02-15.) This is inside the 0.4 to 0.6 range expected for small propellers. Two independent pieces (the motor torque formula and momentum theory) agree, which supports the 0.040 N m.

**What the frame does with it.** Newton's third law: the motor pushes the propeller round with 0.040 N m, and the propeller pushes back on the motor, and through the motor mount on the arm, with the same torque in the opposite direction. This reaction torque acts about the motor axis, so it bends the arm sideways, in the plane of the frame. The two clockwise and two counter-clockwise motors load their arms in opposite directions.

For scale: with an arm about 80 mm long (assumed, close to the Volador), full thrust bends the arm root with 5.04 x 0.08 = 0.40 N m. The reaction torque is ten times smaller, but it acts in a different plane, where a flat printed arm may be less stiff, so it stays in the Stage 4 load set.

### 4.7 Why efficiency falls at light load

This is the result Chapter 5 needs. Look again at where the power goes and how each part changes as the motor slows down.

**Useful power falls fast.** The propeller's power grows with speed cubed (Chapter 2). Going from full throttle to hover, the speed falls from 40,750 to 14,440 RPM, a factor of 2.82. Speed cubed falls by:

```latex
2.82^3 = 22.5
```

So the useful power at hover is about 22 times smaller than at full throttle.

**Internal losses fall slowly.** Bearing friction and the magnetic losses grow roughly in proportion to speed, so they only fall by a factor of about 2.8. The ESC's own electronics use a small constant power that doesn't fall at all.

**A rough illustration** (it assumes exactly these scalings, so it only shows the trend). At full throttle the internal losses are about 0.8 A x 10.7 V = 8.6 W (0.8 A is the no-load current I\_0 of 4.5; 10.7 V is the back-EMF at full throttle, E = 40,750 / 3800 from 4.4; the converted power is E x I, and the slice I\_0 of the current goes to internal losses, so those losses are E x I\_0), against 172 W of shaft power: about 5 %. At hover speed, shaft power is about 172 / 22.5 = 7.6 W, while internal losses are about 8.6 / 2.8 = 3.0 W, around 40 % of it. The same losses that were negligible at full throttle become a large share at hover.

**The propeller gets worse too.** At lower speed the Reynolds number is lower, the blades' friction drag is relatively larger, and the figure of merit drops.

Both effects push the same way, and both get stronger as load falls. That is why the product of the three efficiencies in 4.1 falls from 0.331 to 0.265, and why it must **keep falling** below the lowest bench point. Chapter 5 uses exactly this as its test.

### 4.8 The problem at part throttle

Section 4.6 computed torque from the bench current at full throttle. Try the same at 20 % throttle, where the bench measured 17,311 RPM and 1.5 A.

The torque formula gives:

```latex
\tau = K_t \, (I - I_0) = 2.513 \times 10^{-3} \times (1.5 - 0.8) = 1.76 \times 10^{-3} \ \text{N m}
```

The angular speed is:

```latex
\omega = \frac{2\pi}{60} \times 17{,}311 = 1813 \ \text{rad/s}
```

So the shaft power would be:

```latex
P_{shaft} = \tau \, \omega = 1.76 \times 10^{-3} \times 1813 = 3.2 \ \text{W}
```

But Chapter 3 showed that this thrust (91.2 g) needs **at least 6.9 W** of ideal power. A shaft power of 3.2 W would mean a figure of merit of 6.9 / 3.2 = 2.2, a propeller more than twice as good as physically possible.

The torque formula isn't wrong. The current put into it is. To see why, we need to know how the ESC controls the motor.

### 4.9 How the ESC lowers the voltage

**What the motor needs.** At 17,311 RPM the motor generates a back-EMF of:

```latex
E = \frac{\mathrm{RPM}}{K_v} = \frac{17{,}311}{3800} = 4.6 \ \text{V}
```

To push current against that, the motor needs a voltage only a little above 4.6 V. The battery gives 16.8 V.

**How the ESC gives it.** The ESC could drop the extra 12 V across a resistor, but that would turn most of the battery's power into heat. Instead it acts as a very fast switch: it connects the battery to the motor, disconnects it, connects it again, 48,000 times per second. The fraction of each cycle during which the battery is connected is called the **duty cycle**, d, between 0 and 1. If the battery is connected 30 % of the time, d = 0.3.

**Why the motor sees the average.** The motor's windings are coils of wire, and a coil resists any change in the current through it, in the same way that a mass resists any change in its velocity. Picture pushing a heavy cart with very rapid shoves, thousands per second: the cart doesn't jerk with each shove, it moves at a steady speed set by the **average** push. In the same way, the current in the motor stays almost steady, and the motor behaves as if it were connected to the average voltage:

```latex
V_{motor} = d \times V_{battery}
```

At 20 % throttle, the motor needs a bit more than 4.6 V out of 16.8 V, so the duty cycle is at least:

```latex
d \geq \frac{4.6}{16.8} = 0.27
```

### 4.10 Why battery current and motor current differ

This follows from the cart picture.

**The motor current never stops.** Between shoves the cart keeps rolling. Between connections to the battery, the current in the motor keeps flowing too, because the coils resist any change. During the off part of each cycle it circulates through the motor and the ESC without passing through the battery.

**The battery only supplies it part of the time.** The battery is connected only for the fraction d of each cycle. So, on average, the current drawn from the battery is only that fraction of the motor current:

```latex
I_{battery} = d \times I_{motor}
```

or, turned around:

```latex
I_{motor} = \frac{I_{battery}}{d}
```

**The same result from energy.** The switch wastes almost nothing, so the power leaving the battery equals the power reaching the motor. Battery power is the battery voltage times the battery current. Motor power is the motor voltage, d x V\_battery, times the motor current:

```latex
V_{battery} \times I_{battery} = (d \times V_{battery}) \times I_{motor}
```

Dividing both sides by V\_battery gives back I\_battery = d x I\_motor.

**A mechanical analogy.** The ESC works like a gearbox. A reduction gearbox lowers speed and raises torque, keeping the power the same. The ESC lowers the voltage by the factor d and raises the current by 1/d, keeping the power the same.

**Back to 20 % throttle.** With d of about 0.27, the motor current is roughly:

```latex
I_{motor} \approx \frac{1.5}{0.27} = 5.5 \ \text{A}
```

This is a rough upper estimate, since d is a little above 0.27. The point is that the motor current is several times the 1.5 A measured at the battery. Putting the battery current into the torque formula underestimated the torque, which is why 4.8 gave an impossible result (journal lesson L-006).

**At full throttle** the battery is connected all the time, so d = 1 and the two currents are equal. That is why 4.6 could use the bench current.

### 4.11 What this means for the model

- **Torque is only computed at full throttle.** The frame only needs the maximum torque, and at full throttle the bench current is the motor current. No problem.
- **Hover power uses battery power.** The battery drains according to the **battery** current, and battery power is what the bench measures directly. Chapters 5 and 6 work with battery power throughout, so the difference between the two currents doesn't affect them.

### 4.12 Throttle % is not a physical quantity

Throttle % is the pilot's stick command. The ESC firmware turns it into a duty cycle, and the speed that results also depends on the battery voltage at that moment. Different ESCs, firmware and calibrations make different conversions: one bench gives 20 % = 10,500 RPM, ours gives 20 % = 17,311 RPM (audit item F-018).

So the model states the hover point as **thrust, RPM and current**, which are physical, never as a throttle percentage (A-006). The register's 14 % hover throttle (N-02-09) is only an indicative value for this bench.

### 4.13 Results of Chapter 4

| Result | Value | Used in |
| --- | --- | --- |
| Torque constant K\_t | 2.513 x 10^-3 N m/A | Torque calculation |
| Maximum motor torque on the arm | 0.040 N m (N-02-17) | Stage 4 loads |
| Figure of merit at full throttle | 0.535 (N-02-15) | Check of the torque value |
| Efficiency product, falling at light load | 0.331 to 0.265 on the bench | Chapter 5 test |
| Battery current is the current that matters for endurance | - | Chapters 5 and 6 |

## Chapter 5: Real hover power

**Where we are.** Chapter 2 gave the hover speed: 14,440 RPM. Chapter 3 gave the least power physics allows at that speed: 4.1 W per rotor. Chapter 4 showed that the real system needs several times more, and that its efficiency falls as the load falls. This chapter estimates the real battery power in hover, which Chapter 6 turns into flight time.

**Result.** Each motor draws about **18.3 W** in hover, with 20.2 W as a conservative bound. The aircraft draws **74 W**, which is **5.0 A** from the battery.

### 5.1 Why hover power can't be read directly

**Hover is outside the data.** Hover needs 64.4 g per motor. The lightest bench row is 91.2 g, at 17,311 RPM. There is no row at or below hover, so we can't read or interpolate the power. We have to **extrapolate**: fit a formula to the five rows and use it below them.

**Why not just scale with RPM cubed.** Chapter 2 showed that the power a propeller absorbs grows with speed cubed. If the battery power did the same, it would follow:

```latex
P = a \times \mathrm{RPM}^3
```

with a a fixed number. We can test this exactly as in Chapter 2. If the formula holds, dividing each row's power by its RPM cubed must give the same number every time:

```latex
\frac{P}{\mathrm{RPM}^3} = a
```

| Throttle | RPM | P\_elec (W) | P / RPM^3 (W/RPM^3) |
| --- | --- | --- | --- |
| 20 % | 17,311 | 25.9 | 4.99 x 10^-12 |
| 40 % | 25,612 | 76.6 | 4.56 x 10^-12 |
| 60 % | 30,693 | 127.6 | 4.41 x 10^-12 |
| 80 % | 35,220 | 182.5 | 4.18 x 10^-12 |
| 100 % | 40,750 | 277.8 | 4.11 x 10^-12 |

It isn't constant. It rises by 21 % from the fastest row to the slowest, and it rises **steadily**, row after row. That is a trend, not measurement scatter.

**What the trend means.** At low speed the battery supplies more power than speed cubed predicts. This is Chapter 4, section 4.7: some losses fall much more slowly than the propeller's power when the motor slows down, so they take a growing share at light load. The battery power is propeller power plus those losses, and the losses don't follow RPM cubed.

### 5.2 The old spreadsheet's error

The rev A spreadsheet assumed P = a x RPM^3 and took a from the full-throttle row only. On our bench data that gives:

```latex
a = \frac{P_{100\%}}{\mathrm{RPM}_{100\%}^3} = \frac{277.8}{40{,}750^3} = 4.11 \times 10^{-12} \ \text{W/RPM}^3
```

Applied at hover:

```latex
P_{hover} = a \times \mathrm{RPM}_{hover}^3 = 4.11 \times 10^{-12} \times 14{,}442^3 = 12.4 \ \text{W}
```

This is about a third below the 18.3 W found in this chapter. The reason: the full-throttle row has the **smallest** P / RPM^3 of the table, because at full throttle the slowly-falling losses are a small share. Using it carries the full-throttle efficiency down to hover, where those losses are a large share. (On the old table the same method was about 30 % low, audit item F-002.)

### 5.3 What the power formula should contain

We need a formula for battery power that includes the losses, with a term for each kind of loss according to how it changes with speed. Chapter 4 gives the ingredients.

**Propeller power: grows with RPM cubed.** This is Chapter 2. Term:

```latex
a \times \mathrm{RPM}^3
```

**Losses that grow in proportion to speed.** Two of the motor's internal losses (section 4.5) behave this way:

- **Bearing friction.** The friction torque in a bearing is roughly constant. Power is torque times angular speed, so the power lost grows in proportion to speed.
- **Magnetic losses in the iron.** Each time the iron is magnetised back and forth it loses a roughly fixed amount of energy. The number of times this happens per second is proportional to the speed, so the power lost is proportional to speed too.

Term:

```latex
b \times \mathrm{RPM}
```

**Losses that don't depend on speed.** The ESC's own electronics draw a small, roughly constant power whatever the motor does. Term:

```latex
c
```

**One loss that has no term of its own.** The current also heats the copper wire of the motor's windings, as friction heats a pipe. This loss grows with current squared, and current grows roughly with RPM squared (torque grows with RPM squared, and torque is proportional to current), so the loss grows roughly with RPM to the fourth power. It is the largest loss at full throttle and nearly negligible at hover (Appendix A.2.8 accounts for it). The fits absorb it into the a term, which therefore is not purely propeller power.

**The four candidates.** Combining the terms gives four formulas, from the simplest to the fullest:

| Model | Formula | What it assumes |
| --- | --- | --- |
| M1 | P = a RPM^3 | Only propeller power; efficiency the same at every load |
| M2 | P = a RPM^3 + c | Propeller power plus a constant loss |
| M3 | P = a RPM^3 + b RPM | Propeller power plus losses proportional to speed |
| M4 | P = a RPM^3 + b RPM + c | All three |

None of them is proven by physics. Each is a plausible shape. The bench data decides the coefficients, and a physical test (second half of this chapter) decides which shapes to trust below the data.

### 5.4 Fitting a formula with more than one coefficient

**The idea is the same as Chapter 2.** There we had one coefficient, k, and chose it to make the sum of squared errors as small as possible. Now M3 has two coefficients, a and b, and we choose both together, in the same way.

**Readable numbers.** RPM cubed gives very large numbers. To keep them readable, speed is written in **thousands of RPM**, x = RPM / 1000. So 17,311 RPM becomes x = 17.311. The coefficients change units accordingly, but the result is the same.

M3 then reads:

```latex
P = a \, x^3 + b \, x
```

To shorten the algebra, call the two columns x1 = x^3 and x2 = x:

```latex
P = a \, x_1 + b \, x_2
```

**The error of each row.** For row i, the error is the measured power minus the power the formula predicts:

```latex
e_i = P_i - a \, x_{1,i} - b \, x_{2,i}
```

**The total misfit.** As in Chapter 2, add up the squared errors of the five rows:

```latex
S(a, b) = \sum_i \left( P_i - a \, x_{1,i} - b \, x_{2,i} \right)^2
```

**Finding the minimum.** In Chapter 2, S depended on one coefficient and was a parabola; the minimum was where its slope was zero. Now S depends on two coefficients, so it is a bowl-shaped surface over the (a, b) plane. At the bottom of a bowl, the surface is flat in **both** directions. So two conditions must hold together: the slope in the a direction is zero, and the slope in the b direction is zero.

**First condition: slope in the a direction.** Differentiate S with respect to a, keeping b fixed. The derivative of each squared term is 2 times the bracket times the derivative of the bracket, which is -x1:

```latex
\frac{\partial S}{\partial a} = \sum_i 2 \left( P_i - a \, x_{1,i} - b \, x_{2,i} \right) \left( -x_{1,i} \right) = 0
```

Divide by -2 and multiply out the bracket:

```latex
\sum_i P_i \, x_{1,i} - a \sum_i x_{1,i}^2 - b \sum_i x_{1,i} \, x_{2,i} = 0
```

Move the known sum to the right:

```latex
a \sum x_1^2 + b \sum x_1 x_2 = \sum x_1 P \qquad \text{(equation 1)}
```

**Second condition: slope in the b direction.** The same steps, differentiating with respect to b, give:

```latex
a \sum x_1 x_2 + b \sum x_2^2 = \sum x_2 P \qquad \text{(equation 2)}
```

These are called the **normal equations**. All the sums come from the bench data, so they are two ordinary linear equations with two unknowns, a and b.

**The sums, row by row.**

| Throttle | x | x1 = x^3 | P (W) | x1^2 | x1 x2 | x2^2 | x1 P | x2 P |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20 % | 17.311 | 5,188 | 25.9 | 2.691 x 10^7 | 89,805 | 299.7 | 134,361 | 448.4 |
| 40 % | 25.612 | 16,800 | 76.6 | 2.822 x 10^8 | 430,269 | 656.0 | 1,286,867 | 1,961.8 |
| 60 % | 30.693 | 28,914 | 127.6 | 8.360 x 10^8 | 887,443 | 942.0 | 3,689,402 | 3,916.4 |
| 80 % | 35.220 | 43,687 | 182.5 | 1.909 x 10^9 | 1,538,642 | 1,240.4 | 7,972,897 | 6,427.6 |
| 100 % | 40.750 | 67,668 | 277.8 | 4.579 x 10^9 | 2,757,495 | 1,660.6 | 18,798,287 | 11,320.4 |
| **Sum** |  |  |  | **7.6327 x 10^9** | **5.7037 x 10^6** | **4,798.7** | **3.1882 x 10^7** | **24,074.5** |

**The two equations with numbers.**

```latex
7.6327 \times 10^9 \, a + 5.7037 \times 10^6 \, b = 3.1882 \times 10^7 \qquad \text{(1)}
```

```latex
5.7037 \times 10^6 \, a + 4{,}798.7 \, b = 24{,}074.5 \qquad \text{(2)}
```

**Solving by elimination.** To remove a, multiply equation 2 by the ratio 7.6327 x 10^9 / 5.7037 x 10^6 = 1,338.2, so its a term matches equation 1:

```latex
7.6327 \times 10^9 \, a + 6.4216 \times 10^6 \, b = 3.2217 \times 10^7 \qquad \text{(2')}
```

Subtract equation 1 from equation 2'. The a terms cancel:

```latex
(6.4216 - 5.7037) \times 10^6 \, b = (3.2217 - 3.1882) \times 10^7
```

```latex
0.7180 \times 10^6 \, b = 3.352 \times 10^5
```

```latex
b = 0.467 \ \text{W per thousand RPM}
```

Put b back into equation 1 and solve for a:

```latex
a = \frac{3.1882 \times 10^7 - 5.7037 \times 10^6 \times 0.467}{7.6327 \times 10^9} = \frac{2.922 \times 10^7}{7.6327 \times 10^9} = 3.828 \times 10^{-3} \ \text{W per (thousand RPM)}^3
```

**Back to plain RPM.** Since x = RPM / 1000, a x^3 = (a / 10^9) RPM^3 and b x = (b / 1000) RPM. So in plain RPM, a = 3.828 x 10^-12 W/RPM^3 and b = 4.67 x 10^-4 W/RPM, the values in the register.

**The other models.** M1 has one coefficient and is solved exactly as in Chapter 2. M2 is solved like M3, with a column of ones in place of x2 (the constant c multiplies 1). M4 has three coefficients, so three conditions and three normal equations. The script s02\_sizing.py solves all four the same way with a linear solver.

### 5.5 The four fits

Solving the normal equations for each model gives these coefficients (plain RPM units):

| Model | a (W/RPM^3) | b (W/RPM) | c (W) |
| --- | --- | --- | --- |
| M1 | 4.18 x 10^-12 | - | - |
| M2 | 4.00 x 10^-12 | - | +8.2 |
| M3 | 3.83 x 10^-12 | 4.67 x 10^-4 | - |
| M4 | 3.64 x 10^-12 | 1.03 x 10^-3 | -10.6 |

**How well each fits the bench.** For each row, the error is the predicted power minus the measured power, as a percentage of the measured power:

| Model | 20 % | 40 % | 60 % | 80 % | 100 % |
| --- | --- | --- | --- | --- | --- |
| M1 | -16.3 % | -8.4 % | -5.4 % | 0.0 % | +1.8 % |
| M2 | +11.7 % | -1.5 % | -2.9 % | +0.3 % | +0.5 % |
| M3 | +7.9 % | -0.4 % | -2.0 % | +0.7 % | +0.1 % |
| M4 | +0.5 % | +0.2 % | -1.2 % | +1.0 % | -0.2 % |

M4 fits best: every row within 1.2 %. M1 fits worst, because it can't follow the rising P / RPM^3 of section 5.1.

Correction: the journal's Stage 2 notes say all four models "fit the data". Only M4 does within about 1 %; M1, M2 and M3 miss the lowest row by 16 %, 12 % and 8 %.

**Hover power from each model.** Hover is 14,442 RPM, so:

```latex
\mathrm{RPM}_{hover}^3 = 14{,}442^3 = 3.012 \times 10^{12}
```

Each model's hover power is the sum of its terms at that speed:

| Model | a x RPM^3 | b x RPM | c | Hover power per motor |
| --- | --- | --- | --- | --- |
| M1 | 12.58 W | - | - | **12.6 W** |
| M2 | 12.06 W | - | +8.16 W | **20.2 W** |
| M3 | 11.53 W | 6.74 W | - | **18.3 W** |
| M4 | 10.95 W | 14.81 W | -10.57 W | **15.2 W** |

For example, M3:

```latex
P = a \times \mathrm{RPM}^3 + b \times \mathrm{RPM}
```

```latex
P = 3.828 \times 10^{-12} \times 3.012 \times 10^{12} + 4.668 \times 10^{-4} \times 14{,}442
```

```latex
P = 11.53 + 6.74 = 18.3 \ \text{W}
```

**Two things to notice.**

- Inside the bench range the models agree within a few percent. At hover, just below the range, they spread from 12.6 to 20.2 W, a factor of 1.6. A good fit inside the data says nothing about the behaviour outside it.
- The best fit is not automatically the most trustworthy. M4 has three coefficients for five points, so it has a lot of freedom to bend through the points. Fitting well is easy for it, and proves little.

So the fit quality alone can't choose. We need a test that judges each model **where we use it**, below the data.

### 5.6 The physical test

**The test comes from Chapter 4.** Section 4.1 measured the product of the three efficiencies (ESC, motor, propeller) on the bench:

```latex
\text{product} = \frac{P_{ideal}}{P_{elec}}
```

It falls from 0.331 at full throttle to 0.265 at the lightest row. Section 4.7 explained why, with two effects:

1. The losses that fall slowly with speed (friction, magnetic losses, ESC electronics) take a growing share of a shrinking output.
2. The propeller's figure of merit drops at lower Reynolds number.

Both effects get **stronger** as the load falls further. Nothing reverses them below 91 g. So below the data the product must **keep falling**.

**This gives the test.** Any model we trust must predict a product that keeps falling below the lightest row.

**How to apply it.** For a chosen thrust:

1. Find the speed from Chapter 2's thrust law, RPM = sqrt(T / k).
2. Find the ideal power from Chapter 3, P\_ideal = T x v\_i.
3. Find the battery power from the model at that speed.
4. Divide: product = P\_ideal / P\_model.

We do this at three thrusts: the lightest bench row (91.2 g), hover (64.4 g), and a lighter point (40 g) to see the direction of the trend.

| Thrust | Speed (RPM) | P\_ideal (W) |
| --- | --- | --- |
| 91.2 g | 17,186 | 6.86 |
| 64.4 g | 14,442 | 4.07 |
| 40 g | 11,382 | 1.99 |

(At 91.2 g the thrust law gives 17,186 RPM, 0.7 % below the bench's 17,311 RPM, because the fitted k is not exact at that row.)

**Model power at each thrust:**

| Model | 91.2 g | 64.4 g | 40 g |
| --- | --- | --- | --- |
| M1 | 21.2 W | 12.6 W | 6.2 W |
| M2 | 28.5 W | 20.2 W | 14.1 W |
| M3 | 27.5 W | 18.3 W | 11.0 W |
| M4 | 25.5 W | 15.2 W | 6.5 W |

**The product, P\_ideal / P\_model:**

| Model | 91.2 g (bench value: 0.265) | 64.4 g (hover) | 40 g | Trend below the data | Verdict |
| --- | --- | --- | --- | --- | --- |
| M1 | 0.324 | 0.324 | 0.324 | Flat | **Rejected** |
| M2 | 0.241 | 0.201 | 0.142 | Falling | Accepted |
| M3 | 0.250 | 0.223 | 0.182 | Falling | Accepted |
| M4 | 0.269 | 0.268 | 0.309 | Flat, then rising | **Rejected** |

**Why M1 fails.** It has only the propeller term, so its efficiency is the same at every load by construction. The bench already shows the efficiency changing, so M1 contradicts the data before we even extrapolate.

**Why M4 fails.** Its product stops falling at hover and rises below it, as if the system became more efficient at lighter load. The reason is visible in its coefficients: c = -10.6 W, a **negative** loss. Read literally, a motor standing still would return 10.6 W to the battery. The three free coefficients let M4 pass through the five points by combining a large b with a negative c, terms that roughly cancel inside the data and diverge outside it. The best-fitting model fails the physics.

**Why M2 is only a bound.** Its constant c = +8.2 W is large for what it represents: the ESC's electronics, which draw far less. (The motor's no-load power, 0.8 A at 10 V = 8 W, looks similar, but it was measured at about 37,000 RPM, section 4.5, and it is mostly friction and magnetic loss, which shrink at hover speed. It does not belong in a speed-independent term.) So M2 puts too much loss at low speed, and its hover power is high.

### 5.7 The choice

- **Central value: M3, 18.3 W per motor** (N-02-07). Both its terms have a physical meaning, it passes the test, and it fits the data better than M2.
- **Conservative bound: M2, 20.2 W per motor.**

**Check against Chapter 4.** With M3, the product at hover is:

```latex
\frac{P_{ideal}}{P_{elec}} = \frac{4.07}{18.3} = 0.22
```

That could be, for example, a propeller figure of merit of 0.45 with motor and ESC passing on 0.50. Low, but what light load and low Reynolds number lead us to expect.

**A limitation to weigh in the Q-18 review.** Both accepted models already **overpredict** the lightest bench row: M3 by 8 %, M2 by 12% (section 5.5). That row is the closest to hover. If the same bias continues below it, the true hover power is lower than 18.3 W, perhaps 15 to 18 W. This doesn't rescue M4, which fails for a physical reason. It means 18.3 W is more likely conservative than optimistic, and the endurance in Chapter 6 may come out slightly low.

### 5.8 Aircraft totals

**Total power.** Four motors, plus the flight controller, receiver and GPS (avionics, assumed 1.0 W, A-009):

```latex
P_{total} = 4 \times P_{motor} + P_{avionics}
```

```latex
P_{total} = 4 \times 18.3 + 1.0 = 74 \ \text{W}
```

With the conservative bound: 4 x 20.2 + 1.0 = 82 W.

**Total current.** Power is voltage times current, so current is power divided by voltage. At the battery's nominal voltage of 14.8 V:

```latex
I = \frac{P_{total}}{V} = \frac{74}{14.8} = 5.0 \ \text{A}
```

(N-02-08.) The battery's voltage isn't really constant during a flight; Chapter 6 deals with that.

### 5.9 Results of Chapter 5

| Result | Value | Used in |
| --- | --- | --- |
| Hover power per motor, central (M3) | 18.3 W (N-02-07) | Chapter 6 |
| Hover power per motor, conservative (M2) | 20.2 W | Chapter 6 bound |
| Aircraft hover power | 74 W (82 W bound) | Chapter 6 |
| Aircraft hover current at 14.8 V | 5.0 A (N-02-08) | Chapter 6 |
| Error of the old n^3 method | 12.4 W, a third low | Audit F-002 |

## Chapter 6: Flight time and the cost of mass

**Where we are.** Chapter 5 gave the power the aircraft draws in hover: 74 W. This chapter divides the battery's usable energy by that power to get the flight time, and then (second half) asks how much flight time each gram of frame and each millimetre of arm width costs. That cost is what the frame design trades against stiffness and strength.

**Result.** Hover flight time is **8.2 min**, with a band of 6.6 to 9.0 min.

### 6.1 What the battery is

Our pack is a Tattu R-Line V5: **4S, 850 mAh, 100 g**. Each part of that label has a physical meaning.

**The cell.** A lithium-polymer (LiPo) cell stores energy chemically and delivers it as a voltage set by its chemistry. That voltage depends on how charged the cell is:

| State | Cell voltage |
| --- | --- |
| Fully charged | 4.20 V |
| Middle of the discharge (nominal) | 3.70 V |
| Near empty, under load (where pilots usually land, practice) | about 3.5 V |

**4S: four cells in series.** Connecting cells in series (one after the other) adds their voltages. The mechanical picture: stacking water tanks on top of each other, so their pressure heads add up. For four cells:

```latex
V_{pack} = 4 \times V_{cell}
```

Nominal:

```latex
V_{pack} = 4 \times 3.70 = 14.8 \ \text{V}
```

Fully charged, 4 x 4.20 = 16.8 V. The bench table ran at 16.5 to 16.8 V, so it was measured with an almost full pack.

**850 mAh: the capacity.** Capacity is the total electric charge the pack can deliver, written in milliamp-hours. In the tank picture it is the volume of water. Current is charge per unit time, so charge is current times time:

```latex
Q = I \times t
```

850 mAh = 0.85 Ah means the pack can deliver 0.85 A for one hour, or 5.1 A for 10 minutes. Capacity alone says how long a given current can last, but not how much energy that is.

**Energy.** Power is voltage times current (Chapter 4):

```latex
P = V \times I
```

Energy is power times time:

```latex
E = P \times t = V \times I \times t
```

And current times time is the charge Q, so:

```latex
E = V \times Q
```

In the tank picture: energy is pressure times volume. With V in volts and Q in amp-hours, E comes out in watt-hours (Wh). For our pack at nominal voltage:

```latex
E = 14.8 \times 0.85 = 12.6 \ \text{Wh}
```

One watt-hour is 3600 J, so this is about 45,000 J.

### 6.2 How much of it we can use

Two corrections turn the label energy into the energy available for flight.

**The voltage changes during the flight.** The cell voltage falls from about 4.2 V to about 3.5 V as the pack empties. The energy delivered is the charge times the **average** voltage during the flight. The model uses 3.70 V per cell (A-011, band 3.6 to 3.8 V), so:

```latex
V_{avg} = 4 \times 3.70 = 14.8 \ \text{V}
```

The pack voltage also drops a little under load, because the pack has an internal resistance (Chapter 7). At the hover current of 5 A this drop is small, about 0.1 to 0.2 V with the assumed 20 to 40 milliohm pack, and it sits inside the 3.6 to 3.8 V band.

**Not all the charge is usable.** Draining a LiPo completely damages its cells permanently, and the pilot needs a reserve to land. The model uses 80 % of the capacity (A-010, band 75 to 85 %).

**Usable energy.** With f the usable fraction:

```latex
E_{usable} = f \times Q \times V_{avg}
```

```latex
E_{usable} = 0.80 \times 0.85 \times 14.8 = 10.06 \ \text{Wh}
```

Correction: the original context file and the first replies used 3.8 V per cell (15.2 V, 10.3 Wh). The register uses 3.70 V per cell (A-011), which is the nominal mid-discharge value; 15.2 V was flagged in audit item F-019.

### 6.3 Flight time

**The formula.** Flight time is the usable energy divided by the power drawn:

```latex
t = \frac{E_{usable}}{P_{total}}
```

With energy in Wh and power in W, t comes out in hours.

**Our numbers.** With the central hover power from Chapter 5 (74.1 W):

```latex
t = \frac{10.06}{74.1} = 0.136 \ \text{h}
```

```latex
t = 0.136 \times 60 = 8.2 \ \text{min}
```

(N-02-10.)

**The same result with current.** The usable charge is 0.80 x 850 = 680 mAh, and the hover current is 5.0 A (Chapter 5). From Q = I x t:

```latex
t = \frac{Q_{usable}}{I} = \frac{0.68}{5.0} = 0.136 \ \text{h} = 8.2 \ \text{min}
```

The two routes agree because both use the same 14.8 V.

### 6.4 The uncertainty band

Five inputs are uncertain. Each has a band:

| Input | Central | Pessimistic | Optimistic | Source |
| --- | --- | --- | --- | --- |
| Hover power model | M3 (18.3 W per motor) | M2 (20.2 W) | M3 | Chapter 5 |
| Usable fraction | 80 % | 75 % | 85 % | A-010 |
| Average cell voltage | 3.70 V | 3.60 V | 3.80 V | A-011 |
| Avionics power | 1.0 W | 1.5 W | 0.5 W | A-009 |
| Download wake factor kappa | 1.4 | 1.6 | 1.2 | A-012, Chapter 1 |

Setting every input to its pessimistic value at once gives **6.6 min**. Setting every input to its optimistic value gives **9.0 min**. With only the power model changed to M2, the time is 7.4 min.

This band is wide on purpose: it assumes every input is wrong in the same direction at the same time, which is unlikely. It is a bound, not a typical spread. And Chapter 5 found that M3 probably overestimates hover power, so the true time is more likely in the upper half of the band than the lower.

Correction: the earlier 8 to 11 min band (context file, Stage 1) came from all four power models, including the two that Chapter 5 rejects, and from 3.8 V per cell. Removing both gives 6.6 to 9.0 min (journal lesson L-007).

### 6.5 What a gram of frame costs

**The chain.** Adding mass to the frame sets off a chain of effects:

1. More mass means each motor must make more thrust.
2. More thrust means each propeller must spin faster.
3. Faster spinning means more power.
4. More power from the same battery means less flight time.

We follow a small mass increase through each step.

**A tool for small changes.** If a quantity y depends on x as a power, y = x^n, and x grows by a small fraction epsilon, then:

```latex
(1 + \varepsilon)^n \approx 1 + n \, \varepsilon
```

So y grows by the fraction n times epsilon. For example, if x grows by 1 %, x^3 grows by about 3 % and the square root of x by about 0.5 %. This approximation is accurate when epsilon is small, which it is here (1 g on 250 g is 0.4 %).

**Step 1: thrust.** From Chapter 1, each motor's thrust is proportional to the aircraft weight:

```latex
T = \frac{m g}{4 (1 - f)}
```

So if the mass grows by a fraction epsilon, the thrust grows by the same fraction epsilon.

**Step 2: speed.** From Chapter 2, thrust grows with speed squared, so speed grows with the square root of thrust:

```latex
\mathrm{RPM} = \sqrt{T / k}
```

A square root is a power of 1/2, so the speed grows by epsilon / 2.

**Step 3: power.** The hover power of one motor is the M3 formula from Chapter 5. Its two terms at hover are:

```latex
P_{motor} = a \times \mathrm{RPM}^3 + b \times \mathrm{RPM} = 11.53 + 6.74 = 18.27 \ \text{W}
```

With the speed growing by epsilon / 2:

- The RPM cubed term grows by 3 x (epsilon / 2) = 1.5 epsilon, so by 1.5 epsilon x 11.53 W.
- The RPM term grows by epsilon / 2, so by 0.5 epsilon x 6.74 W.

Adding the two and dividing by the motor's power gives its relative growth:

```latex
\frac{\Delta P_{motor}}{P_{motor}} = \frac{1.5 \times 11.53 + 0.5 \times 6.74}{18.27} \, \varepsilon = 1.13 \, \varepsilon
```

The 1 W of avionics doesn't change with mass. Four motors make 73.1 W of the 74.1 W total, so the total power grows by:

```latex
\frac{\Delta P_{total}}{P_{total}} = 1.13 \times \frac{73.1}{74.1} \, \varepsilon = 1.12 \, \varepsilon
```

**Step 4: flight time.** Time is energy divided by power, t = E / P, which is P to the power -1. With the small-change rule, the time falls by the same fraction the power rises:

```latex
\frac{\Delta t}{t} = -1.12 \, \varepsilon
```

**For one gram.** One gram on 250 g is:

```latex
\varepsilon = \frac{1}{250} = 0.004
```

So the time falls by:

```latex
\Delta t = -1.12 \times 0.004 \times 8.15 \ \text{min} = -0.036 \ \text{min}
```

**Each gram of frame costs 0.036 min, about 2.2 s** (N-02-11). Ten grams cost about 0.36 min, 22 s. The script finds the same value by running the full model at 249 g and 251 g and taking the difference (a finite difference), which checks this hand derivation.

**Why not the ideal value.** Momentum theory (Chapter 3) says ideal power grows with thrust to the power 1.5, which would give 1.5 in place of 1.12, and 0.049 min per gram. The real cost is lower because part of the power (the speed-proportional loss and the avionics) grows more slowly than thrust to the 1.5.

Correction: my earlier reply on momentum theory gave an exponent of 1.05 and 0.4 min per 10 g, from a different fit. With the chosen M3 model the values are 1.12 and 0.36 min per 10 g.

### 6.6 What a millimetre of arm width costs

A wider arm doesn't only add mass. It also blocks more of the propeller's downwash, which increases the download of Chapter 1, so each rotor must make more thrust for the same weight.

**Step 1: how download changes with width.** From Chapter 1, the download fraction is proportional to the arm width w:

```latex
f = \frac{C_d \, \kappa^2 \, w \, L}{4 A}
```

For 1 mm more width, with C\_d = 1.2, kappa = 1.4, L = 39.5 mm and A = 6.21 x 10^-3 m^2:

```latex
\Delta f = \frac{1.2 \times 1.4^2 \times 0.001 \times 0.0395}{4 \times 6.21 \times 10^{-3}} = 0.0037
```

Each millimetre adds 0.0037 to f: the download goes from 3.0 % of the thrust to 3.37 %. That is an increase of 0.37 **percentage points**, a fixed amount per millimetre, because f is proportional to w: f = K x w, with K = C\_d kappa^2 L / (4A) = 3.74 per metre. Seen as relative changes, 1 mm on an 8 mm arm is +12.5 % of width, and f grows by the same +12.5 % (0.030 x 1.125 = 0.0337). Both readings describe the same change.

**Step 2: how thrust changes.** Each motor's thrust is:

```latex
T = \frac{W}{4 (1 - f)}
```

Before the change, the thrust is:

```latex
T_1 = \frac{W}{4 (1 - f)}
```

After f grows by Delta f:

```latex
T_2 = \frac{W}{4 (1 - f - \Delta f)}
```

Divide the two. W and the 4 cancel:

```latex
\frac{T_2}{T_1} = \frac{1 - f}{1 - f - \Delta f}
```

Take (1 - f) out of the denominator as a common factor, and call x = Delta f / (1 - f):

```latex
1 - f - \Delta f = (1 - f)(1 - x)
```

So the (1 - f) cancels and:

```latex
\frac{T_2}{T_1} = \frac{1}{1 - x} = (1 - x)^{-1}
```

This is the small-change rule of 6.5 with n = -1 and a decrease of x, so (1 - x)^-1 is approximately 1 + x. The thrust grows by the fraction x:

```latex
\frac{\Delta T}{T} = \frac{\Delta f}{1 - f} = \frac{0.00374}{0.970} = 0.0039
```

(Exactly, 0.970 / 0.966 = 1.0039, the same to this precision.)

One millimetre of width raises the thrust each rotor must make by 0.39 %.

**Step 3: the rest of the chain.** From here it is the same chain as 6.5, steps 2 to 4, with epsilon = 0.0039 in place of the mass fraction:

```latex
\Delta t = -1.12 \times 0.0039 \times 8.15 \ \text{min} = -0.035 \ \text{min}
```

**Widening all four arms by 1 mm costs 0.035 min, about 2.1 s**, in download alone.

**In grams.** Dividing by the cost of a gram:

```latex
\frac{0.035}{0.036} = 0.96 \ \text{g}
```

So 1 mm of width on all four arms costs about as much flight time as 1 g of frame mass, **on top of** the mass of the extra material itself.

Correction: the register gives -0.033 min/mm (N-02-12) and "about 0.9 g per mm" (L-008). Those come from the approximate formula T = W / 4 x (1 + f) flagged in Chapter 1. With the exact 1 / (1 - f) form the values are -0.035 min/mm and about 1.0 g per mm. Both register entries should be updated; the conclusion doesn't change.

**What it means for the frame.** Width is a cheap way to gain stiffness. A rectangular arm's bending stiffness in the plane of its width grows with the width cubed, and its vertical bending stiffness grows linearly with it. Each extra millimetre costs about 2 s of flight in download, plus its material mass. Stage 3 and Stage 6 weigh this trade.

### 6.7 The Volador comparison

The aircraft currently flies on the Volador carbon frame, at 259.1 g. With the same model and the same 8 mm arm width:

```latex
t_{Volador} = 7.8 \ \text{min}
```

(N-02-13.) The cost-per-gram from 6.5 gives the same answer: 9.1 g heavier than the 250 g design point, so:

```latex
\Delta t = -9.1 \times 0.036 = -0.33 \ \text{min} \quad\Rightarrow\quad 8.15 - 0.33 = 7.8 \ \text{min}
```

A rev B frame at the 250 g limit would gain about 0.3 min, 20 s, over the current build. This small gain is why endurance was dropped as a requirement for the frame (decision D-018, lesson L-005): it belongs to the components, and the frame moves it only a little through its mass.

### 6.8 Why a bigger battery helps less than expected

A bigger battery stores more energy, but it is heavier, and the extra mass raises the hover power. Time is energy divided by power, so the two effects work against each other.

**For small changes.** Energy grows in proportion to capacity Q (same voltage). Power grows with mass with the exponent 1.12 from 6.5. So, approximately:

```latex
t \propto \frac{Q}{m^{1.12}}
```

where m is the whole aircraft's mass, battery included.

**Example: an 1100 mAh pack of the same type.** Assume it has the same energy per gram as the Tattu, 100 g per 850 mAh (an assumption for illustration). Then:

```latex
m_{battery} = 100 \times \frac{1100}{850} = 129 \ \text{g}
```

The aircraft goes from 250 g to 279 g. The capacity grows by 29 %, but the full model gives:

```latex
t = 9.3 \ \text{min}
```

only 14 % more than 8.2 min, and the aircraft breaks the 250 g limit (R-01). So with this battery type, the 250 g limit effectively fixes the battery size.

Correction: my earlier reply used t proportional to Q / m^1.5 and found +10 %. With the real exponent of 1.12 and the full model, the gain is +14 %.

**What actually helps: energy per gram.** The rev A spreadsheet used a GNB 1100 mAh LiHV pack: 88 g, lighter than the Tattu and with more capacity. LiHV (high-voltage LiPo) cells are charged to 4.35 V instead of 4.20 V, so their average voltage is higher; the model uses 3.8 V per cell. At an aircraft mass of 238 g:

```latex
t_{GNB} = 11.4 \ \text{min}
```

(N-02-24, information only.) The gain comes from more energy per gram of battery, not from more capacity alone.

### 6.9 Results of Chapter 6

| Result | Value | Used in |
| --- | --- | --- |
| Usable energy | 10.06 Wh | Flight time |
| Hover flight time at 250 g | 8.2 min, band 6.6 to 9.0 (N-02-10) | Report |
| Cost of one gram of frame | -0.036 min/g (N-02-11) | Stage 3 and 6 trades |
| Cost of 1 mm of width on four arms (download only) | -0.035 min/mm, about 1 g equivalent (N-02-12, corrected) | Stage 3 and 6 trades |
| Flight time with the Volador frame | 7.8 min (N-02-13) | Reference |
| Flight time with GNB 1100 LiHV | 11.4 min (N-02-24) | Information only |

## Chapter 7: Full throttle and the loads

**Where we are.** Chapters 1 to 6 dealt with hover, which sets performance. This chapter goes to the other operating point of Chapter 0, full throttle, which sets the **loads** the frame must carry. It hands Stage 4 three numbers: the maximum thrust on each arm, the motor reaction torque (already found in Chapter 4), and the load factor on everything the frame holds.

**Result.** Each motor pushes at most **5.04 N**. In a full-throttle climb every part of the aircraft is pressed into its mount with **8.2 times** its own weight; for the battery that is **8.1 N**.

### 7.1 Maximum thrust

The bench's 100 % row gives the maximum thrust of one motor:

```latex
T_{max} = 514.1 \ \text{g} = 514.1 \times 9.81 \times 10^{-3} = 5.04 \ \text{N}
```

(N-02-16.) It was measured at 16.5 V, almost the full-charge voltage of the pack (16.8 V, Chapter 6).

**Why this is the loads basis.** In flight the pack voltage drops under the high full-throttle current, and the thrust drops with it (second half of this chapter). So in real flight the motors produce **less** than 5.04 N. For the structure, a larger force is the safe side: a frame sized for 5.04 N also survives any smaller thrust. So the loads use the datasheet value, and the performance numbers use the lower, sagged values. Using each value in its place keeps the loads conservative and the performance honest.

**The force on one arm.** Each arm carries its motor's thrust. With an arm about 80 mm from the centre to the motor axis (assumed, close to the Volador; Stage 3 sets it), the bending moment at the arm root is force times distance:

```latex
M_{root} = T_{max} \times L_{arm} = 5.04 \times 0.080 = 0.40 \ \text{N m}
```

This treats the full 5.04 N as acting on the arm. In fact the motor's own inertia relieves the arm slightly during an acceleration (7.3), so this is again on the safe side.

### 7.2 Thrust-to-weight ratio

The thrust-to-weight ratio (TWR) compares the total maximum thrust with the aircraft's weight:

```latex
\mathrm{TWR} = \frac{4 \, T_{max}}{W}
```

In grams, with the 250 g design mass:

```latex
\mathrm{TWR} = \frac{4 \times 514.1}{250} = 8.2
```

The motors can lift 8.2 times the aircraft's weight. Hover uses only 1/8.2, about 12 % of it, which is why hover sits below the bench data (Chapter 5). The spare thrust is what the pilot uses for climbing, manoeuvring and recovering.

### 7.3 Load factor: what each part feels

**The worst case.** The largest steady force on the structure comes from a full-throttle vertical climb from hover, a "punch-out". All four motors push straight up at their maximum.

**Acceleration of the aircraft.** Newton's second law on the whole aircraft, upward positive:

```latex
4 \, T_{max} - m g = m \, a
```

Divide by m g:

```latex
\frac{4 \, T_{max}}{m g} - 1 = \frac{a}{g}
```

The first term is the TWR, so:

```latex
a = (\mathrm{TWR} - 1) \, g = (8.2 - 1) \, g = 7.2 \, g
```

The aircraft accelerates upward at 7.2 g.

**What each part feels.** Take any part of mass m\_i, the battery for example. Its mount must push it up hard enough to hold it against gravity **and** to accelerate it at 7.2 g. Newton's second law on that part alone:

```latex
F_i - m_i \, g = m_i \, a
```

so the force its mount applies is:

```latex
F_i = m_i \, (g + a) = m_i \, (g + 7.2 g) = 8.2 \, m_i \, g
```

The part is pressed into its mount with 8.2 times its own weight. The number 8.2 is the **load factor**, n\_z:

```latex
n_z = \frac{g + a}{g} = \mathrm{TWR} = 8.2
```

(N-02-18.) The load factor equals the TWR in this case because the 1 g of gravity plus the 7.2 g of acceleration add up to 8.2 g.

This is the same as standing in a lift that accelerates upward: you feel heavier. At 7.2 g of acceleration, everything on the aircraft "weighs" 8.2 times its normal weight.

**The parts that matter for the frame.**

| Part | Mass | Force on its mount, n\_z m\_i g |
| --- | --- | --- |
| Battery | 100 g | 8.2 x 0.100 x 9.81 = **8.1 N** |
| Flight controller and ESC stack | 13.6 g | 1.1 N |
| One motor | 11.6 g | 0.94 N |

The battery is the heaviest single item, so its strap and mount carry the largest inertial load.

**A consistency check.** All the inertial forces together must equal the total thrust, because the thrust is what accelerates everything:

```latex
n_z \, m \, g = 8.2 \times 0.250 \times 9.81 = 20.2 \ \text{N} = 4 \times 5.04 \ \text{N}
```

**How the load travels.** The thrust enters at the four motor mounts, travels inward along the arms, and the centre body passes it on to the battery and the stack. Each motor also needs 0.94 N just to accelerate itself, so the arm actually carries 5.04 - 0.94 = 4.1 N to the centre. Using the full 5.04 N for the arm (7.1) is therefore conservative by about 20 %.

### 7.4 Dynamic factor

**The question.** The load factor above is **quasi-static**: it assumes the thrust rises smoothly and the structure follows it without vibrating. A structure is a spring with mass, and a load applied suddenly makes it overshoot.

**The two extremes.** For a single spring-mass system with stiffness k and no damping, under a force F:

- Applied **slowly**, the deflection settles at the static value, F / k. Dynamic factor 1.
- Applied **instantly**, as a step, the mass overshoots and oscillates between 0 and 2 F / k. Dynamic factor 2.

The factor 2 comes from energy: a constant force F does work F x on the way to deflection x, while the spring stores only k x^2 / 2. They balance at x = 2 F / k.

**What decides between them.** The ratio between how fast the load rises, t\_r, and the structure's natural period, T\_n = 1 / f\_n. For a load that ramps up linearly over t\_r and then stays constant, the classic result for an undamped spring-mass (Biggs, Clough and Penzien) is:

```latex
\mathrm{DF}_{max} = 1 + \frac{\left| \sin(\pi \, t_r / T_n) \right|}{\pi \, t_r / T_n}
```

The largest value of the sine is 1, so an upper bound is:

```latex
\mathrm{DF} \leq 1 + \frac{T_n}{\pi \, t_r}
```

When the rise is much slower than the period (t\_r much larger than T\_n), the factor tends to 1.

**Our case (assumed values).**

- **Rise time.** A small motor spins up from hover to full speed in tens of milliseconds, limited by the propeller's inertia and the current the ESC allows. Take 20 ms as an assumed order of magnitude.
- **Natural period.** The frame's first elastic mode is expected in the hundreds of hertz (Chapter 9). At 500 Hz the period is 2 ms.

```latex
\mathrm{DF} \leq 1 + \frac{2}{\pi \times 20} = 1.03
```

The thrust rises about ten times slower than the frame vibrates, so the response is quasi-static and a dynamic factor of 1 is justified. Stage 4 should confirm the rise time (Blackbox log or literature) and the frame frequency (Stage 7 modal analysis). If either is uncertain, a bounding factor up to 2 can be applied to the punch-out case.

This argument covers thrust steps. Crash impacts are a different case, with rise times of a millisecond or less, and are treated separately (Chapter 8).

### 7.5 Why the battery voltage drops under load

**Open-circuit voltage.** With nothing connected, a battery shows a voltage set by its chemistry and its state of charge (Chapter 6, 6.1). This is the **open-circuit voltage**, V\_oc. For our 4S pack it is 16.8 V fully charged and about 15.2 V (3.8 V per cell) in the middle of a flight.

**Internal resistance.** Inside the battery, the current has to pass through the electrolyte, the electrodes, the tabs and the wires. All of these resist the current, like a resistance R\_int placed inside the battery, in series with the ideal chemical voltage. The mechanical picture: a pressurised tank with a narrow outlet pipe. With no flow, the pressure at the outlet equals the tank pressure. With a large flow, friction in the pipe eats part of the pressure, and the outlet pressure drops.

**The terminal voltage.** The voltage the battery actually delivers at its terminals is the open-circuit voltage minus the drop across the internal resistance (Ohm's law, V = I R, from Chapter 4):

```latex
V_{terminal} = V_{oc} - I \times R_{int}
```

The drop grows with current. At the hover current of 5 A it is small (Chapter 6). At full throttle the current is more than ten times larger.

**Our internal resistance.** It was not measured, because the charger has no function for it (A-004). The model uses an assumed band of **20 to 40 milliohm** for the whole pack. (The old report derived a value from a formula with an unverifiable source, audit item F-005.) Measuring it would remove most of the uncertainty in this section.

### 7.6 A first estimate of the sag

**Full-throttle current.** Four motors at 16.8 A each (the bench's 100 % row):

```latex
I_{total} = 4 \times 16.8 = 67.2 \ \text{A}
```

**Voltage drop** with the two ends of the resistance band:

```latex
\Delta V = 67.2 \times 0.020 = 1.3 \ \text{V} \qquad \text{to} \qquad 67.2 \times 0.040 = 2.7 \ \text{V}
```

The drop is called **sag**. A fully charged pack at 16.8 V would deliver only 14.1 to 15.5 V at full throttle.

**The heat.** The power lost in the internal resistance is I^2 R\_int (Chapter 4): 90 to 180 W inside a 100 g pack. That is one reason full throttle can only last a few seconds.

### 7.7 How thrust depends on voltage

At full throttle the ESC connects the battery straight to the motor (duty cycle 1, Chapter 4), so the motor sees the battery's terminal voltage.

**Speed follows voltage.** From Chapter 4 (4.4), the motor's speed is set mainly by the voltage applied: Kv RPM per volt, minus a loss in the wires. To first order:

```latex
\mathrm{RPM} \propto V
```

**Thrust follows speed squared** (Chapter 2):

```latex
T \propto \mathrm{RPM}^2
```

Combining the two:

```latex
T \propto V^2
```

So the thrust at a lower voltage V is the bench thrust scaled by the voltage ratio squared, taking the bench voltage of 16.5 V as the reference:

```latex
T(V) = T_{bench} \times \left( \frac{V}{16.5} \right)^2
```

This is a first-order approximation: the voltage lost inside the motor does not scale exactly with V, so the true exponent differs a little from 2.

**The current follows too.** The propeller's torque grows with speed squared, and torque is proportional to current (Chapter 4, 4.3). So the current also scales with V^2:

```latex
I(V) = 67.2 \times \left( \frac{V}{16.5} \right)^2
```

### 7.8 The sag, solved properly

**The problem with the first estimate.** Section 7.6 assumed the full 67.2 A flows. But when the voltage sags, the motors slow down, the current falls (7.7), and so the sag is smaller than estimated. Voltage and current depend on each other, so both must be found together.

**The equation.** Put the current of 7.7 into the terminal voltage of 7.5:

```latex
V = V_{oc} - R_{int} \times 67.2 \times \left( \frac{V}{16.5} \right)^2
```

To shorten it, collect the constants into one number c:

```latex
c = \frac{R_{int} \times 67.2}{16.5^2}
```

The equation becomes:

```latex
V = V_{oc} - c \, V^2
```

Rearranged, it is an ordinary quadratic in V:

```latex
c \, V^2 + V - V_{oc} = 0
```

Its positive root is:

```latex
V = \frac{-1 + \sqrt{1 + 4 \, c \, V_{oc}}}{2 \, c}
```

**The worst case: a half-empty pack and the high resistance.** V\_oc = 15.2 V and R\_int = 0.040 ohm:

```latex
c = \frac{0.040 \times 67.2}{16.5^2} = 0.00987 \ \text{per volt}
```

```latex
V = \frac{-1 + \sqrt{1 + 4 \times 0.00987 \times 15.2}}{2 \times 0.00987} = 13.4 \ \text{V}
```

The thrust ratio is:

```latex
\left( \frac{13.4}{16.5} \right)^2 = 0.66
```

The motors produce 34 % less than the bench thrust, and the current is 0.66 x 67.2 = 44 A, not 67.2 A. The first estimate (7.6) would have given 12.5 V, too pessimistic, because it ignored the falling current.

**All four corners of the band:**

| V\_oc | R\_int | Terminal voltage | Thrust ratio | Current | TWR |
| --- | --- | --- | --- | --- | --- |
| 16.8 V (full pack) | 20 mohm | 15.6 V | 0.89 | 60 A | **7.3** |
| 16.8 V | 40 mohm | 14.7 V | 0.79 | 53 A | 6.5 |
| 15.2 V (mid-flight) | 20 mohm | 14.2 V | 0.74 | 50 A | 6.1 |
| 15.2 V | 40 mohm | 13.4 V | 0.66 | 44 A | **5.4** |

The TWR column is the 8.2 of 7.2 times the thrust ratio.

**Result.** With sag, the usable thrust-to-weight is **5.4 to 7.3**, not 8.2 (N-02-19). The thrust loss is 11 to 34 %.

Correction: the original context file gave "about 28 % loss from 16.5 to 14 V" with the full 67.2 A. The self-consistent solution above, which the register uses, gives 11 to 34 % across the band.

**What this means.** The aircraft still has between 5.4 and 7.3 times its weight in thrust, plenty for control. For the loads, the frame keeps the datasheet 5.04 N and n\_z = 8.2 (7.1): sag only makes the real forces smaller. For performance (top speed, Chapter 8), the sagged values are the honest ones.

### 7.9 Can the ESC and battery supply the current?

**The ESC.** Each ESC channel is rated for 40 A continuous (datasheet). The largest current one motor draws is 16.8 A, at full throttle with no sag. The margin is:

```latex
\frac{40}{16.8} = 2.4
```

With sag the current is lower, so the margin is larger. The ESC is not a constraint.

**The battery and its C-rating.** Battery current limits are quoted in **C**, a multiple of the capacity. 1C is the current that would empty the pack in one hour: for 850 mAh, 1C = 0.85 A. The label says 150C:

```latex
I_{max} = 150 \times 0.85 = 127.5 \ \text{A}
```

Full throttle with no sag needs 67.2 A, which in C is:

```latex
\frac{67.2}{0.85} = 79 \, C
```

The margin is:

```latex
\frac{127.5}{67.2} = 1.9
```

(N-02-23.)

**How much to trust it.** There is no common standard for how manufacturers test the C-rating, and it is widely treated as a marketing figure; packs rarely sustain their label rating. So the margin of 1.9 is a sanity check, not a design value. The physically meaningful quantity is the internal resistance, which this chapter already uses: it is what makes the voltage, and the thrust, fall at high current.

### 7.10 Results of Chapter 7

| Result | Value | Used in |
| --- | --- | --- |
| Maximum thrust per motor (loads basis) | 5.04 N (N-02-16) | Stage 4 |
| Maximum motor reaction torque | 0.040 N m (N-02-17, Chapter 4) | Stage 4 |
| Load factor in a punch-out | 8.2 (N-02-18) | Stage 4 |
| Inertial force on the battery mount | 8.1 N | Stage 4 |
| Dynamic factor for thrust steps | about 1 (bound 1.03; to confirm) | Stage 4 |
| TWR with sag | 5.4 to 7.3 (N-02-19) | Chapter 8 |
| ESC margin / battery C margin | 2.4 / 1.9 (N-02-23) | Sanity check |

## Chapter 8: Top speed and crash energy

**Where we are.** Chapter 7 gave the full-throttle thrust. This chapter asks how fast that thrust can push the aircraft in level flight. The frame needs the answer for one reason: speed sets the kinetic energy the aircraft carries into a crash, which is a Stage 4 load case.

**Result.** Top speed is about **30 m/s (109 km/h)**, with a band of 27 to 36 m/s. At that speed the aircraft carries **114 J** of kinetic energy, up to 160 J at the top of the band.

### 8.1 Why the aircraft has to tilt

The propellers can only push along their shafts, and the shafts are fixed to the frame. To move forward, the aircraft tilts nose-down by an angle theta from the horizontal. The thrust then has two components:

- a **vertical** component, T cos(theta), which holds the aircraft up;
- a **horizontal** component, T sin(theta), which pushes it forward against air drag.

The faster it flies, the more drag it meets, the more it must tilt, and the less thrust is left to hold it up. Top speed is where the motors at full throttle can just do both.

### 8.2 The two force balances

In steady level flight nothing accelerates, so both directions balance. With T the total thrust of the four motors, W the weight and D the drag:

**Vertical:**

```latex
T \cos\theta = W
```

**Horizontal:**

```latex
T \sin\theta = D
```

**Drag** is dynamic pressure times a drag area:

```latex
D = \tfrac12 \rho V^2 \, (C_D A)
```

The product C\_D A is the **drag area**, in m^2: the area of a flat plate (C\_D = 1) that would make the same drag. It is the only aerodynamic property of the body we need.

### 8.3 The drag area

The drag area depends on the tilt. Flying level, the air meets the front of the aircraft. Tilted steeply, it meets more of the top. The model blends the two (A-013):

```latex
C_D A(\theta) = A_{front} \cos\theta + A_{top} \sin\theta
```

with A\_front = 0.0025 m^2 (band 0.0015 to 0.0035) and A\_top = 0.0090 m^2 (band 0.006 to 0.012). These are projected areas of the battery, stack, motors and arms, with C\_D about 1 for bluff shapes. Stage 3 will replace them with values from the real geometry.

### 8.4 First attempt: constant thrust

Suppose the thrust stays at its static value, 4 x 5.04 = 20.2 N, at any speed. The vertical balance then fixes the tilt:

```latex
\cos\theta = \frac{W}{T} = \frac{2.45}{20.2} = 0.121 \quad\Rightarrow\quad \theta = 83^\circ
```

and the horizontal balance gives the speed:

```latex
V = \sqrt{\frac{W \tan\theta}{\tfrac12 \rho \, C_D A(\theta)}} = 60 \ \text{m/s}
```

That is 215 km/h, unrealistic for this aircraft. The error is the assumption that thrust doesn't change with speed.

### 8.5 Why thrust falls with forward speed

**The air through the disk.** Tilted by theta, the propeller disk meets the oncoming air at an angle. The part of the air speed along the shaft, flowing into the disk, is:

```latex
V_{axial} = V \sin\theta
```

At the steep tilts of fast flight, most of the flight speed goes straight into the disk.

**What it does to the blade.** A blade section moves around at Omega r and, with axial inflow, also meets air coming at it along the shaft. The air therefore arrives at a steeper angle, closer to the blade's own angle. The blade's angle of attack, the difference between the two, shrinks. Less angle of attack means less lift, so less thrust.

**Pitch speed.** The blade is set at the angle a screw thread of pitch p would have. If the aircraft advanced exactly one pitch per revolution, the air would arrive along the blade, at zero geometric angle of attack. That axial speed is the **pitch speed**:

```latex
V_{pitch} = n \, p = 679.2 \times 0.0508 = 34.5 \ \text{m/s}
```

(n = 40,750 / 60 = 679.2 rev/s, p = 2.0 in = 0.0508 m.)

**Zero thrust is a little above pitch speed.** A curved (cambered) airfoil still makes some lift at zero geometric angle; lift only vanishes at a slightly negative angle. So the propeller reaches zero thrust a little above pitch speed. The model puts it at 1.1 times pitch speed (A-014, band 1.0 to 1.25), which in axial speed is 1.1 x 34.5 = 38.0 m/s.

**The thrust model.** Between zero axial speed (full static thrust) and 38.0 m/s (zero thrust), thrust is assumed to fall in a straight line. Written with the advance ratio J of Chapter 2, J = V\_axial / (n D):

```latex
T = T_0 \left( 1 - \frac{J}{J_0} \right)
```

where T\_0 is the static thrust and J\_0 the advance ratio at zero thrust:

```latex
J_0 = 1.1 \times \frac{p}{D} = 1.1 \times \frac{2.0}{3.5} = 0.629
```

Written with speeds instead of J (since n D = 60.4 m/s is fixed at full throttle):

```latex
T = T_0 \left( 1 - \frac{V \sin\theta}{38.0} \right)
```

This is a first-order model, stated as a limitation: real propeller curves are not straight lines, the in-plane part of the airflow (V cos theta) is ignored, and the speed is held at the full-throttle 40,750 RPM, although an unloaded propeller lets the motor spin slightly faster. Measured propeller data against airspeed would replace it.

**Interactive version.** The [Propeller Inflow Explorer](https://claude.ai/artifact/WHp9dq1HRSok2n6t88CjQT) shows this section live: tilt and speed sliders, the drone in side view, and a zoom on one blade seen from its tip, with the air it feels split into spin, flight and downwash.

**In my own words (Miguel, reference for later).** When talking about the propeller's job, we have to consider the air that goes into the disk. With the drone moving horizontally at 0 deg tilt, no flight air goes into or through the disk. If we tilt the drone and keep the horizontal movement, the air velocity now has a component in the into-disk direction, not only in the disk plane. The air the blade actually feels is then made of the blade's own spinning motion (in hover, the air has no speed of its own, only the relative speed due to the spinning) plus the air's own velocity, now not aligned with the disk plane. That changes the direction of the resultant air velocity, which reduces the angle of attack and therefore the lift.

**Precisions to that summary.**

- **Hover isn't quite zero air speed.** The propeller pulls its own downwash through the disk, about 6.4 m/s in hover (Chapter 3). So even in hover there is a small into-disk flow, which is why the hover air angle is 2.6 deg and not 0. Flight adds to it.
- **At 0 deg tilt the flight air still acts, but along the disk.** The advancing blade meets it head-on and gains a little lift; the retreating blade meets it from behind and loses a little. Over one turn they roughly cancel, so the model keeps only the into-disk part.
- **Speed and tilt come together.** The aircraft can't fly fast without tilting (8.1), so faster flight means more tilt and a larger share of the air going into the disk: at top speed, 27 of 30 m/s.
- **The felt air also gets slightly faster** (about 145 m/s instead of 142 m/s at 75 % radius), which on its own would add lift. But lift grows with angle of attack times speed squared: the speed gains about 3 %, while the angle of attack falls from about 11 deg to about 3 deg. The angle wins, so lift drops.

**In one line:** forward flight tilts the air the blade feels towards the blade's own chord; the angle of attack shrinks and thrust falls; at pitch speed the two line up and thrust is gone.

### 8.6 Solving for top speed

Now there are two unknowns, V and theta, and two balances. They are solved together in three steps for any trial tilt angle:

1. **Vertical balance gives the thrust needed:** T = W / cos(theta).
2. **The thrust model gives the speed at which the propellers make exactly that thrust.** Rearranging T = T\_0 (1 - V sin(theta) / 38.0):

```latex
V = \frac{38.0}{\sin\theta} \left( 1 - \frac{T}{T_0} \right)
```

3. **Horizontal balance check:** compare the forward push, T sin(theta) = W tan(theta), with the drag at that speed.

The top speed is the tilt where the push equals the drag.

| Tilt theta | Thrust needed T | T / T\_0 | Speed V | Forward push W tan(theta) | Drag at V |
| --- | --- | --- | --- | --- | --- |
| 50 deg | 3.82 N | 0.19 | 40.2 m/s | 2.92 N | 8.40 N |
| 55 deg | 4.28 N | 0.21 | 36.5 m/s | 3.50 N | 7.19 N |
| 60 deg | 4.90 N | 0.24 | 33.2 m/s | 4.25 N | 6.09 N |
| **64.5 deg** | **5.70 N** | **0.28** | **30.2 m/s** | **5.14 N** | **5.13 N** |
| 68 deg | 6.55 N | 0.33 | 27.6 m/s | 6.07 N | 4.35 N |

At shallow tilts the drag exceeds the push, so the aircraft can't fly that fast. At steep tilts the push exceeds the drag, so it would still accelerate. They meet at **64.5 deg and 30.2 m/s** (N-02-21). The script finds the crossing with a root-finding routine; the table shows the same search by hand.

**A notable detail.** At top speed the propellers make only 28 % of their static thrust. Most of the 20.2 N is lost to the inflow, which is why the constant-thrust estimate was so far off.

### 8.7 How uncertain it is

| Case | Top speed |
| --- | --- |
| Central | 30.2 m/s |
| Small drag area, zero thrust at 1.25 x pitch speed | 35.8 m/s |
| Large drag area, zero thrust at pitch speed | 26.7 m/s |
| With sag, TWR 5.4 to 7.3 (Chapter 7) | 27.7 to 29.5 m/s |

The band is **27 to 36 m/s**, and about 28 m/s with sag. The two largest uncertainties are the drag area (Stage 3 geometry will narrow it) and the thrust model (only propeller data against airspeed would narrow it).

For reference, the EU A1 category also limits speed to 19 m/s (R-04). That limit is acknowledged and not pursued: it is a flying rule, not a frame-sizing one.

Correction: my early reply gave 27 to 31 m/s with a simpler model (zero thrust exactly at pitch speed, a fixed drag area of 0.003 to 0.006 m^2), and 104 m/s for the constant-thrust case. The register uses the tilt-dependent drag area and the 1.1 factor above, giving 30 m/s and 60 m/s respectively.

### 8.8 Why pitch speed is not top speed

The old report took pitch speed, 34.5 m/s, as the cruise speed (audit item F-004). Two reasons it can't be:

- At pitch speed, along the shaft, the propeller makes little or no thrust. Flying needs thrust, to hold the aircraft up and to beat drag.
- In flight the air meets the disk at V sin(theta), not V. Pitch speed is a limit on the axial inflow, not on the flight speed itself.

Pitch speed is an asymptote of zero thrust, not a speed the aircraft flies at.

### 8.9 Crash energy

**Kinetic energy.** A mass m moving at speed V carries:

```latex
E_k = \tfrac12 m V^2
```

At top speed:

```latex
E_k = \tfrac12 \times 0.250 \times 30.2^2 = 114 \ \text{J}
```

(N-02-22.) Across the speed band it ranges from 89 J to **160 J**.

**For scale.** The same energy is gained by dropping the aircraft from a height h where m g h = E\_k:

```latex
h = \frac{E_k}{m g} = \frac{114}{0.250 \times 9.81} = 46 \ \text{m}
```

A full-speed crash is like a fall from a 15-storey building.

**What the frame does with it.** In a crash this energy must go somewhere: into deforming or breaking parts, and into bouncing. The average force depends on the distance over which the aircraft stops, F = E\_k / s, and in a hard impact s is a few millimetres, so the forces are far beyond anything the frame can carry elastically. That is why the crash requirement (R-07) is about **where** the frame fails, not about surviving: an arm must break before the centre body, so the battery mount and stack are protected and the repair is one printed part. Stage 4 uses the 114 to 160 J as the energy for that case.

### 8.10 Results of Chapter 8

| Result | Value | Used in |
| --- | --- | --- |
| Top speed | 30 m/s (109 km/h), band 27 to 36; about 28 with sag (N-02-21) | Crash energy |
| Tilt at top speed | 64.5 deg | Information |
| Thrust at top speed | 28 % of static | Information |
| Kinetic energy at top speed | 114 J, band up to 160 J (N-02-22) | Stage 4 crash case (R-07) |

## Chapter 9: How the rotors shake the frame

**Where we are.** Chapters 7 and 8 gave the forces the frame must carry. Those are steady or one-off loads. The spinning propellers also push on the frame with forces that repeat many times per second. This chapter finds those frequencies, because Stage 4 and Stage 7 must keep the frame's own vibration frequencies away from them.

**Result.** In hover each rotor shakes the frame at **241 Hz** (once per revolution) and **722 Hz** (once per blade passage). At full throttle these rise to 679 Hz and 2038 Hz.

### 9.1 Forces that repeat with each turn

A propeller turning at n revolutions per second produces two kinds of repeating force.

**Once per revolution: imbalance.** No propeller is perfect. If its centre of mass sits a tiny distance e off the shaft axis, the spinning mass m pulls outward with a centrifugal force:

```latex
F = m \, e \, \omega^2
```

This force rotates with the propeller, so the arm feels it as a push that goes round once per turn. The same happens if one blade makes slightly more thrust than the others (aerodynamic imbalance). Either way the frequency is the rotation frequency, called **1P** ("once per revolution"):

```latex
f_{1P} = \frac{\mathrm{RPM}}{60}
```

**An illustration (assumed imbalance).** Take a 2 mg error at 40 mm from the shaft, about 0.1 % of the 1.75 g propeller's mass. Here m e = 2 x 10^-6 kg x 0.040 m. In hover, omega = 2 pi x 14,440 / 60 = 1512 rad/s:

```latex
F = 2 \times 10^{-6} \times 0.040 \times 1512^2 = 0.18 \ \text{N}
```

At full throttle, omega = 4267 rad/s, and the same imbalance gives 1.5 N, a third of the full thrust. The force grows with speed squared, which is why small imbalances matter and propellers are balanced.

**Once per blade: blade passage.** Each time a blade passes over the arm, the arm sits in that blade's pressure pulse and wake for an instant: the download of Chapter 1 arrives in pulses, not as a steady push. With three blades this happens three times per turn, so the frequency is **3P**:

```latex
f_{3P} = 3 \times \frac{\mathrm{RPM}}{60}
```

**Other sources, smaller.** Harmonics of these (2P, 6P) appear at lower amplitude. The motor itself has a magnetic frequency, 7P for its 14 magnets (Appendix A.2.3), from small torque ripples.

### 9.2 Our frequencies

| Point | RPM | 1P (imbalance) | 3P (blade passage) |
| --- | --- | --- | --- |
| Hover | 14,440 | **241 Hz** | **722 Hz** |
| Full throttle | 40,750 | 679 Hz | 2038 Hz |

(N-02-06, N-02-20.) In flight the speed moves between these two points all the time, so the excitations sweep through the whole range: 1P from 241 to 679 Hz, 3P from 722 to 2038 Hz. Hover is where the aircraft spends most of its time, so the hover values matter most.

Correction: requirement R-08 quotes "about 237 Hz" and "about 711 Hz". Those come from the old 14,200 RPM hover (62.5 g, no download). With the register's hover speed of 14,440 RPM they are 241 Hz and 722 Hz; R-08 should be updated.

### 9.3 Why it matters: resonance

**The frame is a spring with mass.** Each arm, and the frame as a whole, has natural frequencies at which it vibrates freely if struck, like a tuning fork. They depend on stiffness and mass: f\_n = (1 / 2 pi) sqrt(k / m) for a single spring-mass.

**Forced at the wrong frequency, it amplifies.** A single spring-mass with damping ratio zeta, driven by a force at frequency f, vibrates with an amplitude that is the static deflection multiplied by:

```latex
\frac{X}{X_{static}} = \frac{1}{\sqrt{\left(1 - r^2\right)^2 + \left(2 \zeta r\right)^2}} \qquad r = \frac{f}{f_n}
```

At resonance, r = 1, this becomes:

```latex
\frac{X}{X_{static}} = \frac{1}{2 \zeta}
```

A printed structure has little damping. With zeta assumed between 0.02 and 0.05, the amplification at resonance is **10 to 25**. Away from it the factor drops quickly: at 25 % above the natural frequency (r = 1.25) it is about 1.8.

| r = f / f\_n | Amplification, zeta 0.02 | Amplification, zeta 0.05 |
| --- | --- | --- |
| 0.8 | 2.8 | 2.7 |
| 0.9 | 5.2 | 4.8 |
| 1.0 | 25 | 10 |
| 1.1 | 4.7 | 4.2 |
| 1.25 | 1.8 | 1.7 |

**What the amplified vibration does on a drone.**

- **The flight controller feels it.** Its gyroscope, which measures the aircraft's rotation rate, sits on the frame. Frame vibration appears to it as fast fake rotations. The flight controller filters them out, but every filter adds a small delay, and delay makes the control loop less responsive and less stable. A frame resonance near hover 1P or 3P means more filtering and worse flying.
- **Motors run hotter.** Noise that gets through the filters makes the controller command rapid speed changes, which heat the motors.
- **Fatigue.** The arm roots see millions of load cycles: at 241 Hz, about 870,000 per hour of hover.

### 9.4 The Campbell diagram

A **Campbell diagram** puts excitations and natural frequencies on one plot:

- horizontal axis: rotor speed (RPM);
- vertical axis: frequency (Hz);
- each excitation is a straight line through the origin: 1P with slope 1/60, 3P with slope 3/60;
- each natural frequency of the frame is a (nearly) horizontal line, since frame stiffness doesn't depend on rotor speed.

Wherever an excitation line crosses a mode line, there is a speed at which the rotor drives that mode at resonance.

**Our case.** The flight envelope is the band between hover (14,440 RPM) and full throttle (40,750 RPM). Any frame mode between 241 and 2038 Hz will be crossed by 1P or 3P somewhere in that band; crossings during throttle changes can't be avoided entirely. What matters is not to have a crossing **at hover**, where the aircraft dwells. Two placements avoid the hover excitations, to be chosen in Stage 4 (R-08):

- the first frame mode **between** hover 1P and hover 3P (241 to 722 Hz), with margin from both;
- the first frame mode **above** hover 3P (722 Hz), with margin.

The required margin is set in Stage 4; Stage 7 checks it with a modal analysis, and a Blackbox log of the gyro (an FFT of the recorded rotation rates) verifies it in flight.

### 9.5 Results of Chapter 9

| Result | Value | Used in |
| --- | --- | --- |
| Hover 1P / 3P | 241 / 722 Hz (N-02-06) | Stage 4 frequency target, R-08 |
| Full-throttle 1P / 3P | 679 / 2038 Hz (N-02-20) | Campbell diagram, Stage 7 |
| Excitation range in flight | 1P 241 to 679 Hz; 3P 722 to 2038 Hz | Campbell diagram |
| Resonant amplification, zeta 0.02 to 0.05 | 10 to 25 | Why margin matters |

## Chapter 10: What goes to the next stages

**Where we are.** Chapter 0 listed the questions the frame designer asks. Chapters 1 to 9 answered them. This chapter collects every answer in one place, with its uncertainty and the stage that uses it, then lists the corrections found during this revision and what is still open.

### 10.1 Outputs for the frame

**Mass and hover**

| Output | Value | Uncertainty | Chapter | Used in |
| --- | --- | --- | --- | --- |
| Frame mass budget | 61.4 g | hardware +/- 5 g (A-005), GPS placeholder (A-007) | 1 | R-01, Stage 3 |
| Arm download fraction (8 mm arm) | 3.0 % | 2.2 to 3.9 % | 1 | Stage 3 arm width |
| Hover thrust per motor | 64.4 g (0.632 N) | +/- 1 g | 1 | All hover numbers |
| Hover speed | 14,440 RPM | +/- 1 % | 2 | Chapter 9 |
| Hover power, aircraft | 74 W, 5.0 A | 82 W bound (M2) | 5 | Endurance |

**Performance and trades**

| Output | Value | Uncertainty | Chapter | Used in |
| --- | --- | --- | --- | --- |
| Hover flight time at 250 g | 8.2 min | 6.6 to 9.0 min | 6 | Report |
| Cost of 1 g of frame | -0.036 min/g | about +/- 15 % | 6 | Stage 3 and 6 trades |
| Cost of 1 mm of width, four arms | -0.035 min/mm, about 1 g equivalent | as A-012 | 6 | Stage 3 and 6 trades |
| Top speed | 30 m/s | 27 to 36 m/s; about 28 with sag | 8 | Crash energy |

**Loads (Stage 4)**

| Output | Value | Uncertainty | Chapter |
| --- | --- | --- | --- |
| Maximum thrust per motor | 5.04 N | conservative (no sag) | 7 |
| Arm root bending moment | 0.40 N m | arm length assumed 80 mm; about 20 % conservative | 7 |
| Maximum motor reaction torque | 0.040 N m | 0.036 to 0.048 N m | 4 |
| Load factor, punch-out | 8.2 | conservative (no sag) | 7 |
| Inertial force on the battery mount | 8.1 N | as load factor | 7 |
| Dynamic factor, thrust steps | about 1 | bound 1.03; rise time to confirm | 7 |
| Kinetic energy at top speed | 114 J | up to 160 J | 8 |

**Vibration (Stages 4 and 7)**

| Output | Value | Chapter |
| --- | --- | --- |
| Hover 1P / 3P | 241 / 722 Hz | 9 |
| Full-throttle 1P / 3P | 679 / 2038 Hz | 9 |
| Resonant amplification, damping 0.02 to 0.05 | 10 to 25 | 9 |

**Checks on the bought hardware**

| Check | Value | Chapter |
| --- | --- | --- |
| Thrust coefficient constant over the bench range | within 2 % | 2 |
| Figure of merit at full throttle | 0.535, inside the 0.4 to 0.6 range | 4 |
| Thrust-to-weight with sag | 5.4 to 7.3 | 7 |
| ESC current margin | 2.4 | 7 |
| Battery C margin (label value) | 1.9 | 7 |

### 10.2 Corrections to the journal

Found during this revision. None changes a design decision.

| Item | Journal says | Should say | Chapter |
| --- | --- | --- | --- |
| N-02-04 formula | AUW / 4 x (1 + f) | AUW / 4 / (1 - f); value 64.4 g unchanged | 1 |
| N-02-01 largest residual | 1.4 % | 1.5 % (1.46 %) | 2 |
| N-02-25 disk loading | 99 N/m^2 | 102 N/m^2 at 64.4 g (hover v\_i 6.45 m/s, ideal power 4.1 W) | 3 |
| N-02-14 upper value | 0.330 | 0.331 (rounding) | 4 |
| Stage 2 notes, model fits | "All fit the data" | Only M4 within about 1 %; M1, M2, M3 miss the lowest row by 16, 12 and 8 % | 5 |
| F-002 | Spreadsheet low by 30 to 40 % | About 30 %, like for like at 212.8 g; the 14.8 W value is at 250 g | 5 |
| N-02-12 | -0.033 min/mm | -0.035 min/mm (exact download formula) | 6 |
| L-008 | 1 mm costs as much as 0.9 g | about 1.0 g | 6 |
| R-08 | about 237 Hz and 711 Hz | 241 Hz and 722 Hz | 9 |
| F-013 text | Reynolds number about 26,000 | about 27,000 at the 64.4 g hover | 2 |

**New point for the Q-18 review (Chapter 5).** Both accepted power models overpredict the lowest bench row (M3 by 8 %, M2 by 12 %). If that bias continues to hover, the 18.3 W central value is conservative and the flight time sits in the upper half of its band.

### 10.3 What would remove the largest uncertainties

| Open item | Affects | How to close it |
| --- | --- | --- |
| Hover power is extrapolated (A-003) | Flight time band | Hover with a current log (Blackbox or a meter): measured power replaces the model |
| Pack internal resistance (A-004) | Sag, TWR with sag, top speed with sag | A charger or tester with an internal-resistance function |
| Drag areas (A-013) | Top speed, crash energy | Stage 3 geometry: projected areas |
| Thrust against forward speed (A-014) | Top speed | Propeller data against airspeed, or a flight test with GPS speed at full throttle |
| Motor spin-up time | Dynamic factor | Blackbox log of a punch-out |
| Blade chord at 75 % radius | Reynolds number values | Measure a blade |
| Frame damping | Resonant amplification | Tap test or Blackbox gyro FFT on the built frame |

## Appendix A: Losses, motor and ESC in depth

Not needed for the sizing numbers. It explains the mechanisms behind Chapter 4 in more depth, for reference.

### A.1 Propeller losses in detail

**Where the losses come from.** Shaft power splits into two parts (modified momentum theory, Leishman ch. 2):

```latex
P_{shaft} = \kappa \, T v_i + P_0
```

| Symbol | Name | What it is |
| --- | --- | --- |
| kappa | Induced power factor | Extra induced power from uneven inflow and tip losses; about 1.15 to 1.2 |
| P\_0 | Profile power | Power spent dragging the blades through the air against friction |
| sigma | Solidity | Blade area divided by disk area: N\_b c / (pi R) for N\_b blades of chord c |
| C\_d0 | Profile drag coefficient | Drag coefficient of the blade airfoil, averaged along the blade |
| Omega | Angular speed | rad/s |
| N\_b | Number of blades | 3 |

**Deriving P\_0 from first principles.** Take a thin slice of one blade, at radius r, width dr, chord c. It moves at Omega r. Its friction drag is dynamic pressure times area times C\_d0:

```latex
dD = \tfrac12 \rho (\Omega r)^2 \, c \, dr \, C_{d0}
```

**Which way the air moves, and why the area is c dr.** Seen from the blade, the air arrives almost entirely **in the plane of rotation**, head-on to the leading edge, at Omega r. The induced flow v\_i adds a small downward component: at 0.75 R in hover, 6.45 m/s against 50.4 m/s, so the air arrives tilted only atan(6.45 / 50.4) = 7.3 deg below the rotor plane. The blade section is set at a geometric angle of atan(p / (2 pi 0.75 R)) = 13.6 deg, so its angle of attack is about 6 deg. The section is a streamlined airfoil meeting the flow nearly edge-on, not a plate facing it.

The area c dr is a **reference area**, not the area the air hits. For airfoils, drag and lift coefficients are defined per unit of planform area (chord x span). The frontal area the air hits head-on is only thickness x dr, about a tenth of that. Planform is the convention because an airfoil's drag is mostly skin friction on its upper and lower surfaces, which scales with chord, and its pressure drag is small. Any reference area works as long as the coefficient was measured with the same one: C\_d0 values of 0.01 to 0.05 for airfoils are quoted per chord area, so P\_0 must use c dr. P\_0 takes the speed as Omega r and ignores the small downward component. The true speed, sqrt(50.4^2 + 6.45^2) = 50.8 m/s, is 0.8 % higher, so P\_0 is underestimated by about 2.5 % (speed cubed).

The power to push it is that drag times its speed, Omega r. Add up all slices of all blades:

```latex
P_0 = N_b \int_0^R \tfrac12 \rho \, C_{d0} \, c \, \Omega^3 r^3 \, dr = \frac{N_b \, c \, C_{d0} \, \rho \, \Omega^3 R^4}{8}
```

Rewriting with solidity sigma = N\_b c / (pi R) and A = pi R^2:

```latex
P_0 = \frac{\sigma C_{d0}}{8} \, \rho A \, (\Omega R)^3
```

Three consequences:

1. Profile power grows with tip speed cubed, whatever the thrust.
2. C\_d0 is large at low Reynolds number (Chapter 2), so small propellers lose the most here.
3. Even with no blade drag, FoM can't exceed 1 / kappa, about 0.85.

**Both terms scale with n^3.** For a fixed propeller, v\_i \~ sqrt(T) \~ n, so the induced term T v\_i \~ n^3. The profile term is \~ (Omega R)^3 \~ n^3 if C\_d0 is constant. So the whole aerodynamic power scales as n^3, which is why C\_P is a constant (Chapter 2). It stops being exact when C\_d0 changes with Reynolds number, at the low end.

**Illustration (assumed values).** With c = 8 mm, sigma = 3 x 0.008 / (pi x 0.0445) = 0.17. Assume C\_d0 = 0.04 and kappa = 1.15 (neither measured). At hover, V\_tip = 67 m/s: P\_0 = (0.17 x 0.04 / 8) x 1.225 x 6.21 x 10^-3 x 67^3 = 2.0 W, induced 1.15 x 4.1 = 4.7 W, so FoM = 4.1 / 6.7 = 0.61. This only shows the proportions; FoM is not computed this way in the model.

### A.2 The motor

The motor turns electrical power into shaft torque and speed. This part builds its model from zero, using mechanical analogies for every electrical quantity.

#### 2.1 The electrical quantities, in mechanical terms

A useful analogy throughout: electric current behaves like a fluid flowing in pipes.

| Quantity | Symbol, unit | What it is | Mechanical analogy |
| --- | --- | --- | --- |
| Charge | q, coulomb (C) | Amount of electricity | Volume of fluid |
| Current | I, ampere (A) = C/s | Charge passing per second | Volume flow rate |
| Voltage | V, volt (V) = J/C | Energy carried by each coulomb; what pushes current | Pressure difference |
| Power | P = V I, watt (W) | Energy per second | Pressure x flow rate = hydraulic power |
| Resistance | R, ohm | How much a conductor resists current; converts energy to heat | Friction in a pipe |
| Inductance | L, henry (H) | How much a coil resists a **change** of current | Mass (inertia) |

**Power = V I.** Voltage is joules per coulomb, current is coulombs per second; the product is joules per second. The bench table checks this: at 100 %, 16.5 V x 16.8 A = 277.2 W, and the power column says 277.8 W.

**Ohm's law, V = I R.** Pushing current through a resistance needs a voltage proportional to the current, like the pressure drop in a pipe with laminar flow. The energy is lost as heat. The heat power is the voltage drop times the current: (I R) x I = **I^2 R**. Double the current, four times the heat.

**Kirchhoff's voltage law.** Around any closed loop of a circuit, the voltage supplied equals the sum of the voltages used up. It is energy conservation for each coulomb that goes round: the energy it receives equals the energy it gives away.

**Inductance, V = L dI/dt.** A coil of wire opposes changes in its current, just as a mass opposes changes in its velocity (F = m dv/dt). It doesn't oppose a steady current, only a changing one. This matters for the ESC (Part 3).

#### 2.2 Two physical effects, and why one constant links them

Everything a motor does comes from two effects of a magnetic field B (unit: tesla) on a wire.

**Effect 1, Lorentz force: current in a field makes force.** A straight wire of length l carrying current I across a field B feels a force perpendicular to both:

```latex
F = B \, I \, l
```

In a motor, the wires run along the axis at radius r from the shaft. Each force acts tangentially, so it makes a torque F r = B l r I. Adding up every wire in the motor:

```latex
\tau = \Big(\sum B \, l \, r\Big) \, I = K_t \, I
```

The bracket depends only on the magnets, the geometry and the number of turns. It is fixed for a given motor and is called the **torque constant** K\_t (unit N m/A). Torque is proportional to current.

**Effect 2, Faraday's law: a wire moving in a field makes voltage.** A wire of length l moving at speed u across a field B has a voltage e = B l u induced along it. In the motor, wire and magnets move relative to each other at u = omega r. Adding up every wire:

```latex
E = \Big(\sum B \, l \, r\Big) \, \omega = K_e \, \omega
```

This voltage is the **back-EMF** E (EMF: electromotive force, an old name for a generated voltage). Every motor is also a generator: while it spins, it generates E, and E always points **against** the voltage driving the current (Lenz's law; if it pointed the other way the motor would accelerate itself for free).

**The same bracket appears in both.** So K\_e = K\_t: one constant, seen from the mechanical side (torque per amp) and the electrical side (volts per rad/s). Unit check: V s = (W / A) s = (N m / s) s / A = N m / A. Same units, same number.

The same result follows from energy: an ideal motor converts all the electrical power E I into mechanical power tau omega, so K\_e omega I = K\_t I omega.

#### 2.3 How a brushless motor keeps turning

The P1604 is an **outrunner**: the outer bell, which carries the propeller, holds **14 permanent magnets** (14P) with alternating north and south poles facing inward. The fixed inner **stator** has **12 iron teeth** (12N), each wound with a copper coil. The coils are connected into three groups, called **phases** A, B and C.

For torque to keep pushing the same way, the current in a coil must reverse each time a north magnet is replaced by a south one in front of it. Otherwise the force would reverse too. Switching the current direction in step with the rotor position is called **commutation**. Old brushed motors did it with sliding contacts; a brushless motor has no contacts, so the ESC does it electronically (Part 3).

One consequence matters for losses: the current in each coil alternates at the **electrical frequency**, which is the mechanical frequency times the number of pole pairs (14 magnets = 7 north-south pairs):

| Point | Mechanical (rev/s) | Electrical frequency |
| --- | --- | --- |
| Hover | 240.7 | 7 x 240.7 = 1685 Hz |
| Full throttle | 679.2 | 4754 Hz |

**The DC-equivalent model.** The real motor has three phases with alternating currents. Because the ESC commutates them so that, on average, the motor behaves like a simple motor with one current and one voltage, we model it as exactly that. I is the average current, V the average voltage applied. This is the standard model for sizing and is accurate enough for power and torque.

#### 2.4 Kv, the number on the label

Imagine the motor with no propeller, connected to a voltage V. It accelerates. As it speeds up, its back-EMF E grows. The current is pushed by the difference V - E, so as E approaches V the current falls, and with it the torque. The motor stops accelerating when E is just below V, with only a small current left to overcome its internal friction.

So with no load, **back-EMF approximately equals the applied voltage**, and the no-load speed is proportional to voltage. Kv is that proportion:

```latex
K_v = \frac{\text{no-load RPM}}{\text{volt}}, \qquad E = \frac{\mathrm{RPM}}{K_v}
```

Our motor: 3800 RPM per volt. At 16.5 V it would spin at about 62,700 RPM with no propeller. With the propeller at full throttle it does 40,750 RPM; the difference is the voltage lost to resistance under load (2.5).

**From Kv to K\_e and K\_t.** E = RPM / Kv uses RPM; physics uses rad/s, omega = 2 pi RPM / 60. Substituting RPM = 60 omega / (2 pi):

```latex
E = \frac{60}{2\pi K_v}\,\omega \quad\Rightarrow\quad K_e = K_t = \frac{60}{2\pi K_v} = \frac{9.549}{K_v}
```

For 3800 KV: K\_t = 9.549 / 3800 = **2.513 x 10^-3 N m/A**. Each amp makes 2.5 mN m of torque.

**What Kv says about a motor.** A high-Kv motor has few turns of thick wire: little torque per amp, high speed per volt. A low-Kv motor of the same size has many turns of thin wire: more torque per amp, lower speed per volt. 2.9 shows this choice doesn't change efficiency.

#### 2.5 The voltage balance

Apply Kirchhoff's law to the loop formed by the ESC output and the motor winding. The voltage V supplied is used up in two ways:

- **E**, the back-EMF: this part of the energy is converted into mechanical work.
- **I R**, the drop across the winding resistance (plus wires and ESC transistors, lumped together as R): this part becomes heat.

```latex
V = E + I R = \frac{\mathrm{RPM}}{K_v} + I R
```

Inductance doesn't appear because the average current is steady (V = L dI/dt = 0 on average).

Solving for current:

```latex
I = \frac{V - E}{R}
```

The current is set by how much the supply exceeds the back-EMF. This is what makes the motor self-regulating. If the propeller needs more torque than the motor makes, the motor slows, E falls, V - E grows, current rises, torque rises, until motor torque equals propeller torque. The operating speed is where the two torques balance. The analogy is a pump driving a turbine through a pipe: the turbine's back-pressure plays the role of E, pipe friction the role of I R.

#### 2.6 Internal losses: the no-load current I\_0

Not all of K\_t I reaches the propeller. Part of the torque is spent inside the motor:

- **Bearing friction** and air drag on the spinning bell.
- **Iron losses** in the stator teeth. The iron is magnetised back and forth at the electrical frequency (2.3). Each cycle wastes a little energy (**hysteresis**, like the energy lost in each load-unload cycle of a material with a hysteresis loop), so this loss grows with frequency. The changing field also induces small circulating currents inside the iron itself (**eddy currents**), which heat it and grow with frequency squared. The stator is built from thin insulated sheets (laminations) to limit them.

These losses are measured by spinning the motor with no propeller. Then the shaft torque is zero, so all the current goes to the internal losses. That current is the **no-load current** I\_0. Datasheet: 0.8 A at 10 V.

The model treats them as a fixed slice of the current: the first I\_0 amps only overcome internal losses, and the rest makes shaft torque:

```latex
\tau = K_t \, (I - I_0)
```

**Where the 0.8 A was measured.** At 10 V with no load, E is just below 10 V, so the motor spins at roughly 3800 x 9.7 = 37,000 RPM. Since iron and friction losses grow with speed, I\_0 = 0.8 A is representative near full throttle (40,750 RPM), and too high for hover (14,440 RPM).

Correction: the previous version of this chapter said I\_0 was measured "at much lower speed" than full throttle and therefore underestimated there. That was wrong: 10 V with no load means about 37,000 RPM, close to full throttle. The full-throttle torque below is therefore only slightly affected.

#### 2.7 Where every watt goes

Multiply the voltage balance V = E + I R by I. Each term becomes a power:

```latex
V I = E I + I^2 R
```

Now split E I using E = K\_t omega and I = (I - I\_0) + I\_0:

```latex
E I = K_t \omega (I - I_0) + K_t \omega I_0 = \tau \omega + E I_0
```

So every watt from the ESC ends in one of three places:

```latex
\underbrace{V I}_{\text{input}} = \underbrace{\tau \omega}_{\text{shaft}} + \underbrace{E \, I_0}_{\text{iron, friction}} + \underbrace{I^2 R}_{\text{resistive heat}}
```

How each loss changes with load, for a propeller (torque \~ RPM^2, so current \~ RPM^2):

| Loss | Grows with | Share at light load | Share at full load |
| --- | --- | --- | --- |
| Resistive, I^2 R | Current squared, so about RPM^4 | Small | Large |
| Iron and friction, E I\_0 | Speed (hysteresis, bearings), speed squared (eddy currents) | Large | Small |

Efficiency is low at light load, where iron and friction take a large share of a small output, and drops again at very high load, where I^2 R grows fastest. It peaks in between.

#### 2.8 Full throttle, every watt accounted for

At 100 %: V = 16.5 V (the ESC is fully on, so the motor sees the battery voltage), I = 16.8 A, RPM = 40,750.

1. **Back-EMF**: E = 40,750 / 3800 = 10.72 V.
2. **Resistive drop**: V - E = 16.5 - 10.72 = 5.78 V. So R = 5.78 / 16.8 = 0.34 ohm. This lumps winding, wires and ESC transistors; it is not the datasheet winding resistance.
3. **Angular speed**: omega = 2 pi x 40,750 / 60 = 4267 rad/s.
4. **Torque**: tau = 2.513 x 10^-3 x (16.8 - 0.8) = **0.040 N m** (N-02-17).

| Term | Calculation | Power | Share |
| --- | --- | --- | --- |
| Input, V I | 16.5 x 16.8 | 277.2 W | 100 % |
| Resistive heat, I^2 R | 16.8 x 5.78 | 97.1 W | 35 % |
| Iron and friction, E I\_0 | 10.72 x 0.8 | 8.6 W | 3 % |
| **Shaft, tau omega** | 0.040 x 4267 | **171.6 W** | **62 %** |

Motor plus ESC efficiency: **0.62**. Figure of merit: FoM = P\_ideal / P\_shaft = 91.8 / 171.6 = **0.535** (N-02-15), inside the 0.4 to 0.6 range for small propellers.

At full throttle 35 % of the input becomes heat. That is why the datasheet allows peak power for only 10 s: it is a thermal limit, not an electrical one.

#### 2.9 Why the method fails at 20 %

The same steps at 17,311 RPM, 1.5 A: tau = 2.513 x 10^-3 x (1.5 - 0.8) = 1.76 x 10^-3 N m; omega = 1813 rad/s; P\_shaft = 3.2 W. But Chapter 3 says this thrust needs at least 6.9 W. A shaft power below the ideal power would mean FoM above 1, which is impossible.

The model isn't wrong; the input is. The bench measures current at the **battery**, and at part throttle the current in the motor is several times larger. Part 3 explains why.

### A.3 The ESC

The ESC (electronic speed controller) sits between battery and motor. It has two jobs: give the motor a **variable voltage** from a fixed battery, and **commutate** the three phases.

#### 3.1 The problem: a fixed battery, a variable speed

From 2.4 and 2.5, motor speed is set mainly by the voltage applied (E is close to V). The battery gives about 16 V, always. To fly at hover speed, the motor needs much less.

The obvious solution is a resistor in series, which drops the excess voltage. But it would burn the dropped voltage times the current as heat, wasting most of the battery's energy at part throttle. The ESC uses switching instead.

#### 3.2 Transistors as switches

A **MOSFET** (a type of transistor) is an electrically controlled valve for current. It is used fully on or fully off, never in between:

- **On**: almost no resistance. Current flows, almost no voltage across it, so almost no power lost (power = voltage across x current through).
- **Off**: no current. Voltage across it, but zero current, so no power lost.

A switch that is either fully on or fully off wastes almost nothing. The ESC uses six of them, two per phase.

#### 3.3 PWM: switching fast to make an average

**PWM** (pulse width modulation): the ESC switches the battery onto the motor and off again at a fixed rate, 48,000 times per second here (Bluejay firmware). Each cycle lasts 1 / 48,000 = 20.8 microseconds. The fraction of each cycle the switch is on is the **duty cycle** d, from 0 to 1.

The voltage at the motor is a rapid train of pulses: battery voltage for d of the time, zero for the rest. Its average is:

```latex
V_{motor} = d \cdot V_{battery}
```

#### 3.4 Why the motor responds to the average

This is where inductance (2.1) comes in. The motor windings are coils, and coils resist changes of current the way a mass resists changes of velocity.

The mechanical picture: push a heavy cart with rapid on-off shoves, thousands per second. The cart doesn't jerk with each shove. Its speed barely ripples and settles where the **average** push balances friction. In the same way the motor current barely ripples within one 20.8 microsecond cycle, and settles where the **average** voltage balances back-EMF plus resistive drop. The voltage balance of 2.5 holds with V = d V\_battery.

During the off part of each cycle, the current doesn't stop. Like the coasting cart, it keeps flowing, circulating through the motor and the other transistors without passing through the battery. This is the key to the next point.

#### 3.5 Battery current is not motor current

The motor current I\_motor flows all the time. The battery only supplies it during the on part of each cycle, a fraction d of the time. So the average battery current is:

```latex
I_{battery} = d \cdot I_{motor} \quad\Rightarrow\quad I_{motor} = \frac{I_{battery}}{d}
```

The same follows from energy: with an almost lossless switch, battery power equals motor power, V\_bat I\_bat = (d V\_bat) I\_motor.

**The ESC is an electrical gearbox.** A gearbox lowers speed and raises torque, keeping power the same. The ESC lowers voltage by d and raises current by 1/d, keeping power the same. Voltage is the electrical speed, current the electrical torque.

**At 20 % throttle.** The back-EMF is 17,311 / 3800 = 4.6 V, so the motor needs a bit more than 4.6 V from a 16.8 V battery: d is at least 4.6 / 16.8 = 0.27. The motor current is then up to about 1.5 / 0.27 = 5.5 A, several times the 1.5 A logged. That is why tau = K\_t (I - I\_0) gave an impossible answer in 2.9: it used battery current. At full throttle d = 1, the two currents are equal, and the method works. (Journal lesson L-006.)

#### 3.6 Commutation

On top of PWM, the ESC decides which phase gets positive voltage, which negative, and which is left off. It steps through six combinations per electrical cycle, so 6 x 1685 = 10,100 steps per second at hover. Each switch must happen when the magnets reach the right position.

The ESC has no position sensor. It reads the back-EMF on the phase that is momentarily switched off: the moment that voltage crosses zero tells it where the magnets are. This is called **sensorless** control.

#### 3.7 Throttle % is not a physical quantity

Throttle % is the pilot's stick command. The ESC firmware maps it to a duty cycle, and the speed that results also depends on battery voltage. Different ESCs, firmware and calibrations give different maps: one bench gives 20 % = 10,500 RPM, ours 20 % = 17,311 RPM (F-018). Hover is therefore stated as thrust, RPM and current, never as throttle (A-006). The register's 14 % hover throttle (N-02-09) is an indicative mapping of this bench only.

#### 3.8 ESC losses and current rating

- **Conduction loss**: an on transistor still has a small resistance, R\_DS(on), so it heats as I^2 R\_DS(on). In 2.8 it is inside the lumped R.
- **Switching loss**: during each on-off transition, for a few nanoseconds the transistor carries current with voltage across it. A small energy is lost each time, so this loss grows with switching frequency.
- **Fixed consumption**: the ESC's microcontroller and gate drivers draw a small power whatever the speed.

The **40 A** rating is the continuous current per channel the transistors can carry without overheating. Chapter 7 compares it with the motor's peak.

## Appendix B: Old report claims, corrected

Audit material (finding F-013). Not part of the sizing story.

| Claim | Correction |
| --- | --- |
| "Lower KV draws less current for the same load" | Take the same stator and rewind it with N times more turns. Each wire now passes the magnets N times more often, so the back-EMF per RPM and the torque per amp both rise by N: Kv falls by N, K\_t rises by N (2.2, 2.4). The winding space is fixed, so N times more turns must use wire of 1/N the cross-section, and the total wire is N times longer. Resistance grows with length and falls with cross-section, so R rises by N x N = N^2. For the same torque the current falls by N (tau = K\_t I), so the resistive loss (I/N)^2 x (N^2 R) = I^2 R is unchanged. Lower KV trades current for voltage, like a different gear ratio; it doesn't save energy. KV is chosen so the battery voltage gives the RPM the propeller needs. |
| "PWM maintains magnetic saturation"; "4500 KV exceeds saturation" | The stator iron concentrates the coils' magnetic field. Up to a point, more current gives proportionally more field. Beyond it the iron **saturates**: like a material past yield, it stops responding proportionally, and extra current gives little extra field and torque. Saturation only happens at very high current and designers avoid it, because torque per amp drops and losses rise. PWM only sets the average voltage (3.3); it doesn't create or maintain saturation, and Kv has nothing to do with it. Both statements are meaningless. |
| "Torque \~ r^2" | The motor's force acts across the thin air gap between stator and magnets, as a tangential shear stress sigma (force per unit gap area). Torque = stress x gap area x radius = sigma (2 pi r L) r, so tau \~ r^2 L at constant sigma (sigma is limited by magnet strength, saturation and heating). It is a first-order scaling, not a law. 1604 against 1504 (stator diameter 16 vs 15 mm, height 4 mm): (16/15)^2 = 1.14, 14 % more torque. |
| "TCXO mechanically regulates temperature" | A radio needs a precise frequency reference. It comes from a small quartz crystal that vibrates at a fixed frequency, like a tuning fork. Its frequency drifts slightly with temperature. A **TCXO** (temperature-compensated crystal oscillator) measures its temperature and corrects the frequency electronically. An **OCXO** (oven-controlled) keeps the crystal in a tiny heater at constant temperature. Neither regulates anything mechanically. The bought receiver's datasheet doesn't state a TCXO anyway. |
| "Low pitch ensures laminar flow" | Pitch sets the blade angle and how far the propeller advances per turn. Whether the boundary layer is laminar depends on Reynolds number, surface finish and pressure gradient. At Re about 27,000 (Chapter 2) it is transitional, with separation bubbles, for any pitch. |

## References

Cited from general knowledge of the literature; chapter and page numbers not re-checked. The list grows with each chapter.

| Ref | Source | Used for | Chapters |
| --- | --- | --- | --- |
| \[1\] | Buckingham, E. (1914). On physically similar systems. *Physical Review*, 4(4), 345-376 | Pi theorem | 2 |
| \[2\] | McCormick, B. W. (1995). *Aerodynamics, Aeronautics, and Flight Mechanics*, 2nd ed. Wiley | Propeller coefficients C\_T, C\_P, J; blade element velocity triangle | 2, 8 |
| \[3\] | Leishman, J. G. (2006). *Principles of Helicopter Aerodynamics*, 2nd ed. Cambridge University Press | Momentum theory, wake development, figure of merit, modified momentum theory (kappa, profile power), ground effect | 1, 2, 3, 4 |
| \[4\] | Hoerner, S. F. (1965). *Fluid-Dynamic Drag*. Hoerner Fluid Dynamics | Drag coefficient of flat plates and strips normal to the flow; bluff-body drag areas | 1, 8 |
| \[5\] | Cheeseman, I. C. and Bennett, W. E. (1955). The effect of the ground on a helicopter rotor in forward flight. *ARC R&M 3021* | Ground effect formula | 2 |
| \[6\] | Brandt, J. B. and Selig, M. S. (2011). Propeller performance data at low Reynolds numbers. *AIAA 2011-1255* | Small propellers at low Re; FoM range; thrust against advance ratio | 2, 4, 8 |
| \[7\] | UIUC Propeller Data Site, m-selig.ae.illinois.edu/props | Measured small-propeller data | 2, 4, 8 |
| \[8\] | Commission Implementing Regulation (EU) 2019/947 | Open category A1, 250 g and 19 m/s limits | 1, 8 |
| \[9\] | Manufacturer test data, T-Motor P1604 3800 KV with Gemfan 3520-3 (journal Section 2) | Bench table | 0, 2, 3, 4, 5, 7 |
| \[10\] | Johnson, W. (2013). *Rotorcraft Aeromechanics*. Cambridge University Press | Hover momentum theory | 3 |
| \[11\] | Hanselman, D. (2006). *Brushless Permanent Magnet Motor Design*, 2nd ed. Magna Physics | Back-EMF and torque constants, K\_t = K\_e, loss mechanisms, torque scaling with air-gap shear stress | 4 |
| \[12\] | Hendershot, J. R. and Miller, T. J. E. (2010). *Design of Brushless Permanent-Magnet Machines*. Motor Design Books | Rewinding laws (Kv, K\_t, R against number of turns), iron losses | 4, 5 |
| \[13\] | Mohan, N., Undeland, T. M. and Robbins, W. P. (2003). *Power Electronics: Converters, Applications, and Design*, 3rd ed. Wiley | PWM, duty cycle, average voltage, converter power balance, switching losses | 4 |
| \[14\] | Montgomery, D. C. and Runger, G. C. (2014). *Applied Statistics and Probability for Engineers*, 6th ed. Wiley | Least squares, normal equations, regression through the origin | 2, 5 |
| \[15\] | Vig, J. R. (2004). Quartz crystal resonators and oscillators. US Army CERDEC tutorial | TCXO against OCXO | Appendix B |
| \[16\] | Hughes, A. and Drury, B. (2019). *Electric Motors and Drives*, 5th ed. Newnes | Motor basics for non-electrical engineers: back-EMF, Kv, PWM drives | 4 |
| \[17\] | Plett, G. L. (2015). *Battery Management Systems, Vol. 1: Battery Modeling*. Artech House | Battery as open-circuit voltage plus internal resistance; capacity, C-rate | 6, 7 |
| \[18\] | Biggs, J. M. (1964). *Introduction to Structural Dynamics*. McGraw-Hill | Dynamic load factor for step and ramp loads | 7 |
| \[19\] | Clough, R. W. and Penzien, J. (2003). *Dynamics of Structures*, 3rd ed. Computers and Structures | Single-degree-of-freedom response to ramp loading | 7 |
| \[20\] | Rao, S. S. (2017). *Mechanical Vibrations*, 6th ed. Pearson | Rotating unbalance, forced response and amplification, Campbell diagram | 9 |
| \[21\] | Embry-Riddle Aeronautical University, *Introduction to Aerospace Flight Vehicles*, chapter "Aircraft Propellers", eaglepubs.erau.edu | Blade element velocity triangles, thrust against advance ratio (open access, with figures) | 8 |
