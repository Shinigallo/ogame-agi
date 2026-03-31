#!/bin/bash
# Quick mobile session capture for OGame bot

echo "📱 OGame Mobile Session Setup"
echo "========================="
echo
echo "STEP 1: Login from your phone"
echo "URL: https://s161-en.ogame.gameforge.com"
echo "User: TestAgent2026"
echo "Pass: TestAGI2026!"
echo
echo "STEP 2: After login, copy the current page URL"
echo "STEP 3: Paste the URL below (it contains session tokens)"
echo
read -p "🔗 Paste your logged-in URL: " session_url

# Extract session from URL
echo "$session_url" > /home/dario/ogame-agi/data/mobile_session.txt

# Create basic session file
cat > /home/dario/ogame-agi/data/session.json << EOF
{
  "username": "TestAgent2026",
  "url": "https://s161-en.ogame.gameforge.com",
  "mobile_session_url": "$session_url",
  "cookies": [
    {
      "name": "mobile_session",
      "value": "extracted_from_url",
      "domain": ".ogame.gameforge.com"
    }
  ]
}
EOF

echo "✅ Session captured!"
echo "🔄 Restarting bot with mobile session..."

# Restart bot
docker restart ogame-smart-bot

echo "🎉 Bot restarted with your session!"