# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**


- Initial Components: add a pet, schedule a walk, see today's tasks


- Briefly describe your initial UML design.

- User (Object)
    - `name: str` — the owner's display name (Attribute)
    - `email: str` — used for login/identification (Attribute)
    - `pets: list[Pet]` — all pets belonging to this user (Attribute)
    - `sign_up() / log_in()` — authenticate and create/load a user session (Method)
    - `add_pet(pet: Pet)` — append a new pet to the user's pet list (Method)
    - `get_tasks() -> list[Task]` — aggregate all tasks across all owned pets (Method)
    - `complete_task(task: Task)` — mark a task done and remove it from the active schedule (Method)

- Pet (Object)
    - `name: str` — the pet's name (Attribute)
    - `species: str` — e.g. "dog", "cat", "other"; used to apply species-specific scheduling rules (Attribute)
    - `owner: User` — back-reference to the owning User (Attribute)
    - `tasks: list[Task]` — care tasks associated with this specific pet (Attribute)
    - `add_task(task: Task)` — attach a new care task to this pet (Method)
    - `get_pending_tasks() -> list[Task]` — return only incomplete tasks, sorted by priority (Method)

- Task (Object)
    - `title: str` — short label for the task, e.g. "Morning walk" (Attribute)
    - `duration_minutes: int` — how long the task takes; used by the scheduler to fit tasks into the day (Attribute)
    - `priority: str` — "low" | "medium" | "high"; higher-priority tasks are scheduled first (Attribute)
    - `completed: bool` — tracks whether the task has been finished (Attribute)
    - `scheduled_time: str | None` — the time slot assigned by the scheduler, e.g. "8:00 AM" (Attribute)
    - `mark_complete()` — set `completed = True` (Method)

- Scheduler (Object)
    - `user: User` — the user whose pets' tasks are being scheduled (Attribute)
    - `start_time: str` — earliest time slot available for scheduling, e.g. "7:00 AM" (Attribute)
    - `end_time: str` — latest time slot available for scheduling, e.g. "9:00 PM" (Attribute)
    - `scheduled_tasks: list[Task]` — ordered list of tasks that have been assigned time slots (Attribute)
    - `schedule_tasks(tasks: list[Task]) -> list[Task]` — sort tasks by priority and assign time slots sequentially (Method)
    - `get_daily_schedule() -> list[Task]` — return all scheduled tasks for the day in chronological order (Method)
    - `reschedule(task: Task, new_time: str)` — move a task to a different time slot and update the schedule (Method)
    - `clear_schedule()` — remove all scheduled time slots and reset the schedule (Method)

---

**UML Class Diagram**

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
        +title: str
        +duration_minutes: int
        +priority: str
        +completed: bool
        +scheduled_time: str
        +mark_complete()
    }

    class Scheduler {
        +user: User
        +start_time: str
        +end_time: str
        +scheduled_tasks: list~Task~
        +schedule_tasks(tasks: list~Task~)$ list~Task~
        +get_daily_schedule() list~Task~
        +reschedule(task: Task, new_time: str)
        +clear_schedule()
    }

    User "1" --o "0..*" Pet : owns
    Pet "1" --o "0..*" Task : has
    Scheduler "1" --> "1" User : schedules for
    Scheduler "1" --> "0..*" Task : manages
```

- What classes did you include, and what responsibilities did you assign to each?


I included a class for User, Pet, Task, and Scheduler. The User has the ability to add pets, and get and complete tasks. 
The Pet has associated tasks which can be added to. The scheduler has the ability to schedule/reschedule/clear tasks. Each task can only be completed, as all "active" duties are done by the other objects.


**b. Design changes**

- Did your design change during implementation?

- If yes, describe at least one change and why you made it.


Issues from Claude:

Missing Relationships

Task has no back-reference to Pet — User.complete_task(task) needs to find and remove the task from a specific pet's list, but there's no task.pet to navigate to. You'd have to loop through all pets to find it.

Scheduler can't apply species-specific rules — your design notes mention species-based scheduling, but Scheduler only sees User → flat list[Task]. It has no path to task → pet → species.

Logic Bottlenecks

Duplicate "complete" responsibility — both Task.mark_complete() and User.complete_task(task) exist. It's unclear who owns this. User.complete_task presumably calls task.mark_complete(), but then what does it do differently? If it also removes the task from Pet.tasks, you need the back-reference from point 1.

Scheduler.scheduled_tasks can drift out of sync with Pet.tasks — tasks live in two places. If a task is added to a pet after scheduling, or a pet's task is removed, the scheduler's list won't know.

start_time/end_time as str — scheduling arithmetic (e.g., assigning sequential time slots in schedule_tasks) requires parsing strings like "7:00 AM" repeatedly. This is error-prone; consider storing as datetime.time internally.

No task identity — Task has no id field. If a user has two pets each with a "Morning walk" task, reschedule(task, new_time) has no reliable way to distinguish them

Issues Fix
No task → pet link	Add pet: Pet = None attribute to Task.__init__, set it in Pet.add_task
Scheduler can't see species	Pass tasks with their pet context, or let schedule_tasks receive list[Pet] instead
Duplicate complete logic	Have User.complete_task call task.mark_complete() and then remove from the correct pet's list via task.pet
No task identity	Add id: int (e.g., using a class-level counter) to Task
The Task → Pet back-reference is the most load-bearing fix — it unblocks both the complete logic and the species-aware scheduling.


I agreed with Claude on the changes, and let it make the necessary steps. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
