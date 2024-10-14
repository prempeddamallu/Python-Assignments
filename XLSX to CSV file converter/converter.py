import pandas as pd
import sys
import os
from pathlib import Path


def convert_xlsx_to_csv(file_path):
    # Ensure the input file exists
    if not os.path.isfile(file_path):
        print(f"File '{file_path}' does not exist.")
        return

    try:
        # Load the XLSX file
        xlsx = pd.ExcelFile(file_path)

        # Create a directory for CSV files
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_dir = Path.cwd() / base_name
        output_dir.mkdir(exist_ok=True)
        print(f"Output directory created at: {output_dir.resolve()}")

        # Iterate through each sheet and save as CSV
        for sheet_name in xlsx.sheet_names:
            df = pd.read_excel(xlsx, sheet_name=sheet_name)
            csv_file_name = f"{sheet_name}.csv"
            csv_file_path = output_dir / csv_file_name
            df.to_csv(csv_file_path, index=False)
            print(f"Converted sheet '{sheet_name}' to CSV: {csv_file_path.resolve()}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python converter.py <path_to_xlsx_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    convert_xlsx_to_csv(file_path)