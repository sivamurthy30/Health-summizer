#!/usr/bin/env python3
"""Simple API test"""
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

print(f"API Key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 10 else api_key}")
print(f"Key length: {len(api_key)}")
print(f"Starts with sk-: {api_key.startswith('sk-')}")

try:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    print("✅ OpenAI client created")
    
    # Simple test
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=5
    )
    print("✅ API call successful!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    if "authentication" in str(e).lower():
        print("This looks like an invalid API key")
    elif "billing" in str(e).lower():
        print("This looks like a billing issue - check your OpenAI account")