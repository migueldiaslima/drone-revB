#!/bin/bash
# h2_watch.sh - D-066 item 2 and D-064 reaction check during H2. Started by run_H2.sh.
# Checks the saved odb of cycles 5, 10, ... (once the next cycle has been saved, so the
# copy is complete) and the last cycle at the end. Stops H2 if the check reports STOP.
JOB=TO_v03B_H2
LOG=H2_watch.log
PGID=$(cat H2.pgid)
DONE=" "
echo "$(date '+%F %T') watcher started, H2 process group $PGID" >> $LOG
while true; do
  ALIVE=1; kill -0 -- -$PGID 2>/dev/null || ALIVE=0
  CYC=$(find $JOB -name "*_[0-9]*.odb" 2>/dev/null | sed -nE 's/.*_([0-9]+)\.odb$/\1/p' | sort -n | uniq)
  LAST=$(echo "$CYC" | tail -n 1)
  for C in $CYC; do
    case "$DONE" in *" $C "*) continue;; esac
    if [ $((C % 5)) -ne 0 ] && { [ $ALIVE -eq 1 ] || [ "$C" != "$LAST" ]; }; then continue; fi
    if [ $ALIVE -eq 1 ] && [ "$C" = "$LAST" ]; then continue; fi
    ODB=$(find $JOB -name "*_${C}.odb" | head -n 1)
    echo "=== $(date '+%F %T') cycle $C: $ODB" >> $LOG
    abq2025 python ../scripts/h2_modecheck.py "$ODB" >> $LOG 2>&1
    DONE="$DONE$C "
    if tail -n 1 $LOG | grep -q "STOP"; then
      echo "$(date '+%F %T') STOP condition at cycle $C: terminating H2 (group $PGID)" >> $LOG
      kill -TERM -- -$PGID
      exit 0
    fi
  done
  if [ $ALIVE -eq 0 ]; then
    echo "$(date '+%F %T') H2 process ended, watcher done" >> $LOG
    exit 0
  fi
  sleep 60
done
