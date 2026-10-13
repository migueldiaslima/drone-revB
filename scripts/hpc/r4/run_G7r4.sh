#!/bin/bash
# Reference job v04-B revision 4 (build log item 48): G7b_r4_ref (seat tie TIE_LIDRIM), debug mesh, then
# g7_check.py with the rev 4 mass 332.16 g (rev 3 332.25 g, export note: -66.9 mm3 = -0.09 g).
# Input from CAE 2022 (V3r4_jobs.py) in ~/drone_revB/stage6/r4/inputs.
# Run with:   mkdir -p ~/drone_revB/stage6/r4/G7 && cd ~/drone_revB/stage6/r4/G7 && bash ~/drone_revB/stage6/scripts/run_G7r4.sh 60
NCPU=${1:-60}
S=~/drone_revB/stage6/scripts
J=G7b_r4_ref
cp ../inputs/$J.inp . || { echo "missing ../inputs/$J.inp"; exit 1; }
echo "$J running ($NCPU threads)..."
abaqus job=$J input=$J.inp cpus=$NCPU mp_mode=threads memory="80%" interactive > ${J}_run.log 2>&1
tail -n 2 ${J}_run.log
G7_MASS=332.16 abaqus python $S/g7_check.py $J 2>&1 | tee ${J}_check.txt
grep -h "^G7 " ${J}_check.txt
