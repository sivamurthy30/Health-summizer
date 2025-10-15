from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.services.simple_analyzer import SymptomAnalyzer

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    """Simple symptom input and analysis."""
    if request.method == 'POST':
        symptoms = request.form.get('symptoms', '').strip()
        
        if symptoms and len(symptoms) >= 10:
            try:
                analyzer = SymptomAnalyzer()
                analysis_result = analyzer.analyze_symptoms(symptoms)
                
                return render_template('simple_results.html', 
                                     symptoms=symptoms, 
                                     analysis=analysis_result)
            except Exception as e:
                error_message = f"Error analyzing symptoms: {str(e)}"
                return render_template('simple_index.html', error=error_message)
        else:
            error_message = "Please provide at least 10 characters describing your symptoms."
            return render_template('simple_index.html', error=error_message)
    
    return render_template('simple_index.html')

@bp.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'Healthcare Symptom Checker'})