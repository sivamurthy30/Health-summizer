#!/usr/bin/env python3
"""Quick test for Healthcare Symptom Checker"""

print("🏥 Healthcare Symptom Checker - Quick Test")
print("=" * 40)

try:
    from app import create_app
    print("✅ Flask app imports successfully")
    
    app = create_app()
    print("✅ Flask app created successfully")
    
    # Test configuration
    with app.app_context():
        from flask import current_app
        api_key = current_app.config.get('OPENAI_API_KEY')
        if api_key and api_key.startswith('sk-'):
            print("✅ OpenAI API key configured")
        else:
            print("❌ OpenAI API key not properly configured")
    
    print("\n🎉 Basic setup is working!")
    print("\nTo run the application:")
    print("1. source venv/bin/activate")
    print("2. python run.py")
    print("3. Open http://127.0.0.1:5000 in your browser")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure you're in the healthcare-symptom-checker directory")
    print("2. Activate virtual environment: source venv/bin/activate")
    print("3. Install dependencies: pip install -r requirements.txt")