from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    owner = Owner(name="John Doe")
    pet1 = Pet(name="Buddy", species="Dog")
    pet2 = Pet(name="Luna", species="Cat")
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = Task(description="Walk Buddy", time="08:00", duration=30, priority="High", frequency="Daily")
    task2 = Task(description="Feed Luna", time="08:00", duration=10, priority="High", frequency="Daily")
    task3 = Task(description="Play session", time="17:30", duration=20, priority="Medium", frequency="Once")

    pet1.add_task(task1)
    pet2.add_task(task2)
    pet1.add_task(task3)

    scheduler = Scheduler()
    all_tasks = scheduler.get_all_tasks(owner)
    sorted_tasks = scheduler.sort_by_time_and_priority(all_tasks)

    print(f"--- Today's Schedule for {owner.name} ---")
    for task in sorted_tasks:
        status = "✅" if task.is_completed else "❌"
        print(f"[{task.time}] {task.pet_name}: {task.description} ({task.priority} Priority) - Status: {status}")

    warnings = scheduler.check_conflicts(all_tasks)
    if warnings:
        print("\n--- WARNINGS ---")
        for warning in warnings:
            print(f"⚠️ {warning}")

if __name__ == "__main__":
    main()
