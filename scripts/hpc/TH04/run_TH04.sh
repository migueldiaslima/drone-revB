#!/bin/bash
# D-082 (b): build and run TH04b and TH04a side by side, then the check. Run in /tmp/mdias_H4/TH:
#   bash ~/drone_revB/stage6/scripts/run_TH04.sh 30          (TH04b, TH04a)
#   bash ~/drone_revB/stage6/scripts/run_TH04.sh 30 ni       (item 44: islands set to air; TH04b_ni, TH04a_ni)
NCPU=${1:-30}
S=~/drone_revB/stage6/scripts
if [ "$2" = "ni" ]; then SUF=_ni; FLAG=noislands; else SUF=; FLAG=; fi
abaqus python $S/th04_build.py c31.odb $FLAG || exit 1
[ -f TH04a$SUF.inp ] && [ -f TH04b$SUF.inp ] || { echo "inputs not built"; exit 1; }
for J in TH04b$SUF TH04a$SUF; do
  abaqus job=$J input=$J.inp cpus=$NCPU mp_mode=threads memory="40%" interactive > ${J}_run.log 2>&1 &
done
echo "TH04b$SUF and TH04a$SUF running ($NCPU threads each). Waiting..."
wait
tail -n 2 TH04b${SUF}_run.log TH04a${SUF}_run.log
abaqus python $S/th04_check.py TH04b$SUF TH04a$SUF 2>&1 | tee TH04${SUF}_check.txt
