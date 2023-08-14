import sys
import sqlite3

def format_verses(database_name, output_filename):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        # Query to format verses and fetch data
        query = """
        SELECT b.long_name || ' ' || v.chapter || ':' || v.verse || ' ' || v.text AS formatted_verse
        FROM verses v
        JOIN books b ON v.book_number = b.book_number;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Write formatted verses to the output file
        with open(output_filename, 'w') as output_file:
            for row in rows:
                output_file.write(row[0] + '\n')

        print("Formatted verses have been written to", output_filename)

    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py database_name.db output_filename.txt")
    else:
        database_name = sys.argv[1]
        output_filename = sys.argv[2]
        format_verses(database_name, output_filename)
