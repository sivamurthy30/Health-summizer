import os
from openai import OpenAI
from flask import current_app

class SymptomAnalyzer:
    """Simple symptom analyzer using OpenAI."""
    
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client."""
        try:
            api_key = current_app.config.get('OPENAI_API_KEY')
            if api_key:
                self.client = OpenAI(api_key=api_key)
        except Exception as e:
            print(f"Failed to initialize OpenAI client: {str(e)}")
    
    def analyze_symptoms(self, symptoms: str, patient_data=None) -> dict:
        """Analyze symptoms using OpenAI."""
        if not self.client:
            return self._get_demo_response(symptoms)
        
        try:
            prompt = f"""
            You are a medical information assistant. Analyze these symptoms and provide educational information only.
            
            IMPORTANT DISCLAIMERS:
            - This is for educational purposes only
            - Not a substitute for professional medical advice
            - Always consult healthcare professionals for medical concerns
            
            Symptoms: {symptoms}
            
            Please provide:
            1. Possible conditions (educational information only)
            2. General recommendations
            3. When to seek medical care
            4. Emergency warning signs to watch for
            
            Format your response as a clear, helpful analysis while emphasizing the need for professional medical consultation.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful medical information assistant providing educational content only."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content
            
            return {
                'analysis': analysis_text,
                'disclaimer': 'This analysis is for educational purposes only. Always consult with healthcare professionals for medical advice.',
                'emergency_note': 'If experiencing severe symptoms, seek immediate medical attention or call emergency services.'
            }
            
        except Exception as e:
            return self._get_demo_response(symptoms, str(e))
    
    def _get_demo_response(self, symptoms: str, error: str = None) -> dict:
        """Provide a demo response when OpenAI is not available."""
        return {
            'analysis': f"""
            **Educational Analysis for: "{symptoms}"**
            
            Based on the symptoms you've described, here are some general educational points:
            
            **Possible Considerations:**
            - Symptoms may be related to common conditions
            - Multiple factors could be involved
            - Individual cases vary significantly
            
            **General Recommendations:**
            - Monitor symptoms and their progression
            - Stay hydrated and get adequate rest
            - Note any changes or worsening
            
            **When to Seek Medical Care:**
            - If symptoms persist or worsen
            - If you develop additional concerning symptoms
            - For proper diagnosis and treatment
            
            **Emergency Warning Signs:**
            - Severe pain or distress
            - Difficulty breathing
            - High fever
            - Any symptoms that concern you
            
            {f"Note: OpenAI service unavailable ({error}). This is a demo response." if error else ""}
            """,
            'disclaimer': 'This analysis is for educational purposes only. Always consult with healthcare professionals for medical advice.',
            'emergency_note': 'If experiencing severe symptoms, seek immediate medical attention or call emergency services.'
        }