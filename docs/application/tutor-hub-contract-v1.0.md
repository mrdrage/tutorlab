# TutorLab Tutor + Hub Scuola Contract v1.0

## Goal

Expose TutorLab as a reusable didactic service without coupling the engine to Hub Scuola's database or UI.

The application flow is:

`tutor request → target selection → adaptive decision → session generation → student/tutor views → result → evidence → Learning Snapshot → next step`

Hub Scuola owns persistence and learner identity. TutorLab owns didactic selection, generation, evidence interpretation and next-step recommendation.

## Tutor request

The tutor can express:

- subject;
- intent: `continue`, `lesson`, `practice`, `assessment`;
- optional target competency;
- duration;
- maximum challenge band;
- optional quantity hint and notes.

The command is a preference layer, not a bypass of the adaptive engine. A known missing prerequisite takes precedence over a request to practise or advance the root target.

## Planning

`engine.tutor_service.plan(snapshot, request)` returns:

- target selection and reason;
- adaptive decision and final session action;
- objective stack to persist;
- Tutor View session;
- optional Student View session with solutions/rubrics/error signals removed.

Planning does not mutate the caller's Learning Snapshot.

## Hub Scuola boundary

Hub Scuola sends a versioned exchange envelope containing:

- `student_ref.external_id`: opaque identifier owned by Hub Scuola;
- `learning_snapshot`: TutorLab state;
- `request`: tutor command for planning;
- or `session_result` plus the session metadata for transition.

TutorLab does not need access to Hub Scuola tables, names, grades database or authentication system. The external ID is treated as an opaque reference.

## Persistence ownership

Hub Scuola should persist:

1. the Learning Snapshot;
2. the planned objective stack when a session is accepted;
3. the generated session identifier and relevant presentation payload;
4. the returned `snapshot_update` after results are recorded;
5. the `next_step` recommendation.

TutorLab remains stateless between calls except for versioned curriculum/configuration stored in its own package.

## Safety and privacy

Repository fixtures must remain fictional. Real student/minor data must not be committed to TutorLab Git.

Student View must not expose:

- solutions;
- rubrics;
- error signals;
- generation parameters;
- hidden tutor rationale.

## Intent semantics

- `continue`: use the adaptive engine normally.
- `lesson`: use the adaptive engine normally while respecting the requested duration/target.
- `practice`: may keep an otherwise advancing secure target in consolidation for the requested practice session, but never overrides a prerequisite recovery.
- `assessment`: forces `reassess` on the selected working target, but still respects prerequisite selection performed before generation.

## Non-goals

This contract does not define:

- Hub Scuola database migrations;
- HTTP transport;
- authentication or authorization;
- UI components;
- PDF rendering;
- cloud deployment.

Those should be adapters around this contract, not changes to the didactic engine.

## Acceptance criteria

- Tutor requests are schema-valid and bounded.
- Invalid subjects/intents/duration/bands are rejected.
- Planning is deterministic for a fixed snapshot/request/seed.
- Planning does not mutate the input snapshot.
- Known prerequisite gaps cannot be bypassed by practice/lesson commands.
- Assessment generates a reassessment session.
- Student View does not leak tutor-only fields.
- Hub round-trip converts session results into evidence, updates the snapshot and returns a valid next step.
- No GitHub Actions workflow is required.
