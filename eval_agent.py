import json
import os
from agent import PetSitterAgent
from pawpal_system import Owner, Pet, Task

DATA_FILE = "data.json"

def setup_test_data():
    """Sets up a fresh data.json for testing."""
    owner = Owner(name="Test Owner")
    dog = Pet(name="Buddy", species="Dog")
    # Add an initial task
    dog.add_task(Task(description="Morning Walk", time="08:00", duration=30, priority="High", frequency="Daily"))
    owner.add_pet(dog)
    owner.save_to_json(DATA_FILE)
    return owner

def run_eval():
    print("--- Starting Agent Evaluation ---")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("SKIP: GOOGLE_API_KEY not found. Cannot run live evaluation.")
        return

    setup_test_data()
    agent = PetSitterAgent()

    scenarios = [
        {
            "name": "Add Task",
            "prompt": "Add a feeding task for Buddy at 09:00.",
            "check": lambda owner: any(t.description == "feeding" and t.time == "09:00" for t in owner.pets[0].tasks)
        },
        {
            "name": "Conflict Resolution",
            "prompt": "Buddy has a vet appointment at 08:00. Reschedule the morning walk to 10:00 to avoid conflict.",
            "check": lambda owner: any(t.description == "Morning Walk" and t.time == "10:00" for t in owner.pets[0].tasks)
        },
        {
            "name": "Delete Task",
            "prompt": "Remove the feeding task at 09:00.",
            "check": lambda owner: not any(t.description == "feeding" and t.time == "09:00" for t in owner.pets[0].tasks)
        }
    ]

    results = []
    for s in scenarios:
        print(f"Running Scenario: {s['name']}...")
        try:
            response = agent.process_request(s['prompt'])
            print(f"Agent Response: {response}")
            
            # Load current state to verify
            owner = Owner.load_from_json(DATA_FILE)
            passed = s['check'](owner)
            results.append({"name": s['name'], "status": "PASS" if passed else "FAIL"})
        except Exception as e:
            print(f"Error in scenario {s['name']}: {e}")
            results.append({"name": s['name'], "status": "ERROR"})

    print("\n--- Evaluation Summary ---")
    for r in results:
        print(f"[{r['status']}] {r['name']}")
    
    pass_count = sum(1 for r in results if r['status'] == "PASS")
    print(f"\nScore: {pass_count}/{len(scenarios)}")

if __name__ == "__main__":
    run_eval()
