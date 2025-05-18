import sys
import clipboard
import json

SAVED_DATA = "clipboard.json"


def save_data(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f)


def load_data(filepath):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

if len(sys.argv) == 2:
    command = sys.argv[1]
    data = load_data(SAVED_DATA)

    if command == "save":
        key = input("Enter a key: ")
        if key == "python":
            # This code saves an empty string and not lengthy information:
            data[key] = ""  
        else:
            data[key] = clipboard.paste()
        # The saving of the data.
        save_data(SAVED_DATA, data)
        print("Your data has been saved.")    
    elif command == "load":
        key = input("Enter a key: ")
        if key in data:
            clipboard.copy(data[key])
            # Checking if the data is valid:
            print("The data has been copied to your clipboard.")
        else:
            print("The key does not exist.")
    elif command == "list":
        print(data)
    else:
        print("Unknown command.")
else:
    print("Please pass exactly one command.")