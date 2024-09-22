from openai import OpenAI
import json
import os

# Set up OpenAI API key.
client = OpenAI(api_key=os.environ.get("AI_API_KEY"))

# Store local of both parser and death_report .JSON paths, also stores the input given by user.
parser_path = "match_info.json"
mod_path = "mod_info.json"
question = input("Ask something for the Quake expert: ").lower()

# Load .JSON file from given path.
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Asks GPT to analyze the JSON data and respond to the question.
def ask_llm(question, parse_path, mod_path):

    # Prepare the chat-style input with system, user, and assistant roles.
    messages = [
        {"role": "system", "content": "You are an assistant who is an expert in analyzing Quake game match data in JSON format."},
        {"role": "user", "content": f"The following is a JSON structure representing Quake game matches and player stats:\n{json.dumps(parse_path, indent=2)}\n\nBased on this data, please answer the following question: {question}"},
        {"role": "user", "content": f"The following is a JSON structure representing Quake game types os death registred in each game:\n{json.dumps(mod_path, indent=2)}\n\nBased on this data, please answer the following question: {question}"}
    ]

    # Make request to OpenAI GPT chosen model.
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    max_tokens=100,
    temperature=0.7)

    # Get the response text.
    answer = response.choices[0].message.content.strip()
    return answer

# Load both files for sending as argument to the called ask_llm() below.
parser_data = load_json_data(parser_path)
mod_data = load_json_data(mod_path)

print(ask_llm(question, parser_data, mod_data))