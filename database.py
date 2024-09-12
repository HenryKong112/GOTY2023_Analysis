import sqlite3  # Import the SQLite library to handle database operations
import api

def create_table():
    """
    Create a table in the SQLite database.
    """
    conn = sqlite3.connect('goty2023.db')  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments(
            Username VARCHAR(256),  
            Comment_ID VARCHAR(256),
            Parent_ID VARCHAR(256),
            PublishedAt DATETIME,  
            Like INTEGER,
            Comment TEXT 
        );
    ''')  # SQL command to create the table if it doesn't exist
    conn.commit()  # Commit the transaction
    conn.close()  # Close the database connection
    
def insert_data():
    """
    Insert data from CSV files into the SQLite database.
    """
    conn = sqlite3.connect('goty2023.db')  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    for row in api.df_combined.itertuples():  # Iterate over each row in the DataFrame
        cursor.execute(
            """
            INSERT INTO comments (Username, Comment_ID, Parent_ID ,PublishedAt, Like, Comment)
            VALUES (?,?,?,?,?,?)
            """,
            (row.Username, row.Comment_ID, row.Parent_ID, row.PublishedAt, row.Like, row.Comment)
        )  # Insert the data into the table
    conn.commit()  # Commit the transaction
    conn.close()  # Close the database connection

if __name__ == "__main__":
    create_table()
    insert_data()