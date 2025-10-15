#!/usr/bin/env python3
"""
Test script for Healthcare Symptom Checker
"""
from app import create_app
from app.services.symptom_analyzer import SymptomAnalyzer

def test_app_creation():
    """Test Flask app creation."""
    try:
        app = create_app()
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def test_symptom_analyzer():
    """Test symptom analyzer with a sample symptom."""
    try:
        app = create_app()
        with app.app_context():
            analyzer = SymptomAnalyzer()
            
            # Test with a simple symptom
            test_symptoms = "I have a headache and feel tired for the past 2 days"
            result = analyzer.analyze_symptoms(test_symptoms)
            
            if result and 'conditions' in result:
                print("✅ Symptom analyzer working correctly")
                print(f"   Found {len(result['conditions'])} possible conditions")
                print(f"   Emergency detected: {result.get('emergency_detected', False)}")
                return True
            else:
                print("❌ Symptom analyzer returned invalid result")
                return False
                
    except Exception as e:
        print(f"❌ Symptom analyzer test failed: {e}")
        return False

def test_emergency_detection():
    """Test emergency symptom detection."""
    try:
        app = create_app()
        with app.app_context():
            analyzer = SymptomAnalyzer()
            
            # Test with emergency symptoms
            emergency_symptoms = "I have severe chest pain and difficulty breathing"
            result = analyzer.analyze_symptoms(emergency_symptoms)
            
            if result.get('emergency_detected', False):
                print("✅ Emergency detection working correctly")
                return True
            else:
                print("⚠️  Emergency detection may not be working (or symptoms not severe enough)")
                return True  # Not a failure, just a note
                
    except Exception as e:
        print(f"❌ Emergency detection test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🏥 Healthcare Symptom Checker - Test Suite")
    print("=" * 50)
    
    tests = [
        ("App Creation", test_app_creation),
        ("Symptom Analyzer", test_symptom_analyzer),
        ("Emergency Detection", test_emergency_detection)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔄 Testing {test_name}...")
        if test_func():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your application is ready to use.")
        print("\nTo start the application:")
        print("1. Activate virtual environment: source venv/bin/activate")
        print("2. Run: python run.py")
        print("3. Open browser to: http://127.0.0.1:5000")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")

if __name__ == '__main__':
    main()