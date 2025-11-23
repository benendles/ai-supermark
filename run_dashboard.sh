#!/bin/bash

# Quick start script for Streamlit Dashboard

echo "🛒 Starting AI Supermarket Inventory Manager Dashboard..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env file with your WatsonX Orchestrate credentials:"
    echo "   - WO_INSTANCE: Your WatsonX instance URL"
    echo "   - WO_API_KEY: Your API key"
    echo "   - SUPERMARKET_AGENT_ID: Agent ID (default: supermarket_inventory_manager_agent)"
    echo ""
    read -p "Press Enter after editing .env file to continue..."
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
python -c "import streamlit; import requests; from dotenv import load_dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 Installing dependencies..."
    pip install -r ai_supermarket/requirements.txt -q
fi

# Run Streamlit
echo ""
echo "🚀 Starting Streamlit dashboard..."
echo "📱 Dashboard will open at: http://localhost:8501"
echo ""
streamlit run ai_supermarket/frontend/app.py

