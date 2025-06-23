import logging

LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S%Z'
LOG_MSG_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s'


class CustomFormatter(logging.Formatter):
    bold = "\033[1m"
    blue = "\033[94m"
    white = "\033[97m"
    green = "\033[92m"
    yellow = "\033[93m"
    red = "\033[91m"
    bold_white = bold + white
    bold_blue = bold + blue
    bold_green = bold + green
    bold_yellow = bold + yellow
    bold_red = bold + red
    end = "\033[0m"

    FORMATS = {
        logging.DEBUG: blue,
        logging.INFO: white,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: bold_red
    }

    def format(self, record):
        log_color = self.FORMATS.get(record.levelno)
        return logging.Formatter(
            fmt=f'{log_color}{LOG_MSG_FORMAT}{self.end}',
            datefmt=LOG_DATE_FORMAT,
        ).format(record)