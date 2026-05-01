import string
import random
from urllib.parse import urlparse
from src.database import get_connection

def generate_short_code(length=6) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def is_valid_url(url: str) -> bool:
    if not url: return False
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def save_url(long_url: str, short_code: str, db_name="url_shortener.db") -> bool:
    conn = get_connection(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO urls (short_code, long_url) VALUES (?, ?)", (short_code, long_url))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def get_long_url(short_code: str, db_name="url_shortener.db") -> str:
    conn = get_connection(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT long_url FROM urls WHERE short_code = ?", (short_code,))
    row = cursor.fetchone()
    conn.close()
    return row["long_url"] if row else None

def increment_click(short_code: str, db_name="url_shortener.db"):
    conn = get_connection(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (short_code,))
    conn.commit()
    conn.close()

def get_stats(short_code: str, db_name="url_shortener.db") -> dict:
    conn = get_connection(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT long_url, clicks FROM urls WHERE short_code = ?", (short_code,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"short_code": short_code, "long_url": row["long_url"], "clicks": row["clicks"]}
    return None