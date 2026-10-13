Stage 6 v04-B revision 4 (D-086, build log item 48). Scripts: cae_v04B_r4 (laptop, CAE 2022),
cae_v04B/V2_mesh.py (unchanged), hpc/r4, hpc/G7/g7_check.py, hpc/H4/h4_check.py (nexus, Abaqus 2024).

Laptop
 1. Put the full path of the folder holding geometry/v04B_r4/*.step in v04B_r4_paths.txt next to V1r4_build.py.
 2. Open revB_v03B_D056.cae, File > Save As revB_v04B_r4.cae, File > Run Script V1r4_build.py
    -> must end "V1r4 done: all checks OK". Save.
 3. V2_mesh.py with LEVEL = 'debug' -> "G6 PASS". Save.
 4. V3r4_jobs.py -> G7b_r4_ref.inp. Save.
 5. File > Save As revB_v04B_r4_m10.cae; V2_mesh.py with LEVEL = 'prod' -> "G6 PASS"; W2r4_H4.py;
    Optimization Process Manager > Create TO_v04B_r4_H4 (model revB_v04B_G7b, data save last + every 10th,
    max 60 cycles) > Write Files. Save.
 6. Copy G7b_r4_ref.inp, TO_v04B_r4_H4.par, TO_v04B_r4_H4-Job.inp to nexus ~/drone_revB/stage6/r4/inputs.

nexus (scripts straight from the repo: curl -fsSL https://raw.githubusercontent.com/migueldiaslima/drone-revB/main/<path> -o <file>)
 7. Reference job: mkdir -p ~/drone_revB/stage6/r4/G7 && cd ~/drone_revB/stage6/r4/G7 &&
    setsid nohup bash ~/drone_revB/stage6/scripts/run_G7r4.sh 60 > G7r4_all.log 2>&1 &
 8. H4 after G7b_r4_ref passes: bash ~/drone_revB/stage6/scripts/run_H4r4.sh 60
 9. History and cycle 0 ALLSE: cd /tmp/mdias_H4r4 && abaqus python ~/drone_revB/stage6/scripts/h4_check.py TO_v04B_r4_H4 rel
