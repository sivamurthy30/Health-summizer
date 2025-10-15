#!/usr/bin/env python3
"""Final test for Healthcare Symptom Checker with real API"""

from app import create_app
from app.services.symptom_analyzer import SymptomAnalyzer

def test_real_api():
    """Test the symptom analyzer with real API."""
    print("🏥 Testing Healthcare Symptom Checker with Real API")
    print("=" * 50)
    
    try:
        # Create Flask app context
        app = create_app()
        
        with app.app_context():
            # Test symptom analyzer
            analyzer = SymptomAnalyzer()
            
            # Test with simple symptoms
            test_symptoms = "I have a headache and feel tired for the past 2 days"
            print(f"🔄 Testing with symptoms: '{test_symptoms}'")
            
            result = analyzer.analyze_symptoms(test_symptoms)
            
            if result and 'conditions' in result:
                print("✅ API is working! Got real AI analysis:")
                
                for i, condition in enumerate(result['conditions'], 1):
                    print(f"  {i}. {condition['name']} ({condition['probability']} probability)")
                    print(f"     {condition['description']}")
                
                if result.get('emergency_detected'):
                    print("🚨 Emergency detected!")
                else:
                    print("✅ No emergency detected")
                
                print(f"\n📋 General recommendations: {len(result.get('general_recommendations', []))}")
                print(f"⚠️  Disclaimers: {len(result.get('disclaimers', []))}")
                
                return True
            else:
                print("❌ Got invalid response from API")
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        
        error_msg = str(e).lower()
        if "401" in error_msg or "authentication" in error_msg:
            print("💡 API key authentication failed")
            print("   - Check if your OpenAI API key is correct")
            print("   - Verify your OpenAI account has billing set up")
        elif "quota" in error_msg or "billing" in error_msg:
            print("💡 Billing/quota issue")
            print("   - Add credits to your OpenAI account")
        else:
            print("💡 Other error - check the details above")
        
        return False

if __name__ == '__main__':
    if test_real_api():
        print("\n🎉 SUCCESS! Your Healthcare Symptom Checker is working with real AI!")
        print("\nYou can now:")
        print("1. Run: python run.py")
        print("2. Open: http://127.0.0.1:5000")
        print("3. Test with real symptoms")
    else:
        print("\n⚠️  API test failed. Check the error messages above.")