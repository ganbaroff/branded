"""
Advanced example demonstrating error handling, retries, and state management.
"""

from branded import Agent, Config
import time
import random


class RobustAgent(Agent):
    """
    An agent that demonstrates robust error handling and retry logic.
    """
    
    def __init__(self, name: str = "RobustAgent", max_attempts: int = 3):
        super().__init__(name=name)
        self.max_attempts = max_attempts
        self.set_state("attempts", 0)
        self.set_state("successes", 0)
        self.set_state("failures", 0)
    
    def _execute(self) -> None:
        """
        Execute tasks with retry logic and error handling.
        """
        self.logger.info("Starting robust agent execution")
        
        tasks = ["task_1", "task_2", "task_3", "task_4", "task_5"]
        
        for task in tasks:
            if not self._running:
                self.logger.info("Agent stopped during execution")
                break
            
            self._execute_task_with_retry(task)
        
        # Report final statistics
        attempts = self.get_state("attempts")
        successes = self.get_state("successes")
        failures = self.get_state("failures")
        
        self.logger.info("="*50)
        self.logger.info(f"Execution Summary:")
        self.logger.info(f"  Total attempts: {attempts}")
        self.logger.info(f"  Successful: {successes}")
        self.logger.info(f"  Failed: {failures}")
        self.logger.info(f"  Success rate: {successes/len(tasks)*100:.1f}%")
        self.logger.info("="*50)
    
    def _execute_task_with_retry(self, task_name: str) -> bool:
        """
        Execute a task with retry logic.
        
        Args:
            task_name: Name of the task to execute
            
        Returns:
            True if task succeeded, False otherwise
        """
        for attempt in range(1, self.max_attempts + 1):
            try:
                self.logger.info(f"Executing {task_name} (attempt {attempt}/{self.max_attempts})")
                
                # Increment attempt counter
                attempts = self.get_state("attempts")
                self.set_state("attempts", attempts + 1)
                
                # Simulate task that might fail
                success = self._simulate_task(task_name)
                
                if success:
                    self.logger.info(f"✓ {task_name} completed successfully")
                    successes = self.get_state("successes")
                    self.set_state("successes", successes + 1)
                    return True
                else:
                    raise Exception(f"Task {task_name} failed")
                    
            except Exception as e:
                self.logger.warning(f"✗ Attempt {attempt} failed: {e}")
                
                if attempt < self.max_attempts:
                    # Exponential backoff
                    wait_time = 2 ** (attempt - 1)
                    self.logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"✗ {task_name} failed after {self.max_attempts} attempts")
                    failures = self.get_state("failures")
                    self.set_state("failures", failures + 1)
                    return False
    
    def _simulate_task(self, task_name: str) -> bool:
        """
        Simulate a task that might fail randomly.
        
        Args:
            task_name: Name of the task
            
        Returns:
            True if task succeeds, False otherwise
        """
        # Simulate some work
        time.sleep(0.5)
        
        # Randomly succeed or fail (70% success rate)
        return random.random() < 0.7


def main():
    print("=" * 60)
    print("Advanced Agent Example: Error Handling and Retries")
    print("=" * 60)
    print()
    
    # Create a robust agent with retry logic
    agent = RobustAgent(name="RobustAgent", max_attempts=3)
    
    print(f"Agent: {agent}")
    print(f"Max retry attempts: {agent.max_attempts}")
    print()
    
    # Run the agent
    agent.run()
    
    print()
    print("Agent execution completed!")


if __name__ == "__main__":
    # Set random seed for reproducibility (optional)
    # random.seed(42)
    main()
