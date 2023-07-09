import csv 
import json
from datetime import datetime
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# For now, get only data past 2018 and only Dutch lifters
def process_csv(csv_file):
    occurrences = []
    with open(csv_file, newline='') as csvfile:
        data = csv.reader(csvfile)
        header = next(data)  # Retrieve the header row
        
        for row in data:
            date_string = row[header.index("Date")]
            date = datetime.strptime(date_string, "%Y-%m-%d").date()
            # if "Marciano Schildmeijer" in row[0]:
            if "Netherlands" in row and date > datetime(2018, 1, 1).date():
                occurrence = {}
                for i, value in enumerate(row):
                    header_value = header[i]
                    
                    if header_value.lower() in ["name", "weightclasskg", "squat1kg", "squat2kg", "squat3kg", "bench1kg", "bench2kg", "bench3kg", "deadlift1kg", "deadlift2kg", "deadlift3kg", "totalkg", "goodlift", "country"]:
                       occurrence[header_value.lower()] = value
                occurrences.append(occurrence)
    
    return occurrences


def get_best_sbd(data, key): 
    lifts = {}
    keys = [f"{key}1kg", f"{key}2kg", f"{key}3kg"]

    highest = None; 
    for row in data:
        for k in keys:
            if row[k] != "":
                weight = float(row[k])
                
                if highest is None or weight > highest:
                    highest = weight
            
    lifts = highest

    return lifts

def get_best_number_by_key(data, key):
    highest = 0
    
    for row in data:
        total = float(row[key])
        
        if total > highest:
            highest = total
        
    return highest;


def get_best_lifts(data) -> list:
    sbd_keys = ["squat", "bench", "deadlift"]
    result = {}
    
    result["name"] = data[0].get("name")
    result["total"] = get_best_number_by_key(data, "totalkg")
    result["weight-class"] = data[0].get("weightclasskg")
    result["goodlift"] = get_best_number_by_key(data, "goodlift")
    
    for key in sbd_keys:
        result[key] = get_best_sbd(data, key)
    return result;


def get_json_file():
    file_path = os.path.join(os.path.dirname(__file__), "./lifters.json")
    with open(file_path, "r") as json_file:
    # Write the data to the file
        data = json.load(json_file)
        
    return data

def create_json_from_csv(): 
    print("Creating JSON from CSV")
    try:
        data = process_csv("./api/openipf-2023-06-17-3b239855.csv")
    except Exception as e:
        logger.error("Failed to process CSV: %s", str(e))
        return {"error": str(e)}   
    
    with open("./api/lifters.json", "w") as json_file:
    # Write the data to the file
        json.dump(data, json_file)    