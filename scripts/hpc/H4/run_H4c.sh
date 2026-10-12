#!/bin/bash
# H4c restart (DV-24): Tosca 2024 on nexus, v04-B G7b model, debug mesh, no member size, H4c caps (D-082).
# Changes from the first start: run directory on /tmp (home is full); FREQ step given a negative
# Lanczos shift point (-100 Hz^2) so the rigid-body modes are not at the shift (cycle 11 Sturm-count error).
# Needs TO_v04B_H4c.par and TO_v04B_H4c-Job.inp in ~/drone_revB/stage6/inputs.
# Run with:   bash ~/drone_revB/stage6/scripts/run_H4c.sh 54
NCPU=${1:-54}
JOB=TO_v04B_H4c
IN=~/drone_revB/stage6/inputs
WORK=/tmp/mdias_H4c
mkdir -p $WORK && cd $WORK || exit 1
[ -e $JOB ] && { echo "$WORK/$JOB exists: move it away first"; exit 1; }
cp $IN/$JOB-Job.inp . || { echo "missing $IN/$JOB-Job.inp"; exit 1; }
# Lanczos shift: data line after *Frequency, '20, , , , ,' -> '20, , , -100., ,'
L=$(grep -n -i "^\*frequency" $JOB-Job.inp | head -n 1 | cut -d: -f1)
sed -i "$((L+1))s/^20, , , , ,/20, , , -100., ,/" $JOB-Job.inp
sed -n "${L},$((L+1))p" $JOB-Job.inp
sed -n "$((L+1))p" $JOB-Job.inp | grep -q "^20, , , -100., ," || { echo "shift edit failed, NOT started"; exit 1; }
sed -E -e "s/^( *ITER_MAX = ).*/\160/" \
       -e "s/^driver\.Solver\.AddCallArgs = .*/driver.Solver.AddCallArgs = [ 'cpus=$NCPU', 'memory=80%', 'mp_mode=threads',]/" \
       $IN/$JOB.par > $JOB.par
echo "--- par check ---"
grep -n "FILE =\|ITER_MAX\|AddCallArgs\|LE_VALUE\|GE_VALUE\|SYM" $JOB.par
grep -q "ITER_MAX = 60" $JOB.par && grep -q "mp_mode=threads" $JOB.par || { echo "par edit failed, NOT started"; exit 1; }
grep -qi "MEMBER" $JOB.par && { echo "member size found in the par, NOT started"; exit 1; }
for v in 0.216635 0.200186 0.102227 0.394042; do
  grep -q "$v" $JOB.par || { echo "cap $v not in the par, NOT started"; exit 1; }
done
setsid nohup abaqus optimization task=$JOB.par job=$JOB cpus=$NCPU interactive > H4c_run.log 2>&1 < /dev/null &
echo $! > H4c.pgid
date '+%F %T' > H4c_start.txt
echo "H4c started in $WORK with $NCPU cores. Follow:  tail -f $WORK/$JOB/TOSCA.OUT"
