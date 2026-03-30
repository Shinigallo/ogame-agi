
import asyncio
from playwright.async_api import async_playwright
import time
import subprocess
import logging

class AutonomousBrowser:
    """Fully autonomous browser controller for OGame"""
    
    def __init__(self):
        self.username = "TestAgent2026"
        self.password = "TestAGI2026!"
        self.login_url = "https://lobby.ogame.gameforge.com"
        self.logged_in = False
        self.game_session = None
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('AutoBrowser')
        
    async def start_autonomous_session(self):
        """Start completely autonomous OGame session"""
        
        self.logger.info("🚀 Starting Autonomous Browser Session")
        
        async with async_playwright() as playwright:
            # Launch browser
            browser = await playwright.chromium.launch(
                headless=False,  # Keep visible for monitoring
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            
            page = await context.new_page()
            
            try:
                # Autonomous login
                await self.autonomous_login(page)
                
                # Autonomous gameplay loop
                await self.autonomous_gameplay_loop(page)
                
            except Exception as e:
                self.logger.error(f"❌ Autonomous session failed: {e}")
            finally:
                await browser.close()
                
    async def autonomous_login(self, page):
        """Completely autonomous login to OGame"""
        
        self.logger.info("🔐 Executing Autonomous Login...")
        
        # Navigate to OGame lobby
        await page.goto(self.login_url, wait_until='networkidle')
        await asyncio.sleep(3)
        
        # Handle login form
        try:
            # Fill username
            username_input = page.locator('input[type="email"], input[name="email"], input[placeholder*="mail"]').first
            await username_input.fill(self.username)
            await asyncio.sleep(1)
            
            # Fill password  
            password_input = page.locator('input[type="password"]').first
            await password_input.fill(self.password)
            await asyncio.sleep(1)
            
            # Submit login
            login_button = page.locator('button[type="submit"], input[type="submit"], button:has-text("Login")').first
            await login_button.click()
            
            # Wait for login completion
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(5)
            
            # Select universe (Scorpius)
            universe_links = page.locator('a:has-text("Scorpius"), a:has-text("s161")').first
            if await universe_links.count() > 0:
                await universe_links.click()
                await page.wait_for_load_state('networkidle')
                
            self.logged_in = True
            self.logger.info("✅ Autonomous login successful")
            
        except Exception as e:
            self.logger.error(f"❌ Login failed: {e}")
            raise
            
    async def autonomous_gameplay_loop(self, page):
        """Main autonomous gameplay decision loop"""
        
        self.logger.info("🎮 Starting Autonomous Gameplay Loop")
        
        cycle_count = 0
        
        while True:
            try:
                cycle_count += 1
                self.logger.info(f"🔄 Autonomous Cycle #{cycle_count}")
                
                # Analyze current game state
                game_state = await self.analyze_game_state(page)
                
                # Get AI strategic decision
                ai_decision = await self.get_ai_decision(game_state)
                
                # Execute autonomous action
                if ai_decision:
                    await self.execute_autonomous_action(page, ai_decision)
                    
                # Wait for next decision cycle
                self.logger.info(f"⏰ Waiting 5 minutes for next cycle...")
                await asyncio.sleep(300)  # 5 minutes
                
            except Exception as e:
                self.logger.error(f"❌ Gameplay cycle error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error
                
    async def analyze_game_state(self, page):
        """Autonomous game state analysis"""
        
        try:
            # Extract resources
            resources = {}
            
            # Look for resource elements (common OGame patterns)
            metal_elem = page.locator('#resources_metal, .resource_metal, [data-resource="metal"]').first
            crystal_elem = page.locator('#resources_crystal, .resource_crystal, [data-resource="crystal"]').first  
            deuterium_elem = page.locator('#resources_deuterium, .resource_deuterium, [data-resource="deuterium"]').first
            
            if await metal_elem.count() > 0:
                resources['metal'] = await metal_elem.inner_text()
            if await crystal_elem.count() > 0:
                resources['crystal'] = await crystal_elem.inner_text()
            if await deuterium_elem.count() > 0:
                resources['deuterium'] = await deuterium_elem.inner_text()
                
            self.logger.info(f"📊 Resources extracted: {resources}")
            
            return {
                'resources': resources,
                'timestamp': time.time(),
                'page_url': page.url
            }
            
        except Exception as e:
            self.logger.error(f"❌ Game state analysis failed: {e}")
            return None
            
    async def get_ai_decision(self, game_state):
        """Get AI strategic decision via Gemini"""
        
        try:
            # Use Gemini CLI for decision making
            prompt = f"""
            You are an autonomous OGame AGI. Current game state:
            Resources: {game_state.get('resources', {})}
            
            What should be the next autonomous action? Choose ONE:
            1. upgrade_metal_mine
            2. upgrade_crystal_mine  
            3. upgrade_solar_plant
            4. build_research_lab
            5. wait_for_resources
            
            Respond with just the action name, no explanation.
            """
            
            result = subprocess.run([
                'gemini', '-p', prompt.strip()
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                decision = result.stdout.strip().lower()
                self.logger.info(f"🧠 AI Decision: {decision}")
                return decision
            else:
                self.logger.warning("⚠️ AI decision failed, using default")
                return "upgrade_metal_mine"  # Default action
                
        except Exception as e:
            self.logger.error(f"❌ AI decision error: {e}")
            return "upgrade_metal_mine"
            
    async def execute_autonomous_action(self, page, action):
        """Execute autonomous game action"""
        
        self.logger.info(f"🎮 Executing autonomous action: {action}")
        
        try:
            if "upgrade_metal_mine" in action:
                await self.click_building_upgrade(page, "metal_mine")
            elif "upgrade_crystal_mine" in action:
                await self.click_building_upgrade(page, "crystal_mine")
            elif "upgrade_solar_plant" in action:
                await self.click_building_upgrade(page, "solar_plant")
            elif "build_research_lab" in action:
                await self.click_building_upgrade(page, "research_lab")
            elif "wait_for_resources" in action:
                self.logger.info("⏰ AI decided to wait for resources")
                return
                
            self.logger.info("✅ Autonomous action completed")
            
        except Exception as e:
            self.logger.error(f"❌ Action execution failed: {e}")
            
    async def click_building_upgrade(self, page, building_type):
        """Click building upgrade button"""
        
        try:
            # Navigate to buildings page if not there
            buildings_link = page.locator('a[href*="buildings"], a:has-text("Buildings")').first
            if await buildings_link.count() > 0:
                await buildings_link.click()
                await asyncio.sleep(2)
                
            # Look for building upgrade button
            upgrade_selectors = [
                f'a[href*="{building_type}"]',
                f'.{building_type} .upgrade',
                f'#{building_type}_upgrade',
                '.fastBuild', 
                'a:has-text("Upgrade")'
            ]
            
            for selector in upgrade_selectors:
                upgrade_btn = page.locator(selector).first
                if await upgrade_btn.count() > 0:
                    await upgrade_btn.click()
                    await asyncio.sleep(1)
                    self.logger.info(f"✅ Clicked {building_type} upgrade")
                    break
                    
        except Exception as e:
            self.logger.error(f"❌ Building upgrade click failed: {e}")


if __name__ == "__main__":
    browser = AutonomousBrowser()
    asyncio.run(browser.start_autonomous_session())
