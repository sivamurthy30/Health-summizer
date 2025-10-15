import json
import logging
import hashlib
import re
from datetime import datetime
from typing import Dict, Any, List, Optional
from openai import OpenAI
from flask import current_app

class SymptomAnalyzer:
    """Advanced symptom analyzer service with enhanced medical analysis."""
    
    def __init__(self):
        self.client = None
        self._initialize_client()
        self.medical_specialties = self._load_medical_specialties()
        self.emergency_keywords = self._load_emergency_keywords()
        self.drug_interactions = self._load_common_drug_interactions()
    
    def _initialize_client(self):
        """Initialize OpenAI client."""
        try:
            api_key = current_app.config.get('OPENAI_API_KEY')
            if api_key and len(api_key) > 40:
                self.client = OpenAI(api_key=api_key)
                logging.info("OpenAI client initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize OpenAI client: {str(e)}")
    
    def analyze_symptoms(self, symptoms: str, patient_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Enhanced symptom analysis with patient context."""
        if not self.client:
            return self._get_demo_response(symptoms, patient_data)
        
        try:
            # Build enhanced prompt with patient context
            system_prompt = self._get_enhanced_system_prompt()
            user_prompt = self._build_contextual_prompt(symptoms, patient_data)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.2
            )
            
            result = self._parse_response(response.choices[0].message.content)
            
            # Enhanced analysis features
            result['emergency_detected'] = self._detect_emergency_advanced(symptoms, patient_data)
            result['specialist_referral'] = self._suggest_specialist(symptoms, result.get('conditions', []))
            result['risk_factors'] = self._assess_risk_factors(symptoms, patient_data)
            result['follow_up_timeline'] = self._suggest_follow_up_timeline(result.get('conditions', []))
            result['red_flags'] = self._identify_red_flags(symptoms, patient_data)
            
            # Log analysis for quality improvement
            self._log_analysis(symptoms, result, patient_data)
            
            return result
            
        except Exception as e:
            logging.error(f"API error: {str(e)}")
            return self._get_demo_response(symptoms, patient_data)
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for analysis."""
        return """You are a medical information assistant. Analyze symptoms and provide educational information only.

Respond with JSON in this format:
{
    "conditions": [
        {
            "name": "Condition Name",
            "description": "Brief description",
            "probability": "High|Medium|Low",
            "recommendations": ["Action 1", "Action 2"]
        }
    ],
    "general_recommendations": ["General advice"],
    "disclaimers": ["Educational disclaimer"]
}

Always include disclaimers about consulting healthcare professionals."""
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse API response."""
        try:
            # Try to extract JSON from response
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response_text[start:end]
                return json.loads(json_str)
        except:
            pass
        
        # Fallback if parsing fails
        return {
            "conditions": [{
                "name": "General Health Concern",
                "description": "Your symptoms require professional medical evaluation.",
                "probability": "Medium",
                "recommendations": ["Consult with a healthcare professional"]
            }],
            "general_recommendations": ["Seek medical advice for proper evaluation"],
            "disclaimers": ["This is for educational purposes only"]
        }
    
    def _detect_emergency(self, symptoms: str) -> bool:
        """Simple emergency symptom detection."""
        emergency_keywords = [
            'chest pain', 'difficulty breathing', 'shortness of breath',
            'severe bleeding', 'unconscious', 'heart attack', 'stroke',
            'severe allergic reaction', 'anaphylaxis', 'seizure'
        ]
        
        symptoms_lower = symptoms.lower()
        return any(keyword in symptoms_lower for keyword in emergency_keywords)
    
    def _get_demo_response(self, symptoms: str) -> Dict[str, Any]:
        """Demo response when API is unavailable."""
        symptoms_lower = symptoms.lower()
        
        # Simple symptom matching
        if any(word in symptoms_lower for word in ['headache', 'head']):
            condition_name = "Tension Headache"
            description = "A common type of headache often caused by stress or muscle tension."
        elif any(word in symptoms_lower for word in ['cough', 'cold']):
            condition_name = "Common Cold"
            description = "A viral infection of the upper respiratory tract."
        elif any(word in symptoms_lower for word in ['tired', 'fatigue']):
            condition_name = "General Fatigue"
            description = "Feeling of tiredness that can have various causes."
        else:
            condition_name = "General Health Concern"
            description = "Your symptoms require professional medical evaluation."
        
        return {
            "conditions": [{
                "name": condition_name,
                "description": description,
                "probability": "Medium",
                "recommendations": [
                    "Monitor your symptoms",
                    "Get adequate rest and hydration",
                    "Consult a healthcare professional if symptoms persist"
                ]
            }],
            "emergency_detected": self._detect_emergency(symptoms),
            "general_recommendations": [
                "Always consult healthcare professionals for medical concerns",
                "Seek immediate care if symptoms worsen"
            ],
            "disclaimers": [
                "This tool is for educational purposes only",
                "Not a substitute for professional medical diagnosis",
                "Always consult healthcare professionals for medical advice"
            ]
        }

    def _load_medical_specialties(self) -> Dict[str, List[str]]:
        """Load medical specialties and their associated conditions."""
        return {
            'cardiology': ['chest pain', 'heart palpitations', 'shortness of breath', 'irregular heartbeat'],
            'neurology': ['headache', 'dizziness', 'seizure', 'memory loss', 'numbness', 'tingling'],
            'gastroenterology': ['abdominal pain', 'nausea', 'vomiting', 'diarrhea', 'constipation'],
            'dermatology': ['rash', 'skin lesion', 'itching', 'skin discoloration'],
            'orthopedics': ['joint pain', 'back pain', 'muscle pain', 'fracture', 'sprain'],
            'psychiatry': ['depression', 'anxiety', 'mood changes', 'sleep problems'],
            'endocrinology': ['diabetes', 'thyroid', 'hormone', 'weight changes'],
            'pulmonology': ['cough', 'breathing problems', 'chest tightness', 'wheezing']
        }
    
    def _load_emergency_keywords(self) -> Dict[str, int]:
        """Load emergency keywords with severity scores."""
        return {
            'chest pain': 10,
            'difficulty breathing': 10,
            'unconscious': 10,
            'severe bleeding': 10,
            'heart attack': 10,
            'stroke': 10,
            'anaphylaxis': 10,
            'seizure': 9,
            'severe headache': 8,
            'high fever': 7,
            'severe pain': 7,
            'vomiting blood': 9,
            'confusion': 6,
            'severe dizziness': 6
        }
    
    def _load_common_drug_interactions(self) -> Dict[str, List[str]]:
        """Load common drug interactions and warnings."""
        return {
            'blood_thinners': ['aspirin', 'warfarin', 'bleeding risk'],
            'diabetes_meds': ['insulin', 'metformin', 'blood sugar monitoring'],
            'heart_meds': ['beta blockers', 'ACE inhibitors', 'blood pressure'],
            'pain_meds': ['NSAIDs', 'opioids', 'liver function']
        }
    
    def _build_contextual_prompt(self, symptoms: str, patient_data: Optional[Dict[str, Any]]) -> str:
        """Build enhanced prompt with patient context."""
        prompt = f"Analyze these symptoms: {symptoms}\n\n"
        
        if patient_data:
            if patient_data.get('age_range'):
                prompt += f"Patient age range: {patient_data['age_range']}\n"
            if patient_data.get('gender'):
                prompt += f"Gender: {patient_data['gender']}\n"
            if patient_data.get('pain_level'):
                prompt += f"Pain level: {patient_data['pain_level']}\n"
            if patient_data.get('duration'):
                prompt += f"Symptom duration: {patient_data['duration']}\n"
            if patient_data.get('has_fever'):
                prompt += "Patient reports fever\n"
            if patient_data.get('taking_medications'):
                prompt += "Patient is taking medications\n"
        
        prompt += "\nProvide comprehensive analysis including differential diagnosis, urgency assessment, and specialist referral recommendations."
        return prompt
    
    def _get_enhanced_system_prompt(self) -> str:
        """Enhanced system prompt for comprehensive analysis."""
        return """You are an advanced medical information assistant providing comprehensive symptom analysis for educational purposes.

Analyze symptoms considering:
1. Differential diagnosis with probability assessment
2. Age and gender-specific considerations
3. Urgency and triage recommendations
4. Specialist referral suggestions
5. Risk factor assessment
6. Follow-up timeline recommendations

Respond with detailed JSON in this format:
{
    "conditions": [
        {
            "name": "Condition Name",
            "description": "Detailed medical description",
            "probability": "High|Medium|Low",
            "recommendations": ["Specific action 1", "Specific action 2"],
            "urgency": "Emergency|Urgent|Routine",
            "specialty": "Medical specialty if referral needed"
        }
    ],
    "general_recommendations": ["Comprehensive advice"],
    "disclaimers": ["Educational disclaimers"],
    "triage_level": "Emergency|Urgent|Semi-urgent|Routine",
    "confidence_score": 0.85
}

Always emphasize this is educational information only and professional medical consultation is required."""
    
    def _detect_emergency_advanced(self, symptoms: str, patient_data: Optional[Dict[str, Any]]) -> bool:
        """Advanced emergency detection with scoring."""
        symptoms_lower = symptoms.lower()
        emergency_score = 0
        
        # Check emergency keywords with weighted scoring
        for keyword, score in self.emergency_keywords.items():
            if keyword in symptoms_lower:
                emergency_score += score
                logging.warning(f"Emergency keyword detected: {keyword} (score: {score})")
        
        # Additional context-based scoring
        if patient_data:
            if patient_data.get('pain_level') in ['9-10']:
                emergency_score += 8
            if patient_data.get('emergency_symptoms'):
                emergency_score += 10
            if patient_data.get('age_range') in ['0-17', '70+'] and emergency_score > 0:
                emergency_score += 2  # Higher risk for very young or elderly
        
        # Pattern-based detection
        emergency_patterns = [
            r'\b(sudden|severe|intense|excruciating)\s+(chest|heart|breathing)',
            r'\b(can\'t|cannot)\s+(breathe|breath|move|speak)',
            r'\b(losing|lost)\s+(consciousness|vision|feeling)',
            r'\b(severe|heavy|profuse)\s+bleeding'
        ]
        
        for pattern in emergency_patterns:
            if re.search(pattern, symptoms_lower):
                emergency_score += 6
        
        return emergency_score >= 8
    
    def _suggest_specialist(self, symptoms: str, conditions: List[Dict[str, Any]]) -> Optional[str]:
        """Suggest appropriate medical specialist based on symptoms."""
        symptoms_lower = symptoms.lower()
        
        for specialty, keywords in self.medical_specialties.items():
            for keyword in keywords:
                if keyword in symptoms_lower:
                    return specialty.title()
        
        # Check conditions for specialty recommendations
        for condition in conditions:
            condition_name = condition.get('name', '').lower()
            if 'heart' in condition_name or 'cardiac' in condition_name:
                return 'Cardiology'
            elif 'neuro' in condition_name or 'brain' in condition_name:
                return 'Neurology'
            elif 'gastro' in condition_name or 'stomach' in condition_name:
                return 'Gastroenterology'
        
        return None
    
    def _assess_risk_factors(self, symptoms: str, patient_data: Optional[Dict[str, Any]]) -> List[str]:
        """Assess risk factors based on symptoms and patient data."""
        risk_factors = []
        
        if patient_data:
            age_range = patient_data.get('age_range', '')
            if age_range in ['70+']:
                risk_factors.append('Advanced age increases risk of serious conditions')
            elif age_range in ['0-17']:
                risk_factors.append('Pediatric symptoms require specialized evaluation')
            
            if patient_data.get('taking_medications'):
                risk_factors.append('Current medications may interact or mask symptoms')
            
            if patient_data.get('has_allergies'):
                risk_factors.append('Known allergies may complicate treatment options')
        
        # Symptom-based risk factors
        symptoms_lower = symptoms.lower()
        if 'chest pain' in symptoms_lower:
            risk_factors.append('Chest pain requires cardiac evaluation')
        if 'shortness of breath' in symptoms_lower:
            risk_factors.append('Breathing difficulties need immediate assessment')
        
        return risk_factors
    
    def _suggest_follow_up_timeline(self, conditions: List[Dict[str, Any]]) -> str:
        """Suggest appropriate follow-up timeline."""
        if not conditions:
            return "Follow up with healthcare provider within 1-2 weeks"
        
        urgency_levels = [condition.get('urgency', 'Routine') for condition in conditions]
        
        if 'Emergency' in urgency_levels:
            return "Seek immediate emergency care"
        elif 'Urgent' in urgency_levels:
            return "Schedule appointment within 24-48 hours"
        elif 'Semi-urgent' in urgency_levels:
            return "Schedule appointment within 1 week"
        else:
            return "Schedule routine appointment within 2-4 weeks"
    
    def _identify_red_flags(self, symptoms: str, patient_data: Optional[Dict[str, Any]]) -> List[str]:
        """Identify red flag symptoms requiring immediate attention."""
        red_flags = []
        symptoms_lower = symptoms.lower()
        
        red_flag_indicators = {
            'chest pain': 'Chest pain may indicate heart attack or other cardiac emergency',
            'difficulty breathing': 'Breathing difficulties require immediate medical evaluation',
            'severe headache': 'Sudden severe headache may indicate stroke or other emergency',
            'high fever': 'High fever, especially with other symptoms, needs prompt evaluation',
            'confusion': 'Confusion or altered mental state requires immediate assessment',
            'severe bleeding': 'Severe bleeding requires emergency medical care'
        }
        
        for indicator, warning in red_flag_indicators.items():
            if indicator in symptoms_lower:
                red_flags.append(warning)
        
        return red_flags
    
    def _log_analysis(self, symptoms: str, result: Dict[str, Any], patient_data: Optional[Dict[str, Any]]):
        """Log analysis for quality improvement and monitoring."""
        try:
            # Create anonymized log entry
            symptoms_hash = hashlib.sha256(symptoms.encode()).hexdigest()[:16]
            log_entry = {
                'timestamp': datetime.utcnow().isoformat(),
                'symptoms_hash': symptoms_hash,
                'emergency_detected': result.get('emergency_detected', False),
                'conditions_count': len(result.get('conditions', [])),
                'specialist_suggested': result.get('specialist_referral'),
                'triage_level': result.get('triage_level', 'Unknown'),
                'has_patient_data': patient_data is not None
            }
            
            logging.info(f"SYMPTOM_ANALYSIS: {log_entry}")
            
        except Exception as e:
            logging.error(f"Failed to log analysis: {str(e)}")
    
    def get_analysis_statistics(self) -> Dict[str, Any]:
        """Get analysis statistics for monitoring."""
        # This would typically query a database in a production system
        return {
            'total_analyses': 'N/A - Demo Mode',
            'emergency_cases': 'N/A - Demo Mode',
            'most_common_conditions': 'N/A - Demo Mode',
            'specialist_referrals': 'N/A - Demo Mode'
        }
    
    def _get_demo_response(self, symptoms: str, patient_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Enhanced demo response with patient context."""
        symptoms_lower = symptoms.lower()
        
        # Enhanced symptom matching with patient context
        conditions = []
        
        if any(word in symptoms_lower for word in ['headache', 'head']):
            urgency = 'Urgent' if patient_data and patient_data.get('pain_level') == '9-10' else 'Routine'
            conditions.append({
                "name": "Tension Headache",
                "description": "A common type of headache often caused by stress, muscle tension, or dehydration.",
                "probability": "High" if 'stress' in symptoms_lower else "Medium",
                "recommendations": [
                    "Apply cold or warm compress to head and neck",
                    "Practice relaxation techniques",
                    "Stay hydrated and get adequate rest",
                    "Consider over-the-counter pain medication if appropriate"
                ],
                "urgency": urgency,
                "specialty": "Neurology" if urgency == 'Urgent' else None
            })
        
        if any(word in symptoms_lower for word in ['cough', 'cold', 'congestion']):
            conditions.append({
                "name": "Upper Respiratory Infection",
                "description": "A viral infection affecting the nose, throat, and upper airways.",
                "probability": "High",
                "recommendations": [
                    "Get plenty of rest and stay hydrated",
                    "Use humidifier or breathe steam",
                    "Consider over-the-counter medications for symptom relief",
                    "Avoid contact with others to prevent spread"
                ],
                "urgency": "Routine",
                "specialty": None
            })
        
        if any(word in symptoms_lower for word in ['tired', 'fatigue', 'exhausted']):
            conditions.append({
                "name": "General Fatigue",
                "description": "Feeling of tiredness or lack of energy that can have various underlying causes.",
                "probability": "Medium",
                "recommendations": [
                    "Ensure adequate sleep (7-9 hours per night)",
                    "Maintain balanced diet and regular exercise",
                    "Manage stress levels",
                    "Consider underlying medical conditions if persistent"
                ],
                "urgency": "Routine",
                "specialty": None
            })
        
        # Default condition if no specific matches
        if not conditions:
            conditions.append({
                "name": "General Health Concern",
                "description": "Your symptoms require professional medical evaluation for accurate diagnosis.",
                "probability": "Medium",
                "recommendations": [
                    "Monitor symptoms and document any changes",
                    "Consult with healthcare professional for proper evaluation",
                    "Seek immediate care if symptoms worsen significantly"
                ],
                "urgency": "Routine",
                "specialty": None
            })
        
        # Enhanced analysis features
        emergency_detected = self._detect_emergency_advanced(symptoms, patient_data)
        specialist_referral = self._suggest_specialist(symptoms, conditions)
        risk_factors = self._assess_risk_factors(symptoms, patient_data)
        follow_up_timeline = self._suggest_follow_up_timeline(conditions)
        red_flags = self._identify_red_flags(symptoms, patient_data)
        
        return {
            "conditions": conditions,
            "emergency_detected": emergency_detected,
            "specialist_referral": specialist_referral,
            "risk_factors": risk_factors,
            "follow_up_timeline": follow_up_timeline,
            "red_flags": red_flags,
            "general_recommendations": [
                "Always consult healthcare professionals for medical concerns",
                "Monitor symptoms and seek care if they worsen",
                "Keep a symptom diary for healthcare provider review",
                "Follow up as recommended based on symptom severity"
            ],
            "disclaimers": [
                "This analysis is for educational purposes only",
                "Not a substitute for professional medical diagnosis",
                "Always consult healthcare professionals for medical advice",
                "Seek immediate care for emergency symptoms"
            ],
            "triage_level": "Emergency" if emergency_detected else "Routine",
            "confidence_score": 0.75
        }