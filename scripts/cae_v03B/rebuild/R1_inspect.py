# R1 (v2) - read-only. Prints the full attribute list of one coupling, one tie and every load.
# Changes nothing. Send back the message-area text.
from __future__ import print_function
from abaqus import *
from abaqusConstants import *
m = mdb.models['revB_v03B']
a = m.rootAssembly
print('=== R1 inspect v2 ===')
print('--- CP_BATT ---')
print(m.constraints['CP_BATT'])
print('--- CP_MOT_pp ---')
print(m.constraints['CP_MOT_pp'])
print('--- TIE_pp_L ---')
print(m.constraints['TIE_pp_L'])
for n in sorted(m.loads.keys()):
    print('--- load %s ---' % n)
    print(m.loads[n])
print('inertias: %s' % sorted(a.engineeringFeatures.inertias.keys()))
print('=== end R1 ===')
