# allwk_check.py - optional (D-082 item 3): ALLSE against ALLWK per static step of a reference odb.
#   abaqus python allwk_check.py H0_ref.odb      (any odb of a plain reference job)
from __future__ import print_function
import sys, os
from odbAccess import openOdb
o = openOdb(os.path.abspath(sys.argv[-1]), readOnly=True)
bcs = 'yes' if any('BC_' in k.upper() for k in o.steps.keys()) else '?'
for sn in ('LC1', 'LC2a', 'LC2b', 'LC3a'):
    if sn not in o.steps.keys():
        continue
    hr = [r for k, r in o.steps[sn].historyRegions.items() if k.startswith('Assembly')][0]
    se = hr.historyOutputs['ALLSE'].data[-1][1]
    wk = hr.historyOutputs['ALLWK'].data[-1][1] if 'ALLWK' in hr.historyOutputs.keys() else float('nan')
    print('%-5s ALLSE %.6g  ALLWK %.6g  ratio %.3f' % (sn, se, wk, wk / se))
o.close()
