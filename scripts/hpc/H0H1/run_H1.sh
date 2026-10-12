#!/bin/bash
# H1 Tosca smoke test on nemix (Abaqus/Tosca 2025). Run from ~/drone_revB/stage6/H1 with:  bash ../scripts/run_H1.sh
cp ../inputs/TO_v03B_H1.par ../inputs/TO_v03B_H1-Job.inp .
nohup abq2025 optimization task=TO_v03B_H1.par job=TO_v03B_H1 cpus=16 interactive > H1_run.log 2>&1 &
echo "H1 started, PID $!  (follow with: tail -f H1_run.log   and   tail -f TO_v03B_H1/TOSCA.OUT)"
