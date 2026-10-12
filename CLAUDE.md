# Working rules for Claude sessions on this repo

Project: quadcopter frame rev B (3.5 inch true X, Siraya PET-CF, topology optimisation in Abaqus/Tosca). Owner and decision maker: Miguel Dias de Lima (MSc Mechanical Engineering, FEUP; structural FEA, topology optimisation, additive manufacturing). Portfolio project for an airframe engineering role; the output is a report of about 15 pages (LaTeX). Treat him as an expert engineer who wants the reasoning shown, not simplified away.

This file replaces the chat memory the first account has. Follow it in every reply.

## 1. Source of truth

- `docs/journal_quadcopter.md` overrides chat memory. Resume from its Section 1.
- The report may only quote numbers from journal Section 4 (numbers register).
- Never invent values. Every number comes from a doc, a script output, a datasheet Miguel gave, or a calculation shown in the reply. Label assumptions as assumptions.
- The claude.ai project "Drone Rework" (first account) holds the same docs. Repo and project are synced by hand; if they differ, ask Miguel which is newer before editing.

## 2. Roles

The project runs as two chats with separate records:

| Role | Owns | Does |
|---|---|---|
| Main chat | `docs/journal_quadcopter.md` (D-xxx, N-xx-xx, F-xxx, L-xxx, Q-xx, A-xxx), geometry exports (`geometry/`, `scripts/geometry_main/`), export notes | decisions, design, CadQuery generator and gates G0 to G5, handovers and briefs to the set-up chat |
| Set-up chat | `docs/stage6_build_log_v03B.md` (numbered items, DV-xx deviations, set-up F-xx findings), Abaqus/Tosca scripts (`scripts/cae_*`, `scripts/hpc`, `scripts/post`) | CAE model build, HPC runs, checks, reports to the main chat |

- At the start of a session Miguel says which role this chat takes. If he does not, ask before editing any record.
- Do not edit the other role's records. Write a proposal or report doc (as the existing `stage6_*_report.md` and `*_note.md` files) and let the owner record it.
- Never reuse an ID. Take the next free number from the journal or build log.
- Every deviation from a sheet or decision is recorded with its reason (set-up chat: DV-xx in the build log). Decisions stay with Miguel; recommend, do not decide.

## 3. Sessions

- Start: `git pull`; read journal Section 1 and changelog; read the last build log items (Phase H items) and any doc named in Miguel's message.
- End: commit with a message naming the docs and scripts changed; push to the working branch and open a pull request (rules below). Tell Miguel which project docs changed so he can copy them to the claude.ai project.

### Repository writes (Option C, Miguel 2026-10-12)

- Reading the repo is free: pull and read whenever needed.
- Never commit or push to `main`. `main` is protected on GitHub (pull request required, no force push, no deletion); Miguel alone merges.
- Once a plan is agreed with Miguel, commit, push to the working branch and open the pull request without asking again; bugs found on the way may be fixed within the plan. Stop and ask before committing only when something will not work as agreed and the change needs his opinion. Always list the files changed and why when giving the PR link.
- Work on a branch named `<role>/<task>` (`setup/th04-fix`, `main-chat/v05B-export`), created from an up-to-date `main`. One branch and one pull request per task, grouping related changes; not one per small edit.
- Open the pull request with `gh api repos/migueldiaslima/drone-revB/pulls -f title=... -f head=<branch> -f base=main -f body=...` (`gh pr create` uses GraphQL, which is blocked in Claude sessions): title naming the task, body listing the docs and scripts changed and any new IDs (items, DV-xx, D-xxx). Then give Miguel the PR link.
- Never force push, rewrite history, delete branches or files outside the task, or merge pull requests.
- If `main` moved while the branch was open (the other account merged), rebase the branch on `main` before asking for the merge; report any conflict to Miguel instead of resolving it in the other role's records.
- After Miguel merges, `git switch main && git pull` before starting the next branch.

## 4. Writing style (always)

- Never use em dashes, anywhere (chat, docs, code, comments). Use commas, colons, parentheses or spaced hyphens.
- Headings direct and short ("Loads", "The eccentricity", "Result"), never narrating ("The governing fact", "Where the mass came from").
- No rhetorical closing sentences that wrap up without adding information. Stop when the point is made.
- Chat replies: short bold or table headings, decisions listed compactly, open questions stated plainly at the end.
- Alternative routes to the same goal are labelled as mutually exclusive options (Option A / B / C), never mixed into one numbered sequence.
- When Miguel launches a run or process, always give the commands to follow its progress (what to tail, what each stage prints, how to tell it finished or failed) and what to send back.
- Setup and run instructions: anticipate whether each step will actually work for Miguel's situation (software version, machine, disk, licence) before listing it; say what output to expect and what to send back.
- Units mm, N, tonne, s in the model; x forward, y left, z up, origin at the frame centre, z = 0 on the arm top; corners pp (+x+y), pm (+x-y), mp (-x+y), mm (-x-y).

## 5. Explanations (when Miguel asks to understand something)

- Slow, calm pace; split a long topic over 2 or 3 messages rather than compressing.
- Build from the most basic physics or definition upward (for example f = sqrt(k/m), the density field, SIMP rho^3), then small worked numeric examples and tables, analogies where they help (terrain and water level for iso surfaces).
- Derivations as phrased steps: a sentence, then the formula on its own line with spacing, starting from the general formula before substituting. Never several formulas on one line, never bare stacked formulas.
- For each concept make its impact on the project explicit, with project numbers.
- Separate concepts that are easy to confuse (validation vs correspondence to Tosca; mass vs area moment of inertia).
- If Miguel's guess is wrong, correct it explicitly but gently.
- End each part with the answer to his question and a short "Verdict" (or "What this means for us") tied to project numbers.
- Electrical topics: explain from basics for a mechanical engineer, only to the depth the goal needs.
- Figures (matplotlib PNG) when geometry is involved; scripts in `scripts/figures/`.

## 6. Code

- Python ASCII-only (no degree signs, no diameter symbols, no unicode minus). Write "dia 6", "deg".
- Abaqus CAE scripts (Python 2.7 in CAE 2022): do not use `sum` (shadowed by abaqusConstants); explicit arithmetic. Run with File > Run Script; print checks against expected values and stop with a clear message on any mismatch.
- Partition before selecting surfaces: face indices change after a partition.
- Every script checks its inputs (file identity, counts, volumes, areas) against values computed independently from the STEP files.
- nexus scripts: bash plus `abaqus python` (2024) for odb checks; Tosca odbs are flattened to one instance `PART-1-1`, so search instance sets.

## 7. Practical constraints

- Miguel uses Bitvise SSH/SFTP from Windows, not PowerShell. Give shell commands for the nexus terminal and file paths for the Bitvise SFTP window.
- Laptop: Ryzen 5 5600H, 16 GB, Abaqus/CAE 2022 (model building, writing .inp and .par). CAE 2022 cannot open Abaqus 2024/2025 odbs; post-process on the server.
- HPC: nexus (2 x EPYC 7513, 64 cores, 251 GB, Abaqus/Tosca 2024) is the production machine; nemix (2 x Xeon Gold 6130, 32 cores, 125 GB, Abaqus 2025 `abq2025`) is the second machine. No job scheduler: `setsid nohup`.
- nexus `/home` is full: runs go in `/tmp/mdias_<run>`; files that must survive go to `~/drone_revB/stage6`.
- Abaqus GUI on nexus is unusable: report from scripts, no screenshots.
- Tosca: thread mode only (`mp_mode=threads` in the .par `driver.Solver.AddCallArgs`, never on the optimization command line, F-15). Lanczos FREQ needs the negative shift `20, , , -100., ,` (DV-24). Start density 1.0 (DV-13).
- Timing estimates: base them on measured per-cycle times in the build log (H4: about 16 min per cycle at 60 threads on the 1.0 mm mesh), and say how uncertain they are.

## 8. Current state

See `README.md` section "Status" and the last items of the build log.
