from openai import OpenAI
import os
from dotenv import load_dotenv
import json

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# User input
user_message = input("Enter a freight request (e.g., 'Ship 400 lbs from NY to LA next week'): ")

# Updated prompt with sample JSON
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    # prompt engineering here: 
    messages=[
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that extracts structured data from freight booking messages. "
                "Your job is to respond ONLY with a JSON object that contains the following keys: "
                "`pickup`, `dropoff`, `weight`, and `date`. Do not include any explanations or formatting. "
                "Example output:\n"
                '{\n'
                '  "pickup": "New York",\n'
                '  "dropoff": "Los Angeles",\n'
                '  "weight": "400 lbs",\n'
                '  "date": "next Monday"\n'
                '}'
            )
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
)

# Get model's response
response_text = completion.choices[0].message.content.strip()

# Parse JSON or show error
try:
    structured_data = json.loads(response_text)
    print("\n🧠 Assistant extracted (JSON):")
    print(json.dumps(structured_data, indent=2))
except json.JSONDecodeError:
    print("\n⚠️ Response was not valid JSON:")
    print(response_text)

# Get and print response
response_text = completion.choices[0].message.content.strip()

# Try parsing it as JSON (optional, for error safety)
try:
    structured_data = json.loads(response_text)
    print("\n🧠 Assistant extracted (JSON):")
    print(json.dumps(structured_data, indent=2))
except json.JSONDecodeError:
    print("\n⚠️ Response was not valid JSON:")
    print(response_text)