import sqlite3

def create_tables():
    conn = sqlite3.connect('industries.db')
    cursor = conn.cursor()

    # Create industries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS industries (
            industry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            industry_name TEXT NOT NULL,
            age INTEGER,
            division_id INTEGER,
            FOREIGN KEY (division_id) REFERENCES divisions(division_id)
        )
    ''')

    # Create divisions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS divisions (
            division_id INTEGER PRIMARY KEY AUTOINCREMENT,
            division_name TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
