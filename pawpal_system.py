from datetime import time, datetime, timedelta

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.pets: list = []

    def sign_up(self):
        """Create a new user account and print a confirmation message."""
        print(f"Account created for {self.name} ({self.email}).")

    def log_in(self):
        """Log in the user and print a welcome message."""
        print(f"Welcome back, {self.name}!")

    def add_pet(self, pet):
        """Add a pet to the user's list of pets."""
        self.pets.append(pet)

    def get_tasks(self) -> list:
        """Return all tasks across every pet owned by this user."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def complete_task(self, task):
        """Mark a task complete and remove it from its pet's task list."""
        task.mark_complete()
        if task.pet is not None:
            task.pet.tasks.remove(task)


class Pet:
    def __init__(self, name: str, species: str, owner):
        self.name = name
        self.species = species
        self.owner = owner
        self.tasks: list = []

    def add_task(self, task):
        """Link a task to this pet and append it to the pet's task list."""
        task.pet = self
        self.tasks.append(task)

    def get_pending_tasks(self) -> list:
        """Return incomplete tasks for this pet, sorted by priority."""
        pending = [t for t in self.tasks if not t.completed]
        return sorted(pending, key=lambda t: PRIORITY_ORDER.get(t.priority, 3))


class Task:
    _id_counter = 0

    def __init__(self, title: str, duration_minutes: int, priority: str):
        Task._id_counter += 1
        self.id = Task._id_counter
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.completed: bool = False
        self.scheduled_time: time | None = None
        self.pet = None  # back-reference set by Pet.add_task

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True


class Scheduler:
    def __init__(self, user, start_time: time, end_time: time):
        self.user = user
        self.start_time = start_time
        self.end_time = end_time
        self.scheduled_tasks: list = []

    def schedule_tasks(self, pets: list) -> list:
        """Assign time slots to all pending tasks across the given pets."""
        all_pending = []
        for pet in pets:
            all_pending.extend(pet.get_pending_tasks())

        # Sort globally by priority so high-priority tasks get the earliest slots.
        all_pending.sort(key=lambda t: PRIORITY_ORDER.get(t.priority, 3))

        today = datetime.today().date()
        current = datetime.combine(today, self.start_time)
        end = datetime.combine(today, self.end_time)

        self.scheduled_tasks = []
        for task in all_pending:
            slot_end = current + timedelta(minutes=task.duration_minutes)
            if slot_end > end:
                break  # no room left in the day
            task.scheduled_time = current.time()
            self.scheduled_tasks.append(task)
            current = slot_end

        return self.scheduled_tasks

    def get_daily_schedule(self) -> list:
        """Return scheduled tasks ordered by their start time."""
        return sorted(self.scheduled_tasks, key=lambda t: t.scheduled_time)

    def reschedule(self, task, new_time: time):
        """Update a scheduled task's start time if it exists in the schedule."""
        if task in self.scheduled_tasks:
            task.scheduled_time = new_time

    def clear_schedule(self):
        """Remove all scheduled tasks and clear their assigned times."""
        for task in self.scheduled_tasks:
            task.scheduled_time = None
        self.scheduled_tasks = []
