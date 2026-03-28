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
        pass


class Pet:
    def __init__(self, name: str, species: str, owner):
        self.name = name
        self.species = species
        self.owner = owner
        self.tasks: list = []

    def add_task(self, task):
        pass

    def get_pending_tasks(self) -> list:
        pass


class Task:
    def __init__(self, title: str, duration_minutes: int, priority: str):
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.completed: bool = False
        self.scheduled_time = None

    def mark_complete(self):
        pass


class Scheduler:
    def __init__(self, user, start_time: str, end_time: str):
        self.user = user
        self.start_time = start_time
        self.end_time = end_time
        self.scheduled_tasks: list = []

    def schedule_tasks(self, tasks: list) -> list:
        pass

    def get_daily_schedule(self) -> list:
        pass

    def reschedule(self, task, new_time: str):
        pass

    def clear_schedule(self):
        pass
