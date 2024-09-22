import json
import re

def parse_log(file_path):
    matches_data = {}
    current_match = None

    # Open and read the log file.
    with open(file_path, 'r') as file:
        # Search each line for specific keywords.
        for line in file:
            # Check if a new game has started and finalize the current one (if any).
            if "InitGame:" in line:
                if current_match:
                    process_match(current_match, matches_data)
                # Initialize a new game session.
                current_match = {"total_kills": 0, "players": set(), "kills_data": {}}

            # Check if the current game has ended.
            elif "ShutdownGame:" in line:
                if current_match:
                    process_match(current_match, matches_data)
                    current_match = None

            # Check if a kill event happened.
            elif "Kill:" in line:
                current_match["total_kills"] += 1
                process_kill_event(current_match, line)

            # Check if any player has joined the session.
            elif "ClientUserinfoChanged:" in line:
                add_player(current_match, line)
    
    # End the last match case hasn't been finalized after the loop.
    if current_match:
        process_match(current_match, matches_data)

    return matches_data

def process_kill_event(current_match, line):
    # Regex for filtering the names in the kill feed line.
    match = re.search(r'Kill: \d+ \d+ \d+: (.+?) killed (.+?) by (.+)', line)
    if match:
        killer = match.group(1).strip()
        victim = match.group(2).strip()

        # Check if the killer was a player to increment his score.
        if killer != "<world>":
            current_match["kills_data"][killer] = current_match["kills_data"].get(killer, 0) + 1

        # Add the victim to "players" list (for total kills) even if "<world>" kills them.
        current_match["players"].add(victim)

def process_match(current_match, matches_data):
    # Assign a new game ID and store the results of the current match.
    match_id = f"game_{len(matches_data) + 1}"
    matches_data[match_id] = {
        "total_kills": current_match["total_kills"],
        "players": list(current_match["players"]),
        "kills": {player: current_match["kills_data"].get(player, 0) for player in current_match["players"]}
    }

def add_player(current_match, line):
    # Regex for filtering the player names after joined the game.
    match = re.search(r'ClientUserinfoChanged: (\d+) n\\(.+?)\\', line)
    if match:
        player_name = match.group(2).strip()
        current_match["players"].add(player_name)
        # Initialize player's kill count if haven't been added yet.
        if player_name not in current_match["kills_data"]:
            current_match["kills_data"][player_name] = 0

# Set the log file path.
file_path = "qgames.log"
# Parse the log file and store the results.
matches_data = parse_log(file_path)

# Save parsed data to a JSON file
with open("match_info.json", "w") as f:
    json.dump(matches_data, f, indent=2)

print("Match data parsed and saved to matches_data.json")

# Print parsed data in JSON format.
print(json.dumps(matches_data, indent=2))
