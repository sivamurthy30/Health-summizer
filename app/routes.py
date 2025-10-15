from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app, session
from app.forms import SymptomForm, FeedbackForm, SymptomHistoryForm
from app.services.symptom_analyzer import SymptomAnalyzer
import logging
import time
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    """Display symptom input form and handle form submissions."""
    form = SymptomForm()
    
    if form.validate_on_submit():
        symptoms = form.symptoms.data.strip()
        
        # Redirect to analyze route with symptoms
        return redirect(url_for('main.analyze', symptoms=symptoms))
    
    return render_template('index.html', form=form)

@bp.route('/analyze')
def analyze():
    """Process symptom analysis request."""
    symptoms = request.args.get('symptoms', '').strip()
    
    if not symptoms or len(symptoms) < 10:
        flash('Please provide at least 10 characters describing your symptoms.', 'error')
        return redirect(url_for('main.index'))
    
    try:
        # Collect patient data from form
        patient_data = {
            'age_range': form.age_range.data,
            'gender': form.gender.data,
            'pain_level': form.pain_level.data,
            'duration': form.duration.data,
            'has_fever': form.has_fever.data,
            'has_allergies': form.has_allergies.data,
            'taking_medications': form.taking_medications.data,
            'emergency_symptoms': form.emergency_symptoms.data
        }
        
        # Store patient data in session for follow-up forms
        session['patient_data'] = patient_data
        session['last_symptoms'] = symptoms
        
        # Analyze symptoms with enhanced context
        analyzer = SymptomAnalyzer()
        analysis_result = analyzer.analyze_symptoms(symptoms, patient_data)
        
        return render_template('results.html', 
                             symptoms=symptoms, 
                             analysis=analysis_result,
                             patient_data=patient_data)
    
    except Exception as e:
        logging.error(f"Error analyzing symptoms: {str(e)}")
        flash('An error occurred while analyzing your symptoms. Please try again.', 'error')
        flash('If you are experiencing severe symptoms, please seek immediate medical attention.', 'warning')
        return redirect(url_for('main.index'))

@bp.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})

@bp.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    logging.warning(f"404 error: {request.url}")
    return render_template('404.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logging.error(f"500 error: {str(error)}")
    return render_template('500.html'), 500


@bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """Handle user feedback on analysis results."""
    form = FeedbackForm()
    
    if form.validate_on_submit():
        # In a real application, this would save to database
        logging.info(f"User feedback received - Rating: {form.rating.data}, Comments: {form.comments.data}")
        flash('Thank you for your feedback! It helps us improve our service.', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('feedback.html', form=form)

@bp.route('/history', methods=['GET', 'POST'])
def symptom_history():
    """Handle additional symptom history and context."""
    form = SymptomHistoryForm()
    
    if form.validate_on_submit():
        # Get previous analysis data from session
        patient_data = session.get('patient_data', {})
        symptoms = session.get('last_symptoms', '')
        
        # Add history data to patient context
        history_data = {
            'previous_symptoms': form.previous_symptoms.data,
            'family_history': form.family_history.data,
            'lifestyle_factors': form.lifestyle_factors.data
        }
        
        # Combine with existing patient data
        enhanced_patient_data = {**patient_data, **history_data}
        
        # Re-analyze with enhanced context
        analyzer = SymptomAnalyzer()
        analysis_result = analyzer.analyze_symptoms(symptoms, enhanced_patient_data)
        
        return render_template('results.html', 
                             symptoms=symptoms, 
                             analysis=analysis_result,
                             patient_data=enhanced_patient_data,
                             enhanced_analysis=True)
    
    return render_template('history.html', form=form)

@bp.route('/emergency-guide')
def emergency_guide():
    """Display emergency symptoms guide."""
    emergency_info = {
        'immediate_911': [
            'Chest pain or pressure',
            'Difficulty breathing or shortness of breath',
            'Sudden severe headache',
            'Loss of consciousness or fainting',
            'Severe bleeding that won\'t stop',
            'Signs of stroke (face drooping, arm weakness, speech difficulty)',
            'Severe allergic reaction (anaphylaxis)',
            'Seizures',
            'Severe burns',
            'Suspected poisoning or overdose'
        ],
        'urgent_care': [
            'High fever (over 103°F/39.4°C)',
            'Persistent vomiting or diarrhea',
            'Severe pain (8-10/10)',
            'Signs of infection with fever',
            'Difficulty swallowing',
            'Severe headache with neck stiffness',
            'Abdominal pain with vomiting',
            'Cuts that may need stitches'
        ],
        'primary_care': [
            'Persistent cough or cold symptoms',
            'Mild to moderate pain',
            'Skin rashes or irritations',
            'Minor injuries',
            'Routine health concerns',
            'Follow-up for chronic conditions',
            'Preventive care and check-ups'
        ]
    }
    
    return render_template('emergency_guide.html', emergency_info=emergency_info)

@bp.route('/statistics')
def statistics():
    """Display system statistics (for demo purposes)."""
    analyzer = SymptomAnalyzer()
    stats = analyzer.get_analysis_statistics()
    
    # Add some demo statistics
    demo_stats = {
        'total_analyses_today': 42,
        'emergency_cases_today': 3,
        'most_common_symptoms': ['Headache', 'Cough', 'Fatigue', 'Fever'],
        'specialist_referrals_today': {
            'Cardiology': 5,
            'Neurology': 3,
            'Gastroenterology': 2,
            'Dermatology': 1
        },
        'system_uptime': '99.9%',
        'average_response_time': '2.3 seconds'
    }
    
    return render_template('statistics.html', stats=demo_stats)

@bp.route('/api/quick-check', methods=['POST'])
def quick_check_api():
    """API endpoint for quick symptom checking."""
    data = request.get_json()
    
    if not data or 'symptoms' not in data:
        return jsonify({'error': 'Symptoms required'}), 400
    
    symptoms = data['symptoms']
    if len(symptoms.strip()) < 10:
        return jsonify({'error': 'Please provide more detailed symptoms'}), 400
    
    try:
        analyzer = SymptomAnalyzer()
        result = analyzer.analyze_symptoms(symptoms, data.get('patient_data'))
        
        # Return simplified response for API
        api_response = {
            'emergency_detected': result.get('emergency_detected', False),
            'triage_level': result.get('triage_level', 'Routine'),
            'top_condition': result['conditions'][0]['name'] if result.get('conditions') else 'Unknown',
            'specialist_referral': result.get('specialist_referral'),
            'follow_up_timeline': result.get('follow_up_timeline'),
            'confidence_score': result.get('confidence_score', 0.0)
        }
        
        return jsonify(api_response)
        
    except Exception as e:
        logging.error(f"API error: {str(e)}")
        return jsonify({'error': 'Analysis failed'}), 500