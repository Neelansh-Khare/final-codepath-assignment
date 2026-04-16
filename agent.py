import agent_tools
from llm_client import GeminiClient

class PetSitterAgent:
    def __init__(self):
        self.client = GeminiClient()
        # Define the tools the agent can use
        self.tools = [
            agent_tools.get_schedule,
            agent_tools.add_pet_task,
            agent_tools.delete_pet_task,
            agent_tools.update_pet_task
        ]
        self.model = self.client.get_model(tools=self.tools)
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def process_request(self, user_prompt: str):
        """Processes the user request using the agent's tool-calling loop."""
        system_instruction = (
            "You are the PawPal+ AI Pet Sitter. Your goal is to help owners manage their pets' schedules. "
            "You can view, add, delete, or update tasks for pets. "
            "When a user gives a command, first check the current schedule to understand the state. "
            "After making changes, always check if there are any new conflicts. "
            "If conflicts arise from your changes, inform the user or try to resolve them if possible. "
            "Always be helpful and concise."
        )
        
        # Combine system instruction with user prompt for the first message if needed, 
        # but here we'll just send the prompt to the active chat session.
        response = self.chat.send_message(user_prompt)
        return response.text

if __name__ == "__main__":
    # Simple CLI test
    agent = PetSitterAgent()
    print("Agent ready. Type your request (or 'exit' to quit):")
    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            break
        try:
            result = agent.process_request(user_input)
            print(f"Agent: {result}")
        except Exception as e:
            print(f"Error: {e}")
