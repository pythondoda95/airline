# file_handling/logs/file_logger.py
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent / "actions.log"


def log_action(text: str) -> None:
    """
    Very simple team-style logging:
    YYYY-MM-DD HH:MM:SS | MESSAGE
    """
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{now} | {text}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)
