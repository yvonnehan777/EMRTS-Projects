# 4-gallon project
from collections import deque

def water_jug_bfs():
    visited = set()
    queue = deque()

    # Each state is represented as (5-gallon, 3-gallon, steps)
    queue.append((0, 0, []))
    solutions = []

    while queue:
        jug5, jug3, steps = queue.popleft()

        if jug5 == 4:
            solutions.append(steps)
            print("Solution found in", len(steps), "steps:")
            for i, step in enumerate(steps, 1):
                print(f"{i}. {step}")
            print("-" * 30)

        if (jug5, jug3) in visited:
            continue
        visited.add((jug5, jug3))

        possible_moves = [
            (5, jug3, "Fill 5-gallon bucket"),
            (jug5, 3, "Fill 3-gallon bucket"),
            (0, jug3, "Empty 5-gallon bucket"),
            (jug5, 0, "Empty 3-gallon bucket"),
            (jug5 - min(jug5, 3 - jug3), jug3 + min(jug5, 3 - jug3), "Pour 5-gallon into 3-gallon bucket"),
            (jug5 + min(jug3, 5 - jug5), jug3 - min(jug3, 5 - jug5), "Pour 3-gallon into 5-gallon bucket"),
        ]

        for new5, new3, action in possible_moves:
            if (new5, new3) not in visited:
                queue.append((new5, new3, steps + [action]))

    print(f"Total solutions found: {len(solutions)}")

water_jug_bfs()

# State Captial Project
import json
import time
from geopy.geocoders import Nominatim

# Step 1: Load the original JSON file (update this path as needed)
file_path = "/Users/yvonnehan/Downloads/us_state_capitals.json"

with open(file_path, "r") as f:
    data = json.load(f)

# Step 2: Initialize the geocoder
geolocator = Nominatim(user_agent="state_capitals_locator")

# Step 3: Add coordinates to each capital
for capital in data["state_capitals"]:
    full_address = f'{capital["street_address"]}, {capital["city"]}, {capital["state_code"]} {capital["zip"]}'
    print(f"Geocoding: {full_address}")

    try:
        location = geolocator.geocode(full_address)
        if location:
            capital["latitude"] = location.latitude
            capital["longitude"] = location.longitude
            print(f"→ Found: {location.latitude}, {location.longitude}")
        else:
            capital["latitude"] = None
            capital["longitude"] = None
            print("→ Coordinates not found.")
    except Exception as e:
        capital["latitude"] = None
        capital["longitude"] = None
        print(f"→ Error: {e}")

    time.sleep(1)

# Step 4: Save the updated data to a new JSON file
output_path = "/Users/yvonnehan/Downloads/us_state_capitals_with_coords.json"

with open(output_path, "w") as f_out:
    json.dump({"state_capitals": data["state_capitals"]}, f_out, indent=2)

print(f"Successfully saved updated file to: {output_path}")





