from database.database import get_connection

def main():
    connection = None

    try:
        connection = get_connection()
        print("Successfully connected to the database!")

        cursor = connection.cursor()

        cursor.execute("SELECT DB_NAME()")
        print(f"Connected database: {cursor.fetchone()[0]}")

        cursor.execute("""
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = 'tracker'
        """)

        print("\nAvailable tables:")

        for row in cursor.fetchall():
            print("-", row[0])

    except Exception as error:
        print(f"Failed to connect to the database: {error}")

    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    main()