import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from utils.logger import get_logger
logger = get_logger("memory")

class MemoryManager:
    """Enhanced memory management with advanced features"""
    def __init__(self, max_context_length: int = 20):
        self.MEMORY_FILE = "data/memory.json"
        self.max_context_length = max_context_length
        self.memory = self._load()

    def _load(self) -> Dict:
        """Load memory from file or create new if doesn't exist"""
        if not os.path.exists(self.MEMORY_FILE):
            os.makedirs(os.path.dirname(self.MEMORY_FILE), exist_ok=True)
            with open(self.MEMORY_FILE, "w") as f:
                json.dump({
                    "context": [],
                    "preferences": {
                        "audio_device_index": 0
                    }
                }, f)
            logger.info(f"Created new memory file at {self.MEMORY_FILE}")

        with open(self.MEMORY_FILE, "r") as f:
            memory = json.load(f)
            # Ensure required keys exist
            if "context" not in memory:
                memory["context"] = []
            if "preferences" not in memory:
                memory["preferences"] = {"audio_device_index": 0}
            elif "audio_device_index" not in memory["preferences"]:
                memory["preferences"]["audio_device_index"] = 0
            return memory

    def save(self) -> None:
        """Save memory to file"""
        with open(self.MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)
        logger.info(f"Saved memory to {self.MEMORY_FILE}")

    def update_context(self, user_input: str, ai_response: str) -> None:
        """Update memory with new interaction"""
        self.memory["context"].append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "ai": ai_response
        })
        self._trim_context()
        self.save()

    def _trim_context(self) -> None:
        """Keep only recent interactions based on max_context_length"""
        self.memory["context"] = self.memory["context"][-self.max_context_length:]

    def get_context(self, n: Optional[int] = None) -> List[Dict]:
        """Get memory context, optionally limited to last n interactions"""
        context = self.memory.get("context", [])
        return context[-n:] if n else context

    def clear_context(self) -> None:
        """Clear all context memory"""
        self.memory["context"] = []
        self.save()

# Legacy implementation for backward compatibility
class Memory:
    def __init__(self):
        self.MEMORY_FILE = "data/memory.json"
        self.memory = self.load()

    def load(self):
        """Load memory from file or create new if doesn't exist"""
        if not os.path.exists(self.MEMORY_FILE):
            os.makedirs(os.path.dirname(self.MEMORY_FILE), exist_ok=True)
            with open(self.MEMORY_FILE, "w") as f:
                json.dump({
                    "context": [],
                    "preferences": {
                        "audio_device_index": 0
                    }
                }, f)
            logger.info(f"Created new memory file at {self.MEMORY_FILE}")

        with open(self.MEMORY_FILE, "r") as f:
            memory = json.load(f)
            if "preferences" not in memory:
                memory["preferences"] = {"audio_device_index": 0}
            elif "audio_device_index" not in memory["preferences"]:
                memory["preferences"]["audio_device_index"] = 0
            return memory

    def save(self):
        """Save memory to file"""
        with open(self.MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)
        logger.info(f"Saved memory to {self.MEMORY_FILE}")

    def update(self, user_input, ai_response):
        """Update memory with new interaction"""
        self.memory["context"].append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "ai": ai_response
        })
        # Keep only last 20 interactions
        self.memory["context"] = self.memory["context"][-20:]
        self.save()

    def get_context(self):
        """Get the current memory context"""
        return self.memory.get("context", [])

# Legacy functions for backward compatibility
def load_memory():
    memory = Memory()
    return memory.memory

def save_memory(memory_data):
    memory = Memory()
    memory.memory = memory_data
    memory.save()

def update_memory(memory_data, user_input, ai_response):
    memory = Memory()
    memory.memory = memory_data
    memory.update(user_input, ai_response)
