import json
import csv
import os


def json_to_csv(json_filepath, csv_filepath):
    try:
        with open(json_filepath, 'r', encoding='utf-8') as json_file, open(csv_filepath, 'w', newline='', encoding='utf-8') as csv_file:
            first_line = json_file.readline()
            if not first_line:  # Handle empty JSON file
                return

            first_json = json.loads(first_line)
            header = [key for key in first_json.keys() if key != 'link']  # Exclude 'link' from header

            writer = csv.DictWriter(csv_file, fieldnames=header, quoting=csv.QUOTE_ALL)
            writer.writeheader()  # Write the header row

            # Write the first line
            writer.writerow({key: value for key, value in first_json.items() if key != 'link'})

            # Process the rest of the lines
            for line in json_file:
                try:  # Handle potential JSON decoding errors
                    data = json.loads(line)
                    writer.writerow({key: value for key, value in data.items() if key != 'link'})  # Exclude 'link'
                except json.JSONDecodeError as e:
                    print(f"Warning: Skipping invalid JSON line: {line.strip()} - Error: {e}")

    except FileNotFoundError:
        print(f"Error: File not found: {json_filepath}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


json_filepath = 'Data/news.json'
csv_filepath = 'Data/news.csv'

json_to_csv(json_filepath, csv_filepath)