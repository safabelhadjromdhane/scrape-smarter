import logging
from pathlib import Path
from datetime import datetime
import sys

def setup_logger(name: str, log_level: str = "INFO") -> logging.Logger:
    """
    Configure a logger with console and file handlers.
    
    Args:
        name: Logger name (usually __name__)
        log_level: DEBUG/INFO/WARNING/ERROR/CRITICAL
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Create logs directory if not exists
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Timestamped log file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = log_dir / f"{name}_{timestamp}.log"
    
    # Formatter
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(fmt)
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # File Handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Example usage:
if __name__ == "__main__":
    logger = setup_logger("test_logger", "DEBUG")
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")