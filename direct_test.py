#!/usr/bin/env python3
"""Direct test without Flask app context"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Print what we're loading
print("Current working directory:", os.getcwd())
print("Contents of .env file:")
with open('.env', 'r') as f:
    for line_num, line in enumerate(f, 1):
        if 'OPENAI_API_KEY' in line:
            print(f"Line {line_num}: {line.strip()}")

# Get API key
api_key = os.getenv('OPENAI_API_KEY')
print(f"\nLoaded API key: {api_key[:20]}...{api_key[-10:] if api_key else 'None'}")

if api_key:
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=5
        )
        print("✅ API call successful!")
        print(f"Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ API call failed: {e}")
else:
    print("❌ No API key found")