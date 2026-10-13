#!/bin/bash
# Reference jobs v04-B revision 3 (build log item 46): G7a_r3_ref (5 boss ties) and G7b_r3_ref (seat tie),
# debug mesh, side by side, then g7_check.py on both with the rev 3 mass (332.25 g: rev 2 332.79,
# TUB -92.2 mm3 x 1.30e-3 g/mm3 = -0.12 g, point masses -0.42 g).
# Inputs from CAE 2022 (V3r3_jobs.py) in ~/drone_revB/stage6/r3/inputs.
# Run with:   mkdir -p ~/drone_revB/stage6/r3/G7 && cd ~/drone_revB/stage6/r3/G7 && bash ~/drone_revB/stage6/scripts/run_G7r3.sh 30
NCPU=${1:-30}
S=~/drone_revB/stage6/scripts
for J in G7a_r3_ref G7b_r3_ref; do
  cp ../inputs/$J.inp . || { echo "missing ../inputs/$J.inp"; exit 1; }
done
for J in G7a_r3_ref G7b_r3_ref; do
  abaqus job=$J input=$J.inp cpus=$NCPU mp_mode=threads memory="40%" interactive > ${J}_run.log 2>&1 &
done
echo "G7a_r3_ref and G7b_r3_ref running ($NCPU threads each). Waiting..."
wait
for J in G7a_r3_ref G7b_r3_ref; do
  tail -n 2 ${J}_run.log
  G7_MASS=332.25 abaqus python $S/g7_check.py $J 2>&1 | tee ${J}_check.txt
done
grep -h "^G7 " G7a_r3_ref_check.txt G7b_r3_ref_check.txt
