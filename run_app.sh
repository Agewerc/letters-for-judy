#!/bin/bash
# Script to run the Judith Tribute App

echo "🚀 Starting Judith Tribute App..."
echo "📍 Navigate to the displayed URL to view the application"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

cd /workspaces/letters-for-judy/app
streamlit run main.py # --server.port 8501 --server.address 0.0.0.0
