#!/bin/bash
# Gate G7 on nexus (Abaqus 2024): G7a (lid tied at the 5 bosses) and G7b (bosses plus rim), debug mesh,
# run side by side, then g7_check.py on both. Inputs from CAE 2022 (V3_jobs.py) in ../inputs.
# Run from ~/drone_revB/stage6/G7 with:   bash ../scripts/run_G7.sh 32
NCPU=${1:-32}
for J in G7a_ref G7b_ref; do
  cp ../inputs/$J.inp . || { echo "missing ../inputs/$J.inp"; exit 1; }
done
for J in G7a_ref G7b_ref; do
  abaqus job=$J input=$J.inp cpus=$NCPU mp_mode=threads memory="40%" interactive > ${J}_run.log 2>&1 &
done
echo "G7a and G7b running ($NCPU cores each). Waiting..."
wait
for J in G7a_ref G7b_ref; do
  tail -n 2 ${J}_run.log
  abaqus python ../scripts/g7_check.py $J 2>&1 | tee ${J}_check.txt
done
grep -h "^G7 " G7a_ref_check.txt G7b_ref_check.txt
