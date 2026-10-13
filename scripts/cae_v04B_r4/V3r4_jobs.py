# V3r4 - reference job for v04-B revision 4 (G7b only: seat tie TIE_LIDRIM; the five-boss G7a needs the lid pad
# circles, deferred to Stage 7, D-082 item 3). Run in revB_v04B_r4.cae after V2 debug. Based on V3r3:
#   (G7a_r4_ref not written in rev 4)
#   G7b_r4_ref.inp : copy revB_v04B_G7b, the five boss ties replaced by one tie over the whole lid seat:
#                 main = LID bottom (z 21.5), secondary = TUB top faces under the lid (rev 4: 363.23 mm^2, 4 boss annuli incl.)
# Run after V2 (debug) in revB_v04B_r4.cae, work directory = the folder for the inputs.
from __future__ import print_function
from abaqus import *
from abaqusConstants import *

m = mdb.models['revB_v04B']
for job, model in (('G7b_r4_ref', 'revB_v04B_G7b'),):
    if job in mdb.jobs.keys():
        del mdb.jobs[job]
if 'revB_v04B_G7b' in mdb.models.keys():
    del mdb.models['revB_v04B_G7b']
mdb.Model(name='revB_v04B_G7b', objectToCopy=m)
mb = mdb.models['revB_v04B_G7b']
if [k for k in mb.constraints.keys() if k.startswith('TIE_LID')]:
    raise Exception('V3r4 STOPPED: lid ties found in revB_v04B (V1r4 makes none)')
ab = mb.rootAssembly
for k in [k for k in mb.constraints.keys() if k.startswith('TIE_LID_')]:
    del mb.constraints[k]
mb.Tie(name='TIE_LIDRIM', main=ab.instances['LID-1'].surfaces['S_LID_BOTTOM'],
       secondary=ab.instances['TUB-1'].surfaces['S_RIM_UNDER_LID'], positionToleranceMethod=SPECIFIED,
       positionTolerance=0.1, adjust=OFF, tieRotations=OFF, constraintEnforcement=SURFACE_TO_SURFACE, thickness=ON)
for job, model in (('G7b_r4_ref', 'revB_v04B_G7b'),):
    mm = mdb.models[model]
    ties = sorted([k for k in mm.constraints.keys() if k.startswith('TIE_')])
    print('%s: %d ties (%s)' % (job, len(ties), ', '.join([t for t in ties if 'LID' in t])))
    mdb.Job(name=job, model=model, type=ANALYSIS)
    mdb.jobs[job].writeInput(consistencyChecking=OFF)
    print('%s.inp written' % job)
print('=== V3 done: copy G7b_r4_ref.inp to nexus (~/drone_revB/stage6/r4/inputs). Save the model. ===')
