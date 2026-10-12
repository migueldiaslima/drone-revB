# R11 - Q-T2 option B: local Tosca chain test WITHOUT inertia relief (Tosca 2022 does not allow it, F-13).
# Copies model revB_v03B to revB_v03B_NOIR; in the copy only:
#   - deletes the four inertia relief loads;
#   - adds 3-2-1 supports (RP_JNT_pp: U1 U2 U3, RP_JNT_pm: U1 U3, RP_JNT_mp: U3) in each static step,
#     not in FREQ (frequencies stay free-free);
#   - adds RF to F-Output-2;
#   - strain energy caps as 'fraction of initial value' 2.0 (the absolute caps come from the inertia relief run
#     and do not apply to supported, unbalanced loads);
#   - deletes GR_FROZEN (redundant, F-13);
# fixes C_F10 -> R_FREQ_10 in BOTH models if still wrong; creates optimization process TO_v03B_noIR (3 cycles).
# The original model revB_v03B keeps inertia relief and the absolute caps for the HPC.
from __future__ import print_function
from abaqus import *
from abaqusConstants import *

SRC, DST = 'revB_v03B', 'revB_v03B_NOIR'
STATIC = ('LC1', 'LC2a', 'LC2b', 'LC3a')
problems = []

def ok(label, cond, detail=''):
    print('%-48s %s %s' % (label, 'OK' if cond else '<<< CHECK', detail))
    if not cond:
        problems.append(label)

# ---------- 0. fix C_F10 in the source model ----------
def fix_cf10(model):
    t = mdb.models[model].optimizationTasks['TO_v03B']
    c = t.optimizationConstraints['C_F10']
    if c.designResponse != 'R_FREQ_10':
        c.setValues(designResponse='R_FREQ_10')
        print('%s: C_F10 re-pointed to R_FREQ_10' % model)
fix_cf10(SRC)
t0 = mdb.models[SRC].optimizationTasks['TO_v03B']
if 'GR_FROZEN' in t0.geometricRestrictions.keys():
    del t0.geometricRestrictions['GR_FROZEN']
    print('%s: GR_FROZEN deleted (redundant)' % SRC)

# ---------- 1. copy ----------
if DST in mdb.models.keys():
    del mdb.models[DST]
mdb.Model(name=DST, objectToCopy=mdb.models[SRC])
m = mdb.models[DST]
a = m.rootAssembly
ok('copy has task TO_v03B', 'TO_v03B' in m.optimizationTasks.keys())
t = m.optimizationTasks['TO_v03B']

# ---------- 2. remove inertia relief ----------
for n in [k for k in m.loads.keys() if k.startswith('IR_')]:
    del m.loads[n]
ok('no inertia relief loads left', len([k for k in m.loads.keys() if k.startswith('IR_')]) == 0)

# ---------- 3. 3-2-1 supports in each static step ----------
for s in STATIC:
    m.DisplacementBC(name='BC_A_' + s, createStepName=s, region=a.sets['SET_RP_JNT_pp'], u1=0.0, u2=0.0, u3=0.0)
    m.DisplacementBC(name='BC_B_' + s, createStepName=s, region=a.sets['SET_RP_JNT_pm'], u1=0.0, u3=0.0)
    m.DisplacementBC(name='BC_C_' + s, createStepName=s, region=a.sets['SET_RP_JNT_mp'], u3=0.0)
for s in ('FREQ',) + STATIC:
    st = m.steps[s].boundaryConditionStates
    act = sorted([k for k in st.keys() if str(st[k].status) in ('CREATED', 'PROPAGATED', 'MODIFIED')])
    exp = [] if s == 'FREQ' else sorted(['BC_A_' + s, 'BC_B_' + s, 'BC_C_' + s])
    ok('BCs active in %s' % s, act == exp, str(act))

# ---------- 4. RF output (static-step request is named F-STATIC in this model) ----------
print('field output requests in the copy: %s' % sorted(m.fieldOutputRequests.keys()))
# variables live in the step-dependent state, not on the request object
fo = m.fieldOutputRequests['F-STATIC']
for s_ in STATIC:
    try:
        st_ = m.steps[s_].fieldOutputRequestStates['F-STATIC']
    except Exception:
        continue
    v = list(st_.variables)
    print('  F-STATIC in %s (%s): %s' % (s_, st_.status, v))
    if 'RF' not in v:
        v.append('RF')
        fo.setValuesInStep(stepName=s_, variables=tuple(v))
for s_ in STATIC:
    try:
        vv = m.steps[s_].fieldOutputRequestStates['F-STATIC'].variables
    except Exception:
        vv = ()
    ok('F-STATIC has RF in ' + s_, 'RF' in vv, str(vv))

# ---------- 5. task in the copy ----------
fix_cf10(DST)
if 'GR_FROZEN' in t.geometricRestrictions.keys():
    del t.geometricRestrictions['GR_FROZEN']
for s in STATIC:
    t.optimizationConstraints['C_SE_' + s].setValues(restrictionMethod=RELATIVE_LESS_THAN_EQUAL, restrictionValue=2.0)
print('--- constraints in %s ---' % DST)
expf = dict([('C_F%d' % i, 'R_FREQ_%d' % i) for i in range(7, 13)])
for k in sorted(t.optimizationConstraints.keys()):
    c = t.optimizationConstraints[k]
    good = (expf.get(k) == c.designResponse and str(c.restrictionMethod) == 'ABSOLUTE_GREATER_THAN_EQUAL' and abs(c.restrictionValue - 417.0) < 1e-6) if k in expf \
        else (c.designResponse == 'R_' + k[2:] and str(c.restrictionMethod) == 'RELATIVE_LESS_THAN_EQUAL' and abs(c.restrictionValue - 2.0) < 1e-9)
    ok(k, good, '%s %s %s' % (c.designResponse, c.restrictionMethod, c.restrictionValue))
ok('restrictions = GR_ARMS only', sorted(t.geometricRestrictions.keys()) == ['GR_ARMS'], str(sorted(t.geometricRestrictions.keys())))
print('--- source model %s keeps inertia relief: %s' % (SRC, sorted([k for k in mdb.models[SRC].loads.keys() if k.startswith('IR_')])))

# ---------- 6. optimization process ----------
P = 'TO_v03B_noIR'
if P in mdb.optimizationProcesses.keys():
    del mdb.optimizationProcesses[P]
mdb.OptimizationProcess(name=P, model=DST, task='TO_v03B', prototypeJob=P + '-Job')
op = mdb.optimizationProcesses[P]
for kw in (dict(maxDesignCycle=3), dict(dataSaveFrequency=OPT_DATASAVE_EVERY_CYCLE),
           dict(numCpus=5, numDomains=5)):
    try:
        op.setValues(**kw)
        print('process %s: set %s' % (P, kw))
    except Exception as e:
        print('process %s: could not set %s (%s) - set it in the GUI' % (P, kw, e))
        problems.append('process ' + str(kw.keys()))
if problems:
    print('=== R11 finished with items to check: %s ===' % problems)
else:
    print('=== R11 done: all checks OK. Save, then Validate and Submit TO_v03B_noIR. ===')
