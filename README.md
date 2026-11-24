# orca-handoff

Coding agents can stop at any moment: a usage limit, a crash, a stuck terminal. `orca-handoff` makes sure that costs no work. It snapshots an agent's whole working state to git refs and uses task claims that expire on their own, so a dead worker never loses changes and never blocks the next one.

It is one dependency-free Python script (Python 3 + git) that never touches your branch, index or working tree; everything lives under `refs/handoff/`. It was built for [Orca](https://github.com/stablyai/orca) workers but works in any git repository. It was extracted from the handoff tooling in [ounce-core](https://github.com/hffgzktbcc-blip/ounce-core).

```bash
python3 scripts/handoff.py claim <task>            # reserve a task; expires after 4h by itself
python3 scripts/handoff.py watch --push &          # snapshot every minute to refs/handoff/<agent>/<branch>
python3 scripts/handoff.py save --note "doing X" --next "then Y" --push
python3 scripts/handoff.py log "one sentence the next agent must know"
python3 scripts/handoff.py resume                  # where did earlier agents stop?
python3 scripts/handoff.py resume --apply <name>   # restore their work on a new branch
python3 scripts/handoff.py release <task>
```

`status`, `journal` and `digest` (a short Markdown summary for a phone) round it out. Set `AGENT_NAME` (or `--agent`) so snapshots are attributable.

**Install** as a Claude Code skill by copying this folder to `~/.claude/skills/orca-handoff/`. **Test** with `python3 tests/test_handoff.py`.

**Limits:** claims are advisory, and only git state is saved (no processes or terminal scrollback). `--push` publishes untracked files too: likely secrets (`.env*`, `*.pem`, `*.key`, ssh keys, `credentials*`) are excluded, and you can add more with `HANDOFF_FORBIDDEN='regex'`, but review before using it on a new repo. This standalone version has not yet been tested end to end inside an Orca worker run. See [SKILL.md](SKILL.md) for details. MIT licensed.
