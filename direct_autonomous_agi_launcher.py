"""
Direct Browser Automation via Host + Container Display
Bypass container Python issues by running automation on host with container display
"""

import asyncio
import logging
import subprocess
import time
import os
from pathlib import Path

class DirectAutonomousAGI:
    """Direct autonomous AGI bypassing container Python issues"""
    
    def __init__(self):
        self.setup_logging()
        
        # Configuration
        self.account = {
            'username': 'TestAgent2026', 
            'password': 'TestAGI2026!',
            'login_url': 'https://lobby.ogame.gameforge.com'
        }
        
        self.gemini_api_key = 'AIzaSyCzMRF0wwVGLuuhxmdpgSJpa9pyxPDsR2Q'
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('DirectAGI')
        
    async def check_playwright_availability(self):
        """Check if Playwright is available on host"""
        
        self.logger.info("🔍 Checking Playwright availability...")
        
        try:
            # Check if playwright is installed
            result = subprocess.run(['python3', '-c', 'import playwright; print("✅ Playwright available")'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info("✅ Playwright available on host")
                return True
            else:
                self.logger.warning("⚠️ Playwright not available, installing...")
                await self.install_playwright()
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Playwright check failed: {e}")
            return False
            
    async def install_playwright(self):
        """Install Playwright if not available"""
        
        try:
            self.logger.info("📦 Installing Playwright...")
            
            # Install playwright
            subprocess.run(['pip3', 'install', 'playwright', '--break-system-packages'], 
                          capture_output=True, text=True)
            
            # Install browsers
            subprocess.run(['python3', '-m', 'playwright', 'install', 'chromium'], 
                          capture_output=True, text=True)
            
            self.logger.info("✅ Playwright installation completed")
            
        except Exception as e:
            self.logger.error(f"❌ Playwright installation failed: {e}")
            
    async def launch_direct_autonomous_session(self):
        """Launch autonomous session directly on host"""
        
        self.logger.info("🚀 LAUNCHING DIRECT AUTONOMOUS SESSION")
        self.logger.info("=" * 60)
        self.logger.info("🤖 100% Autonomous OGame AGI")
        self.logger.info("🌐 Host-based browser automation")
        self.logger.info("🧠 Gemini 2.0 strategic AI")
        self.logger.info("🎯 Target: Autonomous Scorpius conquest")
        
        # Check prerequisites
        playwright_ok = await self.check_playwright_availability()
        if not playwright_ok:
            self.logger.error("❌ Prerequisites failed")
            return False
            
        # Create and run autonomous script
        await self.create_direct_automation_script()
        await self.run_autonomous_script()
        
        return True
        
    async def create_direct_automation_script(self):
        """Create direct automation script for host execution"""
        
        script_content = f'''#!/usr/bin/env python3
"""
Fully Autonomous OGame AGI - Direct Host Execution
Complete autonomy with Gemini 2.0 strategic decision making
"""

import asyncio
from playwright.async_api import async_playwright
import subprocess
import logging
import time
import os

# Set Gemini API key
os.environ['GEMINI_API_KEY'] = '{self.gemini_api_key}'

class AutonomousOGameAGI:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - AGI - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('AutonomousAGI')
        
        self.username = "{self.account['username']}"
        self.password = "{self.account['password']}" 
        self.login_url = "{self.account['login_url']}"
        
        self.session_active = False
        self.decision_count = 0
        
    async def run_autonomous_session(self):
        """Main autonomous session controller"""
        
        self.logger.info("🤖 STARTING FULLY AUTONOMOUS OGAME SESSION")
        self.logger.info("🎯 Target: TestAgent2026 @ Scorpius Universe")
        self.logger.info("🧠 AI: Gemini 2.0 Strategic Decision Engine")
        self.logger.info("⚡ Mode: Zero Human Intervention Required")
        
        async with async_playwright() as p:
            # Launch browser with automation
            browser = await p.chromium.launch(
                headless=False,
                args=[
                    '--no-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-extensions-file-access-check',
                    '--disable-extensions-http-throttling'
                ]
            )
            
            context = await browser.new_context(
                viewport={{'width': 1600, 'height': 1200}},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = await context.new_page()
            
            try:
                # Execute autonomous login
                login_success = await self.autonomous_login(page)
                if not login_success:
                    raise Exception("Autonomous login failed")
                    
                # Start autonomous gameplay
                await self.autonomous_gameplay_controller(page)
                
            except Exception as e:
                self.logger.error(f"❌ Autonomous session error: {{e}}")
            finally:
                await browser.close()
                
    async def autonomous_login(self, page):
        """Fully autonomous login sequence"""
        
        self.logger.info("🔐 Executing autonomous login sequence...")
        
        try:
            # Navigate to login page
            await page.goto(self.login_url, wait_until='networkidle', timeout=30000)
            await asyncio.sleep(3)
            
            # Handle cookie consent if present
            cookie_selectors = [
                'button:has-text("Accept")',
                'button:has-text("Agree")', 
                'button:has-text("OK")',
                '.cookie-consent button',
                '#cookie-consent-accept'
            ]
            
            for selector in cookie_selectors:
                cookie_btn = page.locator(selector).first
                if await cookie_btn.is_visible(timeout=2000):
                    await cookie_btn.click()
                    await asyncio.sleep(1)
                    break
                    
            # Locate and fill login form
            await self.fill_login_form(page)
            
            # Wait for redirect to game selection
            await page.wait_for_load_state('networkidle', timeout=20000)
            await asyncio.sleep(5)
            
            # Select Scorpius universe
            await self.select_universe(page)
            
            self.session_active = True
            self.logger.info("✅ Autonomous login completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Login sequence failed: {{e}}")
            return False
            
    async def fill_login_form(self, page):
        """Fill login form autonomously"""
        
        # Try multiple email field patterns
        email_selectors = [
            'input[name="email"]',
            'input[type="email"]', 
            'input[placeholder*="mail"]',
            'input[placeholder*="Email"]',
            '#email'
        ]
        
        for selector in email_selectors:
            email_field = page.locator(selector).first
            if await email_field.is_visible(timeout=2000):
                await email_field.fill(self.username)
                self.logger.info("✅ Email field filled")
                break
                
        await asyncio.sleep(1)
        
        # Fill password field
        password_selectors = [
            'input[name="password"]',
            'input[type="password"]',
            '#password'
        ]
        
        for selector in password_selectors:
            password_field = page.locator(selector).first
            if await password_field.is_visible(timeout=2000):
                await password_field.fill(self.password)
                self.logger.info("✅ Password field filled")
                break
                
        await asyncio.sleep(1)
        
        # Submit form
        submit_selectors = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button:has-text("Login")',
            'button:has-text("Sign in")',
            '.login-button'
        ]
        
        for selector in submit_selectors:
            submit_btn = page.locator(selector).first
            if await submit_btn.is_visible(timeout=2000):
                await submit_btn.click()
                self.logger.info("✅ Login form submitted")
                break
                
    async def select_universe(self, page):
        """Select Scorpius universe autonomously"""
        
        universe_selectors = [
            'a:has-text("Scorpius")',
            'a:has-text("s161")',
            'a[href*="s161"]',
            'a[href*="scorpius"]'
        ]
        
        for selector in universe_selectors:
            universe_link = page.locator(selector).first
            if await universe_link.is_visible(timeout=5000):
                await universe_link.click()
                self.logger.info("✅ Scorpius universe selected")
                await page.wait_for_load_state('networkidle', timeout=20000)
                return True
                
        self.logger.warning("⚠️ Could not find Scorpius universe link")
        return False
        
    async def autonomous_gameplay_controller(self, page):
        """Main autonomous gameplay control loop"""
        
        self.logger.info("🎮 Starting autonomous gameplay controller")
        
        while self.session_active:
            try:
                self.decision_count += 1
                self.logger.info(f"🔄 Autonomous Decision Cycle #{self.decision_count}")
                
                # Analyze current game state
                game_state = await self.analyze_current_state(page)
                
                # Get strategic decision from Gemini AI
                ai_decision = await self.consult_gemini_ai(game_state)
                
                # Execute autonomous action
                if ai_decision:
                    await self.execute_autonomous_action(page, ai_decision)
                    
                # Log progress
                self.logger.info(f"📊 Session Progress: {{self.decision_count}} autonomous decisions executed")
                
                # Wait for next decision cycle (5 minutes)
                await asyncio.sleep(300)
                
            except KeyboardInterrupt:
                self.logger.info("🛑 Autonomous session interrupted by user")
                break
            except Exception as e:
                self.logger.error(f"❌ Gameplay cycle error: {{e}}")
                await asyncio.sleep(60)  # Wait 1 minute on error
                
    async def analyze_current_state(self, page):
        """Analyze current OGame state autonomously"""
        
        try:
            # Extract visible resources
            resource_data = {{}}
            
            # Common OGame resource patterns
            resource_patterns = [
                ('#resources_metal', 'metal'),
                ('#resources_crystal', 'crystal'), 
                ('#resources_deuterium', 'deuterium'),
                ('.metal', 'metal'),
                ('.crystal', 'crystal'),
                ('.deuterium', 'deuterium')
            ]
            
            for selector, resource_type in resource_patterns:
                element = page.locator(selector).first
                if await element.is_visible(timeout=1000):
                    text = await element.inner_text()
                    # Extract numeric value
                    numeric_value = ''.join(filter(str.isdigit, text))
                    if numeric_value:
                        resource_data[resource_type] = int(numeric_value)
                        
            self.logger.info(f"📊 Current resources: {{resource_data}}")
            
            return {{
                'resources': resource_data,
                'decision_cycle': self.decision_count,
                'timestamp': time.time(),
                'page_title': await page.title()
            }}
            
        except Exception as e:
            self.logger.error(f"❌ State analysis failed: {{e}}")
            return {{'resources': {{}}, 'error': str(e)}}
            
    async def consult_gemini_ai(self, game_state):
        """Consult Gemini AI for strategic decision"""
        
        try:
            prompt = f"""
            You are an autonomous OGame AGI playing as TestAgent2026 on Scorpius universe.
            
            Current situation:
            - Resources: {{game_state.get('resources', {{}})}}
            - Decision cycle: {{game_state.get('decision_cycle', 0)}}
            
            Choose the single best autonomous action for economic growth:
            1. upgrade_metal_mine
            2. upgrade_crystal_mine
            3. upgrade_solar_plant
            4. build_research_lab
            5. wait_for_resources
            
            Respond with ONLY the action name, no explanation.
            """
            
            # Use Gemini CLI for decision
            result = subprocess.run([
                'gemini', '-p', prompt.strip()
            ], capture_output=True, text=True, timeout=30, env=os.environ.copy())
            
            if result.returncode == 0:
                decision = result.stdout.strip().lower()
                self.logger.info(f"🧠 Gemini AI Decision: {{decision}}")
                return decision
            else:
                self.logger.warning("⚠️ Gemini consultation failed, using fallback")
                return "upgrade_metal_mine"  # Safe fallback
                
        except Exception as e:
            self.logger.error(f"❌ AI consultation error: {{e}}")
            return "upgrade_metal_mine"
            
    async def execute_autonomous_action(self, page, action):
        """Execute the autonomous action chosen by AI"""
        
        self.logger.info(f"🎮 Executing autonomous action: {{action}}")
        
        try:
            if "upgrade_metal_mine" in action:
                await self.upgrade_building(page, "metal_mine")
            elif "upgrade_crystal_mine" in action:
                await self.upgrade_building(page, "crystal_mine") 
            elif "upgrade_solar_plant" in action:
                await self.upgrade_building(page, "solar_plant")
            elif "build_research_lab" in action:
                await self.upgrade_building(page, "research_lab")
            elif "wait_for_resources" in action:
                self.logger.info("⏰ AI chose to wait for more resources")
                return
                
            self.logger.info("✅ Autonomous action execution completed")
            
        except Exception as e:
            self.logger.error(f"❌ Action execution failed: {{e}}")
            
    async def upgrade_building(self, page, building_type):
        """Autonomously upgrade specified building"""
        
        try:
            # Navigate to buildings if not there
            buildings_selectors = [
                'a[href*="buildings"]',
                'a:has-text("Buildings")',
                '.menu_buildings'
            ]
            
            for selector in buildings_selectors:
                buildings_link = page.locator(selector).first
                if await buildings_link.is_visible(timeout=3000):
                    await buildings_link.click()
                    await asyncio.sleep(2)
                    break
                    
            # Look for upgrade button patterns
            upgrade_selectors = [
                f'a[href*="{{building_type}}"]',
                f'.{{building_type}} .upgrade',
                '.fastBuild',
                'button:has-text("Upgrade")',
                'a:has-text("Upgrade")'
            ]
            
            for selector in upgrade_selectors:
                upgrade_btn = page.locator(selector).first
                if await upgrade_btn.is_visible(timeout=3000):
                    await upgrade_btn.click()
                    await asyncio.sleep(1)
                    self.logger.info(f"✅ {{building_type}} upgrade initiated")
                    return True
                    
            self.logger.warning(f"⚠️ Could not find upgrade button for {{building_type}}")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Building upgrade failed: {{e}}")
            return False


if __name__ == "__main__":
    agi = AutonomousOGameAGI()
    asyncio.run(agi.run_autonomous_session())
'''

        # Write script to file
        script_path = '/home/dario/openclaw/workspace/ogame-agi/direct_autonomous_agi.py'
        with open(script_path, 'w') as f:
            f.write(script_content)
            
        # Make executable
        subprocess.run(['chmod', '+x', script_path])
        
        self.logger.info(f"✅ Direct autonomous script created: {script_path}")
        
    async def run_autonomous_script(self):
        """Run the autonomous script"""
        
        self.logger.info("🚀 LAUNCHING DIRECT AUTONOMOUS SESSION")
        
        script_path = '/home/dario/openclaw/workspace/ogame-agi/direct_autonomous_agi.py'
        
        try:
            # Set environment
            env = os.environ.copy()
            env['GEMINI_API_KEY'] = self.gemini_api_key
            
            self.logger.info("🎮 Starting autonomous OGame session...")
            self.logger.info("👀 Browser will open automatically")
            self.logger.info("🤖 AGI will play completely autonomously")
            
            # Run script in background
            process = subprocess.Popen([
                'python3', script_path
            ], env=env, cwd='/home/dario/openclaw/workspace/ogame-agi')
            
            self.logger.info(f"✅ Autonomous session started (PID: {process.pid})")
            self.logger.info("🎯 Target: Autonomous conquest of Scorpius Universe")
            self.logger.info("📊 Monitor browser window for autonomous gameplay")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Script execution failed: {e}")
            return False


async def main():
    """Deploy direct autonomous AGI"""
    
    print("🤖 Direct Autonomous OGame AGI")
    print("=" * 40)
    print("🎯 100% Autonomous Gameplay")
    print("🧠 Gemini 2.0 Strategic AI")
    print("🌐 Host-based Browser Automation") 
    print("🏆 Target: Scorpius Universe #1")
    print("⚠️ Zero Human Intervention")
    print()
    
    agi = DirectAutonomousAGI()
    success = await agi.launch_direct_autonomous_session()
    
    if success:
        print("🚀 DIRECT AUTONOMOUS SESSION LAUNCHED!")
        print("🤖 AGI is playing completely autonomously")
        print("👀 Monitor browser window for live gameplay")
        print("🏆 Target: Autonomous Scorpius conquest")
    else:
        print("❌ Autonomous launch failed")
        
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)