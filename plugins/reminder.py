import threading
import time
from utils.logger import get_logger

logger = get_logger("reminder")

class ReminderPlugin:
    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        if not args or len(args) < 3:
            return "Usage: set <message> <delay_seconds>"
            
        if args[0].lower() == "set":
            try:
                delay = float(args[-1])
                message = " ".join(args[1:-1])
                return self.set_reminder(message, delay)
            except ValueError:
                return "Error: Delay must be a number"
        else:
            return f"Unknown command: {args[0]}"

    def set_reminder(self, message, delay):
        def remind():
            time.sleep(delay)
            logger.info(f"Reminder triggered: {message}")
            print(f"Reminder: {message}")

        threading.Thread(target=remind).start()
        logger.info(f"Set reminder: '{message}' in {delay} seconds")
        return f"Reminder set for {delay} seconds: '{message}'"

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    reminder = ReminderPlugin()
    return reminder.run(*args, **kwargs)
