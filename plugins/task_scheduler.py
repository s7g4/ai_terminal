import schedule
import time
from core.memory import MemoryManager
from utils.logger import get_logger

logger = get_logger("task_scheduler")

class TaskSchedulerPlugin:
    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        if not args:
            return "Available commands: schedule <task_function> <time_str>, run"
        
        command = args[0].lower()
        if command == "schedule" and len(args) == 3:
            task_function = args[1]
            time_str = args[2]
            return self.schedule_task(task_function, time_str)
        elif command == "run":
            return self.run_scheduler()
        else:
            return f"Unknown command: {command}"

    def __init__(self):
        self.memory = MemoryManager()
        self.load_scheduled_tasks()

    def schedule_task(self, task_function, time_str, task_name=None):
        """Schedule a task and store it in memory"""
        if not task_name:
            task_name = task_function.__name__
            
        job = schedule.every().day.at(time_str).do(self._wrap_task(task_function, task_name))
        self._save_task(job, task_name, time_str)
        logger.info(f"Scheduled task '{task_name}' at {time_str}")

    def _wrap_task(self, task_function, task_name):
        """Wrapper to log task execution"""
        def wrapped():
            try:
                result = task_function()
                self.memory.update_context(
                    f"Task executed: {task_name}",
                    f"Result: {str(result)[:100]}..." if result else "No result"
                )
                return result
            except Exception as e:
                logger.error(f"Task failed: {task_name} - {str(e)}")
                raise
        return wrapped

    def _save_task(self, job, task_name, time_str):
        """Save task to memory"""
        tasks = self.memory.memory.get("scheduled_tasks", [])
        tasks.append({
            "name": task_name,
            "time": time_str,
            "last_run": None,
            "next_run": str(job.next_run)
        })
        self.memory.memory["scheduled_tasks"] = tasks
        self.memory.save()

    def load_scheduled_tasks(self):
        """Load previously scheduled tasks from memory"""
        if "scheduled_tasks" in self.memory.memory:
            logger.info(f"Loaded {len(self.memory.memory['scheduled_tasks'])} scheduled tasks from memory")

    def run_scheduler(self):
        """Run the scheduler loop"""
        logger.info("Starting task scheduler")
        while True:
            schedule.run_pending()
            time.sleep(1)

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    scheduler = TaskSchedulerPlugin()
    return scheduler.run(*args, **kwargs)
