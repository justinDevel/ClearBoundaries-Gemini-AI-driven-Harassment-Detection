

from datetime import timedelta, datetime, timezone
import logging


logger = logging.getLogger(__name__)


def get_current_datetime():
    current_time = datetime.now(timezone.utc)

    return current_time.isoformat()





