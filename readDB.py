import sqlite3

DATABASE_FILE = 'customers.db'
TABLE_NAME = 'customers'  # You may need to change this if your table is named differently

def view_customer_data():
    """Connects to the database and prints all records from the customer table."""
    conn = None # Initialize connection to None
    try:
        # 1. Connect to the SQLite database file
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        print(f"--- Data from {TABLE_NAME} in {DATABASE_FILE} ---")

        # 2. Execute a SELECT query to get all columns and rows
        cursor.execute(f"SELECT * FROM {TABLE_NAME}")

        # 3. Fetch all the results
        records = cursor.fetchall()

        # 4. Get column names (headers)
        column_names = [description[0] for description in cursor.description]
        print("| " + " | ".join(column_names) + " |")
        print("-" * (sum(len(c) for c in column_names) + 3 * len(column_names) + 1)) # Simple separator line

        # 5. Print the fetched records
        if records:
            for row in records:
                # Convert all items to string for printing
                print("| " + " | ".join(map(str, row)) + " |")
        else:
            print(f"\nNo records found in the '{TABLE_NAME}' table.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # 6. Close the connection
        if conn:
            conn.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    view_customer_data()