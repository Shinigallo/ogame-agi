#!/bin/bash
# Smart OGame Bot Launcher

set -e

echo "🧠 Smart OGame Bot Launcher (Token-Efficient)"
echo "=============================================="

# Check for required files
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "📋 Copy .env.smart to .env and configure credentials"
    exit 1
fi

source .env

# Validate credentials
if [ -z "$OGAME_USERNAME" ] || [ -z "$OGAME_PASSWORD" ]; then
    echo "❌ Missing credentials in .env"
    exit 1
fi

echo "📋 Smart Bot Configuration:"
echo "   Username: $OGAME_USERNAME"
echo "   Quick Check: ${QUICK_CHECK_INTERVAL:-60}s"
echo "   AI Interval: ${AI_DECISION_INTERVAL:-1800}s (30min)"
echo "   Max Session: ${MAX_SESSION_TIME:-3600}s (1h)"
echo "   Metal Alert: ${METAL_THRESHOLD:-50000}"
echo ""

# Deployment options
echo "🚀 Deployment Options:"
echo "   1) Docker Compose (recommended)"
echo "   2) Direct Python"
echo "   3) Test mode (dry run)"
echo ""

read -p "Choose option (1-3): " choice

case $choice in
    1)
        echo "🐳 Starting Smart Bot with Docker..."
        
        # Create required directories
        mkdir -p data logs knowledge
        
        # Start smart bot
        docker-compose -f docker-compose.smart.yml up --build -d
        
        echo ""
        echo "✅ Smart Bot started!"
        echo "📊 Monitor: docker-compose -f docker-compose.smart.yml logs -f"
        echo "📈 Dashboard: http://localhost:8080"
        echo "⏹️  Stop: docker-compose -f docker-compose.smart.yml down"
        echo ""
        echo "🤖 Bot Mode: Event-driven (minimal token usage)"
        echo "   - Quick checks every 60s (no AI)"
        echo "   - AI decisions only when needed"
        echo "   - Cron-based scheduling"
        echo "   - Auto-session cleanup"
        ;;
        
    2)
        echo "🐍 Starting with Python..."
        
        if [ ! -d "venv" ]; then
            python3 -m venv venv
        fi
        
        source venv/bin/activate
        pip install -r requirements.smart.txt
        playwright install chromium
        
        mkdir -p data logs
        
        echo "🏃 Running Smart Bot..."
        python src/smart_ogame_bot.py
        ;;
        
    3)
        echo "🧪 Test mode..."
        
        export TEST_MODE=true
        export DRY_RUN=true
        
        if [ ! -d "venv" ]; then
            python3 -m venv venv
        fi
        
        source venv/bin/activate
        pip install -r requirements.smart.txt
        
        echo "🔍 Running in test mode (no real actions)..."
        python src/smart_ogame_bot.py
        ;;
        
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac