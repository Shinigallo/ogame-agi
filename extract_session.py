#!/usr/bin/env python3
"""
Simplest OGame Login - Extract session from your own browser
"""

import json
import requests
from pathlib import Path

def extract_session():
    """Extract session manually"""
    
    print("🎮 OGame Session Extractor")
    print("=" * 40)
    print()
    print("STEPS:")
    print("1. Open https://s161-en.ogame.gameforge.com in your browser")
    print("2. Login with: TestAgent2026 / TestAGI2026!")
    print("3. Go to game overview page")
    print("4. Open Developer Tools (F12)")
    print("5. Go to Application/Storage > Cookies")
    print("6. Copy the cookies and paste below")
    print()
    
    # Manual cookie input
    print("📋 Paste your session cookies (JSON format):")
    print("Example: [{'name': 'session', 'value': 'abc123', 'domain': '.ogame.gameforge.com'}]")
    
    try:
        cookies_input = input("Cookies JSON: ")
        cookies = json.loads(cookies_input)
        
        # Save session
        session_data = {
            'username': 'TestAgent2026',
            'url': 'https://s161-en.ogame.gameforge.com',
            'cookies': cookies
        }
        
        # Create data directory
        Path('data').mkdir(exist_ok=True)
        
        with open('data/session.json', 'w') as f:
            json.dump(session_data, f, indent=2)
            
        print("✅ Session saved to data/session.json")
        print("🔄 Restart the bot to use this session!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    extract_session()