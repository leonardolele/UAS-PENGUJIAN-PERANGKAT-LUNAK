import sqlite3

DB_FILE = "url_shortener.db"

def get_connection(db_name=DB_FILE):
    conn = sqlite3.connect(db_name, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_name=DB_FILE):
    conn = get_connection(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            long_url TEXT NOT NULL,
            clicks INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()