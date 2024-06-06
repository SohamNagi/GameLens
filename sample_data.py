import sqlite3

# filename to form database
file = "SampleData.sqlite"

try:
    conn = sqlite3.connect(file)
    print("Database SampleData.sqlite formed.")

    # Create a cursor object
    cursor = conn.cursor()

    # SQL command to create a table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        home_team TEXT NOT NULL,
        away_team TEXT NOT NULL,
        home_goals INTEGER NOT NULL,
        away_goals INTEGER NOT NULL
    );
    """

    # Execute the SQL command
    cursor.execute(create_table_query)

    # Dummy data
    matches = [
        ("Team A", "Team B", 2, 1),
        ("Team C", "Team D", 3, 3),
        ("Team E", "Team F", 0, 2),
        ("Team G", "Team H", 1, 1)
    ]

    # Insert dummy data into the table
    insert_query = "INSERT INTO matches (home_team, away_team, home_goals, away_goals) VALUES (?, ?, ?, ?)"
    cursor.executemany(insert_query, matches)

    # Commit the changes
    conn.commit()

    print("Table 'matches' created and dummy data inserted successfully.")

    # Query to check the inserted data
    cursor.execute("SELECT * FROM matches")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
finally:
    if conn:
        conn.close()
