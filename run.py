#!/usr/bin/env python3
"""
Healthcare Symptom Checker Application Entry Point
"""
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Get configuration from environment variables
    debug_mode = os.environ.get('DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    
    print(f"Starting Healthcare Symptom Checker on {host}:{port}")
    print(f"Debug mode: {debug_mode}")
    
    app.run(
        host=host,
        port=port,
        debug=debug_mode
    )