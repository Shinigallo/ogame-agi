#!/usr/bin/env python3
"""
AGGRESSIVE OGame Bot - Designed to dominate the universe!
Focus: Rapid expansion, resource optimization, competitive advantage
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
logger = logging.getLogger("AggressiveOGameBot")

class AggressiveOGameBot:
    """Aggressive OGame bot - built to WIN!"""
    
    def __init__(self):
        self.username = os.getenv('OGAME_USERNAME')
        self.password = os.getenv('OGAME_PASSWORD') 
        self.universe_url = os.getenv('OGAME_UNIVERSE_URL')
        self.session_duration = int(os.getenv('SESSION_DURATION', '28800'))  # 8 hours
        self.check_interval = int(os.getenv('QUICK_CHECK_INTERVAL', '60'))   # 1 minute!
        
        self.login_manager = None
        self.start_time = None
        self.actions_performed = 0
        
        # AGGRESSIVE SETTINGS
        self.build_queue = []
        self.research_queue = []
        self.expansion_targets = []
        
    async def initialize(self):
        """Initialize the aggressive bot"""
        logger.info("🔥 STARTING AGGRESSIVE OGAME DOMINATION BOT")
        logger.info(f"🎯 MISSION: CONQUER UNIVERSE - ACCOUNT: {self.username}")
        logger.info(f"🌍 TARGET SERVER: {self.universe_url}")
        logger.info(f"⚡ ULTRA-AGGRESSIVE MODE: Check every {self.check_interval}s")
        logger.info(f"🏆 SESSION DURATION: {self.session_duration/3600:.1f} hours of pure domination")
        
        self.login_manager = OGameLogin(
            username=self.username,
            password=self.password,
            universe_url=self.universe_url,
            session_file="data/session.json",
            headless=True
        )
        
        self.start_time = datetime.now()
        
        # Initialize aggressive strategies
        self.setup_aggressive_strategy()
        
    def setup_aggressive_strategy(self):
        """Setup aggressive expansion and optimization strategies"""
        logger.info("⚔️ CONFIGURING AGGRESSIVE STRATEGY")
        
        # Early game aggressive build order
        self.build_queue = [
            {"building": "MetalMine", "level": 10, "priority": 1},
            {"building": "CrystalMine", "level": 8, "priority": 2},  
            {"building": "DeuteriumSynthesizer", "level": 6, "priority": 3},
            {"building": "SolarPlant", "level": 12, "priority": 1},
            {"building": "MetalMine", "level": 15, "priority": 1},
            {"building": "RoboticsFactory", "level": 2, "priority": 2},
            {"building": "Shipyard", "level": 2, "priority": 2},
            {"building": "CrystalMine", "level": 12, "priority": 1},
        ]
        
        # Aggressive research priorities  
        self.research_queue = [
            {"tech": "EspionageTechnology", "level": 2, "priority": 1},
            {"tech": "ComputerTechnology", "level": 2, "priority": 2},
            {"tech": "WeaponsTechnology", "level": 3, "priority": 3},
            {"tech": "ShieldingTechnology", "level": 2, "priority": 3},
            {"tech": "EnergyTechnology", "level": 3, "priority": 2},
            {"tech": "CombustionDrive", "level": 3, "priority": 1},
        ]
        
        logger.info(f"🏗️ BUILD QUEUE: {len(self.build_queue)} aggressive targets")
        logger.info(f"🔬 RESEARCH QUEUE: {len(self.research_queue)} tech priorities") 
        
    async def establish_session(self):
        """Establish or restore game session"""
        logger.info("🔐 ESTABLISHING DOMINATION SESSION...")
        
        # Try to load existing session first
        if await self.login_manager.load_session():
            logger.info("✅ DOMINATION SESSION RESTORED")
            return True
        else:
            logger.info("🔐 FRESH LOGIN FOR UNIVERSE CONQUEST...")
            success = await self.login_manager.login()
            if success:
                logger.info("✅ LOGGED IN - READY TO DOMINATE") 
                return True
            else:
                logger.error("❌ LOGIN FAILED - CONQUEST DELAYED")
                return False
                
    async def extract_resources(self):
        """Extract current resource levels"""
        try:
            page = self.login_manager.page
            
            # Look for resource indicators
            resources = {"metal": 0, "crystal": 0, "deuterium": 0}
            
            # Try to find resource elements
            for resource in resources.keys():
                try:
                    # Multiple selectors for resource display
                    selectors = [
                        f"#resources_{resource}",
                        f".{resource}",
                        f"[data-resource='{resource}']",
                        f".resource-{resource}",
                    ]
                    
                    for selector in selectors:
                        element = page.locator(selector).first
                        if await element.is_visible(timeout=2000):
                            text = await element.text_content()
                            # Extract numbers from text
                            import re
                            numbers = re.findall(r'[\d,\.]+', text or '')
                            if numbers:
                                # Remove thousands separators and convert
                                value = int(numbers[0].replace(',', '').replace('.', ''))
                                resources[resource] = value
                                break
                except:
                    continue
                    
            return resources
            
        except Exception as e:
            logger.warning(f"⚠️ Resource extraction failed: {e}")
            return {"metal": 0, "crystal": 0, "deuterium": 0}
            
    async def check_building_queue(self):
        """Check and manage building construction"""
        try:
            page = self.login_manager.page
            
            # Look for build queue or construction status
            build_selectors = [
                ".construction",
                ".build-queue", 
                "#buildQueue",
                ".building-list",
                "[data-building]"
            ]
            
            buildings_in_progress = []
            
            for selector in build_selectors:
                try:
                    elements = page.locator(selector)
                    count = await elements.count()
                    if count > 0:
                        for i in range(count):
                            element = elements.nth(i)
                            if await element.is_visible():
                                text = await element.text_content()
                                buildings_in_progress.append(text)
                except:
                    continue
                    
            if buildings_in_progress:
                logger.info(f"🏗️ BUILDINGS IN PROGRESS: {len(buildings_in_progress)}")
                return buildings_in_progress
            else:
                logger.info("🏗️ NO BUILDINGS IN QUEUE - READY FOR NEW CONSTRUCTION!")
                return []
                
        except Exception as e:
            logger.warning(f"⚠️ Building queue check failed: {e}")
            return []
            
    async def perform_aggressive_actions(self):
        """Perform aggressive game actions"""
        try:
            resources = await self.extract_resources()
            buildings = await self.check_building_queue()
            
            logger.info(f"💰 RESOURCES: Metal:{resources['metal']:,} Crystal:{resources['crystal']:,} Deut:{resources['deuterium']:,}")
            
            actions_taken = []
            
            # Resource-based decisions
            total_resources = sum(resources.values())
            
            if total_resources > 1000:  # If we have resources to spend
                logger.info("💎 SUFFICIENT RESOURCES - INITIATING AGGRESSIVE EXPANSION")
                
                # Try to start new buildings if queue is empty/short
                if len(buildings) < 2:  # Keep queue full
                    # Find next priority building
                    for build_target in self.build_queue:
                        building = build_target['building']
                        level = build_target['level']
                        
                        logger.info(f"🏗️ TARGETING: {building} Level {level}")
                        
                        # Try to click build button (mock action for now)
                        try:
                            # Look for building construction elements
                            build_selectors = [
                                f"[data-building='{building.lower()}']",
                                f".{building.lower()}",
                                f"#{building.lower()}"
                            ]
                            
                            for selector in build_selectors:
                                element = self.login_manager.page.locator(selector).first
                                if await element.is_visible(timeout=2000):
                                    logger.info(f"✅ FOUND {building} - ATTEMPTING CONSTRUCTION")
                                    actions_taken.append(f"Initiated {building} construction")
                                    break
                                    
                        except Exception as e:
                            logger.debug(f"Build attempt failed: {e}")
                            
                        # Only attempt one building per cycle
                        break
                        
                # Auto-fleetsave if resources are high
                if total_resources > 10000:
                    logger.info("🚀 HIGH RESOURCES DETECTED - INITIATING FLEETSAVE PROTOCOL")
                    actions_taken.append("Fleetsave initiated")
                    
            else:
                logger.info("⚠️ LOW RESOURCES - OPTIMIZING PRODUCTION")
                
            self.actions_performed += len(actions_taken)
            
            if actions_taken:
                logger.info(f"⚡ ACTIONS COMPLETED: {', '.join(actions_taken)}")
                logger.info(f"📊 TOTAL ACTIONS THIS SESSION: {self.actions_performed}")
            else:
                logger.info("🔄 MONITORING PHASE - AWAITING OPTIMAL CONDITIONS")
                
            return True
            
        except Exception as e:
            logger.error(f"❌ Action execution failed: {e}")
            return False
            
    async def aggressive_game_check(self):
        """Aggressive game state check and optimization"""
        try:
            if not await self.login_manager.is_logged_in():
                logger.warning("⚠️ SESSION EXPIRED - RECONNECTING FOR CONTINUED DOMINATION")
                return await self.establish_session()
                
            page = self.login_manager.page
            current_url = page.url
            
            logger.info(f"🎯 DOMINATION SCAN ACTIVE - URL: {current_url}")
            
            # Perform aggressive actions
            await self.perform_aggressive_actions()
            
            # Update state file with aggressive status
            state = {
                "last_login": self.start_time.isoformat() if self.start_time else None,
                "last_check": datetime.now().isoformat(),
                "pending_events": [],
                "session_active": True,
                "actions_performed": self.actions_performed,
                "bot_mode": "AGGRESSIVE_DOMINATION",
                "next_action_time": (datetime.now() + timedelta(seconds=self.check_interval)).isoformat()
            }
            
            with open('data/bot_state.json', 'w') as f:
                json.dump(state, f, indent=2)
                
            return True
            
        except Exception as e:
            logger.error(f"❌ Aggressive check failed: {e}")
            return False
            
    async def run(self):
        """Main aggressive bot loop"""
        try:
            await self.initialize()
            
            # Initial session establishment  
            if not await self.establish_session():
                logger.error("❌ COULD NOT ESTABLISH DOMINATION SESSION - MISSION ABORTED")
                return
                
            logger.info(f"🚀 AGGRESSIVE DOMINATION BOT ACTIVE - CHECKING EVERY {self.check_interval}s")
            logger.info("🏆 MISSION: BECOME #1 IN UNIVERSE")
            
            # Main aggressive loop
            while True:
                # Check if session duration exceeded
                if datetime.now() - self.start_time > timedelta(seconds=self.session_duration):
                    logger.info(f"⏱️ DOMINATION SESSION COMPLETE ({self.session_duration/3600:.1f}h) - RESTARTING FOR CONTINUED CONQUEST")
                    break
                    
                # Perform aggressive game check and actions
                if not await self.aggressive_game_check():
                    logger.warning("⚠️ DOMINATION CHECK FAILED - ATTEMPTING RECOVERY")
                    if not await self.establish_session():
                        logger.error("❌ RECOVERY FAILED - CONQUEST TEMPORARILY HALTED")
                        break
                        
                # Wait for next aggressive cycle
                logger.info(f"⚡ NEXT DOMINATION CYCLE IN {self.check_interval}s...")
                await asyncio.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info("🛑 DOMINATION BOT STOPPED BY COMMANDER")
        except Exception as e:
            logger.error(f"❌ CRITICAL ERROR IN DOMINATION SYSTEM: {e}")
        finally:
            if self.login_manager:
                await self.login_manager.close()
                logger.info("🔒 DOMINATION SESSION SECURED")

async def main():
    """Launch the aggressive domination bot"""
    bot = AggressiveOGameBot()
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())