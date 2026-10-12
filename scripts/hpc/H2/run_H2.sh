#!/bin/bash
# H2 full Tosca run (D-065, D-066) on nemix. Run from ~/drone_revB/stage6/H2 with:
#   bash ../scripts/run_H2.sh 32      (or 16 if the bench showed no gain)
NCPU=${1:-32}
cp ../inputs/TO_v03B_H1-Job.inp .
sed -E -e "s/^( *ITER_MAX = ).*/\160/" \
       -e "s/^driver\.Solver\.AddCallArgs = .*/driver.Solver.AddCallArgs = [ 'cpus=$NCPU', 'memory=90%',]/" \
       ../inputs/TO_v03B_H1.par > TO_v03B_H2.par
echo "--- par check ---"
grep -n "FILE =\|ITER_MAX\|AddCallArgs\|DENSITY_UPDATE" TO_v03B_H2.par
grep -q "ITER_MAX = 60" TO_v03B_H2.par && grep -q "'cpus=$NCPU', 'memory=90%'" TO_v03B_H2.par \
  || { echo "par edit failed, H2 NOT started"; exit 1; }
setsid nohup abq2025 optimization task=TO_v03B_H2.par job=TO_v03B_H2 cpus=$NCPU interactive \
  > H2_run.log 2>&1 < /dev/null &
echo $! > H2.pgid
date '+%F %T' > H2_start.txt
nohup bash ../scripts/h2_watch.sh > /dev/null 2>&1 < /dev/null &
echo "H2 started with $NCPU cores, process group $(cat H2.pgid); watcher started."
echo "Follow:  tail -f TO_v03B_H2/TOSCA.OUT     and     tail -f H2_watch.log"
