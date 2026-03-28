import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import time, datetime, timedelta
from pawpal_system import User, Pet, Task, Scheduler


# ── Helpers ──────────────────────────────────────────────────────────────────

def make_owner():
    return User("Alice", "alice@example.com")

def make_pet(owner=None):
    owner = owner or make_owner()
    return Pet("Buddy", "dog", owner)

def make_scheduler(pet, start="08:00", end="18:00"):
    h_s, m_s = map(int, start.split(":"))
    h_e, m_e = map(int, end.split(":"))
    owner = pet.owner
    s = Scheduler(owner, time(h_s, m_s), time(h_e, m_e))
    s.schedule_tasks([pet])
    return s


# ── Phase 1 tests (kept from before) ─────────────────────────────────────────

def test_mark_complete_changes_status():
    task = Task("Feed cat", 10, "high")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    user = make_owner()
    pet = Pet("Whiskers", "cat", user)
    task = Task("Brush fur", 15, "low")
    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1


# ── Sorting correctness ───────────────────────────────────────────────────────

def test_sort_by_time_returns_chronological_order():
    """Tasks added in reverse priority order should still sort by start time."""
    pet = make_pet()
    pet.add_task(Task("Evening walk", 30, "low"))
    pet.add_task(Task("Morning walk", 30, "high"))
    pet.add_task(Task("Midday feed",  15, "medium"))

    s = make_scheduler(pet)
    sorted_tasks = s.sort_by_time()

    times = [t.scheduled_time for t in sorted_tasks]
    assert times == sorted(times), "Tasks are not in chronological order"


def test_sort_by_time_pet_with_no_tasks():
    """Scheduler with no tasks should return an empty sorted list without error."""
    pet = make_pet()
    s = make_scheduler(pet)
    assert s.sort_by_time() == []


# ── Recurrence logic ─────────────────────────────────────────────────────────

def test_daily_recurrence_creates_new_task():
    """Completing a daily task should add one new task to the pet."""
    pet = make_pet()
    task = Task("Morning walk", 30, "high", frequency="daily")
    pet.add_task(task)

    assert len(pet.tasks) == 1
    task.mark_complete()
    assert len(pet.tasks) == 2


def test_daily_recurrence_due_date_is_tomorrow():
    """The auto-created task's due_date should be today + 1 day."""
    pet = make_pet()
    task = Task("Morning walk", 30, "high", frequency="daily")
    pet.add_task(task)
    task.mark_complete()

    new_task = pet.tasks[-1]
    assert new_task.due_date == datetime.today().date() + timedelta(days=1)


def test_weekly_recurrence_due_date_is_seven_days():
    """The auto-created task's due_date should be today + 7 days."""
    pet = make_pet()
    task = Task("Vet checkup", 60, "high", frequency="weekly")
    pet.add_task(task)
    task.mark_complete()

    new_task = pet.tasks[-1]
    assert new_task.due_date == datetime.today().date() + timedelta(days=7)


def test_once_task_does_not_recur():
    """Completing a one-time task should not add any new tasks."""
    pet = make_pet()
    task = Task("Bath time", 20, "medium", frequency="once")
    pet.add_task(task)
    task.mark_complete()

    assert len(pet.tasks) == 1


def test_recurrence_without_pet_does_not_crash():
    """A recurring task not linked to a pet should complete silently."""
    task = Task("Standalone", 10, "low", frequency="daily")
    task.mark_complete()   # task.pet is None — should not raise
    assert task.completed == True


# ── Conflict detection ────────────────────────────────────────────────────────

def test_no_conflicts_in_normal_schedule():
    """A freshly generated schedule with sequential slots should have no conflicts."""
    pet = make_pet()
    pet.add_task(Task("Walk",  30, "high"))
    pet.add_task(Task("Feed",  10, "medium"))
    s = make_scheduler(pet)
    assert s.detect_conflicts() == []


def test_conflict_detected_when_tasks_overlap():
    """Manually overlapping two tasks should produce a conflict warning."""
    pet = make_pet()
    pet.add_task(Task("Walk", 30, "high"))
    pet.add_task(Task("Feed", 10, "medium"))
    s = make_scheduler(pet)

    # Force an overlap: push the second task back to the same start time as the first
    tasks = s.sort_by_time()
    tasks[1].scheduled_time = tasks[0].scheduled_time

    conflicts = s.detect_conflicts()
    assert len(conflicts) == 1
    assert "CONFLICT" in conflicts[0]


def test_no_conflict_for_single_task():
    """A schedule with one task cannot conflict with itself."""
    pet = make_pet()
    pet.add_task(Task("Solo walk", 30, "high"))
    s = make_scheduler(pet)
    assert s.detect_conflicts() == []


# ── Filter tasks ──────────────────────────────────────────────────────────────

def test_filter_by_pet_name():
    """filter_tasks should only return tasks belonging to the named pet."""
    owner = make_owner()
    buddy = Pet("Buddy", "dog", owner)
    kitty = Pet("Kitty", "cat", owner)
    owner.add_pet(buddy)
    owner.add_pet(kitty)

    buddy.add_task(Task("Walk",     30, "high"))
    kitty.add_task(Task("Playtime", 20, "low"))

    s = Scheduler(owner, time(8, 0), time(18, 0))
    s.schedule_tasks([buddy, kitty])

    buddy_tasks = s.filter_tasks(pet_name="Buddy")
    assert all(t.pet.name == "Buddy" for t in buddy_tasks)
    assert len(buddy_tasks) == 1


def test_filter_by_completion_status():
    """filter_tasks(completed=False) should exclude completed tasks."""
    pet = make_pet()
    pet.add_task(Task("Walk", 30, "high"))
    pet.add_task(Task("Feed", 10, "medium"))
    s = make_scheduler(pet)

    s.scheduled_tasks[0].completed = True   # manually mark first task done
    pending = s.filter_tasks(completed=False)
    assert all(not t.completed for t in pending)
    assert len(pending) == 1
