# PawPal+ — Final UML Class Diagram

```mermaid
classDiagram
    direction LR
    class User {
        +name: str
        +email: str
        +pets: list~Pet~
        +sign_up()
        +log_in()
        +add_pet(pet: Pet)
        +get_tasks() list~Task~
        +complete_task(task: Task)
    }

    class Pet {
        +name: str
        +species: str
        +owner: User
        +tasks: list~Task~
        +add_task(task: Task)
        +get_pending_tasks() list~Task~
    }

    class Task {
        +id: int
        +title: str
        +duration_minutes: int
        +priority: str
        +frequency: str
        +completed: bool
        +scheduled_time: time
        +pet: Pet
        +mark_complete()
    }

    class Scheduler {
        +user: User
        +start_time: time
        +end_time: time
        +scheduled_tasks: list~Task~
        +schedule_tasks(pets: list~Pet~) list~Task~
        +sort_by_time() list~Task~
        +filter_tasks(pet_name, completed) list~Task~
        +detect_conflicts() list~str~
        +get_daily_schedule() list~Task~
        +reschedule(task: Task, new_time: time)
        +clear_schedule()
    }

    User "1" --o "0..*" Pet : owns
    Pet "1" --o "0..*" Task : has
    Task "0..*" --> "0..1" Pet : back-ref
    Scheduler "1" --> "1" User : schedules for
    Scheduler "1" --> "0..*" Task : manages
```
```