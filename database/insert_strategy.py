import sqlite3

def insert_strategy(
    database_url: str,
    ticket: str,
    method: str,
    parameters: str,
    results
):
    conn = sqlite3.connect(database_url)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO strategies (ticket, method, parameters, results)
        VALUES (?, ?, ?, ?)
    """, (ticket, method, parameters, results))

    conn.commit()
    conn.close()

