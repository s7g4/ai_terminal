import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "jarvis_terminal.log")
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5MB
BACKUP_COUNT = 3

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA
    }

    def format(self, record):
        log_fmt = "%(asctime)s | [%(levelname)s] | %(name)s | %(message)s"
        color = self.COLORS.get(record.levelname, "")
        formatter = logging.Formatter(color + log_fmt + Style.RESET_ALL)
        return formatter.format(record)

def get_logger(name="JARVIS", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # Avoid duplicate logs if called multiple times

    if not logger.handlers:
        # Console Handler
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(ColorFormatter())
        logger.addHandler(ch)

        # File Handler
        fh = RotatingFileHandler(LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
        fh.setLevel(level)
        file_formatter = logging.Formatter("%(asctime)s | [%(levelname)s] | %(name)s | %(message)s")
        fh.setFormatter(file_formatter)
        logger.addHandler(fh)

    return logger
