import sqlite3
from local_app.utils import get_all_phases, get_all_topics, get_all_subtopics

def create_table(cursor, table_name, columns):
    """Create a table in the SQLite database."""
    columns = [column.replace('-', '_') for column in columns]
    columns_definition = ', '.join(columns)
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})")

def insert_data(cursor, table_name, data):
    """Insert data into the SQLite database."""
    columns = list(data[0].keys())
    # replace '-' with '_' in column names
    columns = [column.replace('-', '_') for column in columns]
    placeholders = ', '.join(['?' for _ in range(len(columns))])
    column_names = ', '.join(columns)
    for row in data:
        values = [row[column] for column in columns]
        cursor.execute(f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})", values)

def list_of_dicts_to_sqlite(data, db_file, table_name):
    """Convert list of dictionaries to SQLite database."""
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Determine columns from the first dictionary
    columns = list(data[0].keys())

    # Create the table
    create_table(cursor, table_name, columns)

    # Insert data into the table
    insert_data(cursor, table_name, data)

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Example usage
if __name__ == '__main__':
    school_data = {
        'phases': get_all_phases(),
        'topics': get_all_topics(),
        'subtopics': get_all_subtopics()
    }

    db_file = 'school.db'
    for table, data in school_data.items():
        list_of_dicts_to_sqlite(data, db_file, table)
