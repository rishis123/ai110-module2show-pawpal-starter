import streamlit as st
from pawpal_system import User, Pet, Task, Scheduler
from datetime import time

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Owner ─────────────────────────────────────────────────────────────────────
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = User(owner_name, "owner@email.com")

owner: User = st.session_state.owner

# ── Add a Pet ─────────────────────────────────────────────────────────────────
st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    new_pet = Pet(pet_name, species, owner)
    owner.add_pet(new_pet)
    st.success(f"Added {pet_name} the {species}!")

if owner.pets:
    st.write("Your pets:", [f"{p.name} ({p.species})" for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ── Add a Task ────────────────────────────────────────────────────────────────
st.subheader("Add a Task")

if owner.pets:
    pet_names = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Assign to pet", pet_names)
    selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        task = Task(task_title, int(duration), priority, frequency=frequency)
        selected_pet.add_task(task)
        st.success(f"Added '{task_title}' to {selected_pet_name}.")

    # ── Filter controls ───────────────────────────────────────────────────────
    all_tasks = owner.get_tasks()
    if all_tasks:
        st.markdown("**All tasks**")
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            filter_pet = st.selectbox("Filter by pet", ["All"] + pet_names, key="filter_pet")
        with filter_col2:
            filter_status = st.selectbox("Filter by status", ["All", "Pending", "Done"], key="filter_status")

        # Apply filters manually here since we're not in a Scheduler yet
        shown = all_tasks
        if filter_pet != "All":
            shown = [t for t in shown if t.pet and t.pet.name == filter_pet]
        if filter_status == "Pending":
            shown = [t for t in shown if not t.completed]
        elif filter_status == "Done":
            shown = [t for t in shown if t.completed]

        PRIORITY_BADGE = {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}
        st.table([
            {
                "Pet": t.pet.name,
                "Task": t.title,
                "Duration (min)": t.duration_minutes,
                "Priority": PRIORITY_BADGE.get(t.priority, t.priority),
                "Frequency": t.frequency,
                "Done": "✅" if t.completed else "⬜",
            }
            for t in shown
        ])
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

# ── Build Schedule ────────────────────────────────────────────────────────────
st.subheader("Build Schedule")

time_col1, time_col2 = st.columns(2)
with time_col1:
    start_time = st.time_input("Day starts at", value=time(8, 0))
with time_col2:
    end_time = st.time_input("Day ends at", value=time(18, 0))

if st.button("Generate schedule"):
    if not owner.pets:
        st.warning("Add a pet and some tasks first.")
    elif start_time >= end_time:
        st.error("Start time must be before end time.")
    else:
        scheduler = Scheduler(owner, start_time, end_time)
        scheduled = scheduler.schedule_tasks(owner.pets)

        if not scheduled:
            st.warning("No tasks could be scheduled — check that task durations fit within your time window.")
        else:
            # ── Conflict warnings ─────────────────────────────────────────────
            conflicts = scheduler.detect_conflicts()
            if conflicts:
                st.error(f"⚠️ {len(conflicts)} scheduling conflict(s) detected — review before your day starts:")
                for msg in conflicts:
                    # Extract the two task names from the message for a friendlier tip
                    st.warning(msg)
                st.caption("Tip: use the reschedule option or shorten a task's duration to resolve overlaps.")
            else:
                st.success(f"Schedule generated — {len(scheduled)} task(s) planned, no conflicts!")

            # ── Sorted schedule table ─────────────────────────────────────────
            PRIORITY_BADGE = {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}
            st.table([
                {
                    "Time": t.scheduled_time.strftime("%I:%M %p"),
                    "Pet": t.pet.name,
                    "Task": t.title,
                    "Duration (min)": t.duration_minutes,
                    "Priority": PRIORITY_BADGE.get(t.priority, t.priority),
                    "Frequency": t.frequency,
                }
                for t in scheduler.sort_by_time()   # uses Scheduler.sort_by_time()
            ])

            # ── Unscheduled tasks notice ──────────────────────────────────────
            all_pending = [t for pet in owner.pets for t in pet.get_pending_tasks()]
            unscheduled = [t for t in all_pending if t not in scheduled]
            if unscheduled:
                st.info(
                    f"{len(unscheduled)} task(s) didn't fit in your time window: "
                    + ", ".join(f"'{t.title}'" for t in unscheduled)
                )
