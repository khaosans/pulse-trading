#!/bin/bash

# PulseTrade Demo Launch Script

echo "🚀 Starting PulseTrade Demo..."
echo "================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo "🌐 Opening PulseTrade Demo..."
echo "📍 URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"
echo ""

# Run Streamlit app
streamlit run demo_app.py --server.port 8501 --server.headless true



