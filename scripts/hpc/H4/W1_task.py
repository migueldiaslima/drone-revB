# W1 - Tosca task for H4c / H4 on the G7b model (D-082: lid tied over the whole seat, DV-23 tie).
# Set STAGE first:
#   'H4c' : run in revB_v04B.cae (debug mesh). Uses model revB_v04B_G7b as written by V3.
#           Caps = 2 x G7b ALLSE (D-082): 0.216635 / 0.200186 / 0.102227 / 0.394042 N mm. No member size.
#   'H4ref': run in revB_v04B_m10.cae (1.0 mm mesh). Re-creates revB_v04B_G7b from revB_v04B (the copy
#           saved in this file still has the debug mesh) and writes H4_ref.inp. Caps are set later (H4).
#   'H4'  : run in revB_v04B_m10.cae after H4_ref. Set CAPS_H4 from the H4_ref check. Member size
#           GR_MS (2.5 mm, DESIGN_ALL) must exist: the script checks it and stops if not.
# The script re-points every task region to the v04-B sets, sets the strain-energy caps and prints
# the task for the build log. The optimization process is then created by hand (section at the end).
from __future__ import print_function
from abaqus import *
from abaqusConstants import *

STAGE = 'H4c'                                                    # <-- 'H4c', 'H4ref' or 'H4'
CAPS_H4C = {'LC1': 0.216635, 'LC2a': 0.200186, 'LC2b': 0.102227, 'LC3a': 0.394042}
CAPS_H4 = {'LC1': None, 'LC2a': None, 'LC2b': None, 'LC3a': None}   # <-- from h4ref_check (2 x ALLSE)
MODEL = 'revB_v04B_G7b'


def stop(msg):
    raise Exception('W1 STOPPED: ' + msg)


def count_el(mm):
    n = 0
    for pn in ('TUB', 'LID', 'ARM'):
        n += len(mm.parts[pn].elements) * (4 if pn == 'ARM' else 1)
    return n


def make_g7b():
    src = mdb.models['revB_v04B']
    if MODEL in mdb.models.keys():
        del mdb.models[MODEL]
    mdb.Model(name=MODEL, objectToCopy=src)
    mb = mdb.models[MODEL]
    ab = mb.rootAssembly
    for k in [k for k in mb.constraints.keys() if k.startswith('TIE_LID_')]:
        del mb.constraints[k]
    mb.Tie(name='TIE_LIDRIM', main=ab.instances['LID-1'].surfaces['S_LID_BOTTOM'],
           secondary=ab.instances['TUB-1'].surfaces['S_RIM_UNDER_LID'], positionToleranceMethod=SPECIFIED,
           positionTolerance=0.1, adjust=OFF, tieRotations=OFF, constraintEnforcement=SURFACE_TO_SURFACE,
           thickness=ON)
    return mb


def setup_task():
    if MODEL not in mdb.models.keys():
        stop('model %s not found (run V3 first)' % MODEL)
    m = mdb.models[MODEL]
    a = m.rootAssembly
    ties = sorted([k for k in m.constraints.keys() if k.startswith('TIE_')])
    print('ties: %s' % ', '.join(ties))
    if 'TIE_LIDRIM' not in ties or any(k.startswith('TIE_LID_') for k in ties):
        stop('model %s does not have the G7b seat tie only' % MODEL)
    ne = count_el(m)
    exp = 175232 if STAGE == 'H4c' else 768232
    print('mesh: %d elements (expected %d for %s)' % (ne, exp, STAGE))
    if ne != exp:
        stop('wrong mesh for %s' % STAGE)

    tn = list(m.optimizationTasks.keys())
    if len(tn) != 1:
        stop('expected one optimization task, found %s' % tn)
    t = m.optimizationTasks[tn[0]]
    print('task %s' % tn[0])
    for label, fn in (('task region -> DESIGN_ALL', lambda: t.setValues(region=a.sets['DESIGN_ALL'])),):
        try:
            fn()
            print('%-34s OK' % label)
        except Exception as e:
            stop('%s: %s' % (label, e))
    for k, g in t.geometricRestrictions.items():
        try:
            if 'ARM' in k.upper() or 'SYM' in str(type(g)).upper():
                g.setValues(region=a.sets['DESIGN_ARMS'])
                print('restriction %-22s -> DESIGN_ARMS OK' % k)
            else:
                g.setValues(region=a.sets['DESIGN_ALL'])
                print('restriction %-22s -> DESIGN_ALL OK' % k)
        except Exception as e:
            stop('restriction %s: %s' % (k, e))
    for k, r in t.designResponses.items():
        try:
            if 'VOL' in k.upper():
                r.setValues(region=a.sets['DESIGN_ALL'])
                print('response %-25s -> DESIGN_ALL OK' % k)
        except Exception as e:
            stop('response %s: %s' % (k, e))

    caps = CAPS_H4C if STAGE == 'H4c' else CAPS_H4
    if None in caps.values():
        stop('set CAPS_H4 from the H4_ref check first')
    nset = 0
    for k, c in t.optimizationConstraints.items():
        dr = c.designResponse
        for lc, cap in caps.items():
            if dr.upper().endswith('SE_' + lc.upper()):
                c.setValues(restrictionMethod=ABSOLUTE_LESS_THAN_EQUAL, restrictionValue=cap)
                nset += 1
    if nset != 4:
        stop('%d strain-energy constraints updated, expected 4' % nset)

    gr = sorted(t.geometricRestrictions.keys())
    ms = [k for k in gr if k.upper() == 'GR_MS' or 'MEMBER' in k.upper() or 'MEMBER' in str(type(t.geometricRestrictions[k])).upper()]
    if STAGE == 'H4c' and ms:
        stop('member size restriction %s present: H4c runs without member size (C-5); delete it' % ms)
    if STAGE == 'H4' and not ms:
        stop('create the member size restriction GR_MS (minimum 2.5 mm, region DESIGN_ALL) as in H3, then re-run')

    print('--- task for the build log ---')
    for k, r in sorted(t.designResponses.items()):
        print('response   %-12s %s' % (k, ', '.join('%s=%s' % (x, getattr(r, x)) for x in ('identifier', 'operation', 'stepOptions')
                                                    if hasattr(r, x))[:140]))
    for k, c in sorted(t.optimizationConstraints.items()):
        print('constraint %-12s %-14s %-28s %s' % (k, c.designResponse, c.restrictionMethod, c.restrictionValue))
    print('restrictions: %s' % ', '.join(gr))
    print('=== W1 %s: task ready. Save, then create the optimization process by hand (see the end of W1). ===' % STAGE)


if STAGE == 'H4ref':
    mb = make_g7b()
    ne = count_el(mb)
    print('%s re-created from revB_v04B: %d elements (1.0 mm mesh expected 768,232)' % (MODEL, ne))
    if abs(ne - 768232) > 0:
        stop('element count %d, expected 768232: is the 1.0 mm mesh in revB_v04B?' % ne)
    if 'H4_ref' in mdb.jobs.keys():
        del mdb.jobs['H4_ref']
    mdb.Job(name='H4_ref', model=MODEL, type=ANALYSIS)
    mdb.jobs['H4_ref'].writeInput(consistencyChecking=OFF)
    print('=== W1 H4ref: H4_ref.inp written. Save the model, run H4_ref on nexus (run_H4ref.sh). ===')

else:
    setup_task()
# Process (Job module > Optimization Process Manager > Create):
#   name TO_v04B_H4c (or TO_v04B_H4), model revB_v04B_G7b, task as printed above;
#   Data Save: last cycle and every 10th cycle (as H3); maximum cycles 60; then Write Files.
#   Copy TO_v04B_<stage>.par and TO_v04B_<stage>-Job.inp to nexus ~/drone_revB/stage6/inputs.
