# Nexus runs for the report figures (Miguel, 2026-10-14 morning)

One script, about 15 to 20 min on nexus, no Abaqus licence-heavy job (only `abaqus python` reading odbs). It produces the data for: iso snapshots at cycles 0, 10, 20, 28; mode shapes 7 to 12 of the final thresholded model; mesh and set-up figures; stress maps of the other load cases. The figures themselves are drawn in the set-up workspace from the files you send back.

## 1. Check the saved cycles (nexus terminal)

```
ls -la /tmp/mdias_H4r4/TO_v04B_r4_H4/SAVE.odb/ | grep -E "_0(00|10|20|28)\.odb"
ls -la /tmp/mdias_H4r4/TH/TH_r4b_i30_final.odb /tmp/mdias_H4r4/TH/c28.odb /tmp/mdias_H4r4/TH/dist_TH_r4_i30_final.inp /tmp/mdias_H4r4/TH/TH_r4b_i30_final.inp
df -h /tmp | tail -1
```
Expected: four files `TO_v04B_r4_H4-Job_000.odb`, `_010`, `_020`, `_028` (about 3 GB each), the four TH files, and at least 2 GB free in /tmp. If the cycle files are named differently, send me the `ls` output before going on.

## 2. Get the scripts (by commit, checked)

```
cd ~/drone_revB/stage6/scripts
R=https://raw.githubusercontent.com/migueldiaslima/drone-revB/823bf65495f65f49ca7961ff6d537e9f675aefcf/scripts
wget -q -O export_th_figs.py $R/post/export_th_figs.py
wget -q -O run_figs.sh $R/hpc/figs/run_figs.sh
wget -q -O iso_mt.py $R/post/iso_mt.py
sha256sum export_th_figs.py run_figs.sh iso_mt.py
```
The hashes must start with `e835ecbc` (export_th_figs.py), `740a7689` (run_figs.sh), `b6083f8b` (iso_mt.py). If any file is 0 bytes or the hash differs, stop and send me the output.

## 3. Start (survives logout)

```
cd /tmp/mdias_H4r4
setsid nohup bash ~/drone_revB/stage6/scripts/run_figs.sh > run_figs.log 2>&1 &
```
The `Done` line the shell may print at once is the `setsid` hand-off, not the end of the run.

## 4. Follow it

```
cat /tmp/mdias_H4r4/run_figs.log
ps -u mdias -o pid,etime,pcpu,cmd | grep -E "iso_mt|export_th|run_figs" | grep -v grep
```

| Stage | Log lines | Time (estimate) |
|---|---|---|
| inputs | `inputs present; free space ...` | seconds |
| iso cycle 0, 10, 20, 28 | `START iso ...`, then `iso 0.30: <n> triangles -> mt_..._030.stl`, `DONE iso ...` | 2 to 4 min each (reading a 3 GB odb) |
| export | `START export`, three summary lines, `DONE export` | 3 to 5 min |
| copies | `ls` of /tmp/mdias_H4r4/figs | seconds |
| end | `ALL DONE hh:mm:ss` | total about 15 to 20 min |

Failed: a line `FAILED ...` names the log to read (`/tmp/mdias_H4r4/figs/iso_<cycle>.log` or `export.log`); an iso failure does not stop the rest. Send me `tail -n 20` of that log.

## 5. Send back

In Bitvise SFTP, from `/tmp/mdias_H4r4/figs/`:
- `mt_TO_v04B_r4_H4-Job_000_030.stl`, `mt_TO_v04B_r4_H4-Job_010_030.stl`, `mt_TO_v04B_r4_H4-Job_020_030.stl`, `mt_c28_030.stl`
- `th_figs.npz`, `th_figs_setup.txt`, `export.log`
- `stress_TH_r4b_i30_final_LC1.npz`, `_LC2a.npz`, `_LC2b.npz` (if copied)
- and the text of `run_figs.log`.

## Tested before delivery

- `export_th_figs.py` on the offline mock (`scripts/post/test_stress/`, `mkmock_figs.py`): surface triangles equal an independent count (10,714), mode displacements equal the mock fields, input blocks extracted per step.
- `run_figs.sh`: syntax check and a dry run with a stub `abaqus` command, including the missing-input stop and a failing iso step (the run continues and reports `DONE WITH 1 FAILED ISO STEP(S)`).
- Renderers (`scripts/figures/su_render.py`, `fig_iso_snapshots.py`, `fig_th_figs.py`) on the real cycle 28 surfaces and on the mock export.
- Not testable here: the real odb surface and node-set names. `stress_th.py` already found all 30 tie and coupling surfaces in the same odb with the same lookup; the reference-point sets are searched by name (`RP`, `CP_`) and reported, not required.
