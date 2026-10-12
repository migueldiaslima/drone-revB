# R10 - read-only. Inertia relief smoke test (D-041): reads revB_v03B_IR321.odb (LC1 with inertia relief
# and 3-2-1 supports on RP_JNT_pp / pm / mp) and compares with the free LC1 of revB_v03B_D056_ref.odb.
from __future__ import print_function
from odbAccess import openOdb
import os
REF_ALLSE = 0.090893      # LC1, revB_v03B_D056_ref, N mm
o = openOdb(os.path.abspath('revB_v03B_IR321.odb'), readOnly=True)
s = o.steps['LC1']
hr = [r for k, r in s.historyRegions.items() if k.startswith('Assembly')]
ho = hr[0].historyOutputs
se = ho['ALLSE'].data[len(ho['ALLSE'].data) - 1][1]
print('=== R10: inertia relief + 3-2-1 supports, LC1 ===')
print('ALLSE %.6g N mm | free run %.6g | difference %.3f %%' % (se, REF_ALLSE, 100.0 * (se - REF_ALLSE) / REF_ALLSE))
fr = s.frames[len(s.frames) - 1]
if 'RF' not in fr.fieldOutputs.keys():
    print('RF not in the field output: add RF to F-Output-2 and re-run')
else:
    rf = fr.fieldOutputs['RF']
    tot = [0.0, 0.0, 0.0]
    ra = o.rootAssembly
    for nm in ('SET_RP_JNT_PP', 'SET_RP_JNT_PM', 'SET_RP_JNT_MP'):
        key = [k for k in ra.nodeSets.keys() if k.upper() == nm]
        if not key:
            print('%s: node set not found in the odb' % nm)
            continue
        sub = rf.getSubset(region=ra.nodeSets[key[0]])
        for v in sub.values:
            print('%-14s RF = (%+.3e, %+.3e, %+.3e) N' % (nm, v.data[0], v.data[1], v.data[2]))
            for i in range(3):
                tot[i] += v.data[i]
    print('sum of reactions = (%+.3e, %+.3e, %+.3e) N; applied net thrust 20.16 N' % tuple(tot))
o.close()
print('=== end R10 ===')
