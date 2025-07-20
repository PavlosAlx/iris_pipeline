import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file="file_errors.log",
                  max_bytes=2000,
                  backup_count=5,
                  level="INFO",
                  format="%(asctime)s - %(levelname)s - %(name)s- %(message)s"):
    

    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(level)

    # remove existing handlers to avoid duplicates
    if root.handlers:
        for handler in root.handlers[:]:
            root.removeHandler(handler)

    # rotating file handler
    file_handler = RotatingFileHandler(
        filename = log_file,
        maxBytes = max_bytes,
        backupCount = backup_count
        )
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(format))
    root.addHandler(file_handler)

    # console handler - messages to appear in the console as well
    console_handler  = logging.StreamHandler()
    console_handler .setLevel(level)
    console_handler .setFormatter(logging.Formatter(format))
    root.addHandler(console_handler )

    return 

def get_logger(name):
    return logging.getLogger(name)

def ensure_dir(path):
    dirpath = os.path.dirname(path) or "."
    os.makedirs(dirpath, exist_ok=True)
    return 