import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / 'history.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS estimations (id INTEGER PRIMARY KEY, N INT, tile INT, misses INT, accesses INT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
