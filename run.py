#!/usr/bin/env python3
"""
Healthcare Symptom Checker Application Entry Point
"""
import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

app = create_app()

if __name__ == '__main__':
    # Get configuration from environment variables
    debug_mode = os.environ.get('DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    
    print(f"Environment PORT: {os.environ.get('PORT', 'Not set')}")
    print(f"Starting Healthcare Symptom Checker on {host}:{port}")
    print(f"Debug mode: {debug_mode}")
    
    app.run(
        host=host,
        port=port,
        debug=debug_mode
    )