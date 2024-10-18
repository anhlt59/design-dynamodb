import logging
import sys

from app.common.configs import LOG_FORMAT, LOG_LEVEL

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(handler)

# set log level
logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("pynamodb").setLevel(logging.WARNING)
