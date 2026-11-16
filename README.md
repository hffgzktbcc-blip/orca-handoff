# orca-handoff

A small skill/script for [Orca](https://github.com/stablyai/orca) workers (any git repo really): continuous out-of-band snapshots plus expiring claims, so ownership is a lease and work survives a worker dying. Extracted from the handoff tooling in [ounce-core](https://github.com/hffgzktbcc-blip/ounce-core). See `SKILL.md` for commands and limits. MIT.

Install as a Claude Code skill: copy this folder to `~/.claude/skills/orca-handoff/`.
Test: `python3 tests/test_handoff.py`
