"""Base template for all JARVIS plugins"""
from utils.config_loader import load_config
import re

class BasePlugin:
    def __init__(self):
        self.config = load_config()
        self.name = self.__class__.__name__
        
    def parse_voice_command(self, command):
        """Standard voice command parsing"""
        command = command.lower().strip('?')
        
        # Common patterns to extract key phrases
        patterns = {
            'weather': r'(weather|temperature).*(in|for|at)\s+(.*)',
            'calculate': r'(calculate|evaluate|what is)\s+(.*)',
            'search': r'(search|look up|find).*(on|for)\s+(.*)',
            'play': r'(play|start)\s+(.*)'
        }
        
        # Try to match patterns
        for intent, pattern in patterns.items():
            match = re.search(pattern, command)
            if match:
                return intent, match.groups()[-1].strip()
                
        return None, command

    def run(self, *args, **kwargs):
        """Main execution method to be overridden"""
        raise NotImplementedError("Plugins must implement run()")

    def handle_error(self, error):
        """Standard error handling"""
        return f"{self.name} error: {str(error)}"

    def validate_config(self, required_keys=[]):
        """Validate required config keys"""
        missing = [key for key in required_keys if not self.config.get(key)]
        if missing:
            raise ValueError(f"Missing config keys: {', '.join(missing)}")
