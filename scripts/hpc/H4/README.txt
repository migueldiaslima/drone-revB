Stage 6 v04-B: H4c (D-082, lid tied over the seat)

Laptop (revB_v04B.cae, debug mesh):
 1. W1_task.py with STAGE = 'H4c'  -> must end "W1 H4c: task ready"; save
 2. Job module > Optimization Process Manager > Create: name TO_v04B_H4c, model revB_v04B_G7b,
    task as printed; Data Save: last cycle + every 10th (as H3); then Write Files
 3. copy TO_v04B_H4c.par and TO_v04B_H4c-Job.inp to nexus ~/drone_revB/stage6/inputs

nexus:
 4. scripts to ~/drone_revB/stage6/scripts (run_H4c.sh, h4_check.py, cyclecheck.py, seatcheck.py, allwk_check.py)
 5. mkdir -p ~/drone_revB/stage6/H4c && cd ~/drone_revB/stage6/H4c && bash ../scripts/run_H4c.sh 54
 6. at the end (or any time):  abaqus python ../scripts/h4_check.py TO_v04B_H4c H4c
    on the last saved odb:     abaqus python ../scripts/cyclecheck.py <odb>   and   seatcheck.py <odb>
 Optional (D-082 item 3): abaqus python ../scripts/allwk_check.py ../H3ref/H3_ref.odb
