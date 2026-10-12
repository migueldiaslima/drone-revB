#!/bin/bash
# CPU bench before H2: the H0 reference job at 32 cores against the H0 run at 16.
# Run from ~/drone_revB/stage6/bench with:  bash ../scripts/run_bench.sh
cp ../H0/H0_ref.inp B32.inp
echo "B32 running in the foreground (about 2 min)..."
abq2025 job=B32 input=B32.inp cpus=32 memory="90%" interactive > B32_run.log 2>&1
echo "--- wallclock, H0 (16 cores) then B32 (32 cores) ---"
grep -H "WALLCLOCK TIME" ../H0/H0_ref.msg B32.msg
echo "--- results check against 2022 ---"
abq2025 python ../scripts/h0_check.py B32
