# R12 - DV-18 / F-14: add statically determinate 3-2-1 supports to every static step of revB_v03B,
# keeping inertia relief (as tested in T4: reactions ~0, ALLSE identical, no singularities).
# FREQ stays free-free. Adds RF to F-STATIC. Rewrites the H0 input revB_v03B_D056_ref.inp.
# Run in revB_v03B_D056.cae (saved), work directory = project folder.
from __future__ import print_function
from abaqus import *
from abaqusConstants import *
m = mdb.models['revB_v03B']
a = m.rootAssembly
STATIC = ('LC1', 'LC2a', 'LC2b', 'LC3a')
probs = []
def ok(label, cond, detail=''):
    print('%-44s %s %s' % (label, 'OK' if cond else '<<< CHECK', detail))
    if not cond:
        probs.append(label)

for k in [k for k in m.boundaryConditions.keys() if k.startswith('BC_')]:
    del m.boundaryConditions[k]
for s in STATIC:
    m.DisplacementBC(name='BC_A_' + s, createStepName=s, region=a.sets['SET_RP_JNT_pp'], u1=0.0, u2=0.0, u3=0.0)
    m.DisplacementBC(name='BC_B_' + s, createStepName=s, region=a.sets['SET_RP_JNT_pm'], u1=0.0, u3=0.0)
    m.DisplacementBC(name='BC_C_' + s, createStepName=s, region=a.sets['SET_RP_JNT_mp'], u3=0.0)
for s in ('FREQ',) + STATIC:
    st = m.steps[s].boundaryConditionStates
    act = sorted([k for k in st.keys() if str(st[k].status) in ('CREATED', 'PROPAGATED', 'MODIFIED')])
    exp = [] if s == 'FREQ' else sorted(['BC_A_' + s, 'BC_B_' + s, 'BC_C_' + s])
    ok('supports active in ' + s, act == exp, str(act))
ir = sorted([k for k in m.loads.keys() if k.startswith('IR_')])
ok('inertia relief kept', ir == ['IR_LC1', 'IR_LC2a', 'IR_LC2b', 'IR_LC3a'], str(ir))
v = list(m.steps['LC1'].fieldOutputRequestStates['F-STATIC'].variables)
if 'RF' not in v:
    v.append('RF')
    m.fieldOutputRequests['F-STATIC'].setValuesInStep(stepName='LC1', variables=tuple(v))
for s in STATIC:
    ok('F-STATIC has RF in ' + s, 'RF' in m.steps[s].fieldOutputRequestStates['F-STATIC'].variables)
t = m.optimizationTasks['TO_v03B']
ok('task: no frozen restriction, arms symmetry only', sorted(t.geometricRestrictions.keys()) == ['GR_ARMS'])
mdb.jobs['revB_v03B_D056_ref'].writeInput(consistencyChecking=OFF)
print('H0 input rewritten: revB_v03B_D056_ref.inp')
print('=== R12 %s ===' % ('done: all OK. Save, then Write Files for TO_v03B_H1.' if not probs else 'items to check: %s' % probs))
