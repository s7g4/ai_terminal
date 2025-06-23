from utils.logger import get_logger
from core.memory import MemoryManager

logger = get_logger("todo_list")

class TodoListPlugin:
    def __init__(self):
        self.memory = MemoryManager()
        self.todo_list = self.memory.memory.get("todo_list", [])

    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        if not args:
            return "Available commands: add <task>, remove <task>, list"
            
        command = args[0].lower()
        if command == "add" and len(args) > 1:
            return self.add_task(" ".join(args[1:]))
        elif command == "remove" and len(args) > 1:
            return self.remove_task(" ".join(args[1:]))
        elif command == "list":
            return self.list_tasks()
        else:
            return f"Unknown command: {command}"

    def add_task(self, task):
        self.todo_list.append(task)
        self._save_tasks()
        logger.info(f"Added task: {task}")
        return f"Task '{task}' added."

    def remove_task(self, task):
        if task in self.todo_list:
            self.todo_list.remove(task)
            self._save_tasks()
            logger.info(f"Removed task: {task}")
            return f"Task '{task}' removed."
        else:
            logger.warning(f"Task not found: {task}")
            return f"Task '{task}' not found."

    def list_tasks(self):
        logger.info(f"Listed {len(self.todo_list)} tasks")
        return "\n".join(f"• {task}" for task in self.todo_list) if self.todo_list else "No tasks found."

    def _save_tasks(self):
        """Save tasks to memory"""
        self.memory.memory["todo_list"] = self.todo_list
        self.memory.save()

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    todo = TodoListPlugin()
    return todo.run(*args, **kwargs)
