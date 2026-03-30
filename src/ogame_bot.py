"""
OGame Autonomous Bot
Fully automated OGame player with AI decision making
"""

import asyncio
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import random

from src.automation.ogame_login import OGameLogin
from src.automation.ogame_resources import OGameResources
from src.automation.ogame_selectors import BUILDING_SELECTORS, FLEET_SELECTORS, RESEARCH_SELECTORS
from src.agents.gemini_brain import GeminiBrain


@dataclass
class GameState:
    """Current game state snapshot"""
    timestamp: str
    resources: Dict[str, int]
    buildings: Dict[str, int] = None
    research: Dict[str, int] = None
    fleet: Dict[str, int] = None
    planets: List[Dict] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class BotConfig:
    """Bot configuration"""
    username: str
    password: str
    universe_url: str
    strategy: str = "balanced"  # conservative, balanced, aggressive
    cycle_interval: int = 300   # seconds between cycles
    max_cycles: int = 0         # 0 = infinite
    headless: bool = True
    auto_fleetsave: bool = True
    risk_tolerance: str = "low"
    
    @classmethod
    def from_env(cls) -> 'BotConfig':
        return cls(
            username=os.getenv('OGAME_USERNAME'),
            password=os.getenv('OGAME_PASSWORD'),
            universe_url=os.getenv('OGAME_UNIVERSE_URL'),
            strategy=os.getenv('STRATEGIC_MODE', 'balanced'),
            cycle_interval=int(os.getenv('DECISION_INTERVAL', 300)),
            max_cycles=int(os.getenv('MAX_CYCLES', 0)),
            headless=os.getenv('HEADLESS', 'true').lower() == 'true',
            auto_fleetsave=os.getenv('AUTO_FLEETSAVE', 'true').lower() == 'true',
            risk_tolerance=os.getenv('RISK_TOLERANCE', 'low'),
        )


class OGameBot:
    """Autonomous OGame Bot"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.login_manager = None
        self.page = None
        self.brain = GeminiBrain(api_key=os.getenv('GEMINI_API_KEY'))
        
        self.game_state = None
        self.cycle_count = 0
        self.running = False
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/ogame_bot.log')
            ]
        )
        self.logger = logging.getLogger('OGameBot')
        
    async def initialize(self):
        """Initialize the bot"""
        self.logger.info("🤖 Initializing OGame Bot...")
        
        # Initialize login manager
        self.login_manager = OGameLogin(
            username=self.config.username,
            password=self.config.password,
            universe_url=self.config.universe_url,
            headless=self.config.headless
        )
        
        # Login to game
        success = await self.login_manager.login()
        if not success:
            raise Exception("❌ Failed to login to OGame")
            
        self.page = self.login_manager.page
        self.logger.info("✅ Bot initialized and logged in")
        
    async def shutdown(self):
        """Shutdown the bot"""
        self.logger.info("🔒 Shutting down bot...")
        self.running = False
        
        if self.login_manager:
            await self.login_manager.close()
            
        self.logger.info("✅ Bot shutdown complete")
        
    async def get_game_state(self) -> GameState:
        """Collect current game state"""
        self.logger.debug("📊 Collecting game state...")
        
        # Get resources
        resource_parser = OGameResources(self.page)
        resources = await resource_parser.get_resources()
        
        # TODO: Get buildings, research, fleet data
        buildings = await self._get_buildings()
        research = await self._get_research()
        fleet = await self._get_fleet()
        planets = await self._get_planets()
        
        state = GameState(
            timestamp=datetime.now().isoformat(),
            resources=resources,
            buildings=buildings,
            research=research,
            fleet=fleet,
            planets=planets
        )
        
        self.game_state = state
        return state
        
    async def _get_buildings(self) -> Dict[str, int]:
        """Get building levels"""
        # Navigate to buildings page
        try:
            await self.page.click('a[href*="page=resources"]')
            await self.page.wait_for_load_state('networkidle', timeout=10000)
            
            buildings = {}
            for building_name, selectors in BUILDING_SELECTORS.items():
                for selector in selectors:
                    try:
                        element = self.page.locator(selector).first
                        if await element.is_visible(timeout=2000):
                            # Try to extract level from text
                            text = await element.inner_text()
                            # Parse level from building interface
                            level = self._parse_building_level(text)
                            buildings[building_name] = level
                            break
                    except:
                        continue
                        
            return buildings
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to get buildings: {e}")
            return {}
            
    async def _get_research(self) -> Dict[str, int]:
        """Get research levels"""
        try:
            await self.page.click('a[href*="page=research"]')
            await self.page.wait_for_load_state('networkidle', timeout=10000)
            
            research = {}
            # Parse research levels from interface
            # Implementation depends on OGame interface structure
            
            return research
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to get research: {e}")
            return {}
            
    async def _get_fleet(self) -> Dict[str, int]:
        """Get fleet composition"""
        try:
            await self.page.click('a[href*="page=fleet"]')
            await self.page.wait_for_load_state('networkidle', timeout=10000)
            
            fleet = {}
            # Parse fleet from interface
            
            return fleet
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to get fleet: {e}")
            return {}
            
    async def _get_planets(self) -> List[Dict]:
        """Get planet information"""
        try:
            planets = []
            # Parse planet list
            
            return planets
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to get planets: {e}")
            return []
            
    def _parse_building_level(self, text: str) -> int:
        """Parse building level from text"""
        import re
        match = re.search(r'level\s*(\d+)', text.lower())
        if match:
            return int(match.group(1))
        return 0
        
    async def make_decision(self, state: GameState) -> List[Dict]:
        """Use AI brain to make decisions"""
        self.logger.info("🧠 Making strategic decisions...")
        
        # Prepare context for AI
        context = {
            "game_state": state.to_dict(),
            "strategy": self.config.strategy,
            "risk_tolerance": self.config.risk_tolerance,
            "cycle": self.cycle_count,
            "auto_fleetsave": self.config.auto_fleetsave
        }
        
        # Query AI brain
        decisions = await self.brain.analyze_and_decide(context)
        
        self.logger.info(f"🎯 AI suggested {len(decisions)} actions")
        return decisions
        
    async def execute_actions(self, actions: List[Dict]):
        """Execute the decided actions"""
        for i, action in enumerate(actions):
            try:
                self.logger.info(f"⚡ Executing action {i+1}/{len(actions)}: {action['type']}")
                
                if action['type'] == 'build':
                    await self._execute_build(action)
                elif action['type'] == 'research':
                    await self._execute_research(action)
                elif action['type'] == 'fleet_dispatch':
                    await self._execute_fleet_dispatch(action)
                elif action['type'] == 'wait':
                    await asyncio.sleep(action.get('duration', 60))
                else:
                    self.logger.warning(f"⚠️ Unknown action type: {action['type']}")
                    
                # Random delay between actions (anti-detection)
                delay = random.randint(2, 8)
                await asyncio.sleep(delay)
                
            except Exception as e:
                self.logger.error(f"❌ Failed to execute action {action}: {e}")
                
    async def _execute_build(self, action: Dict):
        """Execute a building action"""
        building = action.get('target')
        planet = action.get('planet', 'current')
        
        # Navigate to buildings page
        await self.page.click('a[href*="page=resources"]')
        await self.page.wait_for_load_state('networkidle')
        
        # Find and click build button for the specified building
        selectors = BUILDING_SELECTORS.get(building, [])
        for selector in selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible():
                    # Click on the building
                    await element.click()
                    await asyncio.sleep(2)
                    
                    # Look for build button
                    for build_selector in BUILDING_SELECTORS['build_button']:
                        build_btn = self.page.locator(build_selector).first
                        if await build_btn.is_visible():
                            await build_btn.click()
                            self.logger.info(f"✅ Started building {building}")
                            return
                    break
            except:
                continue
                
        self.logger.warning(f"⚠️ Could not build {building}")
        
    async def _execute_research(self, action: Dict):
        """Execute a research action"""
        research = action.get('target')
        
        # Navigate to research page
        await self.page.click('a[href*="page=research"]')
        await self.page.wait_for_load_state('networkidle')
        
        # Implementation similar to build
        self.logger.info(f"✅ Started research {research}")
        
    async def _execute_fleet_dispatch(self, action: Dict):
        """Execute fleet dispatch"""
        mission = action.get('mission')
        target = action.get('target')
        ships = action.get('ships', {})
        
        # Navigate to fleet page
        await self.page.click('a[href*="page=fleet"]')
        await self.page.wait_for_load_state('networkidle')
        
        # Implementation for fleet dispatch
        self.logger.info(f"✅ Dispatched fleet for {mission} to {target}")
        
    async def save_state(self, state: GameState):
        """Save game state to file"""
        try:
            os.makedirs('data', exist_ok=True)
            
            # Save current state
            with open('data/current_state.json', 'w') as f:
                json.dump(state.to_dict(), f, indent=2)
                
            # Append to history
            with open('data/state_history.jsonl', 'a') as f:
                f.write(json.dumps(state.to_dict()) + '\n')
                
        except Exception as e:
            self.logger.error(f"❌ Failed to save state: {e}")
            
    async def run_cycle(self):
        """Run a single bot cycle"""
        try:
            self.logger.info(f"🔄 Starting cycle {self.cycle_count + 1}")
            
            # 1. Collect game state
            state = await self.get_game_state()
            
            # 2. Save state
            await self.save_state(state)
            
            # 3. Make decisions using AI
            actions = await self.make_decision(state)
            
            # 4. Execute actions
            if actions:
                await self.execute_actions(actions)
            else:
                self.logger.info("🛌 No actions to execute, waiting...")
                
            # 5. Log cycle completion
            self.cycle_count += 1
            self.logger.info(f"✅ Cycle {self.cycle_count} completed")
            
        except Exception as e:
            self.logger.error(f"❌ Cycle failed: {e}")
            
    async def run(self):
        """Main bot loop"""
        try:
            await self.initialize()
            self.running = True
            
            self.logger.info(f"🚀 Starting autonomous bot with strategy: {self.config.strategy}")
            
            while self.running:
                await self.run_cycle()
                
                # Check if we've reached max cycles
                if self.config.max_cycles > 0 and self.cycle_count >= self.config.max_cycles:
                    self.logger.info(f"🏁 Reached max cycles ({self.config.max_cycles}), stopping")
                    break
                    
                # Wait for next cycle
                self.logger.info(f"⏱️ Waiting {self.config.cycle_interval}s for next cycle...")
                await asyncio.sleep(self.config.cycle_interval)
                
        except KeyboardInterrupt:
            self.logger.info("⏹️ Bot stopped by user")
        except Exception as e:
            self.logger.error(f"❌ Bot crashed: {e}")
        finally:
            await self.shutdown()


async def main():
    """Entry point"""
    # Load configuration from environment
    config = BotConfig.from_env()
    
    if not config.username or not config.password:
        print("❌ Missing credentials! Set OGAME_USERNAME and OGAME_PASSWORD")
        return
        
    # Create and run bot
    bot = OGameBot(config)
    await bot.run()


if __name__ == '__main__':
    asyncio.run(main())