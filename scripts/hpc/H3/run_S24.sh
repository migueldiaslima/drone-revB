#!/bin/bash
# S24: Tosca 2024 smoke test on nexus with the H1 files (2.5 / 1.5 mesh, 2 cycles).
# Needs TO_v03B_H1.par and TO_v03B_H1-Job.inp (from nemix ~/drone_revB/stage6/inputs) in ../inputs.
# Run from ~/drone_revB/stage6/S24 with:  bash ../scripts/run_S24.sh
cp ../inputs/TO_v03B_H1-Job.inp .
sed -E -e "s/^( *ITER_MAX = ).*/\12/" \
       -e "s/^driver\.Solver\.AddCallArgs = .*/driver.Solver.AddCallArgs = [ 'cpus=64', 'memory=90%', 'mp_mode=threads',]/" \
       ../inputs/TO_v03B_H1.par > TO_v03B_S24.par
grep -n "ITER_MAX\|AddCallArgs" TO_v03B_S24.par
echo "S24 running in the foreground (about 10 min)..."
abaqus optimization task=TO_v03B_S24.par job=TO_v03B_S24 cpus=64 interactive > S24_run.log 2>&1
tail -n 5 S24_run.log
abaqus python ../scripts/h1_check.py TO_v03B_S24
