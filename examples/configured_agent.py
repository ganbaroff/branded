"""
Example of using configuration files with agents.
"""

from branded import Agent, Config
import os


def main():
    # Load configuration from file
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "example_config.yaml")
    
    try:
        config = Config(config_path=config_path)
        
        # Get configuration values
        agent_name = config.get("agent.name", "ConfiguredAgent")
        log_level = config.get("settings.log_level", "INFO")
        
        print(f"Configuration loaded from: {config_path}")
        print(f"Agent name: {agent_name}")
        print(f"Log level: {log_level}")
        
        # Create agent with configuration
        agent = Agent(name=agent_name, config=config, log_level=log_level)
        
        # Run the agent
        agent.run()
        
        print("Configured agent execution completed!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Using default configuration instead...")
        
        # Fallback to default config
        agent = Agent(name="DefaultAgent")
        agent.run()


if __name__ == "__main__":
    main()
