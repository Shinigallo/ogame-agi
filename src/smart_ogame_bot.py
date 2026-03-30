"""
OGame Smart Bot - Event-Driven & Cron-Based
Minimizes token usage with intelligent scheduling
"""

import asyncio
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

from src.automation.ogame_login import OGameLogin
from src.automation.ogame_resources import OGameResources
from src.agents.gemini_brain import GeminiBrain


@dataclass
class GameEvent:
    """Game event that triggers bot action"""
    event_type: str  # building_complete, research_complete, fleet_return, resources_full
    trigger_time: datetime
    data: Dict
    processed: bool = False


@dataclass  
class BotState:
    """Persistent bot state"""
    last_login: Optional[str] = None
    last_check: Optional[str] = None
    pending_events: List[GameEvent] = None
    session_active: bool = False
    next_action_time: Optional[str] = None
    
    def __post_init__(self):
        if self.pending_events is None:
            self.pending_events = []


class SmartOGameBot:
    """Event-driven OGame bot with minimal token usage"""
    
    def __init__(self):
        self.config = self._load_config()
        self.login_manager = None
        self.page = None
        self.brain = GeminiBrain(api_key=os.getenv('GEMINI_API_KEY'))
        
        self.state = self._load_state()
        self.logger = self._setup_logging()
        
    def _load_config(self) -> Dict:
        """Load configuration"""
        return {
            'username': os.getenv('OGAME_USERNAME'),
            'password': os.getenv('OGAME_PASSWORD'), 
            'universe_url': os.getenv('OGAME_UNIVERSE_URL'),
            'gemini_key': os.getenv('GEMINI_API_KEY'),
            'strategy': os.getenv('STRATEGIC_MODE', 'balanced'),
            'check_interval': int(os.getenv('QUICK_CHECK_INTERVAL', 60)),  # Quick checks every 1min
            'ai_interval': int(os.getenv('AI_DECISION_INTERVAL', 1800)),    # AI decisions every 30min
            'max_session_time': int(os.getenv('MAX_SESSION_TIME', 3600))   # Max 1h sessions
        }
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/smart_bot.log')
            ]
        )
        return logging.getLogger('SmartOGameBot')
        
    def _load_state(self) -> BotState:
        """Load persistent state"""
        try:
            with open('data/bot_state.json', 'r') as f:
                data = json.load(f)
                return BotState(**data)
        except FileNotFoundError:
            return BotState()
            
    def _save_state(self):
        """Save persistent state"""
        os.makedirs('data', exist_ok=True)
        with open('data/bot_state.json', 'w') as f:
            json.dump(asdict(self.state), f, indent=2, default=str)
            
    async def quick_check(self) -> List[GameEvent]:
        """Quick check for game events (no AI, minimal tokens)"""
        events = []
        
        try:
            # Ensure logged in
            if not await self._ensure_session():
                return events
                
            # Parse page for time-based events
            events.extend(await self._check_building_timers())
            events.extend(await self._check_research_timers()) 
            events.extend(await self._check_fleet_timers())
            events.extend(await self._check_resource_alerts())
            
            # Update state
            self.state.last_check = datetime.now().isoformat()
            self._save_state()
            
            if events:
                self.logger.info(f"🔔 Found {len(events)} new events")
                
        except Exception as e:
            self.logger.error(f"❌ Quick check failed: {e}")
            
        return events
        
    async def _ensure_session(self) -> bool:
        """Ensure we have active game session"""
        try:
            # Check if session exists and is valid
            if self.login_manager and await self.login_manager.is_logged_in():
                return True
                
            self.logger.info("🔐 Establishing game session...")
            
            # Create new session
            self.login_manager = OGameLogin(
                username=self.config['username'],
                password=self.config['password'],
                universe_url=self.config['universe_url'],
                headless=True
            )
            
            success = await self.login_manager.login()
            if success:
                self.page = self.login_manager.page
                self.state.session_active = True
                self.state.last_login = datetime.now().isoformat()
                self.logger.info("✅ Session established")
                return True
            else:
                self.logger.error("❌ Login failed")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Session error: {e}")
            return False
            
    async def _check_building_timers(self) -> List[GameEvent]:
        """Check building completion timers"""
        events = []
        
        try:
            # Look for construction timers
            timer_selectors = [
                '#buildtime',
                '.construction_time',
                '[id*="timer"]',
                '.countdown'
            ]
            
            for selector in timer_selectors:
                elements = await self.page.locator(selector).all()
                for element in elements:
                    try:
                        timer_text = await element.inner_text()
                        if timer_text and self._is_timer_format(timer_text):
                            completion_time = self._parse_timer(timer_text)
                            
                            events.append(GameEvent(
                                event_type='building_complete',
                                trigger_time=completion_time,
                                data={'timer_text': timer_text, 'selector': selector}
                            ))
                    except:
                        continue
                        
        except Exception as e:
            self.logger.debug(f"Building timer check failed: {e}")
            
        return events
        
    async def _check_research_timers(self) -> List[GameEvent]:
        """Check research completion timers"""
        events = []
        
        try:
            # Navigate to research if not already there
            current_url = self.page.url
            if 'research' not in current_url:
                await self.page.click('a[href*="research"]', timeout=5000)
                await asyncio.sleep(2)
                
            # Similar timer parsing for research
            research_timer = await self.page.locator('#researchtime').first.inner_text()
            if research_timer and self._is_timer_format(research_timer):
                completion_time = self._parse_timer(research_timer)
                
                events.append(GameEvent(
                    event_type='research_complete',
                    trigger_time=completion_time,
                    data={'timer_text': research_timer}
                ))
                
        except Exception as e:
            self.logger.debug(f"Research timer check failed: {e}")
            
        return events
        
    async def _check_fleet_timers(self) -> List[GameEvent]:
        """Check fleet return timers"""
        events = []
        
        try:
            # Check fleet movements
            fleet_selectors = [
                '.fleetDetails',
                '.fleet_movement',
                '[id*="fleet"]'
            ]
            
            for selector in fleet_selectors:
                elements = await self.page.locator(selector).all()
                for element in elements:
                    try:
                        fleet_info = await element.inner_text()
                        # Parse fleet return times
                        if 'return' in fleet_info.lower():
                            # Extract return time
                            return_time = self._extract_fleet_return_time(fleet_info)
                            if return_time:
                                events.append(GameEvent(
                                    event_type='fleet_return',
                                    trigger_time=return_time,
                                    data={'fleet_info': fleet_info}
                                ))
                    except:
                        continue
                        
        except Exception as e:
            self.logger.debug(f"Fleet timer check failed: {e}")
            
        return events
        
    async def _check_resource_alerts(self) -> List[GameEvent]:
        """Check if resources need attention"""
        events = []
        
        try:
            resource_parser = OGameResources(self.page)
            resources = await resource_parser.get_resources()
            
            # Check resource thresholds
            thresholds = {
                'metal': int(os.getenv('METAL_THRESHOLD', 50000)),
                'crystal': int(os.getenv('CRYSTAL_THRESHOLD', 25000)),
                'deuterium': int(os.getenv('DEUTERIUM_THRESHOLD', 12500))
            }
            
            for resource, amount in resources.items():
                if resource in thresholds and amount >= thresholds[resource]:
                    events.append(GameEvent(
                        event_type='resources_full',
                        trigger_time=datetime.now(),
                        data={'resource': resource, 'amount': amount, 'threshold': thresholds[resource]}
                    ))
                    
        except Exception as e:
            self.logger.debug(f"Resource check failed: {e}")
            
        return events
        
    def _is_timer_format(self, text: str) -> bool:
        """Check if text contains timer format"""
        import re
        timer_patterns = [
            r'\d+h\s*\d+m\s*\d+s',  # 1h 23m 45s
            r'\d+:\d+:\d+',          # 1:23:45
            r'\d+d\s*\d+h',          # 1d 2h
        ]
        
        for pattern in timer_patterns:
            if re.search(pattern, text):
                return True
        return False
        
    def _parse_timer(self, timer_text: str) -> datetime:
        """Parse timer text to datetime"""
        import re
        
        now = datetime.now()
        
        # Parse different timer formats
        if 'h' in timer_text and 'm' in timer_text:
            # Format: "1h 23m 45s"
            hours = re.search(r'(\d+)h', timer_text)
            minutes = re.search(r'(\d+)m', timer_text)
            seconds = re.search(r'(\d+)s', timer_text)
            
            total_seconds = 0
            if hours: total_seconds += int(hours.group(1)) * 3600
            if minutes: total_seconds += int(minutes.group(1)) * 60
            if seconds: total_seconds += int(seconds.group(1))
            
            return now + timedelta(seconds=total_seconds)
            
        elif ':' in timer_text:
            # Format: "1:23:45"
            parts = timer_text.strip().split(':')
            if len(parts) == 3:
                hours, minutes, seconds = map(int, parts)
                total_seconds = hours * 3600 + minutes * 60 + seconds
                return now + timedelta(seconds=total_seconds)
                
        # Default: assume 5 minutes
        return now + timedelta(minutes=5)
        
    def _extract_fleet_return_time(self, fleet_info: str) -> Optional[datetime]:
        """Extract fleet return time from text"""
        import re
        
        # Look for time patterns in fleet info
        time_match = re.search(r'(\d{2}):(\d{2}):(\d{2})', fleet_info)
        if time_match:
            hour, minute, second = map(int, time_match.groups())
            
            # Assume return is today or tomorrow
            now = datetime.now()
            return_time = now.replace(hour=hour, minute=minute, second=second, microsecond=0)
            
            if return_time < now:
                return_time += timedelta(days=1)
                
            return return_time
            
        return None
        
    async def schedule_smart_actions(self, events: List[GameEvent]):
        """Schedule actions based on events using OpenClaw cron"""
        from tools import cron  # OpenClaw cron integration
        
        for event in events:
            if event.processed:
                continue
                
            # Calculate when to act (slightly before event completion)
            action_time = event.trigger_time - timedelta(minutes=2)
            
            if action_time <= datetime.now():
                # Act now
                await self.handle_immediate_event(event)
            else:
                # Schedule cron job
                await self.schedule_cron_action(event, action_time)
                
            event.processed = True
            
    async def handle_immediate_event(self, event: GameEvent):
        """Handle events that need immediate attention"""
        self.logger.info(f"⚡ Handling immediate event: {event.event_type}")
        
        if event.event_type == 'resources_full':
            # Quick resource spending decision (minimal AI)
            await self.quick_resource_action(event.data)
            
        elif event.event_type in ['building_complete', 'research_complete']:
            # Schedule AI decision for next steps
            await self.schedule_ai_decision("completion_followup", delay_minutes=1)
            
        elif event.event_type == 'fleet_return':
            # Check if fleetsave needed
            await self.check_fleetsave_needed()
            
    async def schedule_cron_action(self, event: GameEvent, action_time: datetime):
        """Schedule cron job for future event"""
        from tools import cron
        
        job_data = {
            "name": f"ogame_{event.event_type}_{int(action_time.timestamp())}",
            "schedule": {
                "kind": "at",
                "at": action_time.isoformat() + "Z"
            },
            "payload": {
                "kind": "systemEvent",
                "text": f"OGame event ready: {event.event_type} - {json.dumps(event.data)}"
            },
            "sessionTarget": "current"
        }
        
        try:
            result = await cron(action="add", job=job_data)
            self.logger.info(f"📅 Scheduled cron job for {event.event_type} at {action_time}")
        except Exception as e:
            self.logger.error(f"❌ Failed to schedule cron: {e}")
            
    async def schedule_ai_decision(self, reason: str, delay_minutes: int = 30):
        """Schedule AI decision with cron"""
        from tools import cron
        
        decision_time = datetime.now() + timedelta(minutes=delay_minutes)
        
        job_data = {
            "name": f"ogame_ai_decision_{int(decision_time.timestamp())}",
            "schedule": {
                "kind": "at", 
                "at": decision_time.isoformat() + "Z"
            },
            "payload": {
                "kind": "systemEvent",
                "text": f"OGame AI decision needed: {reason}"
            },
            "sessionTarget": "current"
        }
        
        try:
            await cron(action="add", job=job_data)
            self.logger.info(f"🧠 Scheduled AI decision in {delay_minutes} minutes (reason: {reason})")
        except Exception as e:
            self.logger.error(f"❌ Failed to schedule AI decision: {e}")
            
    async def quick_resource_action(self, resource_data: Dict):
        """Quick resource spending without AI (rule-based)"""
        resource = resource_data['resource']
        amount = resource_data['amount']
        
        self.logger.info(f"💰 Quick action for {resource}: {amount}")
        
        # Simple rule-based decisions (no AI tokens)
        if resource == 'metal' and amount > 50000:
            # Build metal mine or shipyard units
            await self._try_quick_build(['metal_mine', 'light_fighter'])
            
        elif resource == 'crystal' and amount > 25000:
            # Build crystal mine or research
            await self._try_quick_build(['crystal_mine', 'research_lab'])
            
        elif resource == 'deuterium' and amount > 12000:
            # Build deuterium or advanced ships
            await self._try_quick_build(['deuterium_synthesizer', 'heavy_fighter'])
            
    async def _try_quick_build(self, targets: List[str]):
        """Try to build from target list (first available)"""
        for target in targets:
            try:
                # Quick build attempt without full AI analysis
                success = await self._execute_quick_build(target)
                if success:
                    self.logger.info(f"✅ Quick build: {target}")
                    break
            except Exception as e:
                self.logger.debug(f"Quick build {target} failed: {e}")
                continue
                
    async def _execute_quick_build(self, target: str) -> bool:
        """Execute quick build action"""
        # Simplified build logic - just try to click build button
        try:
            # Navigate to appropriate page
            if target in ['metal_mine', 'crystal_mine', 'deuterium_synthesizer']:
                await self.page.click('a[href*="page=resources"]')
            elif target in ['light_fighter', 'heavy_fighter']:
                await self.page.click('a[href*="page=fleet"]')
            elif target == 'research_lab':
                await self.page.click('a[href*="page=station"]')
                
            await asyncio.sleep(2)
            
            # Try to find and click build button
            build_selectors = [
                f'#{target}',
                f'[data-building="{target}"]',
                f'[data-ship="{target}"]'
            ]
            
            for selector in build_selectors:
                try:
                    element = self.page.locator(selector).first
                    if await element.is_visible(timeout=2000):
                        await element.click()
                        await asyncio.sleep(1)
                        
                        # Click build button
                        build_btn = self.page.locator('button:has-text("Build")').first
                        if await build_btn.is_visible(timeout=2000):
                            await build_btn.click()
                            return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            self.logger.debug(f"Build execution failed: {e}")
            return False
            
    async def cleanup_session(self):
        """Cleanup session if running too long"""
        if not self.state.last_login:
            return
            
        session_start = datetime.fromisoformat(self.state.last_login)
        session_age = (datetime.now() - session_start).total_seconds()
        
        if session_age > self.config['max_session_time']:
            self.logger.info("🔒 Session timeout - cleaning up")
            
            # Ensure fleetsave before logout
            await self.check_fleetsave_needed()
            
            # Close session
            if self.login_manager:
                await self.login_manager.close()
                
            self.state.session_active = False
            self.state.last_login = None
            self._save_state()
            
    async def check_fleetsave_needed(self) -> bool:
        """Check if fleetsave is needed"""
        try:
            # Quick check for fleets
            await self.page.click('a[href*="page=fleet"]')
            await asyncio.sleep(2)
            
            # Look for ships
            ship_elements = await self.page.locator('[data-ship]').all()
            
            if ship_elements:
                # Has ships - schedule fleetsave
                await self.schedule_ai_decision("fleetsave_needed", delay_minutes=1)
                return True
                
            return False
            
        except Exception as e:
            self.logger.debug(f"Fleetsave check failed: {e}")
            return False
            
    async def run_smart_cycle(self):
        """Run one smart bot cycle"""
        try:
            # 1. Quick check for events (no AI, minimal cost)
            events = await self.quick_check()
            
            # 2. Schedule smart actions based on events
            if events:
                await self.schedule_smart_actions(events)
                
            # 3. Update pending events in state
            self.state.pending_events.extend(events)
            self._save_state()
            
            # 4. Cleanup old session if needed
            await self.cleanup_session()
            
        except Exception as e:
            self.logger.error(f"❌ Smart cycle failed: {e}")
            
    async def run(self):
        """Main bot loop - lightweight monitoring"""
        self.logger.info("🤖 Starting Smart OGame Bot (Event-Driven)")
        
        while True:
            try:
                await self.run_smart_cycle()
                
                # Short sleep between quick checks
                await asyncio.sleep(self.config['check_interval'])
                
            except KeyboardInterrupt:
                self.logger.info("⏹️ Bot stopped by user")
                break
            except Exception as e:
                self.logger.error(f"❌ Bot error: {e}")
                await asyncio.sleep(60)  # Wait before retry
                
        # Cleanup
        if self.login_manager:
            await self.login_manager.close()


async def main():
    """Entry point"""
    bot = SmartOGameBot()
    await bot.run()


if __name__ == '__main__':
    asyncio.run(main())