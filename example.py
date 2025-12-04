"""
Example script demonstrating how to use API keys with the branded AI agent.

This example shows how to load and use API keys from the configuration module.
"""

from config import load_openai_key, ConfigurationError


def main():
    """Main function demonstrating API key usage."""
    print("Branded AI Agent - Example Usage")
    print("=" * 50)
    
    try:
        # Load the API key
        api_key = load_openai_key()
        
        # Mask the API key for display (show only first 8 and last 4 characters for keys > 20 chars)
        if len(api_key) > 20:
            masked_key = f"{api_key[:8]}...{api_key[-4:]}"
        else:
            masked_key = "***"
        
        print(f"✓ API key loaded successfully: {masked_key}")
        print()
        print("You can now use this API key to:")
        print("  - Initialize your AI model")
        print("  - Make API calls to OpenAI")
        print("  - Build your AI agent functionality")
        print()
        print("Next steps:")
        print("  1. Import your preferred AI library (e.g., openai)")
        print("  2. Initialize it with the API key")
        print("  3. Start building your agent!")
        
    except ConfigurationError as e:
        print(f"✗ Error: {e}")
        print()
        print("Please follow the setup instructions in README.md to configure your API key.")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
