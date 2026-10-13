# W2r4 - as W2r3, for v04-B revision 4 (D-086); W2r3 header follows. W2r3 - as W2, for v04-B revision 3 (D-083 caps 2.0 x cycle 0), in revB_v04B_r4_m10.cae; the 1.0 mm
# element count is not known in advance: the script requires more than 500,000 elements (debug about
# 175,000) and prints the count for the build log. Process name TO_v04B_r4_H4.
#
# Original W2 header: H4 production task in one step (DV-25: H4c skipped, caps relative 2.0 x cycle 0 = D-063 on the
# same mesh). Run in revB_v04B_r4_m10.cae (1.0 mm mesh in model revB_v04B). It:
#   1. re-creates revB_v04B_G7b from revB_v04B (seat tie TIE_LIDRIM, 1.0 mm mesh, 768,232 elements);
#   2. re-points the task regions (DESIGN_ALL, DESIGN_ARMS, R_VOL);
#   3. sets the 4 strain-energy constraints to RELATIVE <= 2.0 (cycle 0 = solid reference on this mesh);
#   4. creates the member size restriction GR_MS (minimum 2.5 mm, DESIGN_ALL) if it does not exist.
# Then create the optimization process by hand (end of this file).
from __future__ import print_function
from abaqus import *
from abaqusConstants import *

MODEL = 'revB_v04B_G7b'


def stop(msg):
    raise Exception('W2 STOPPED: ' + msg)


src = mdb.models['revB_v04B']
n = 0
for pn in ('TUB', 'LID', 'ARM'):
    n += len(src.parts[pn].elements) * (4 if pn == 'ARM' else 1)
print('revB_v04B mesh: %d elements (1.0 mm mesh: rev 2 had 768,232)' % n)
if n < 500000:
    stop('revB_v04B does not hold the 1.0 mm mesh: open revB_v04B_r4_m10.cae')
if 'CP_ANT' not in src.constraints.keys():
    stop('CP_ANT missing: this is not the revision 3 model')
if 'S_GPS_SEAT' not in src.parts['TUB'].surfaces.keys():
    stop('S_GPS_SEAT not on the TUB: this is not the revision 4 model')
if MODEL in mdb.models.keys():
    del mdb.models[MODEL]
mdb.Model(name=MODEL, objectToCopy=src)
m = mdb.models[MODEL]
a = m.rootAssembly
for k in [k for k in m.constraints.keys() if k.startswith('TIE_LID_')]:
    del m.constraints[k]
m.Tie(name='TIE_LIDRIM', main=a.instances['LID-1'].surfaces['S_LID_BOTTOM'],
      secondary=a.instances['TUB-1'].surfaces['S_RIM_UNDER_LID'], positionToleranceMethod=SPECIFIED,
      positionTolerance=0.1, adjust=OFF, tieRotations=OFF, constraintEnforcement=SURFACE_TO_SURFACE, thickness=ON)
print('ties: %s' % ', '.join(sorted(k for k in m.constraints.keys() if k.startswith('TIE_'))))

t = m.optimizationTasks[list(m.optimizationTasks.keys())[0]]
t.setValues(region=a.sets['DESIGN_ALL'])
for k, g in t.geometricRestrictions.items():
    if 'ARM' in k.upper():
        g.setValues(region=a.sets['DESIGN_ARMS'])
for k, r in t.designResponses.items():
    if 'VOL' in k.upper():
        r.setValues(region=a.sets['DESIGN_ALL'])
print('task regions re-pointed')
nset = 0
for k, c in t.optimizationConstraints.items():
    if 'SE_LC' in c.designResponse.upper():
        c.setValues(restrictionMethod=RELATIVE_LESS_THAN_EQUAL, restrictionValue=2.0)
        nset += 1
if nset != 4:
    stop('%d strain-energy constraints set, expected 4' % nset)
if 'GR_MS' not in t.geometricRestrictions.keys():
    try:
        t.TopologyMemberSize(name='GR_MS', region=a.sets['DESIGN_ALL'], minThickness=2.5, sizeRestriction=MINIMUM)
        print('GR_MS created by script')
    except Exception as e:
        print('GR_MS NOT created by script (%s): create it by hand, see below' % e)
print('--- task ---')
for k, c in sorted(t.optimizationConstraints.items()):
    print('constraint %-12s %-14s %-28s %s' % (k, c.designResponse, c.restrictionMethod, c.restrictionValue))
print('restrictions: %s' % ', '.join(sorted(t.geometricRestrictions.keys())))
print('=== W2 done. If GR_MS is missing above: Optimization module > Create Geometric Restriction > Member Size,')
print('    region DESIGN_ALL, minimum thickness 2.5 (as H3). Then save and create the process. ===')
# Process: Job module > Optimization Process Manager > Create: name TO_v04B_r4_H4, model revB_v04B_G7b,
# task as printed; Data Save: last cycle + every 10th; Write Files; copy TO_v04B_r4_H4.par and
# TO_v04B_r4_H4-Job.inp to nexus ~/drone_revB/stage6/r4/inputs.
