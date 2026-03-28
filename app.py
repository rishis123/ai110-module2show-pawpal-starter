import streamlit as st
from pawpal_system import User, Pet, Task, Scheduler
from datetime import time

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Owner ────────────────────────────────────────────────────────────────────
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = User(owner_name, "owner@email.com")

owner: User = st.session_state.owner

# ── Add a Pet ────────────────────────────────────────────────────────────────
st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    new_pet = Pet(pet_name, species, owner)
    owner.add_pet(new_pet)          # User.add_pet appends to owner.pets
    st.success(f"Added {pet_name} the {species}!")

if owner.pets:
    st.write("Your pets:", [f"{p.name} ({p.species})" for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ── Add a Task ───────────────────────────────────────────────────────────────
st.subheader("Add a Task")

if owner.pets:
    pet_names = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Assign to pet", pet_names)
    selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        task = Task(task_title, int(duration), priority)
        selected_pet.add_task(task)     # Pet.add_task links task.pet and appends to pet.tasks
        st.success(f"Added '{task_title}' to {selected_pet_name}.")

    all_tasks = owner.get_tasks()
    if all_tasks:
        st.write("All tasks:")
        st.table([
            {"pet": t.pet.name, "title": t.title, "duration": t.duration_minutes,
             "priority": t.priority, "done": t.completed}
            for t in all_tasks
        ])
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

# ── Generate Schedule ────────────────────────────────────────────────────────
st.subheader("Build Schedule")

start_time = st.time_input("Day starts at", value=time(8, 0))
end_time = st.time_input("Day ends at", value=time(18, 0))

if st.button("Generate schedule"):
    if not owner.pets:
        st.warning("Add a pet and some tasks first.")
    else:
        scheduler = Scheduler(owner, start_time, end_time)
        scheduled = scheduler.schedule_tasks(owner.pets)   # Scheduler.schedule_tasks assigns time slots
        if scheduled:
            st.success("Schedule generated!")
            st.table([
                {"time": str(t.scheduled_time), "pet": t.pet.name,
                 "task": t.title, "duration": t.duration_minutes, "priority": t.priority}
                for t in scheduler.get_daily_schedule()
            ])
        else:
            st.warning("No tasks could be scheduled. Check task durations vs. available time.")
