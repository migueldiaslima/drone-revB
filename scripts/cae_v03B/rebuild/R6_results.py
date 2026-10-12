# R6 - read-only. Summary of the reference run revB_v03B_ref.odb:
# frequencies (modes 1 to 12), ALLSE / ALLWK per static step, C_i,0 = 2 ALLSE, max |U| per step.
from __future__ import print_function
from odbAccess import openOdb
import os
o = openOdb(os.path.abspath('revB_v03B_ref.odb'), readOnly=True)
print('=== R6 results ===')
st = o.steps['FREQ']
print('FREQ: %d modes' % (len(st.frames) - 1))
nf = len(st.frames)
for i in range(1, min(13, nf)):
    print('  %s' % st.frames[i].description)
for sn in ('LC1', 'LC2a', 'LC2b', 'LC3a'):
    s = o.steps[sn]
    hr = [r for k, r in s.historyRegions.items() if k.startswith('Assembly')]
    se = wk = None
    if hr:
        ho = hr[0].historyOutputs
        if 'ALLSE' in ho.keys():
            se = ho['ALLSE'].data[-1][1]
        if 'ALLWK' in ho.keys():
            wk = ho['ALLWK'].data[-1][1]
    fr = s.frames[len(s.frames) - 1]
    umax = 0.0; where = ''
    for v in fr.fieldOutputs['U'].values:
        if v.magnitude > umax:
            umax = v.magnitude; where = '%s.%d' % (v.instance.name if v.instance else '', v.nodeLabel)
    if se is None:
        print('%-5s ALLSE not found (history keys: %s)' % (sn, hr[0].historyOutputs.keys() if hr else 'none'))
    else:
        print('%-5s ALLSE %.5g N mm | C0 = 2 ALLSE = %.5g N mm | ALLWK %s | max |U| %.4g mm at %s' % (
            sn, se, 2 * se, ('%.5g' % wk) if wk is not None else 'n/a', umax, where))
o.close()
print('=== end R6 ===')
