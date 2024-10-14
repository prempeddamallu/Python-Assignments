import json
import pandas as pd
import mysql.connector
from mysql.connector import Error
import re

# Load JSON data
def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None

json_data = load_json_data('sample_data_for_assignment.json')

# MySQL connection setup
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',  
            database='data_manipulation'    
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Create table and load data
def load_data_to_mysql(connection):
    cursor = connection.cursor()
    # Create table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS json_to_sql_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        {columns}
    )
    """
    columns = ", ".join([f"{col} VARCHAR(255)" for col in json_data['cols']])
    create_table_query = create_table_query.format(columns=columns)
    cursor.execute(create_table_query)
    
    # Insert data
    insert_query = f"INSERT INTO json_to_sql_table ({', '.join(json_data['cols'])}) VALUES ({', '.join(['%s'] * len(json_data['cols']))})"
    cursor.executemany(insert_query, json_data['data'])
    connection.commit()
    cursor.close()
    print("Data loaded to MySQL")

# Unload data from MySQL to pandas dataframe
def unload_data_to_dataframe(connection):
    query = "SELECT * FROM json_to_sql_table"
    df = pd.read_sql(query, connection)
    return df

# Function to display the DataFrame
def display_dataframe():
    connection = create_connection()
    if connection:
        df = unload_data_to_dataframe(connection)
        connection.close()
        return df

# Update email addresses
def update_emails(df):
    df['email'] = df['email'].apply(lambda x: re.sub(r'@.*$', '@gmail.com', x))
    return df

# Convert postalZip to integers
def convert_postal_zip(df):
    def clean_postal_zip(value):
        if isinstance(value, str):
            return int(''.join(filter(str.isdigit, value)))
        elif isinstance(value, int):
            return value
        return 0
    
    df['postalZip'] = df['postalZip'].apply(clean_postal_zip)
    return df

# Process phone numbers to ASCII characters
def process_phone_numbers(df):
    def phone_to_ascii(phone):
        phone_str = re.sub(r'\D', '', phone)  # Remove non-digit characters
        ascii_chars = []
        for i in range(0, len(phone_str) - 1, 2):
            num = int(phone_str[i:i+2])
            if 65 <= num <= 99:
                ascii_chars.append(chr(num))
            else:
                ascii_chars.append('O')
        return ''.join(ascii_chars)
    
    df['phone'] = df['phone'].apply(phone_to_ascii)
    return df

# Main program
def main():
    connection = create_connection()
    if connection:
        load_data_to_mysql(connection)

        
        df = display_dataframe()
        print("Displaying all data : ")
        print(df)

        df = update_emails(df)
        print("Updating emails : ")
        print(df)

        df = convert_postal_zip(df)
        print("Converting postal zip : ")
        print(df)

        df = process_phone_numbers(df)
        print("Processing phone numbers : ")
        print(df)
        
        connection.close()

if __name__ == "__main__":
    main()

