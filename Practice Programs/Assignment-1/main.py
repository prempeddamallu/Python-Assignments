import mysql.connector as connector

def connect_to_database():
    try:
        connection = connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='employees'
        )
        print("Connection to the database was successful.")
        return connection
    except connector.Error as err:
        print("Error:", err)
        return None


def fetch_large_data(cursor, query, chunk_size=1000):
    try:
        cursor.execute(query)
        while True:
            rows = cursor.fetchmany(chunk_size)
            if not rows:
                break
            yield rows
    except connector.Error as err:
        print("Error fetching data:",err)



def process_data(rows):
    try:
        for row in rows:
            print(row)
    except Exception as e:
       print("Error processing data:",e)


def main():
    connection = connect_to_database()
    if connection is None:
        print("Failed to connect to the database.")
        return
    
    cursor = connection.cursor()
    
    query = "select * from employees limit 10"
    # query = "select first_name from employees limit 10"
    
    for chunk in fetch_large_data(cursor, query):
        process_data(chunk)
    
    cursor.close()
    connection.close()
    print("Database connection closed.")

if __name__ == "__main__":
    main()


