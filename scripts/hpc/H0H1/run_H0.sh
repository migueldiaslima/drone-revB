#!/bin/bash
# H0 reference job on nemix (Abaqus 2025). Run from ~/drone_revB/stage6/H0 with:  bash ../scripts/run_H0.sh
cp ../inputs/revB_v03B_D056_ref.inp H0_ref.inp
nohup abq2025 job=H0_ref input=H0_ref.inp cpus=16 memory="35%" interactive > H0_run.log 2>&1 &
echo "H0 started, PID $!  (follow with: tail -f H0_ref.sta   or   tail -f H0_run.log)"
