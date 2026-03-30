#!/bin/bash
# OGame Bot Launcher Script

set -e

echo "🤖 OGame Autonomous Bot Launcher"
echo "================================"

# Check for required files
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "📋 Copy .env.example to .env and configure your credentials"
    exit 1
fi

# Load environment
source .env

# Validate required variables
if [ -z "$OGAME_USERNAME" ] || [ -z "$OGAME_PASSWORD" ]; then
    echo "❌ Missing credentials in .env file"
    echo "   Required: OGAME_USERNAME, OGAME_PASSWORD"
    exit 1
fi

# Create required directories
mkdir -p data logs knowledge

echo "📋 Configuration:"
echo "   Username: $OGAME_USERNAME"
echo "   Universe: ${OGAME_UNIVERSE_URL:-default}"
echo "   Strategy: ${STRATEGIC_MODE:-balanced}"
echo "   Interval: ${DECISION_INTERVAL:-300}s"
echo "   Headless: ${HEADLESS:-true}"
echo ""

# Choose deployment method
echo "🚀 Deployment Options:"
echo "   1) Docker Compose (recommended)"
echo "   2) Direct Python execution"
echo "   3) Build Docker image only"
echo ""

read -p "Choose option (1-3): " choice

case $choice in
    1)
        echo "🐳 Starting with Docker Compose..."
        docker-compose -f docker-compose.bot.yml up --build -d
        echo ""
        echo "✅ Bot started in background!"
        echo "📊 Monitor logs: docker-compose -f docker-compose.bot.yml logs -f"
        echo "🔍 Check status: docker-compose -f docker-compose.bot.yml ps"
        echo "⏹️  Stop bot: docker-compose -f docker-compose.bot.yml down"
        ;;
    2)
        echo "🐍 Starting with Python..."
        
        # Check Python environment
        if ! command -v python3 &> /dev/null; then
            echo "❌ Python 3 not found"
            exit 1
        fi
        
        # Install dependencies if needed
        if [ ! -d "venv" ]; then
            echo "📦 Creating virtual environment..."
            python3 -m venv venv
        fi
        
        source venv/bin/activate
        pip install -r requirements.txt
        
        # Install Playwright browsers
        playwright install chromium
        
        echo "🏃 Running bot..."
        python src/ogame_bot.py
        ;;
    3)
        echo "🔨 Building Docker image..."
        docker build -f Dockerfile.bot -t ogame-bot:latest .
        echo "✅ Image built successfully!"
        echo "🏃 Run with: docker run --env-file .env ogame-bot:latest"
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac