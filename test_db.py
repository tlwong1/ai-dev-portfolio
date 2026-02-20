from monitor import check_url
from database import init_db, save_check
from config import URLS

init_db()

print("Running checks and saving to DB...\n")
for url in URLS:
    result = check_url(url)
    save_check(result)
    print(f"[{result['status'].upper()}] {url} → saved to DB")

print("\n✅ Done! Check the database:")
import sqlite3
conn = sqlite3.connect("uptime.db")
for row in conn.execute("SELECT * FROM checks ORDER BY id DESC LIMIT 5"):
    print(row)
conn.close()