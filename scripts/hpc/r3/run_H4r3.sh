#!/bin/bash
# H4 rev 3 (D-083, D-084; copy of run_H4.sh with rev 3 names). H4 production (DV-25): Tosca 2024 on nexus, v04-B G7b model, 1.0 mm mesh, member size 2.5 mm, caps 2.0 x cycle 0.
# Changes from the first start: run directory on /tmp (home is full); FREQ step given a negative
# Lanczos shift point (-100 Hz^2) so the rigid-body modes are not at the shift (cycle 11 Sturm-count error).
# Needs TO_v04B_H4.par and TO_v04B_H4-Job.inp in ~/drone_revB/stage6/inputs.
# Run with:   bash ~/drone_revB/stage6/scripts/run_H4r3.sh 60
NCPU=${1:-54}
JOB=TO_v04B_r3_H4
IN=~/drone_revB/stage6/r3/inputs
WORK=/tmp/mdias_H4r3
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
grep -qi "MEMBER\|MIN_MEMBER" $JOB.par || { echo "member size NOT in the par (GR_MS missing), NOT started"; exit 1; }
setsid nohup abaqus optimization task=$JOB.par job=$JOB cpus=$NCPU interactive > H4_run.log 2>&1 < /dev/null &
echo $! > H4.pgid
date '+%F %T' > H4_start.txt
echo "H4 rev 3 started in $WORK with $NCPU cores. Follow:  tail -f $WORK/$JOB/TOSCA.OUT"
