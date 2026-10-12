#!/bin/bash
# h3_prune.sh - keeps disk use on nexus /home low during H3 (about 3 GB per saved odb).
# Every 60 s: deletes saved cycle odbs except every 10th, the 3 newest and cycle 0.
JOB=TO_v03B_H3
LOG=H3_prune.log
PGID=$(cat H3.pgid)
echo "$(date '+%F %T') pruner started" >> $LOG
while true; do
  ALIVE=1; kill -0 -- -$PGID 2>/dev/null || ALIVE=0
  FILES=$(find $JOB/SAVE.odb -name "*_[0-9]*.odb" 2>/dev/null | sort)
  KEEP=$(echo "$FILES" | tail -n 3)
  for F in $FILES; do
    C=$(echo "$F" | sed -nE 's/.*_([0-9]+)\.odb$/\1/p')
    [ -z "$C" ] && continue
    [ $((10#$C % 10)) -eq 0 ] && continue
    echo "$KEEP" | grep -qx "$F" && continue
    rm -f "$F" && echo "$(date '+%F %T') deleted $F" >> $LOG
  done
  echo "$(date '+%F %T') free on home: $(df -h --output=avail ~ | tail -n 1)" >> $LOG
  [ $ALIVE -eq 0 ] && { echo "$(date '+%F %T') H3 ended, pruner done" >> $LOG; exit 0; }
  sleep 60
done
