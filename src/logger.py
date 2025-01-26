import logging


def setup_logger(name: str) -> logging.Logger:
    """
    Configure and return a logger with both console and file handlers.

    Args:
        name: The name of the logger to create

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()

    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    return logger
