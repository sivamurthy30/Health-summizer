from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, IntegerField, StringField, RadioField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange, Optional
import re

class SymptomForm(FlaskForm):
    """Enhanced form for symptom input with additional medical information."""
    
    # Basic symptom description
    symptoms = TextAreaField(
        'Describe your symptoms',
        validators=[
            DataRequired(message='Please describe your symptoms.'),
            Length(min=10, max=2000, message='Please provide between 10 and 2000 characters.')
        ],
        render_kw={
            'placeholder': 'Please describe your symptoms in detail (minimum 10 characters)...',
            'rows': 5,
            'class': 'form-control'
        }
    )
    
    # Patient demographics (optional for better analysis)
    age_range = SelectField(
        'Age Range (Optional)',
        choices=[
            ('', 'Select age range'),
            ('0-17', 'Under 18'),
            ('18-30', '18-30 years'),
            ('31-50', '31-50 years'),
            ('51-70', '51-70 years'),
            ('70+', 'Over 70')
        ],
        validators=[Optional()],
        render_kw={'class': 'form-select'}
    )
    
    gender = SelectField(
        'Gender (Optional)',
        choices=[
            ('', 'Select gender'),
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
            ('prefer_not_to_say', 'Prefer not to say')
        ],
        validators=[Optional()],
        render_kw={'class': 'form-select'}
    )
    
    # Symptom severity and duration
    pain_level = SelectField(
        'Pain Level (if applicable)',
        choices=[
            ('', 'No pain or not applicable'),
            ('1-3', 'Mild (1-3/10)'),
            ('4-6', 'Moderate (4-6/10)'),
            ('7-8', 'Severe (7-8/10)'),
            ('9-10', 'Extreme (9-10/10)')
        ],
        validators=[Optional()],
        render_kw={'class': 'form-select'}
    )
    
    duration = SelectField(
        'How long have you had these symptoms?',
        choices=[
            ('', 'Select duration'),
            ('hours', 'A few hours'),
            ('1-2_days', '1-2 days'),
            ('3-7_days', '3-7 days'),
            ('1-2_weeks', '1-2 weeks'),
            ('2-4_weeks', '2-4 weeks'),
            ('months', 'Several months'),
            ('chronic', 'Chronic (ongoing)')
        ],
        validators=[Optional()],
        render_kw={'class': 'form-select'}
    )
    
    # Medical history flags
    has_fever = BooleanField(
        'Currently have fever',
        render_kw={'class': 'form-check-input'}
    )
    
    has_allergies = BooleanField(
        'Known allergies',
        render_kw={'class': 'form-check-input'}
    )
    
    taking_medications = BooleanField(
        'Currently taking medications',
        render_kw={'class': 'form-check-input'}
    )
    
    # Emergency indicators
    emergency_symptoms = BooleanField(
        'I am experiencing severe or life-threatening symptoms',
        render_kw={'class': 'form-check-input'}
    )
    
    submit = SubmitField('Analyze Symptoms', render_kw={'class': 'btn btn-primary btn-lg'})
    
    def validate_symptoms(self, field):
        """Enhanced validation for symptom input."""
        # Remove extra whitespace and check actual content length
        cleaned_text = re.sub(r'\s+', ' ', field.data.strip())
        
        if len(cleaned_text) < 10:
            raise ValidationError('Please provide at least 10 meaningful characters describing your symptoms.')
        
        # Basic sanitization check - reject if contains suspicious patterns
        suspicious_patterns = [
            r'<script',
            r'javascript:',
            r'on\w+\s*=',  # onclick, onload, etc.
            r'<iframe',
            r'<object',
            r'<embed'
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, field.data, re.IGNORECASE):
                raise ValidationError('Invalid characters detected in input.')
        
        # Store cleaned text back to field
        field.data = cleaned_text
    
    def validate_emergency_symptoms(self, field):
        """Validate emergency symptoms checkbox."""
        if field.data:
            # If user indicates emergency symptoms, add validation message
            raise ValidationError('If you are experiencing severe or life-threatening symptoms, please call 911 or go to the nearest emergency room immediately.')

class FeedbackForm(FlaskForm):
    """Form for user feedback on analysis results."""
    
    rating = RadioField(
        'How helpful was this analysis?',
        choices=[
            ('5', 'Very helpful'),
            ('4', 'Helpful'),
            ('3', 'Somewhat helpful'),
            ('2', 'Not very helpful'),
            ('1', 'Not helpful at all')
        ],
        validators=[DataRequired()],
        render_kw={'class': 'form-check-input'}
    )
    
    comments = TextAreaField(
        'Additional comments (optional)',
        validators=[Optional(), Length(max=500)],
        render_kw={
            'placeholder': 'Any additional feedback about the analysis...',
            'rows': 3,
            'class': 'form-control'
        }
    )
    
    submit = SubmitField('Submit Feedback', render_kw={'class': 'btn btn-success'})

class SymptomHistoryForm(FlaskForm):
    """Form for tracking symptom history and progression."""
    
    previous_symptoms = TextAreaField(
        'Previous or related symptoms',
        validators=[Optional(), Length(max=1000)],
        render_kw={
            'placeholder': 'Describe any previous symptoms or medical history relevant to your current condition...',
            'rows': 4,
            'class': 'form-control'
        }
    )
    
    family_history = TextAreaField(
        'Relevant family medical history',
        validators=[Optional(), Length(max=500)],
        render_kw={
            'placeholder': 'Any relevant family medical history...',
            'rows': 3,
            'class': 'form-control'
        }
    )
    
    lifestyle_factors = TextAreaField(
        'Lifestyle factors (diet, exercise, stress, etc.)',
        validators=[Optional(), Length(max=500)],
        render_kw={
            'placeholder': 'Recent changes in diet, exercise, stress levels, travel, etc...',
            'rows': 3,
            'class': 'form-control'
        }
    )
    
    submit = SubmitField('Add to Analysis', render_kw={'class': 'btn btn-info'})