import sqlite3

DB_FILE = "uptime.db"

def init_db():
    """Create the database table if it doesn't exist"""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status TEXT NOT NULL,
            response_time_ms REAL,
            status_code INTEGER,
            checked_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print(f"✅ Database initialized: {DB_FILE}")

def save_check(result):
    """Save one check result to the database"""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        INSERT INTO checks (url, status, response_time_ms, status_code, checked_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        result["url"],
        result["status"],
        result["response_time_ms"],
        result["status_code"],
        result["checked_at"]
    ))
    conn.commit()
    conn.close()

def get_last_status(url):
    """Get the previous status of a URL (for alerting later)"""
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute(
        "SELECT status FROM checks WHERE url=? ORDER BY id DESC LIMIT 1",
        (url,)
    ).fetchone()
    conn.close()
    return row[0] if row else None