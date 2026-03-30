"""
OGame Login Manager
Handles authentication and session management
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from dotenv import load_dotenv

from .ogame_selectors import LOGIN_SELECTORS, COOKIE_SELECTORS, UNIVERSE_SELECTORS

logger = logging.getLogger(__name__)


class OGameLogin:
    """Manages OGame login and session persistence"""
    
    def __init__(
        self,
        username: str,
        password: str,
        universe_url: str,
        session_file: str = "data/session.json",
        headless: bool = True
    ):
        self.username = username
        self.password = password
        self.universe_url = universe_url
        self.session_file = Path(session_file)
        self.headless = headless
        
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
    async def initialize(self):
        """Initialize Playwright browser"""
        logger.info("🚀 Initializing Playwright...")
        
        self.playwright = await async_playwright().start()
        
        # Launch browser
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
            ]
        )
        
        # Create context with stealth settings
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
        )
        
        self.page = await self.context.new_page()
        
        logger.info("✅ Playwright initialized")
        
    async def close(self):
        """Close browser and cleanup"""
        logger.info("🔒 Closing browser...")
        
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
            
        logger.info("✅ Browser closed")
        
    async def _handle_cookies(self):
        """Accept cookie consent if present"""
        for selector in COOKIE_SELECTORS:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible(timeout=2000):
                    await element.click()
                    logger.info(f"✅ Accepted cookies: {selector}")
                    await asyncio.sleep(1)
                    return True
            except:
                continue
        return False
        
    async def _fill_login_form(self) -> bool:
        """Fill the login form with credentials"""
        # Fill email
        email_filled = False
        for selector in LOGIN_SELECTORS['email']:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible(timeout=2000):
                    await element.fill(self.username)
                    logger.info(f"✅ Email filled: {selector}")
                    email_filled = True
                    break
            except:
                continue
                
        if not email_filled:
            logger.error("❌ Email field not found")
            return False
            
        await asyncio.sleep(0.5)
        
        # Fill password
        password_filled = False
        for selector in LOGIN_SELECTORS['password']:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible(timeout=2000):
                    await element.fill(self.password)
                    logger.info(f"✅ Password filled: {selector}")
                    password_filled = True
                    break
            except:
                continue
                
        if not password_filled:
            logger.error("❌ Password field not found")
            return False
            
        await asyncio.sleep(0.5)
        
        # Submit form
        submitted = False
        for selector in LOGIN_SELECTORS['submit']:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible(timeout=2000):
                    await element.click()
                    logger.info(f"✅ Form submitted: {selector}")
                    submitted = True
                    break
            except:
                continue
                
        if not submitted:
            logger.error("❌ Submit button not found")
            return False
            
        return True
        
    async def _select_universe(self) -> bool:
        """Select the game universe"""
        await asyncio.sleep(3)  # Wait for redirect
        
        for selector in UNIVERSE_SELECTORS:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible(timeout=5000):
                    await element.click()
                    logger.info(f"✅ Universe selected: {selector}")
                    await self.page.wait_for_load_state('networkidle', timeout=30000)
                    return True
            except:
                continue
                
        logger.warning("⚠️ Universe selector not found (may already be on game page)")
        return True  # Not a fatal error
        
    async def login(self) -> bool:
        """Perform full login sequence"""
        try:
            await self.initialize()
            
            logger.info("🔐 Starting login sequence...")
            logger.info(f"   Username: {self.username}")
            logger.info(f"   URL: {self.universe_url}")
            
            # Navigate to login page
            await self.page.goto(self.universe_url, wait_until='networkidle', timeout=60000)
            await asyncio.sleep(2)
            
            # Handle cookies
            await self._handle_cookies()
            
            # Check if already logged in
            if await self.is_logged_in():
                logger.info("✅ Already logged in")
                await self.save_session()
                return True
                
            # Fill login form
            if not await self._fill_login_form():
                return False
                
            # Wait for redirect
            await asyncio.sleep(5)
            
            # Select universe
            await self._select_universe()
            
            # Verify login
            if await self.is_logged_in():
                await self.save_session()
                logger.info("✅ Login successful")
                return True
            else:
                logger.error("❌ Login verification failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Login error: {e}")
            return False
            
    async def is_logged_in(self) -> bool:
        """Check if currently logged in"""
        try:
            # Look for game interface elements
            game_elements = [
                '#planetList',
                '#resources',
                '#navigation',
                '.planet-list',
                '[data-section="overview"]',
            ]
            
            for selector in game_elements:
                try:
                    element = self.page.locator(selector).first
                    if await element.is_visible(timeout=3000):
                        return True
                except:
                    continue
                    
            # Check URL
            current_url = self.page.url
            if 'ogame.gameforge.com' in current_url and 'login' not in current_url.lower():
                return True
                
            return False
            
        except Exception as e:
            logger.debug(f"Login check error: {e}")
            return False
            
    async def save_session(self):
        """Save session cookies to file"""
        try:
            self.session_file.parent.mkdir(parents=True, exist_ok=True)
            
            cookies = await self.context.cookies()
            
            session_data = {
                'username': self.username,
                'url': self.universe_url,
                'cookies': cookies
            }
            
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
                
            logger.info(f"✅ Session saved to {self.session_file}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save session: {e}")
            
    async def load_session(self) -> bool:
        """Load session from file"""
        try:
            if not self.session_file.exists():
                logger.info("No session file found")
                return False
                
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
                
            if session_data.get('username') != self.username:
                logger.warning("Session username mismatch")
                return False
                
            await self.initialize()
            
            # Navigate to game
            await self.page.goto(self.universe_url, wait_until='networkidle', timeout=60000)
            
            # Set cookies
            cookies = session_data.get('cookies', [])
            await self.context.add_cookies(cookies)
            
            # Reload page
            await self.page.reload()
            await asyncio.sleep(2)
            
            if await self.is_logged_in():
                logger.info("✅ Session loaded successfully")
                return True
            else:
                logger.warning("⚠️ Session may be expired")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to load session: {e}")
            return False
            
    async def logout(self):
        """Logout and cleanup"""
        try:
            # Clear cookies
            if self.context:
                await self.context.clear_cookies()
                
            # Delete session file
            if self.session_file.exists():
                self.session_file.unlink()
                logger.info("🗑️ Session file deleted")
                
            await self.close()
            logger.info("✅ Logged out")
            
        except Exception as e:
            logger.error(f"❌ Logout error: {e}")
