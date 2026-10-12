# V3r3 - reference jobs for v04-B revision 3 (as V3, job names with _r3; run in revB_v04B_r3.cae after V2 debug):
#   G7a_r3_ref.inp : model revB_v04B, lid tied at the five screw bosses only (TIE_LID_1..5)
#   G7b_r3_ref.inp : copy revB_v04B_G7b, the five boss ties replaced by one tie over the whole lid seat:
#                 main = LID bottom (z 21.5), secondary = TUB top faces under the lid (626 mm^2, bosses incl.)
# Run after V2 (debug) in revB_v04B.cae, work directory = the folder for the inputs.
from __future__ import print_function
from abaqus import *
from abaqusConstants import *

m = mdb.models['revB_v04B']
for job, model in (('G7a_r3_ref', 'revB_v04B'), ('G7b_r3_ref', 'revB_v04B_G7b')):
    if job in mdb.jobs.keys():
        del mdb.jobs[job]
if 'revB_v04B_G7b' in mdb.models.keys():
    del mdb.models['revB_v04B_G7b']
mdb.Model(name='revB_v04B_G7b', objectToCopy=m)
mb = mdb.models['revB_v04B_G7b']
ab = mb.rootAssembly
for k in [k for k in mb.constraints.keys() if k.startswith('TIE_LID_')]:
    del mb.constraints[k]
mb.Tie(name='TIE_LIDRIM', main=ab.instances['LID-1'].surfaces['S_LID_BOTTOM'],
       secondary=ab.instances['TUB-1'].surfaces['S_RIM_UNDER_LID'], positionToleranceMethod=SPECIFIED,
       positionTolerance=0.1, adjust=OFF, tieRotations=OFF, constraintEnforcement=SURFACE_TO_SURFACE, thickness=ON)
for job, model in (('G7a_r3_ref', 'revB_v04B'), ('G7b_r3_ref', 'revB_v04B_G7b')):
    mm = mdb.models[model]
    ties = sorted([k for k in mm.constraints.keys() if k.startswith('TIE_')])
    print('%s: %d ties (%s)' % (job, len(ties), ', '.join([t for t in ties if 'LID' in t])))
    mdb.Job(name=job, model=model, type=ANALYSIS)
    mdb.jobs[job].writeInput(consistencyChecking=OFF)
    print('%s.inp written' % job)
print('=== V3 done: copy G7a_r3_ref.inp and G7b_r3_ref.inp to nexus (~/drone_revB/stage6/r3/inputs). Save the model. ===')
