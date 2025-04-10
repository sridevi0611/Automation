import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser_context_args():
    """Configure browser context arguments."""
    return {
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "java_script_enabled": True,
        "has_touch": False,
        "is_mobile": False,
        "color_scheme": "light",
        "locale": "en-US",
        "timezone_id": "America/New_York",
        "geolocation": {"latitude": 40.7128, "longitude": -74.0060},
        "permissions": ["geolocation"],
        "extra_http_headers": {
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }
    }

@pytest.fixture(scope="session")
def browser():
    """Create a browser instance for the test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # Set to True for CI/CD environments
            slow_mo=50,  # Slow down operations by 50ms for better visibility
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars',
                '--start-maximized',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                '--window-size=1920,1080'
            ]
        )
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def context(browser, browser_context_args):
    """Create a new context for each test."""
    context = browser.new_context(**browser_context_args)
    
    # Add stealth script
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en']
        });
    """)
    
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context):
    """Create a new page in a new context for each test."""
    page = context.new_page()
    
    # Set default timeout
    page.set_default_timeout(30000)
    
    yield page
    page.close() 