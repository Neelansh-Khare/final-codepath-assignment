import json
from pawpal_system import Owner, Pet, Task, Scheduler
from dataclasses import asdict

DATA_FILE = "data.json"

def get_current_owner():
    """Helper to load the owner state from data.json."""
    return Owner.load_from_json(DATA_FILE)

def save_owner(owner):
    """Helper to save the owner state to data.json."""
    owner.save_to_json(DATA_FILE)

def get_schedule():
    """Retrieves all tasks for all pets in a human-readable format."""
    owner = get_current_owner()
    scheduler = Scheduler()
    all_tasks = scheduler.get_all_tasks(owner)
    sorted_tasks = scheduler.sort_by_time_and_priority(all_tasks)
    
    if not sorted_tasks:
        return "No tasks currently scheduled."
    
    output = []
    for task in sorted_tasks:
        status = "Completed" if task.is_completed else "Pending"
        output.append(f"Pet: {task.pet_name} | Task: {task.description} | Time: {task.time} | Duration: {task.duration}m | Priority: {task.priority} | Frequency: {task.frequency} | Status: {status}")
    
    conflicts = scheduler.check_conflicts(sorted_tasks)
    if conflicts:
        output.append("\nWARNING: Current Schedule Conflicts:")
        for c in conflicts:
            output.append(f"- {c}")
            
    return "\n".join(output)

def add_pet_task(pet_name: str, description: str, time: str, duration: int = 30, priority: str = "Medium", frequency: str = "Once"):
    """Adds a new task for a specific pet."""
    owner = get_current_owner()
    pet = next((p for p in owner.pets if p.name.lower() == pet_name.lower()), None)
    if not pet:
        return f"Error: Pet '{pet_name}' not found."
    
    new_task = Task(
        description=description,
        time=time,
        duration=duration,
        priority=priority,
        frequency=frequency
    )
    pet.add_task(new_task)
    save_owner(owner)
    return f"Successfully added task '{description}' for {pet_name} at {time}."

def delete_pet_task(pet_name: str, task_description: str, time: str):
    """Deletes a specific task for a pet based on description and time."""
    owner = get_current_owner()
    pet = next((p for p in owner.pets if p.name.lower() == pet_name.lower()), None)
    if not pet:
        return f"Error: Pet '{pet_name}' not found."
    
    original_count = len(pet.tasks)
    pet.tasks = [t for t in pet.tasks if not (t.description.lower() == task_description.lower() and t.time == time)]
    
    if len(pet.tasks) < original_count:
        save_owner(owner)
        return f"Successfully deleted task '{task_description}' for {pet_name} at {time}."
    else:
        return f"Error: Task '{task_description}' at {time} not found for {pet_name}."

def update_pet_task(pet_name: str, old_description: str, old_time: str, new_description=None, new_time=None, new_duration=None, new_priority=None, new_frequency=None):
    """Updates an existing task's details."""
    owner = get_current_owner()
    pet = next((p for p in owner.pets if p.name.lower() == pet_name.lower()), None)
    if not pet:
        return f"Error: Pet '{pet_name}' not found."
    
    task = next((t for t in pet.tasks if t.description.lower() == old_description.lower() and t.time == old_time), None)
    if not task:
        return f"Error: Task '{old_description}' at {old_time} not found for {pet_name}."
    
    if new_description: task.description = new_description
    if new_time: task.time = new_time
    if new_duration: task.duration = new_duration
    if new_priority: task.priority = new_priority
    if new_frequency: task.frequency = new_frequency
    
    save_owner(owner)
    return f"Successfully updated task for {pet_name}."
