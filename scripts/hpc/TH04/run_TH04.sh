#!/bin/bash
# D-082 (b): build and run TH04b and TH04a side by side, then the check. Run in /tmp/mdias_H4/TH:
#   bash ~/drone_revB/stage6/scripts/run_TH04.sh 30
NCPU=${1:-30}
S=~/drone_revB/stage6/scripts
abaqus python $S/th04_build.py c31.odb || exit 1
[ -f TH04a.inp ] && [ -f TH04b.inp ] || { echo "inputs not built"; exit 1; }
for J in TH04b TH04a; do
  abaqus job=$J input=$J.inp cpus=$NCPU mp_mode=threads memory="40%" interactive > ${J}_run.log 2>&1 &
done
echo "TH04b and TH04a running ($NCPU threads each). Waiting..."
wait
tail -n 2 TH04b_run.log TH04a_run.log
abaqus python $S/th04_check.py TH04b TH04a 2>&1 | tee TH04_check.txt
