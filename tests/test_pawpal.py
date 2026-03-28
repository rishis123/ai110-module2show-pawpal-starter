import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import User, Pet, Task


def test_mark_complete_changes_status():
    task = Task("Feed cat", 10, "high")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    user = User("Alice", "alice@example.com")
    pet = Pet("Whiskers", "cat", user)
    task = Task("Brush fur", 15, "low")

    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1
