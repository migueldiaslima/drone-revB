#!/bin/bash
# H3 production Tosca run (1.0 mm, member size 2.5 mm, H3 caps) on nexus (Abaqus/Tosca 2024).
# Needs TO_v03B_H3.par and TO_v03B_H3-Job.inp (written by CAE 2022) in ../inputs.
# Run from ~/drone_revB/stage6/H3 with:  bash ../scripts/run_H3.sh 64
NCPU=${1:-64}
cp ../inputs/TO_v03B_H3-Job.inp .
sed -E -e "s/^( *ITER_MAX = ).*/\160/" \
       -e "s/^driver\.Solver\.AddCallArgs = .*/driver.Solver.AddCallArgs = [ 'cpus=$NCPU', 'memory=90%', 'mp_mode=threads',]/" \
       ../inputs/TO_v03B_H3.par > TO_v03B_H3.par
echo "--- par check ---"
grep -n "FILE =\|ITER_MAX\|AddCallArgs\|LE_VALUE\|GE_VALUE\|THICK\|MEMBER" TO_v03B_H3.par
grep -q "ITER_MAX = 60" TO_v03B_H3.par && grep -q "mp_mode=threads" TO_v03B_H3.par \
  || { echo "par edit failed, H3 NOT started"; exit 1; }
setsid nohup abaqus optimization task=TO_v03B_H3.par job=TO_v03B_H3 cpus=$NCPU interactive \
  > H3_run.log 2>&1 < /dev/null &
echo $! > H3.pgid
date '+%F %T' > H3_start.txt
nohup bash ../scripts/h3_prune.sh > /dev/null 2>&1 < /dev/null &
echo "H3 started with $NCPU cores, process group $(cat H3.pgid); disk pruner started."
echo "Follow:  tail -f TO_v03B_H3/TOSCA.OUT     and     cat H3_prune.log"
