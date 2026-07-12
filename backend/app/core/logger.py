import logging
from logging import FileHandler
from pathlib import Path


CURRENT_FILE = Path(__file__).resolve()

BACKEND_DIR = CURRENT_FILE.parents[2]

LOG_DIR = BACKEND_DIR / "logs"

LOG_DIR.mkdir(
    exist_ok=True
)

LOG_FILE = LOG_DIR / "app.log"


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )
)

logger = logging.getLogger(__name__)

file_handler = FileHandler(LOG_FILE)

formatter = logging.Formatter(

    "%(asctime)s | %(levelname)s | %(message)s"

)

file_handler.setFormatter(
    formatter
)

logger.addHandler(
    file_handler
)

