#!/usr/bin/env python3
"""
Debug script for OpenAI API connection
"""
import os
from dotenv import load_dotenv

def check_environment():
    """Check environment configuration."""
    print("🔍 Checking Environment Configuration")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False
    
    print(f"✅ OPENAI_API_KEY found: {api_key[:10]}...{api_key[-4:]}")
    
    # Check API key format
    if not api_key.startswith('sk-'):
        print("⚠️  API key doesn't start with 'sk-' - this might be invalid")
        return False
    
    if len(api_key) < 40:
        print("⚠️  API key seems too short - real OpenAI keys are longer")
        return False
    
    print("✅ API key format looks correct")
    return True

def test_openai_connection():
    """Test OpenAI API connection."""
    print("\n🔍 Testing OpenAI API Connection")
    print("=" * 40)
    
    try:
        from openai import OpenAI
        
        api_key = os.getenv('OPENAI_API_KEY')
        client = OpenAI(api_key=api_key)
        
        print("✅ OpenAI client created successfully")
        
        # Test with a simple request
        print("🔄 Testing API call...")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello, API is working!'"}
            ],
            max_tokens=10,
            timeout=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ API call successful: {result}")
        return True
        
    except Exception as e:
        error_msg = str(e).lower()
        print(f"❌ API call failed: {e}")
        
        if "api key" in error_msg or "authentication" in error_msg:
            print("💡 This looks like an API key authentication issue")
            print("   - Make sure you have a valid OpenAI API key")
            print("   - Check if the key has sufficient credits")
            print("   - Verify the key is active on OpenAI platform")
        elif "quota" in error_msg or "billing" in error_msg:
            print("💡 This looks like a billing/quota issue")
            print("   - Check your OpenAI account billing status")
            print("   - Verify you have available credits")
        elif "rate limit" in error_msg:
            print("💡 Rate limit exceeded - try again in a moment")
        else:
            print("💡 Unknown error - check your internet connection")
        
        return False

def check_flask_app():
    """Test Flask app configuration."""
    print("\n🔍 Testing Flask App Configuration")
    print("=" * 40)
    
    try:
        from app import create_app
        app = create_app()
        
        with app.app_context():
            from flask import current_app
            api_key = current_app.config.get('OPENAI_API_KEY')
            
            if api_key:
                print(f"✅ Flask app has API key: {api_key[:10]}...{api_key[-4:]}")
                return True
            else:
                print("❌ Flask app doesn't have API key configured")
                return False
                
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def main():
    """Run all diagnostic tests."""
    print("🏥 Healthcare Symptom Checker - API Diagnostics")
    print("=" * 50)
    
    tests = [
        check_environment,
        test_openai_connection,
        check_flask_app
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! API should be working.")
    else:
        print("⚠️  Some issues found. Please fix them and try again.")
        print("\n💡 Common solutions:")
        print("1. Get a real OpenAI API key from https://platform.openai.com/")
        print("2. Make sure your OpenAI account has billing set up")
        print("3. Check that your API key has sufficient credits")
        print("4. Verify the API key is correctly set in the .env file")

if __name__ == '__main__':
    main()