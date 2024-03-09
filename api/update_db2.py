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

# Assuming a basic structure for the 'users' table, modify as needed
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT,
    date_joined DATETIME
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Tables 'uploads' and 'users' created successfully.")
