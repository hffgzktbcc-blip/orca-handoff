---
name: orca-handoff
description: Snapshot an agent's working state to git refs and use expiring task claims so a worker that dies (usage limit, crash, stuck terminal) loses no work and never blocks others. Use in Orca worktrees when handing work between agents or before long steps.
---

# orca-handoff

Git-only, dependency-free (Python 3 + git). Nothing touches your branch, index or working tree.

```bash
python3 scripts/handoff.py claim <task>            # reserve a task; expires after 4h by itself
python3 scripts/handoff.py watch --push &          # snapshot every minute to refs/handoff/<agent>/<branch>
python3 scripts/handoff.py save --note "doing X" --next "then Y" --push
python3 scripts/handoff.py log "one sentence the next agent must know"
python3 scripts/handoff.py resume                  # where did earlier agents stop?
python3 scripts/handoff.py resume --apply <name>   # restore their work on a new branch
python3 scripts/handoff.py release <task>
```

Set `AGENT_NAME` (or `--agent`) so snapshots are attributable.

## Limits (read before relying on it)
- Claims are advisory: nothing stops an agent ignoring one.
- Git state only: no processes, scrollback or PTY state.
- Untracked files are snapshotted, and `--push` publishes them. Likely secrets (`.env*`, `*.pem`, `*.key`, ssh keys, `credentials*`) are excluded; add more with `HANDOFF_FORBIDDEN='regex'`. Review before using with a new repo.
- Orca side: not yet tested end to end inside an Orca worker run.
