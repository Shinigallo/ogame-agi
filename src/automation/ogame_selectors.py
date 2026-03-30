"""
OGame Web Selectors
CSS and XPath selectors for OGame gameforge
"""

# Login page selectors
LOGIN_SELECTORS = {
    # Email/username field - multiple patterns
    'email': [
        'input[name="email"]',
        'input[type="email"]',
        'input[placeholder*="mail" i]',
        'input[placeholder*="email" i]',
        '#email',
        'input[id="email"]',
    ],
    
    # Password field
    'password': [
        'input[name="password"]',
        'input[type="password"]',
        '#password',
        'input[id="password"]',
    ],
    
    # Submit/Login button
    'submit': [
        'button[type="submit"]',
        'input[type="submit"]',
        'button:has-text("Login")',
        'button:has-text("Sign in")',
        'button:has-text("Log in")',
        '.login-button',
        '#loginSubmit',
    ],
}

# Cookie consent selectors
COOKIE_SELECTORS = [
    'button:has-text("Accept")',
    'button:has-text("Agree")',
    'button:has-text("OK")',
    'button:has-text("I accept")',
    '.cookie-consent button',
    '#cookie-consent-accept',
    '[data-testid="cookie-accept"]',
    '.cc-btn.cc-accept',
]

# Universe selection selectors
UNIVERSE_SELECTORS = [
    'a:has-text("Scorpius")',
    'a:has-text("s161")',
    'a[href*="s161"]',
    'a[href*="scorpius"]',
    '[data-universe="161"]',
    '.universe-item:has-text("Scorpius")',
]

# Resource bar selectors - OLD OGame (6.x, 7.x)
RESOURCE_SELECTORS_OLD = {
    'metal': [
        '#metal_box',
        '#resources_metal',
        'span[id*="metal"]',
        'div[id="metal_box"]',
    ],
    'crystal': [
        '#crystal_box',
        '#resources_crystal',
        'span[id*="crystal"]',
        'div[id="crystal_box"]',
    ],
    'deuterium': [
        '#deuterium_box',
        '#resources_deuterium',
        'span[id*="deuterium"]',
        'div[id="deuterium_box"]',
    ],
    'energy': [
        '#energy_box',
        '#resources_energy',
        'span[id*="energy"]',
        'div[id="energy_box"]',
    ],
    'dark_matter': [
        '#darkmatter_box',
        '#resources_darkmatter',
        '#dm_amount',
        'span[id*="dark"]',
    ],
}

# Resource bar selectors - NEW OGame (8.x, 9.x, 10.x)
RESOURCE_SELECTORS_NEW = {
    'metal': [
        'div[data-resource="metal"]',
        'span[data-value="metal"]',
        '.resource-0',
        '#metal',
        'li[data-resource="metal"]',
    ],
    'crystal': [
        'div[data-resource="crystal"]',
        'span[data-value="crystal"]',
        '.resource-1',
        '#crystal',
        'li[data-resource="crystal"]',
    ],
    'deuterium': [
        'div[data-resource="deuterium"]',
        'span[data-value="deuterium"]',
        '.resource-2',
        '#deuterium',
        'li[data-resource="deuterium"]',
    ],
    'energy': [
        'div[data-resource="energy"]',
        'span[data-value="energy"]',
        '.resource-3',
        '#energy',
        'li[data-resource="energy"]',
    ],
    'dark_matter': [
        'div[data-resource="darkmatter"]',
        '#darkmatter',
        '.darkmatter',
        'li[data-resource="darkmatter"]',
    ],
}

# Building page selectors
BUILDING_SELECTORS = {
    'metal_mine': ['#building1', '[data-building="metal_mine"]', '.building[data-id="1"]'],
    'crystal_mine': ['#building2', '[data-building="crystal_mine"]', '.building[data-id="2"]'],
    'deuterium_synthesizer': ['#building3', '[data-building="deuterium_synthesizer"]', '.building[data-id="3"]'],
    'solar_plant': ['#building4', '[data-building="solar_plant"]', '.building[data-id="4"]'],
    'build_button': [
        'button:has-text("Build")',
        '.build-it',
        '#build_it',
        'button[data-status="available"]',
    ],
}

# Fleet page selectors
FLEET_SELECTORS = {
    'fleet1': ['#fleet1', '[data-ship="light_fighter"]'],
    'fleet2': ['#fleet2', '[data-ship="heavy_fighter"]'],
    'fleet3': ['#fleet3', '[data-ship="cruiser"]'],
    'fleet4': ['#fleet4', '[data-ship="battleship"]'],
    'fleet5': ['#fleet5', '[data-ship="battlecruiser"]'],
    'fleet_send': ['button:has-text("Send")', '#sendfleet', '.send-btn'],
    'slots': ['.flight-time', '#slots'],
}

# Research page selectors
RESEARCH_SELECTORS = {
    'research': ['a[href*="research"]', '#research', '.research-link'],
    'espionage': ['#research1', '[data-tech="106"]'],
    'computer': ['#research3', '[data-tech="108"]'],
    'armor': ['#research15', '[data-tech="115"]'],
    'weapons': ['#research14', '[data-tech="109"]'],
    'shields': ['#research13', '[data-tech="110"]'],
}

# Error messages
ERROR_SELECTORS = [
    '.error',
    '#error',
    '.alert-error',
    '.message.error',
    '[data-error="true"]',
]

# Login error messages
LOGIN_ERROR_SELECTORS = [
    'span:has-text("Invalid")',
    '.login-error',
    '#login-error',
    'small:has-text("incorrect")',
]

# Page state selectors
PAGE_SELECTORS = {
    'overview': ['#overview', '#home', 'a[href*="page=overview"]'],
    'resources': ['#resources', '#resource', 'a[href*="page=resources"]'],
    'station': ['#station', '#facilities', 'a[href*="page=station"]'],
    'trade': ['#trade', 'a[href*="page=trader"]'],
    'fleet': ['#fleet', 'a[href*="page=fleet"]'],
    'technology': ['#technology', '#research', 'a[href*="page=research"]'],
    'galaxy': ['#galaxy', 'a[href*="page=galaxy"]'],
    'messages': ['#messages', 'a[href*="page=messages"]'],
    'settings': ['#settings', 'a[href*="page=settings"]'],
}
