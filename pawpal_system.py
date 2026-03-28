from datetime import time


class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.pets: list = []

    def sign_up(self):
        pass

    def log_in(self):
        pass

    def add_pet(self, pet):
        pass

    def get_tasks(self) -> list:
        pass

    def complete_task(self, task):
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
        task.pet = self
        self.tasks.append(task)

    def get_pending_tasks(self) -> list:
        pass


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
        self.completed = True


class Scheduler:
    def __init__(self, user, start_time: time, end_time: time):
        self.user = user
        self.start_time = start_time
        self.end_time = end_time
        self.scheduled_tasks: list = []

    def schedule_tasks(self, pets: list) -> list:
        pass

    def get_daily_schedule(self) -> list:
        pass

    def reschedule(self, task, new_time: time):
        pass

    def clear_schedule(self):
        pass
