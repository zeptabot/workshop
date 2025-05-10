import os
import json

input_folder = "/data/inputs"
output_folder = "/data/outputs"

def compute_avg_price(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        properties = json.load(f)

    print(f"Properties: {properties}")

    avg_prices_by_rooms = {}

    for property in properties:
        info = property.get('info', {})
        price = info.get('price')
        rooms_no = info.get('roomsNo')

        if rooms_no not in avg_prices_by_rooms:
            avg_prices_by_rooms[rooms_no] = {
                'totalPrice': 0,
                'count': 0,
            }

        avg_prices_by_rooms[rooms_no]['totalPrice'] += price
        avg_prices_by_rooms[rooms_no]['count'] += 1

    for rooms_no in avg_prices_by_rooms:
        total = avg_prices_by_rooms[rooms_no]['totalPrice']
        count = avg_prices_by_rooms[rooms_no]['count']
        avg = round(total / count, 2)
        avg_prices_by_rooms[rooms_no]['averagePrice'] = avg

    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, "results.json")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(avg_prices_by_rooms, f, indent=2)

    print(f"Avg prices: {avg_prices_by_rooms}")

def process_folder(path):
    try:
        files = os.listdir(path)
        print(f"files: {files}")
        for file in files:
            full_path = os.path.join(path, file)
            if os.path.isdir(full_path):
                process_folder(full_path)
            else:
                print(f"path to file: {full_path}")
                compute_avg_price(full_path)
    except Exception as e:
        print(f"Error processing folder {path}: {e}")

process_folder(input_folder)