# Quake Game Expert

🚀 **Quake Game Expert** is a set of Python scripts that parse Quake game logs and extract match data, including player statistics, kill counts, and kill methods. Additionally, it includes an integration with OpenAI's API, enabling users to ask questions about the parsed data using natural language.

## 📁 Project Structure

This repository contains the following files and directories:

```
unit_tests/                   # Directory for unit tests
    ├── __init__.py           # Empty file to help with "unittest discovery"
    ├── test_death_report.py  # Unit test for death_report.py
    └── test_parser.py        # Unit test for parser.py
death_report.py               # Parses means of death from game logs
llm_query.py                  # Queries parsed data using OpenAI's API
parser.py                     # Parses player stats and match events
qgames.log                    # A sample Quake game log file
requirements.txt              # Non-built-in package dependencies
```

## ✨ Features

- Extract player stats: total kills, individual player kills, and match participation.
- Extract detailed information about the means of death.
- Integrates with OpenAI's API for interactive, question-based match data analysis.

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/plgbernardo/quake-log-parser
   cd quake-log-parser
   ```

2. **Install dependencies**:

   The required Python packages are listed in the `requirements.txt` file. To install them, run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API key**:

   You will need a valid API key from OpenAI. Set it as an environment variable:

   ```bash
   export AI_API_KEY="your_openai_api_key_here"
   ```

## 🚀 How to Run the Program

### 1. **Run the Log Parser**

   To extract player statistics and kills, execute:

   ```bash
   python parser.py
   ```

   To extract the means of death (MOD) information, run:

   ```bash
   python death_report.py
   ```

   These scripts will generate two JSON files:
   
   - `match_info.json`: Contains player stats and total kills.
   - `mod_info.json`: Contains means of death data.

### 2. **Run the Querying Script (OpenAI Integration)**

   After generating the JSON files, you can query the data by executing:

   ```bash
   python llm_query.py
   ```

   The script will prompt you to ask a question. For example:

   ```
   Ask something for the Quake expert: "Which player had the most kills?"
   ```

   The OpenAI API will analyze the parsed data and provide an answer.

## 🧪 How to Test

### Unit Tests

This repository includes unit tests for the `parser.py` and `death_report.py` modules. The tests use the **unittest** framework and **unittest.mock** to simulate file inputs. 

### Running the Tests

To run the unit tests, navigate to the root of the project and execute the following command:

```bash
python -m unittest discover unit_tests/
```

This command will automatically discover and run all unit tests located in the `unit_tests` directory.

### Test Files

- **`unit_tests/test_parser.py`**:
  - **`test_parse_log_basic`**: Tests the log parsing functionality using a mock game log with player stats and kills.
  - **`test_process_kill_event`**: Simulates a kill event and checks if the event is processed correctly in the current match.
  - **`test_process_match`**: Verifies that match data is correctly stored after the game ends.
  - **`test_add_player`**: Tests the addition of a player to the match during gameplay.

- **`unit_tests/test_death_report.py`**:
  - **`test_parse_log_with_mod`**: Tests parsing logs with different means of death (MOD) and ensures proper data extraction.
  - **`test_process_kill_event`**: Verifies that kill events are correctly processed and categorized by the MOD.
  - **`test_process_match`**: Ensures that the means of death are correctly stored and categorized after the match ends.

## 📊 Functions Overview

### `parser.py`
- **`parse_log(file_content)`**: Parses the Quake log, extracting match data, total kills, and player stats.
- **`process_kill_event(current_match, line)`**: Tracks kills per player and identifies kills made by the world.
- **`process_match(current_match, matches_data)`**: Finalizes and stores match data (kills, players).
- **`add_player(current_match, line)`**: Adds players who join the game and initializes their kill counts.

### `death_report.py`
- **`parse_log(file_content)`**: Extracts the means of death (MOD) used in each match.
- **`process_kill_event(current_match, line)`**: Tracks each kill's MOD and updates the match data.
- **`process_match(current_match, matches_data)`**: Finalizes and stores the MOD data for each match.

### `llm_query.py`
- **`load_json_data(file_path)`**: Loads the JSON data produced by the log parsers.
- **`ask_llm(question, parse_path, mod_path)`**: Sends the parsed data and user query to OpenAI's API for analysis and response.

## 📊 Example Questions for Quake Expert

- "How many kills did player X achieve?"
- "What was the most common cause of death in game 2?"
- "Which player had the most kills by MOD_SHOTGUN?"

--- 
