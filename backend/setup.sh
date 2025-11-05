#!/bin/bash

# Wardrobe AI Backend - Quick Setup Script

echo "================================================"
echo "  Wardrobe AI Backend - Quick Setup"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

# Create directories
echo ""
echo "Creating necessary directories..."
mkdir -p app/static/uploads
mkdir -p app/static/generated
mkdir -p data/chroma_db

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your OPENROUTER_API_KEY"
    echo "   Get your key from: https://openrouter.ai/"
else
    echo ""
    echo "✓ .env file already exists"
fi

# Run basic tests
echo ""
echo "Running setup verification..."
python test_basic.py

echo ""
echo "================================================"
echo "  Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OPENROUTER_API_KEY"
echo "2. Run: python run.py"
echo "3. Visit: http://localhost:5000"
echo ""
echo "For API examples, see: API_EXAMPLES.md"
echo ""
