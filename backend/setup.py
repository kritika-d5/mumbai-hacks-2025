"""
Setup script for NewsPrism backend
Run: python setup.py
"""

import subprocess
import sys
import os

def run_command(command, description):
    print(f"\n{description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(f"✓ {description} completed")
    return True

def main():
    print("NewsPrism Backend Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("Error: Python 3.10+ required")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        sys.exit(1)
    
    # Download spaCy model
    if not run_command("python -m spacy download en_core_web_sm", "Downloading spaCy model"):
        print("Warning: spaCy model download failed. You may need to install it manually.")
    
    # Create .env file if it doesn't exist
    if not os.path.exists(".env"):
        print("\nCreating .env file from .env.example...")
        if os.path.exists(".env.example"):
            with open(".env.example", "r") as f:
                content = f.read()
            with open(".env", "w") as f:
                f.write(content)
            print("✓ .env file created. Please edit it with your API keys.")
        else:
            print("Warning: .env.example not found")
    
    print("\n" + "=" * 50)
    print("Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Set up PostgreSQL database")
    print("3. Run: alembic upgrade head (to create database tables)")
    print("4. Run: python -m uvicorn app.main:app --reload")

if __name__ == "__main__":
    main()

