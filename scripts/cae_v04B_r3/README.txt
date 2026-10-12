Stage 6 v04-B revision 3 (D-083 to D-085, build log item 46). Scripts: cae_v04B_r3 (laptop, CAE 2022),
cae_v04B/V2_mesh.py (unchanged), hpc/r3 and hpc/G7, hpc/H4 (nexus, Abaqus 2024).

Laptop
 1. Put the folder holding geometry/v04B_r3/*.step in v04B_r3_paths.txt next to V1r3_build.py.
 2. Open revB_v03B_D056.cae, File > Save As revB_v04B_r3.cae, File > Run Script V1r3_build.py
    -> must end "V1r3 done: all checks OK". Save.
 3. V2_mesh.py with LEVEL = 'debug' -> "G6 PASS". Save.
 4. V3r3_jobs.py -> G7a_r3_ref.inp, G7b_r3_ref.inp. Save.
 5. File > Save As revB_v04B_r3_m10.cae; V2_mesh.py with LEVEL = 'prod' -> "G6 PASS"; W2r3_H4.py;
    Optimization Process Manager > Create TO_v04B_r3_H4 (model revB_v04B_G7b, data save last + every 10th,
    max 60 cycles) > Write Files. Save.
 6. Copy G7a_r3_ref.inp, G7b_r3_ref.inp, TO_v04B_r3_H4.par, TO_v04B_r3_H4-Job.inp to nexus
    ~/drone_revB/stage6/r3/inputs.

nexus
 7. Scripts to ~/drone_revB/stage6/scripts: run_G7r3.sh, run_H4r3.sh, g7_check.py, h4_check.py
    (cyclecheck.py, seatcheck.py already there).
 8. Reference jobs: mkdir -p ~/drone_revB/stage6/r3/G7 && cd ~/drone_revB/stage6/r3/G7 &&
    setsid nohup bash ~/drone_revB/stage6/scripts/run_G7r3.sh 30 > G7r3_all.log 2>&1 &
 9. H4 after the reference jobs pass: bash ~/drone_revB/stage6/scripts/run_H4r3.sh 60
10. History and cycle 0 ALLSE: cd /tmp/mdias_H4r3 && abaqus python ~/drone_revB/stage6/scripts/h4_check.py TO_v04B_r3_H4 rel
