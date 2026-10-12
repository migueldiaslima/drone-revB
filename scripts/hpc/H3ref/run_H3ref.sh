#!/bin/bash
# H3 reference job (D-063 caps at 1.0 mm). Run from ~/drone_revB/stage6/H3ref with:
#   bash ../scripts/run_H3ref.sh 32
NCPU=${1:-32}
cp ../inputs/H3_ref.inp .
setsid nohup abq2025 job=H3_ref input=H3_ref.inp cpus=$NCPU mp_mode=threads memory="90%" interactive \
  > H3ref_run.log 2>&1 < /dev/null &
echo $! > H3ref.pgid
echo "H3_ref started with $NCPU cores, process group $(cat H3ref.pgid)"
echo "Follow:  tail -f H3_ref.sta     (and H3ref_run.log if it stops)"
