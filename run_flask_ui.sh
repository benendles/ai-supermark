#!/bin/bash

# Script to run the Flask-based UI for WatsonX Orchestrate Agent

echo "🚀 Starting WatsonX Orchestrate Agent UI (Flask)"
echo "================================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file. Please edit it with your credentials."
    else
        echo "❌ .env.example not found. Please create .env manually."
        exit 1
    fi
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r ai_supermarket/requirements.txt

# Check if Flask dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "📦 Installing Flask..."
    pip install -q flask flask-cors
fi

# Run Flask app
echo ""
echo "✅ Starting Flask server..."
echo "📍 Server will be available at: http://localhost:5000"
echo "💡 Press Ctrl+C to stop the server"
echo ""

cd ai_supermarket/frontend
python flask_app.py

