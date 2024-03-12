import logging
import sys


class CustomFormatter(logging.Formatter):
    color_codes = {
        "green": "\x1b[32m",
        "grey": "\x1b[38;20m",
        "yellow": "\x1b[33;20m",
        "red": "\x1b[31;20m",
        "bold_red": "\x1b[31;1m",
        "reset": "\x1b[0m"
    }

    log_pattern = "[%(asctime)s]%(levelname)7s[%(filename)20s:%(lineno)4s - %(funcName)15s()]:%(message)s"

    FORMATS = {
        logging.DEBUG: color_codes["green"] + log_pattern + color_codes["reset"],
        logging.INFO: color_codes["grey"] + log_pattern + color_codes["reset"],
        logging.WARNING: color_codes["yellow"] + log_pattern + color_codes["reset"],
        logging.ERROR: color_codes["red"] + log_pattern + color_codes["reset"],
        logging.CRITICAL: color_codes["bold_red"] + log_pattern + color_codes["reset"]
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger("smart_tagger")
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(CustomFormatter())

logger.addHandler(stream_handler)
logger.propagate = False


def get_logger(log_name: str = "") -> logging.Logger:
    """
    Provide a logger.
    :param log_name: Name of the logger (not the displayed name in logs).
    :return: The logger.
    """

    if not log_name:
        return logging.getLogger("smart_tagger")

    new_logger = logging.getLogger(f"smart_tagger.{log_name}")

    return new_logger
