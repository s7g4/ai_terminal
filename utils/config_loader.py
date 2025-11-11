import os
import json
from dotenv import load_dotenv

def load_config():
    """Load configuration from .env and config.json files."""
    # Load environment variables from .env file
    load_dotenv()

    # Default configuration
    config = {
        "use_model": "ollama",  # Changed to Ollama as free alternative
        "ollama_model": "llama3.2",  # Default Ollama model
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
        "llm_model": "gpt-3.5-turbo",  # For OpenAI if switched
        "voice_rate": 150,
        "voice_volume": 1.0,
        "memory_limit": 20,
        "log_level": "INFO"
    }

    # Load from config.json if exists
    config_file = os.path.join(os.path.dirname(__file__), "..", "config.json")
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                user_config = json.load(f)
                config.update(user_config)
        except json.JSONDecodeError as e:
            print(f"Warning: Could not parse config.json: {e}")

    return config

def load_personality():
    """Load personality settings from personality.json."""
    personality_file = os.path.join(os.path.dirname(__file__), "..", "data", "personality.json")
    if os.path.exists(personality_file):
        try:
            with open(personality_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Warning: Could not parse personality.json: {e}")
            return {}
    return {}
