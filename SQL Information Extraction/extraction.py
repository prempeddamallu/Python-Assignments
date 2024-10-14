import re
import json
import argparse

def extract_information(sql_content):
    data = {}

    # Extracting the procedure name
    proc_name_pattern = r'CREATE\s+OR\s+REPLACE\s+PROCEDURE\s+(\w+)'
    proc_name_match = re.search(proc_name_pattern, sql_content, re.IGNORECASE)
    if proc_name_match:
        data['procedure_name'] = proc_name_match.group(1)

    # Extracting input parameters
    params_pattern = r'(\w+\s+\w+(\(.*?\))?\s+DEFAULT\s+\w+|\w+\s+\w+(\(.*?\))?)'
    params = re.findall(params_pattern, sql_content)
    data['parameters'] = [param[0] for param in params]

    # Extracting SQL queries
    sql_statements = []
    sql_patterns = [
        r'CREATE\s+TABLE.*?\);',  # Create table statements
        r'INSERT\s+INTO.*?;',     # Insert statements
        r'UPDATE\s+.*?;',         # Update statements
        r'DELETE\s+FROM.*?;',     # Delete statements
        r'MERGE\s+INTO.*?;'        # Merge statements
    ]

    for pattern in sql_patterns:
        matches = re.findall(pattern, sql_content, re.DOTALL | re.IGNORECASE)
        sql_statements.extend(matches)

    data['sql_statements'] = sql_statements

    return data

def main():
    parser = argparse.ArgumentParser(description='Extract information from a SQL file.')
    parser.add_argument('sql_file', help='The SQL file to process')
    args = parser.parse_args()

    # Read the content of the SQL file
    with open(args.sql_file, 'r') as file:
        sql_content = file.read()

    # Extract information
    extracted_data = extract_information(sql_content)

    # Output the extracted information as a JSON file
    json_output = args.sql_file.replace('.sql', '.json')
    with open(json_output, 'w') as json_file:
        json.dump(extracted_data, json_file, indent=4)

    print(f"Information extracted and saved to {json_output}")

if __name__ == '__main__':
    main()



