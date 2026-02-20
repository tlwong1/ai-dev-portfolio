import requests
import datetime


def check_url(url, timeout=5):
    """
    Ping a URL and return a result dict with:
    - url: the URL checked
    - status: "up" or "down"
    - response_time_ms: how long the request took in milliseconds
    - status_code: the HTTP status code (or None if request failed)
    - checked_at: timestamp of the check
    """
    checked_at = datetime.datetime.utcnow().isoformat()

    try:
        response = requests.head(url, timeout=timeout)
        response_time_ms = response.elapsed.total_seconds() * 1000
        status = "up" if response.status_code < 400 else "down"
        status_code = response.status_code

    except requests.exceptions.Timeout:
        response_time_ms = None
        status = "down"
        status_code = None

    except requests.exceptions.RequestException:
        response_time_ms = None
        status = "down"
        status_code = None

    return {
        "url": url,
        "status": status,
        "response_time_ms": response_time_ms,
        "status_code": status_code,
        "checked_at": checked_at,
    }


if __name__ == "__main__":
    # Quick manual test — run with: python monitor.py
    test_urls = [
        "https://www.google.com",
        "https://httpstat.us/500",   # simulates a server error
        "https://httpstat.us/404",   # simulates a not found
    ]

    for url in test_urls:
        result = check_url(url)
        print(f"[{result['status'].upper()}] {result['url']}")
        print(f"  Status code: {result['status_code']}")
        print(f"  Response time: {result['response_time_ms']:.1f}ms" if result['response_time_ms'] else "  Response time: N/A")
        print(f"  Checked at: {result['checked_at']}")
        print()
