from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timedelta

@dataclass
class Task:
    description: str
    time: str  # Format "HH:MM"
    duration: int  # minutes
    priority: str  # "Low", "Medium", "High"
    frequency: str  # "Daily", "Weekly", "Once"
    is_completed: bool = False

    def mark_complete(self):
        """Marks the task as completed."""
        pass

@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Adds a task to the pet's list."""
        pass

@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Adds a pet to the owner's list."""
        pass

class Scheduler:
    def get_all_tasks(self, owner: Owner) -> List[Task]:
        """Retrieves all tasks for all of the owner's pets."""
        pass

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sorts tasks by their scheduled time."""
        pass

    def filter_tasks(self, tasks: List[Task], status: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filters tasks by completion status or pet name."""
        pass

    def check_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detects if multiple tasks are scheduled at the same time and returns warning messages."""
        pass
