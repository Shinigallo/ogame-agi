#!/usr/bin/env python3
"""
Simple OGame Monitor - Minimal bot for continuous monitoring
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
sys.path.append('/app/src')

from automation.ogame_login import OGameLogin

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SimpleOGameBot")

class SimpleOGameBot:
    """Simple OGame bot without AI - just monitoring and basic actions"""
    
    def __init__(self):
        self.username = os.getenv('OGAME_USERNAME')
        self.password = os.getenv('OGAME_PASSWORD') 
        self.universe_url = os.getenv('OGAME_UNIVERSE_URL')
        self.session_duration = int(os.getenv('SESSION_DURATION', '28800'))  # 8 hours
        self.check_interval = int(os.getenv('QUICK_CHECK_INTERVAL', '300'))   # 5 minutes
        
        self.login_manager = None
        self.start_time = None
        
    async def initialize(self):
        """Initialize the bot"""
        logger.info("🤖 Starting Simple OGame Monitor")
        logger.info(f"👤 Account: {self.username}")
        logger.info(f"🌍 Server: {self.universe_url}")
        logger.info(f"⏱️ Session duration: {self.session_duration/3600:.1f} hours")
        
        self.login_manager = OGameLogin(
            username=self.username,
            password=self.password,
            universe_url=self.universe_url,
            session_file="data/session.json",
            headless=True
        )
        
        self.start_time = datetime.now()
        
    async def establish_session(self):
        """Establish or restore game session"""
        logger.info("🔐 Establishing game session...")
        
        # Try to load existing session first
        if await self.login_manager.load_session():
            logger.info("✅ Session restored from file")
            return True
        else:
            logger.info("🔐 Performing fresh login...")
            success = await self.login_manager.login()
            if success:
                logger.info("✅ Fresh login successful") 
                return True
            else:
                logger.error("❌ Login failed")
                return False
                
    async def check_game_state(self):
        """Check current game state and resources"""
        try:
            if not await self.login_manager.is_logged_in():
                logger.warning("⚠️ Session expired, attempting reconnect...")
                return await self.establish_session()
                
            # Basic game state check
            page = self.login_manager.page
            current_url = page.url
            
            logger.info(f"📊 Monitoring active - URL: {current_url}")
            
            # Update state file
            state = {
                "last_login": self.start_time.isoformat() if self.start_time else None,
                "last_check": datetime.now().isoformat(),
                "pending_events": [],
                "session_active": True,
                "next_action_time": (datetime.now() + timedelta(seconds=self.check_interval)).isoformat()
            }
            
            with open('data/bot_state.json', 'w') as f:
                json.dump(state, f, indent=2)
                
            return True
            
        except Exception as e:
            logger.error(f"❌ Check failed: {e}")
            return False
            
    async def run(self):
        """Main bot loop"""
        try:
            await self.initialize()
            
            # Initial session establishment  
            if not await self.establish_session():
                logger.error("❌ Could not establish session - exiting")
                return
                
            logger.info(f"🚀 Bot active - checking every {self.check_interval}s")
            
            # Main monitoring loop
            while True:
                # Check if session duration exceeded
                if datetime.now() - self.start_time > timedelta(seconds=self.session_duration):
                    logger.info(f"⏱️ Session duration exceeded ({self.session_duration}s) - restarting")
                    break
                    
                # Perform game state check
                if not await self.check_game_state():
                    logger.warning("⚠️ Check failed - attempting session recovery...")
                    if not await self.establish_session():
                        logger.error("❌ Session recovery failed - exiting")
                        break
                        
                # Wait for next check
                logger.info(f"😴 Waiting {self.check_interval}s until next check...")
                await asyncio.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info("🛑 Bot stopped by user")
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}")
        finally:
            if self.login_manager:
                await self.login_manager.close()
                logger.info("🔒 Session closed")

async def main():
    """Entry point"""
    bot = SimpleOGameBot()
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())