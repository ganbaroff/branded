"""
Example of creating a custom agent by extending the base Agent class.
"""

from branded import Agent
import time


class CustomAgent(Agent):
    """
    A custom agent that performs specific tasks.
    """
    
    def __init__(self, name: str = "CustomAgent", iterations: int = 3):
        super().__init__(name=name)
        self.iterations = iterations
    
    def _execute(self) -> None:
        """
        Override the execute method with custom behavior.
        """
        self.logger.info(f"Starting custom execution with {self.iterations} iterations")
        
        for i in range(self.iterations):
            if not self._running:
                self.logger.info("Agent stopped by external request")
                break
            
            self.logger.info(f"Iteration {i + 1}/{self.iterations}")
            self.set_state(f"iteration_{i}", f"Completed at {time.time()}")
            
            # Simulate some work
            time.sleep(1)
        
        self.logger.info("Custom execution completed")
        
        # Display final state
        for key, value in self._state.items():
            self.logger.info(f"State: {key} = {value}")


def main():
    # Create a custom agent with 5 iterations
    agent = CustomAgent(name="MyCustomAgent", iterations=5)
    
    print(f"Created: {agent}")
    
    # Run the agent
    agent.run()
    
    print("Custom agent execution completed!")


if __name__ == "__main__":
    main()
