import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create the 'uploads' table
c.execute('''
CREATE TABLE IF NOT EXISTS uploads (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    date_created DATETIME NOT NULL
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Table 'uploads' created successfully.")
