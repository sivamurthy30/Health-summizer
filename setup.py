#!/usr/bin/env python3
"""
Setup script for Healthcare Symptom Checker
"""
import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def setup_virtual_environment():
    """Set up virtual environment."""
    if os.path.exists('venv'):
        print("📁 Virtual environment already exists")
        return True
    
    return run_command('python3 -m venv venv', 'Creating virtual environment')

def install_dependencies():
    """Install Python dependencies."""
    # Determine the correct pip path
    if os.name == 'nt':  # Windows
        pip_path = 'venv\\Scripts\\pip'
    else:  # macOS/Linux
        pip_path = 'venv/bin/pip'
    
    return run_command(f'{pip_path} install -r requirements.txt', 'Installing dependencies')

def setup_environment_file():
    """Set up environment configuration file."""
    if os.path.exists('.env'):
        print("📁 .env file already exists")
        return True
    
    if os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file and add your OpenAI API key")
        return True
    else:
        print("❌ .env.example file not found")
        return False

def main():
    """Main setup function."""
    print("🏥 Healthcare Symptom Checker Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Set up virtual environment
    if not setup_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Set up environment file
    if not setup_environment_file():
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Activate virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # macOS/Linux
        print("   source venv/bin/activate")
    print("3. Run the application:")
    print("   python run.py")
    print("\n⚠️  Remember: This is for educational purposes only!")

if __name__ == '__main__':
    main()