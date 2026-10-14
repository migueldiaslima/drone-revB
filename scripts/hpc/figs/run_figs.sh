#!/bin/bash
# run_figs.sh - report figures, nexus part (build log item 70; docs/report_figures_setup.md items 3, 7, 15, 16, 19).
# Runs in /tmp/mdias_H4r4/figs:
#   1. iso 0.3 surfaces of the production run at saved cycles 0, 10, 20 and 28 (iso_mt.py, whole frame)
#   2. export of the final thresholded model for the mode, mesh and set-up figures (export_th_figs.py)
#   3. copies the stress npz of LC1, LC2a, LC2b (written by stress_th.py) for the other stress maps
# Usage: bash ~/drone_revB/stage6/scripts/run_figs.sh            (start it with setsid nohup, see the instructions)
# Each stage prints START / DONE lines with the time; the last line is ALL DONE or FAILED <stage>.
R4=/tmp/mdias_H4r4
TH=$R4/TH
SAVE=$R4/TO_v04B_r4_H4/SAVE.odb
S=~/drone_revB/stage6/scripts
OUT=$R4/figs
ABQ=${ABQ:-abaqus}
mkdir -p $OUT && cd $OUT || { echo "FAILED mkdir $OUT"; exit 1; }
NFAIL=0
echo "run_figs.sh started $(date +%H:%M:%S) in $OUT"
# inputs
for f in $SAVE/TO_v04B_r4_H4-Job_000.odb $SAVE/TO_v04B_r4_H4-Job_010.odb $SAVE/TO_v04B_r4_H4-Job_020.odb $TH/c28.odb \
         $TH/TH_r4b_i30_final.odb $TH/dist_TH_r4_i30_final.inp $TH/TH_r4b_i30_final.inp $S/iso_mt.py $S/export_th_figs.py; do
  [ -e "$f" ] || { echo "FAILED input missing: $f"; exit 1; }
done
echo "inputs present; free space in /tmp: $(df -h /tmp | awk 'NR==2{print $4}')"
# 1. iso surfaces (the odb name gives the file name: mt_TO_v04B_r4_H4-Job_0NN_030.stl, mt_c28_030.stl)
for o in $SAVE/TO_v04B_r4_H4-Job_000.odb $SAVE/TO_v04B_r4_H4-Job_010.odb $SAVE/TO_v04B_r4_H4-Job_020.odb $TH/c28.odb; do
  echo "START iso $(basename $o) $(date +%H:%M:%S)"
  if $ABQ python $S/iso_mt.py $o 0.3 > iso_$(basename $o .odb).log 2>&1; then
    tail -n 1 iso_$(basename $o .odb).log
    echo "DONE iso $(basename $o) $(date +%H:%M:%S)"
  else
    echo "FAILED iso $(basename $o) (see iso_$(basename $o .odb).log); continuing"
    NFAIL=$((NFAIL+1))
  fi
done
# 2. export of the final thresholded model
echo "START export $(date +%H:%M:%S)"
$ABQ python $S/export_th_figs.py $TH/TH_r4b_i30_final.odb $TH/dist_TH_r4_i30_final.inp $TH/TH_r4b_i30_final.inp > export.log 2>&1 || { echo "FAILED export (see export.log)"; exit 1; }
tail -n 3 export.log
echo "DONE export $(date +%H:%M:%S)"
# 3. stress npz of the other load cases
for c in LC1 LC2a LC2b LC3a; do
  [ -f $TH/stress_TH_r4b_i30_final_$c.npz ] && cp $TH/stress_TH_r4b_i30_final_$c.npz . || echo "note: stress_TH_r4b_i30_final_$c.npz not found in $TH"
done
ls -la $OUT
if [ $NFAIL -eq 0 ]; then echo "ALL DONE $(date +%H:%M:%S)"; else echo "DONE WITH $NFAIL FAILED ISO STEP(S) $(date +%H:%M:%S)"; fi
