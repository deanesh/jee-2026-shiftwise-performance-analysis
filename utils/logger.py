# utils/logger.py

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_logger(
    name: str = __name__,
    log_file: str = "logs/jee_analysis.log",
    level: int = logging.INFO,
    max_bytes: int = 5 * 1024 * 1024,  # 5 MB per file
    backup_count: int = 3
) -> logging.Logger:
    """
    Returns a logger that logs to console and a single consolidated file with rollover.
    Log format: YYYY-MM-DD HH:MM:SS | LEVEL | filename::function | message

    Parameters:
    -----------
    name : str
        Logger name
    log_file : str
        Path to the log file
    level : int
        Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    max_bytes : int
        Max size per log file before rollover
    backup_count : int
        Number of backup files to keep
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Ensure log folder exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(filename)s::%(funcName)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # File handler with rotation
        fh = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger