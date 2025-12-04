"""
Simple example of creating and running a basic agent.
"""

from branded import Agent


def main():
    # Create a basic agent
    agent = Agent(name="SimpleAgent", log_level="INFO")
    
    # Set some state
    agent.set_state("counter", 0)
    agent.set_state("message", "Hello from Simple Agent!")
    
    print(f"Agent created: {agent}")
    print(f"Agent state - counter: {agent.get_state('counter')}")
    print(f"Agent state - message: {agent.get_state('message')}")
    
    # Run the agent
    agent.run()
    
    print("Agent execution completed!")


if __name__ == "__main__":
    main()
