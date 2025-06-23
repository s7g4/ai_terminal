import os
import json
import requests

NOTES_FILE = "data/notes.json"

from utils.logger import get_logger

logger = get_logger("notes")

class NotesManager:
    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        if not args:
            return "Available commands: add <content>, list, search <keyword>"
            
        command = args[0].lower()
        if command == "add" and len(args) > 1:
            self.add_note(" ".join(args[1:]))
            return "Note added successfully"
        elif command == "list":
            notes = self.list_notes()
            return "\n".join([f"{i+1}. {note['content']}" for i, note in enumerate(notes)]) if notes else "No notes found"
        elif command == "search" and len(args) > 1:
            results = self.search_note(" ".join(args[1:]))
            if isinstance(results, list):
                return "\n".join([f"{i+1}. {note['content']}" for i, note in enumerate(results)]) if results else "No matching notes found"
            return results
        else:
            return f"Unknown command: {command}"

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "w") as f:
                json.dump([], f)
        logger.info("Notes manager initialized")

    def add_note(self, content):
        notes = self._load_notes()
        notes.append({"content": content})
        self._save_notes(notes)
        logger.info(f"Added note: {content[:50]}...")

    def list_notes(self):
        notes = self._load_notes()
        logger.info(f"Listed {len(notes)} notes")
        return notes

    def search_note(self, keyword):
        notes = self._load_notes()
        results = [note for note in notes if keyword.lower() in note["content"].lower()]
        if results:
            logger.info(f"Found {len(results)} notes matching '{keyword}'")
            return results
        else:
            logger.info(f"No local notes found, searching online for '{keyword}'")
            return self.search_online_note(keyword)

    def search_online_note(self, keyword):
        try:
            response = requests.get(
                f"https://api.duckduckgo.com/?q={keyword}+notes&format=json"
            )
            data = response.json()
            result = data.get("Abstract") or "No online notes found."
            logger.info(f"Online search result for '{keyword}': {result[:50]}...")
            return result
        except Exception as e:
            logger.error(f"Online search failed: {str(e)}")
            return "Online search failed."

    def _load_notes(self):
        try:
            with open(NOTES_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load notes: {str(e)}")
            return []

    def _save_notes(self, notes):
        try:
            with open(NOTES_FILE, "w") as f:
                json.dump(notes, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save notes: {str(e)}")

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    notes_manager = NotesManager()
    return notes_manager.run(*args, **kwargs)
