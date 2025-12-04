"""
Configuration module for loading API keys and environment variables.

This module provides utilities to load and validate API keys from environment
variables, ensuring they are properly configured before use.
"""

import os
from typing import Optional


class ConfigurationError(Exception):
    """Raised when there's an issue with the configuration."""
    pass


def load_api_key(key_name: str, required: bool = True) -> Optional[str]:
    """
    Load an API key from environment variables.
    
    Args:
        key_name: The name of the environment variable containing the API key
        required: Whether the API key is required (raises error if missing)
    
    Returns:
        The API key value, or None if not required and not found
    
    Raises:
        ConfigurationError: If the required API key is not found
    """
    api_key = os.getenv(key_name)
    
    # Treat empty strings as missing keys
    if api_key == "":
        api_key = None
    
    if required and not api_key:
        raise ConfigurationError(
            f"Missing required API key: {key_name}\n"
            f"Please set the {key_name} environment variable.\n"
            f"See README.md for instructions on obtaining and configuring API keys."
        )
    
    return api_key


def load_openai_key() -> str:
    """
    Load the OpenAI API key from environment variables.
    
    Returns:
        The OpenAI API key
    
    Raises:
        ConfigurationError: If the API key is not found
    """
    return load_api_key("OPENAI_API_KEY", required=True)


def load_anthropic_key() -> Optional[str]:
    """
    Load the Anthropic API key from environment variables (optional).
    
    Returns:
        The Anthropic API key, or None if not configured
    """
    return load_api_key("ANTHROPIC_API_KEY", required=False)


def load_google_ai_key() -> Optional[str]:
    """
    Load the Google AI API key from environment variables (optional).
    
    Returns:
        The Google AI API key, or None if not configured
    """
    return load_api_key("GOOGLE_AI_API_KEY", required=False)


def load_huggingface_token() -> Optional[str]:
    """
    Load the Hugging Face token from environment variables (optional).
    
    Returns:
        The Hugging Face token, or None if not configured
    """
    return load_api_key("HUGGINGFACE_API_TOKEN", required=False)


def validate_configuration() -> dict:
    """
    Validate that all required API keys are configured.
    
    Returns:
        A dictionary containing information about configured API keys
    
    Raises:
        ConfigurationError: If any required API key is missing
    """
    config_status = {}
    
    # Check OpenAI key (required)
    try:
        load_openai_key()
        config_status["openai"] = True
    except ConfigurationError:
        raise  # Re-raise for required keys
    
    # Check optional keys
    config_status["anthropic"] = bool(load_anthropic_key())
    config_status["google_ai"] = bool(load_google_ai_key())
    config_status["huggingface"] = bool(load_huggingface_token())
    
    return config_status


if __name__ == "__main__":
    """Example usage and configuration check."""
    print("Checking API key configuration...")
    print("-" * 40)
    
    try:
        config = validate_configuration()
        print("✓ OpenAI API key configured" if config["openai"] else "✗ OpenAI API key missing")
        print("✓ Anthropic API key configured" if config["anthropic"] else "○ Anthropic API key not configured (optional)")
        print("✓ Google AI API key configured" if config["google_ai"] else "○ Google AI API key not configured (optional)")
        print("✓ Hugging Face token configured" if config["huggingface"] else "○ Hugging Face token not configured (optional)")
        print("-" * 40)
        print("Configuration check passed!")
    except ConfigurationError as e:
        print(f"✗ Configuration error: {e}")
        exit(1)
