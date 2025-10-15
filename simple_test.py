#!/usr/bin/env python3
"""Simple OpenAI API test"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from openai import OpenAI
    
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"API Key: {api_key[:20]}...{api_key[-10:]}")
    
    # Create client
    client = OpenAI(api_key=api_key)
    print("✅ OpenAI client created")
    
    # Test API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Say 'Hello, API is working!'"}
        ],
        max_tokens=10
    )
    
    result = response.choices[0].message.content
    print(f"✅ API Response: {result}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Error type: {type(e)}")
    import traceback
    traceback.print_exc()