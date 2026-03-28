from datetime import time
from pawpal_system import User, Pet, Task, Scheduler

# --- Owner ---
owner = User(name="Rishi", email="rishi@example.com")
owner.sign_up()

# --- Pets ---
buddy = Pet(name="Buddy", species="dog", owner=owner)
whiskers = Pet(name="Whiskers", species="cat", owner=owner)
owner.add_pet(buddy)
owner.add_pet(whiskers)

# --- Tasks (added out of order intentionally) ---
buddy.add_task(Task("Evening walk",    duration_minutes=30, priority="medium"))
buddy.add_task(Task("Morning walk",    duration_minutes=30, priority="high", frequency="daily"))
buddy.add_task(Task("Feed breakfast",  duration_minutes=10, priority="high"))

whiskers.add_task(Task("Clean litter box", duration_minutes=10, priority="medium"))
whiskers.add_task(Task("Playtime",         duration_minutes=20, priority="low"))

# --- Scheduler ---
scheduler = Scheduler(user=owner, start_time=time(7, 0), end_time=time(21, 0))
scheduler.schedule_tasks(owner.pets)

# --- Step 2: Sorting by time ---
print("\n========== Today's Schedule (sorted by time) ==========")
for task in scheduler.sort_by_time():
    pet_name = task.pet.name if task.pet else "Unknown"
    slot = task.scheduled_time.strftime("%I:%M %p")
    print(f"  {slot}  [{task.priority.upper():6}]  {pet_name}: {task.title}  ({task.duration_minutes} min)")

# --- Step 2: Filtering ---
print("\n--- Buddy's tasks only ---")
for t in scheduler.filter_tasks(pet_name="Buddy"):
    print(f"  {t.scheduled_time.strftime('%I:%M %p')}  {t.title}")

print("\n--- Incomplete tasks only ---")
for t in scheduler.filter_tasks(completed=False):
    print(f"  {t.title} ({t.pet.name})")

# --- Step 3: Recurring task demo ---
print("\n--- Recurring task: complete 'Morning walk' (daily) ---")
morning_walk = next(t for t in buddy.tasks if t.title == "Morning walk")
print(f"  Before: Buddy has {len(buddy.tasks)} task(s)")
morning_walk.mark_complete()
print(f"  After:  Buddy has {len(buddy.tasks)} task(s)  "
      f"(new '{buddy.tasks[-1].title}' auto-created, due {buddy.tasks[-1].due_date})")

# --- Step 4: Conflict detection ---
print("\n--- Conflict detection ---")
# Force a conflict: manually set two tasks to the same start time
tasks = scheduler.sort_by_time()
if len(tasks) >= 2:
    tasks[1].scheduled_time = tasks[0].scheduled_time  # create overlap deliberately

conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  ⚠ {warning}")
else:
    print("  No conflicts detected.")

print()
