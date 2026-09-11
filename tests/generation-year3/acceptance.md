# Year-3 Generation Acceptance

The macro-block is accepted only if:

1. Every Mathematics node in `year-3.json` is registered and executable.
2. Every English node in `year-3.json` is registered and executable.
3. Each node builds `recover`, `consolidate`, `advance`, `extend` and `reassess` sessions.
4. Every session passes the Session Engine quality gate.
5. Learner-facing task data contains no solution, rubric, generation parameters or error signals.
6. Open English production and mediation tasks remain rubric-scored rather than receiving invented semantic scores.
7. Listening scripts stay on the tutor side.
8. Year-1 and year-2 coverage checks remain green.
9. Learning Snapshot and adaptive-engine checks remain green.
10. The cumulative triennium checker covers all six curriculum files and rejects uncovered curriculum nodes.
11. A supported year-3 target dispatches successfully.
12. A target outside the supported curriculum returns `needs_review`.
