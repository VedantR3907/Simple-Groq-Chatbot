import os
import json

DATABASE_FILE = os.path.join(os.getcwd(), 'database.json')

def save_to_json(question, answer):

    # Initialize the database if it does not exist
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'w') as file:
            json.dump([], file)

    try:
        # Read the existing data
        with open(DATABASE_FILE, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        data = []

    # Append the new question and answer
    data.append({"user": question, "assistant": answer})
    # Write the updated data back to the file
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)

    return "success"
    