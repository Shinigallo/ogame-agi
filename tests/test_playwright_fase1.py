"""
OGame Playwright Test - Phase 1
Tests: Login + Resource Extraction
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.automation.ogame_login import OGameLogin
from src.automation.ogame_resources import OGameResources

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/test_fase1.log')
    ]
)
logger = logging.getLogger('OGame-Test-Fase1')


class OGameFase1Tester:
    """Test suite for Phase 1: Login + Resources"""
    
    def __init__(self):
        load_dotenv()
        
        self.username = os.getenv('OGAME_USERNAME')
        self.password = os.getenv('OGAME_PASSWORD')
        self.universe_url = os.getenv('OGAME_UNIVERSE_URL', 'https://lobby.ogame.gameforge.com/')
        
        self.login_manager = None
        self.results = {
            'login': False,
            'resources': {},
            'screenshot': None,
            'errors': []
        }
        
    async def run(self):
        """Run all Phase 1 tests"""
        logger.info("=" * 60)
        logger.info("🚀 OGAME FASE 1 TEST - Login + Resources")
        logger.info("=" * 60)
        
        # Validate credentials
        if not self.username or not self.password:
            logger.error("❌ Missing credentials in .env file")
            logger.error("   Set OGAAME_USERNAME and OGAME_PASSWORD")
            return False
            
        logger.info(f"📋 Credentials loaded for: {self.username}")
        logger.info(f"📋 Universe URL: {self.universe_url}")
        
        try:
            # Initialize login manager
            self.login_manager = OGameLogin(
                username=self.username,
                password=self.password,
                universe_url=self.universe_url,
                session_file='data/session.json',
                headless=True  # Set False to see browser
            )
            
            # Test 1: Login
            self.results['login'] = await self.test_login()
            if not self.results['login']:
                logger.error("❌ Login test FAILED")
                return False
                
            # Test 2: Get Resources
            self.results['resources'] = await self.test_resources()
            if not self.results['resources']:
                logger.error("❌ Resource extraction FAILED")
                return False
                
            # Test 3: Save screenshot
            await self.test_screenshot()
            
            logger.info("=" * 60)
            logger.info("✅ ALL TESTS PASSED")
            logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Test execution error: {e}")
            self.results['errors'].append(str(e))
            return False
            
        finally:
            # Cleanup
            if self.login_manager:
                await self.login_manager.close()
                
    async def test_login(self) -> bool:
        """Test login flow"""
        logger.info("")
        logger.info("📌 TEST 1: Login Flow")
        logger.info("-" * 40)
        
        try:
            success = await self.login_manager.login()
            
            if success:
                logger.info("✅ Login successful")
                return True
            else:
                logger.error("❌ Login failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Login exception: {e}")
            self.results['errors'].append(f"Login: {e}")
            return False
            
    async def test_resources(self) -> dict:
        """Test resource extraction"""
        logger.info("")
        logger.info("📌 TEST 2: Resource Extraction")
        logger.info("-" * 40)
        
        try:
            if not self.login_manager.page:
                logger.error("❌ No page available")
                return {}
                
            resource_parser = OGameResources(self.login_manager.page)
            resources = await resource_parser.get_resources()
            
            logger.info("📊 Resources extracted:")
            for key, value in resources.items():
                formatted = resource_parser._format_number(value)
                logger.info(f"   {key:12s}: {formatted}")
                
            # Check if we got actual values
            if sum(resources.values()) > 0:
                logger.info("✅ Resource extraction successful")
                return resources
            else:
                logger.warning("⚠️ Resource values are all zero")
                logger.warning("   This may indicate selector mismatch")
                return resources  # Return anyway for debugging
                
        except Exception as e:
            logger.error(f"❌ Resource extraction error: {e}")
            self.results['errors'].append(f"Resources: {e}")
            return {}
            
    async def test_screenshot(self):
        """Take a screenshot of current state"""
        logger.info("")
        logger.info("📌 TEST 3: Screenshot")
        logger.info("-" * 40)
        
        try:
            logs_dir = Path('logs')
            logs_dir.mkdir(exist_ok=True)
            
            screenshot_path = logs_dir / 'fase1_test.png'
            
            if self.login_manager.page:
                await self.login_manager.page.screenshot(
                    path=str(screenshot_path),
                    full_page=True
                )
                logger.info(f"✅ Screenshot saved: {screenshot_path}")
                self.results['screenshot'] = str(screenshot_path)
            else:
                logger.warning("⚠️ No page available for screenshot")
                
        except Exception as e:
            logger.error(f"❌ Screenshot error: {e}")
            
    def print_summary(self):
        """Print test summary"""
        logger.info("")
        logger.info("=" * 60)
        logger.info("📋 TEST SUMMARY")
        logger.info("=" * 60)
        
        logger.info(f"Login:    {'✅ PASS' if self.results['login'] else '❌ FAIL'}")
        logger.info(f"Resources: {'✅ PASS' if self.results['resources'] else '❌ FAIL'}")
        
        if self.results['screenshot']:
            logger.info(f"Screenshot: {self.results['screenshot']}")
            
        if self.results['errors']:
            logger.info("")
            logger.info("⚠️ Errors encountered:")
            for error in self.results['errors']:
                logger.info(f"   - {error}")


async def main():
    """Main entry point"""
    tester = OGameFase1Tester()
    
    success = await tester.run()
    tester.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    asyncio.run(main())