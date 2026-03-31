#!/usr/bin/env python3
"""
OGame Manual Login Helper
Apre browser visibile per login manuale e salva session
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append('/app/src')

from automation.ogame_login import OGameLogin

async def manual_login():
    """Login assistito con browser visibile"""
    
    print("🎮 OGame Manual Login Helper")
    print("=" * 50)
    
    # Get credentials
    username = os.getenv('OGAME_USERNAME', 'TestAgent2026')
    password = os.getenv('OGAME_PASSWORD', 'TestAGI2026!')
    url = os.getenv('OGAME_UNIVERSE_URL', 'https://s161-en.ogame.gameforge.com')
    
    print(f"📋 Account: {username}")
    print(f"🌍 Server: {url}")
    print()
    
    # Initialize with visible browser
    login_manager = OGameLogin(
        username=username,
        password=password, 
        universe_url=url,
        session_file="data/session.json",
        headless=False  # 👁️ BROWSER VISIBILE
    )
    
    try:
        print("🚀 Opening browser...")
        await login_manager.initialize()
        
        print("🌐 Navigating to OGame...")
        await login_manager.page.goto(url)
        
        print()
        print("🎯 MANUAL LOGIN TIME!")
        print("=" * 30)
        print("1. Complete the login in the browser window")
        print("2. Handle any CAPTCHA/verification")  
        print("3. Navigate to the game overview page")
        print("4. Press ENTER here when ready...")
        
        input("⌨️  Press ENTER after successful login: ")
        
        # Check if logged in
        if await login_manager.is_logged_in():
            print("✅ Login detected! Saving session...")
            await login_manager.save_session()
            print("💾 Session saved to data/session.json")
            print()
            print("🎉 SUCCESS! Bot can now use saved session.")
            print("🔄 Restart the bot to use automatic login.")
            return True
        else:
            print("❌ Login not detected. Try again.")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    finally:
        print("🔒 Closing browser...")
        await login_manager.close()

if __name__ == "__main__":
    asyncio.run(manual_login())