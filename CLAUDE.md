# Working rules for Claude sessions on this repo

## Source of truth
- `docs/journal_quadcopter.md` overrides chat memory. Resume from its Section 1.
- The report may only quote numbers from journal Section 4 (numbers register).
- The claude.ai project "Drone Rework" holds the same docs. If the repo and the project differ, ask Miguel which is newer before editing.

## Chat ownership
- Main chat: owns the journal (decisions D-xxx, numbers N-xx-xx, findings F-xxx, lessons L-xxx, questions Q-xx) and the geometry exports.
- Set-up chat: owns `docs/stage6_build_log_v03B.md` (items, deviations DV-xx) and the Abaqus/Tosca scripts.
- A second account working here states which role it takes and does not edit the other role's records; it proposes changes instead.
- Never reuse an ID. Take the next free number from the journal or build log.

## Sessions
- Start: `git pull`, read journal Section 1 and the latest build log items.
- End: commit with a message naming the docs and scripts changed; push.

## Style (always)
- No em dashes. Direct short headings. No rhetorical closings.
- ASCII-only Python. In Abaqus CAE scripts do not use `sum` (shadowed); use explicit arithmetic.
- Explanations slow and basics-first, with worked numbers and a "Verdict".
- Mutually exclusive options labelled clearly (A / B / C).
- Setup instructions anticipate whether each step will work.
- Never invent values; label assumptions.

## Practical constraints
- Miguel uses Bitvise SSH/SFTP (Windows), not PowerShell.
- nexus `/home` is full: runs go in `/tmp/mdias_<run>`. Thread mode for Tosca (`mp_mode=threads` in AddCallArgs).
- Abaqus GUI on nexus is unusable: report from scripts, no screenshots.
- CAE 2022 (laptop) cannot open Abaqus 2024/2025 odbs; post-process on nexus.
- Lanczos frequency step in Tosca runs needs the negative shift (DV-24): `20, , , -100., ,`.
