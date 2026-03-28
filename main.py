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

# --- Tasks ---
buddy.add_task(Task("Morning walk",    duration_minutes=30, priority="high"))
buddy.add_task(Task("Feed breakfast",  duration_minutes=10, priority="high"))
buddy.add_task(Task("Evening walk",    duration_minutes=30, priority="medium"))

whiskers.add_task(Task("Clean litter box", duration_minutes=10, priority="medium"))
whiskers.add_task(Task("Playtime",         duration_minutes=20, priority="low"))

# --- Scheduler ---
scheduler = Scheduler(user=owner, start_time=time(7, 0), end_time=time(21, 0))
scheduler.schedule_tasks(owner.pets)

# --- Print Today's Schedule ---
print("\n========== Today's Schedule ==========")
for task in scheduler.get_daily_schedule():
    pet_name = task.pet.name if task.pet else "Unknown"
    slot = task.scheduled_time.strftime("%I:%M %p")
    print(f"  {slot}  [{task.priority.upper():6}]  {pet_name}: {task.title}  ({task.duration_minutes} min)")
print("======================================\n")
