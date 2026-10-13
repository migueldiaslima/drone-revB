# Receiver cradle v1 (production part, pending three measurements)

Main chat, 2026-10-13. Generator `scripts/geometry_main/s07_receiver_cradle.py`; renders `scripts/figures/rx_cradle_render.py`, `figures/rx_cradle_1..4.png`. Files `geometry/retainers/`: RX_CRADLE_v1.step (model frame), RX_CRADLE_v1_TPU.stl (print frame, floor on the bed; git-ignored, sent to Miguel), rx_cradle_checks.json. Basis: brief v04-B section 5.1, D-073, D-074.

## Part

| Item | Value |
|---|---|
| Material | TPU 95A HF (snap walls deflect 0.6 mm; root strain about 6 % in a 1.2 mm wall over 4.1 mm, too much for PET-CF) |
| Pocket | 19.0 x 11.0 (receiver 18.4 x 10.4 + 0.3 per side), floor z +4.1 to +5.5, inside y +2.45 to +13.45 |
| Snap lips | both side walls, x -6 to +6, 0.9 over the wall face (0.6 over the PCB edge), underside 0.1 above the receiver top, 45 deg lead-in; wall top z +10.8 |
| End stops | both ends, up to the PCB top (1.0 above the floor), from the -y wall to y +9.75; wires and the IPEX lead leave over them |
| Ears | dia 5.8 x 1.4 at (+-12.75, +12.75), hole dia 2.4 (M2, TPU), clamped between the anti-loosening nut and the nylon nut |
| Mass, CG | 731.8 mm^3, 0.89 g (density 1.21e-3 g/mm^3 assumed, as the antenna holder); CG (0, 8.24, 6.06) |

## Checks (all pass)

One solid; no overlap with the receiver envelope; no interference with any v04-B component dummy, the TUB or the LID; C-5 capacitor 1.75 mm; C-6 floor to the FC parts envelope 0.30 mm (envelope z <= +3.8, Q-60 still open); ears seated on the lock nuts and under the nylon nuts; screw clearance 0.2 mm radial; IPEX lead leaving above the PCB top clears the end stop; TUB 4.85 mm, LID 10.7 mm, K8 entry 6.6 mm; free radius around each nylon nut above the ear 3.4 mm (nut driver OD at most 6.8 mm, otherwise a 4 mm open-end wrench, or hold the nut and turn the screw from below); STL manifold, no open edges.

## Open inputs (Miguel)

| Q | Input | Effect |
|---|---|---|
| Q-61 | Receiver thickness: PCB edge, maximum over components, with heat shrink | lip height (now from the 4.0 mm allowance) and end stop height (now PCB 1.0 assumed) |
| Q-62 | Receiver layout: IPEX end, pad end, button and LED | lip extent x -6 to +6 and orientation (IPEX now towards -x, the K8 entry) |
| Q-60 | FC parts height in x +-11, y +1 to +15 | floor level (now +4.1, needs parts <= +3.8) |

## For the set-up chat

The cradle stays in the RP_FC lump (receiver 0.7 g and cradle there since rev 2). Mass 0.89 g against the 0.87 g estimate in the v04-B export note (+0.02 g), CG at (0, 8.2, 6.1) against RP_FC at (0, 0, 0): no change to the export.

## Print and assembly

Floor on the bed, TPU 95A HF, 0.4 nozzle, 0.2 mm layers, 100 % infill (3 lines per wall), no supports (lip underside overhang 0.9 mm). Assembly step 7 of the brief: ears over the pp and mp screws onto the anti-loosening nuts, nylon nuts, then press the receiver in from above (IPEX end towards -x); plug the IPEX lead in step 10 from above between the lips.
