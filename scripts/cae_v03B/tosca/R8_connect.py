# R8 - (D-059 version of R3) recreates the 11 couplings, 8 ties and the LC3a floor pressure on the new instances (same names and settings).
from __future__ import print_function
from abaqus import *
from abaqusConstants import *
m = mdb.models['revB_v03B']
a = m.rootAssembly
B = a.instances['BODY-1']
C = ['pp', 'pm', 'mp', 'mm']

def stop(msg):
    raise Exception('R8 STOPPED: ' + msg)

cp = [('CP_BATT', 'SET_RP_BATT', B, 'S_BATT_SEAT'),
      ('CP_FC', 'SET_RP_FC', B, 'S_FC_SEAT'),
      ('CP_GPS', 'SET_RP_GPS', B, 'S_GPS_SEAT')]
for c in C:
    arm = a.instances['ARM_%s-1' % c]
    cp.append(('CP_MOT_' + c, 'SET_RP_MOT_' + c, arm, 'S_MOT_SEAT'))
    cp.append(('CP_JNT_' + c, 'SET_RP_JNT_' + c, arm, 'S_JNT'))
missing = [s for (n, s, i, f) in cp if s not in a.sets.keys()]
if missing:
    stop('RP sets not found: %s; assembly sets are %s' % (missing, sorted(a.sets.keys())))

# clean re-run: remove anything a previous partial run created
for n in [k for k in m.constraints.keys() if k.startswith('CP_') or k.startswith('TIE_')]:
    del m.constraints[n]
if 'LC3a_P' in m.loads.keys():
    del m.loads['LC3a_P']

for n, rpset, inst, surf in cp:
    m.Coupling(name=n, controlPoint=a.sets[rpset], surface=inst.surfaces[surf],
               influenceRadius=WHOLE_SURFACE, couplingType=DISTRIBUTING,
               adjust=False, weightingMethod=UNIFORM,
               localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)

for c in C:
    arm = a.instances['ARM_%s-1' % c]
    for s in ('L', 'R'):
        m.Tie(name='TIE_%s_%s' % (c, s),
              main=arm.surfaces['S_PRONG_BOSS_%s' % s],
              secondary=B.surfaces['S_FIN_BOSS_%s_%s' % (c, s)],
              positionToleranceMethod=SPECIFIED, positionTolerance=0.3,
              adjust=OFF, tieRotations=OFF, constraintEnforcement=SURFACE_TO_SURFACE, thickness=ON)

m.Pressure(name='LC3a_P', createStepName='LC3a', region=B.surfaces['S_FLOOR'],
           distributionType=UNIFORM, field='', magnitude=0.03525)

# ---- checks ----
print('=== R8 checks ===')
for n, rpset, inst, surf in cp:
    k = m.constraints[n]
    print('%-10s %s %s dof %s  ->  %s.%s' % (n, k.couplingType, k.weightingMethod,
          (k.u1, k.u2, k.u3, k.ur1, k.ur2, k.ur3), inst.name, surf))
for c in C:
    for s in ('L', 'R'):
        k = m.constraints['TIE_%s_%s' % (c, s)]
        print('TIE_%s_%s  tol %s %s adjust %s rot %s' % (c, s, k.positionToleranceMethod,
              k.positionTolerance, k.adjust, k.tieRotations))
st = m.steps['LC3a'].loadStates['LC3a_P']
print('LC3a_P magnitude %s, status %s; other steps: %s' % (st.magnitude, st.status,
      [(sn, m.steps[sn].loadStates['LC3a_P'].status) for sn in ('LC1', 'LC2a', 'LC2b')
       if 'LC3a_P' in m.steps[sn].loadStates.keys()]))
print('constraints: %d couplings, %d ties' % (len([k for k in m.constraints.keys() if k.startswith('CP_')]),
      len([k for k in m.constraints.keys() if k.startswith('TIE_')])))
print('=== R8 done. Save the model, then run R9_mesh.py. ===')
