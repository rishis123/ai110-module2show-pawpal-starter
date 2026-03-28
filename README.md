# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

### Smarter Scheduling

The scheduler goes beyond basic slot assignment with four additional capabilities:

- **Sort by time** — `Scheduler.sort_by_time()` returns the day's tasks ordered by start time using a `lambda` key, replacing manual list management.
- **Filter tasks** — `Scheduler.filter_tasks(pet_name, completed)` lets you narrow the schedule by pet or completion status, or combine both filters at once.
- **Recurring tasks** — `Task` now accepts a `frequency` of `"once"`, `"daily"`, or `"weekly"`. When a recurring task is marked complete, `mark_complete()` automatically creates the next occurrence with a `due_date` calculated via `timedelta`.
- **Conflict detection** — `Scheduler.detect_conflicts()` scans adjacent scheduled tasks and returns a plain-English warning for any pair whose time windows overlap, without crashing the program.

## Testing PawPal+

### Run the test suite

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Area | Tests |
|---|---|
| **Task completion** | `mark_complete()` flips `completed` to `True` |
| **Pet task list** | `add_task()` increases `pet.tasks` count |
| **Sorting** | `sort_by_time()` returns chronological order; handles empty schedule |
| **Recurrence** | Daily tasks auto-create a new task on completion with `due_date = today + 1`; weekly uses `+ 7`; one-time tasks do not recur; unlinked tasks don't crash |
| **Conflict detection** | Clean schedule has no conflicts; manually overlapping two tasks triggers a warning; single-task schedule never conflicts |
| **Filtering** | `filter_tasks(pet_name=...)` isolates one pet's tasks; `filter_tasks(completed=False)` excludes done tasks |

### Confidence level

★★★★☆ — Core scheduling paths (priority ordering, slot assignment, recurrence, conflict detection) are fully covered. The remaining gap is integration-level edge cases: tasks whose duration alone exceeds the full day window, and `filter_tasks` combining both arguments simultaneously.
