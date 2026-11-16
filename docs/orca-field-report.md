# Field report: driving Orca from an external agent (Orca CLI 1.4.259, macOS)

One session, one project ([ounce-core](https://github.com/hffgzktbcc-blip/ounce-core), a Rust Switch emulator). A coordinating Claude Code session outside any Orca terminal started three workers (Claude, Codex, Antigravity) in separate worktrees, to implement a "Day-1 ergonomics" batch. Observations only; each is from one session, not a survey.

## What worked
- `orca worktree create --no-parent --agent <id> --prompt …` started Claude workers that delivered. Two of three workers committed with full `cargo test` green ([#458](https://github.com/hffgzktbcc-blip/ounce-core/pull/458), [#459](https://github.com/hffgzktbcc-blip/ounce-core/pull/459)); the third (a CLI worker in another repo) had not committed when this was written.
- `orca terminal list/read` was enough to supervise from outside.
- Antigravity is accepted as an agent id.

## Friction
1. **External coordinators can't use `worker-start`.** It needs an Orca-terminal sender (`no_active_sender_terminal`); `--from` exists only on that command. Workers started via `worktree create` are therefore untracked by orchestration. Already tracked: stablyai/orca#28190, #25775.
2. **`terminal close` returned `tab_not_found` for stuck Codex terminals** that were then actually closed or left orphaned. Repro and per-agent results: stablyai/orca#37843.
3. **A Codex worker pointed at a dead local endpoint looked alive.** It sat at "Reconnecting… Connection failed" and `terminal list` exposes no field that distinguishes that from a working terminal. (Not filed: I couldn't write a minimal repro.)

## Pattern that helped the project itself
The batch's CLI items were chosen so agents can script the tool: `--max-frames N`, repeatable `--press BUTTON@FRAME`, and (in progress) `--json` and `--timeout` on a runner. Deterministic exit conditions and machine-readable output are what let a supervisor decide "done" without reading a terminal.

## Resilience: expiring claims + out-of-band snapshots
Workers die (usage limits, dead endpoints, stuck terminals). [orca-handoff](https://github.com/hffgzktbcc-blip/orca-handoff) snapshots working state to `refs/handoff/*` and uses claims that expire on their own. Limits: advisory, git-only, not yet tested inside an Orca worker run. Design discussion: stablyai/orca#21556.
