"""
OGame Resource Parser
Extracts resources from game interface
"""

import asyncio
import logging
import re
from typing import Dict, Optional
from playwright.async_api import Page

from .ogame_selectors import RESOURCE_SELECTORS_OLD, RESOURCE_SELECTORS_NEW

logger = logging.getLogger(__name__)


class OGameResources:
    """Parses resource values from OGame interface"""
    
    def __init__(self, page: Page):
        self.page = page
        
    def _parse_number(self, text: str) -> int:
        """Parse OGame formatted number to int"""
        if not text:
            return 0
            
        # Remove any non-numeric chars except . , and -
        text = text.strip()
        
        # Handle negative numbers
        negative = '-' in text
        text = text.replace('-', '')
        
        # Remove thousands separators (OGame uses . or ,)
        # Pattern: 1.234.567 or 1,234,567
        text = re.sub(r'[.,]', '', text)
        
        # Also handle spaces
        text = text.replace(' ', '')
        
        # Extract just the digits
        digits = re.sub(r'[^\d]', '', text)
        
        try:
            value = int(digits) if digits else 0
            return -value if negative else value
        except ValueError:
            return 0
            
    async def _get_element_text(self, selectors: list) -> Optional[str]:
        """Try multiple selectors and return first successful text"""
        for selector in selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible(timeout=2000):
                    text = await element.inner_text()
                    if text:
                        return text.strip()
            except:
                continue
        return None
            
    async def _get_value_from_element(self, selectors: list) -> Optional[str]:
        """Get value from element (text, data-attr, or aria-label)"""
        for selector in selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible(timeout=2000):
                    # Try data attribute first
                    value = await element.get_attribute('data-value')
                    if value:
                        return value
                    
                    # Try aria-label
                    value = await element.get_attribute('aria-label')
                    if value:
                        return value
                    
                    # Try title
                    value = await element.get_attribute('title')
                    if value:
                        return value
                    
                    # Fall back to text
                    text = await element.inner_text()
                    if text:
                        return text.strip()
            except:
                continue
        return None
        
    async def get_resources(self) -> Dict[str, int]:
        """
        Extract all resources from the game interface.
        
        Returns:
            Dict with keys: metal, crystal, deuterium, energy, dark_matter
        """
        resources = {
            'metal': 0,
            'crystal': 0,
            'deuterium': 0,
            'energy': 0,
            'dark_matter': 0,
        }
        
        try:
            # Try NEW selectors first (OGame 8.x, 9.x, 10.x)
            for resource_key in ['metal', 'crystal', 'deuterium', 'energy', 'dark_matter']:
                selectors = RESOURCE_SELECTORS_NEW.get(resource_key, [])
                value = await self._get_value_from_element(selectors)
                if value:
                    resources[resource_key] = self._parse_number(value)
                    logger.debug(f"✅ {resource_key}: {resources[resource_key]}")
                    
            # If no new selectors worked, try OLD ones
            if all(v == 0 for v in [resources['metal'], resources['crystal'], resources['deuterium']]):
                logger.debug("Trying old selectors...")
                for resource_key in ['metal', 'crystal', 'deuterium', 'energy', 'dark_matter']:
                    selectors = RESOURCE_SELECTORS_OLD.get(resource_key, [])
                    value = await self._get_element_text(selectors)
                    if value:
                        resources[resource_key] = self._parse_number(value)
                        logger.debug(f"✅ {resource_key} (old): {resources[resource_key]}")
                        
            # Try alternative methods for dark matter
            if resources['dark_matter'] == 0:
                darkmatter_selectors = [
                    '#darkmatter',
                    '.darkmatter_value',
                    '[class*="darkmatter"]',
                    'span:has-text("Dark matter")',
                ]
                for selector in darkmatter_selectors:
                    try:
                        element = self.page.locator(selector).first
                        if await element.is_visible(timeout=1000):
                            text = await element.inner_text()
                            if text and 'dark' in text.lower():
                                # Extract number from text
                                match = re.search(r'[\d.,]+', text)
                                if match:
                                    resources['dark_matter'] = self._parse_number(match.group())
                                    break
                    except:
                        continue
                        
        except Exception as e:
            logger.error(f"❌ Error parsing resources: {e}")
            
        return resources
        
    async def get_resources_detailed(self) -> Dict:
        """
        Get resources with additional metadata.
        
        Returns:
            Extended dict with values, formatted strings, and storage info
        """
        basic = await self.get_resources()
        
        detailed = {
            **basic,
            'raw_values': basic,
            'formatted': {
                'metal': self._format_number(basic['metal']),
                'crystal': self._format_number(basic['crystal']),
                'deuterium': self._format_number(basic['deuterium']),
                'energy': self._format_number(basic['energy']),
                'dark_matter': self._format_number(basic['dark_matter']),
            },
            'timestamp': asyncio.get_event_loop().time(),
        }
        
        return detailed
        
    def _format_number(self, value: int) -> str:
        """Format number for display (e.g., 1.234.567)"""
        if value >= 1_000_000:
            return f"{value:,}".replace(',', '.')
        elif value >= 1000:
            return f"{value:,}".replace(',', '.')
        return str(value)
        
    async def wait_for_resources_update(self, timeout: int = 10000):
        """Wait for resources to change (useful after building/upgrading)"""
        current = await self.get_resources()
        metal_before = current['metal']
        
        import time
        start = time.time()
        
        while time.time() - start < timeout / 1000:
            await asyncio.sleep(2)
            new = await self.get_resources()
            if new['metal'] != metal_before:
                logger.info("✅ Resources updated")
                return new
                
        logger.warning("⚠️ Resource update timeout")
        return current