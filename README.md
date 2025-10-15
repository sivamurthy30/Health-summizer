# Healthcare Symptom Checker

A web application that provides educational health information based on user-submitted symptoms using AI analysis. This tool is designed for educational purposes only and emphasizes the importance of professional medical consultation.

## ⚠️ Important Disclaimer

**This application is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider for medical concerns. In case of emergency, call 911 immediately.**

## Features

- 🔍 **Symptom Analysis**: AI-powered analysis of user-submitted symptoms
- 🚨 **Emergency Detection**: Automatic detection of potentially serious symptoms
- 📱 **Responsive Design**: Mobile-friendly interface using Bootstrap
- 🔒 **Privacy Focused**: No storage of personally identifiable information
- ⚡ **Rate Limiting**: Built-in protection against abuse
- 🛡️ **Safety First**: Prominent disclaimers and emergency guidance

## Technology Stack

- **Backend**: Python 3.8+, Flask
- **AI Integration**: OpenAI GPT API
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Database**: SQLite (optional, for query history)
- **Deployment**: WSGI-compatible (Gunicorn recommended)

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- pip (Python package installer)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd healthcare-symptom-checker
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
DEBUG=True

# Database Configuration (optional)
DATABASE_URL=sqlite:///symptom_checker.db

# Server Configuration
HOST=127.0.0.1
PORT=5000
```

### 5. Obtain OpenAI API Key

1. Visit [OpenAI's website](https://platform.openai.com/)
2. Create an account or sign in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

**Note**: Keep your API key secure and never commit it to version control.

## Running the Application

### Development Mode

```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000`

### Production Mode

For production deployment, use a WSGI server like Gunicorn:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

## Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for symptom analysis | None | Yes |
| `SECRET_KEY` | Flask secret key for sessions | Auto-generated | Recommended |
| `FLASK_ENV` | Flask environment (development/production) | development | No |
| `DEBUG` | Enable debug mode | True | No |
| `DATABASE_URL` | Database connection string | SQLite file | No |
| `HOST` | Server host address | 127.0.0.1 | No |
| `PORT` | Server port number | 5000 | No |

### Rate Limiting

The application includes built-in rate limiting:
- **Analysis requests**: 10 requests per 15 minutes per IP
- **General requests**: Standard Flask rate limiting

## API Endpoints

### Main Routes

- `GET /` - Home page with symptom input form
- `POST /` - Process symptom form submission
- `GET /analyze` - Display analysis results
- `GET /health` - Health check endpoint

### Health Check

```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000000",
  "service": "Healthcare Symptom Checker"
}
```

## Usage

1. **Access the Application**: Navigate to the application URL
2. **Read Disclaimers**: Review the educational disclaimers
3. **Enter Symptoms**: Describe symptoms in detail (minimum 10 characters)
4. **Submit for Analysis**: Click "Analyze Symptoms"
5. **Review Results**: Read the educational information provided
6. **Seek Professional Care**: Consult healthcare professionals as recommended

### Example Symptom Descriptions

**Good Example:**
> "I've had a persistent cough for 3 days with yellow mucus, mild fever around 100°F, and fatigue. The cough is worse at night."

**Too Brief:**
> "I feel sick" or "My head hurts"

## Safety Features

### Emergency Detection

The application automatically detects potentially serious symptoms and displays emergency warnings for:

- Chest pain or difficulty breathing
- Severe bleeding or injuries
- Loss of consciousness
- Severe allergic reactions
- Signs of stroke or heart attack
- Suicidal thoughts

### Privacy Protection

- No storage of personally identifiable information
- Symptom descriptions are processed securely
- Optional query history uses hashed data only
- Session-based tracking without user identification

## Troubleshooting

### Common Issues

**"Service configuration error"**
- Check that `OPENAI_API_KEY` is set correctly in `.env`
- Verify the API key is valid and has sufficient credits

**"The analysis service is taking too long"**
- Check internet connectivity
- Verify OpenAI API service status
- Consider increasing `API_TIMEOUT` in config

**"Too many requests"**
- Wait for the rate limit window to reset (15 minutes)
- Check if multiple users are sharing the same IP address

### Logging

Application logs are written to the console by default. For production, configure proper logging:

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## Development

### Project Structure

```
healthcare-symptom-checker/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── routes.py                # Main application routes
│   ├── forms.py                 # WTForms form definitions
│   ├── models.py                # Database models (optional)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── symptom_analyzer.py  # AI symptom analysis service
│   │   └── database_service.py  # Database operations (optional)
│   ├── templates/               # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── results.html
│   │   ├── 404.html
│   │   └── 500.html
│   └── static/                  # Static assets (CSS, JS)
├── config.py                    # Application configuration
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── run.py                       # Application entry point
└── README.md                    # This file
```

### Adding Features

1. **New Routes**: Add to `app/routes.py`
2. **New Templates**: Create in `app/templates/`
3. **New Services**: Add to `app/services/`
4. **Configuration**: Update `config.py`

## Deployment

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure HTTPS/SSL
- [ ] Set up proper logging
- [ ] Configure reverse proxy (nginx)
- [ ] Set up monitoring and health checks
- [ ] Implement backup strategy (if using database)

### Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:create_app()"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is intended for educational purposes. Please ensure compliance with healthcare regulations and OpenAI's usage policies in your jurisdiction.

## Support

For technical issues:
1. Check the troubleshooting section
2. Review application logs
3. Verify configuration settings
4. Contact system administrator

**For medical emergencies: Call 911 or your local emergency services immediately.**

## Acknowledgments

- OpenAI for providing the GPT API
- Flask community for the web framework
- Bootstrap for the responsive UI components
- Healthcare professionals who emphasize the importance of proper medical care