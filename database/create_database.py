import sqlite3

def create_database(database_url: str):
    conn = sqlite3.connect(database_url)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS strategies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket TEXT,
            method TEXT,
            parameters TEXT,
            results REAL,
            created_at DATE DEFAULT (date('now'))
        )
    """)

    conn.commit()
    conn.close()


