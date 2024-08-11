import json
import os

FILE_PATH = "budget_data.json"

def load_data():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    return []

def save_data(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

def create_item(description, amount):
    data = load_data()
    new_id = len(data) + 1
    item = {
        "id": new_id,
        "description": description,
        "amount": amount
    }
    data.append(item)
    save_data(data)
    return item

def read_items():
    return load_data()

def update_item(item_id, description=None, amount=None):
    data = load_data()
    for item in data:
        if item["id"] == item_id:
            if description:
                item["description"] = description
            if amount:
                item["amount"] = amount
            save_data(data)
            return item
    return None

def delete_item(item_id):
    data = load_data()
    data = [item for item in data if item["id"] != item_id]
    save_data(data)
    return data


