import json
import re

def parse_log(file_content):
    matches_data = {}
    current_match = None

    # Iterate each line for specific keywords.
    for line in file_content.splitlines():
        # Check if a new game has started and process the current one (if any).
        if "InitGame:" in line:
            if current_match:
                process_match(current_match, matches_data)
            # Initialize a new game session.
            current_match = {"kills_by_means": {}}
        
        # Check if the current game has ended.
        elif "ShutdownGame:" in line:
            if current_match:
                process_match(current_match, matches_data)
                current_match = None

        # Check if a kill event happened and update the means of death.
        elif "Kill:" in line:
            process_kill_event(current_match, line)
    
    # End the last match case hasn't been finalized after the loop.
    if current_match:
        process_match(current_match, matches_data)

    return matches_data

def process_kill_event(current_match, line):
    # Regular expression to extract the "MOD_*" from kill feed event.
    match = re.search(r'Kill: \d+ \d+ \d+: (.+) killed (.+) by (MOD_\w+)', line)
    if match:
        # Catch used "MOD_*"
        death_means = match.group(3).strip()

        # Update the current match's "kills_by_means" with the type of death (MOD).
        current_match["kills_by_means"][death_means] = current_match["kills_by_means"].get(death_means, 0) + 1

def process_match(current_match, matches_data):
    # Assign a ID and store the kills_by_means for that game.
    match_id = f"game_{len(matches_data) + 1}"
    matches_data[match_id] = {
        "kills_by_means": current_match["kills_by_means"]
    }

def read_json(file_path):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read the file's content into a string
        file_content = file.read()
    
    return file_content

# Set the log file path.
file_path = "qgames.log"

# Get the file content.
file_content = read_json(file_path)

# Parse the log file and store the results.
matches_data = parse_log(file_content)

# Save parsed data to a JSON file.
with open("mod_info.json", "w") as f:
    json.dump(matches_data, f, indent=2)

# Print the parsed data in JSON format.
print(json.dumps(matches_data, indent=2))
