import time
import logging
from datetime import datetime

from monitor import check_url
from database import init_db, save_check, get_last_status
from config import URLS, CHECK_INTERVAL_SECONDS

# === Logging setup ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("monitor.log"),
        logging.StreamHandler()
    ]
)

def main():
    init_db()
    logging.info("Uptime Monitor STARTED - watching %d URLs", len(URLS))

    while True:
        cycle_start = datetime.now()

        for url in URLS:
            result = check_url(url)
            save_check(result)

            previous_status = get_last_status(url)
            if previous_status and previous_status != result["status"]:
                logging.warning(
                    "ALERT - STATUS CHANGE: %s went %s -> %s (code: %s)",
                    url,
                    previous_status.upper(),
                    result["status"].upper(),
                    result["status_code"]
                )

            time_str = f"{result['response_time_ms']:.0f}ms" if result['response_time_ms'] else "N/A"
            logging.info("[%s] %s | %s", result["status"].upper(), url, time_str)

        elapsed = (datetime.now() - cycle_start).total_seconds()
        sleep_time = max(0, CHECK_INTERVAL_SECONDS - elapsed)
        logging.info("Sleeping %.0fs...\n", sleep_time)
        time.sleep(sleep_time)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Monitor stopped by user (Ctrl+C)")
    except Exception as e:
        logging.error("Unexpected error: %s", e)