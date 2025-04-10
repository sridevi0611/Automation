# test_ibinder_login.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

class TestIBinderLogin:
    def setup_method(self):
        # Setup Chrome options
        chrome_options = Options()
        # Add additional options for stability
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize the Chrome driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(20)
        
        # Add stealth script
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        })
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })
        
    def wait_for_page_load(self, timeout=30):
        """Wait for the page to be fully loaded"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            page_state = self.driver.execute_script('return document.readyState;')
            if page_state == 'complete':
                return True
            time.sleep(1)
        return False
        
    def find_element_with_multiple_selectors(self, selectors, timeout=20):
        """Try multiple selectors to find an element"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            for by, value in selectors:
                try:
                    # First try to find the element
                    element = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((by, value))
                    )
                    # Then wait for it to be clickable
                    WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((by, value))
                    )
                    return element
                except (TimeoutException, NoSuchElementException):
                    continue
            time.sleep(1)
            # Print page source for debugging
            print(f"Current page source: {self.driver.page_source[:500]}")
        raise TimeoutException(f"Could not find element with any of these selectors: {selectors}")
        
    def teardown_method(self):
        if self.driver:
            self.driver.quit()
            
    def test_successful_login(self):
        # Test data
        login_url = "https://test-signin.ibinder.com/Account/Login"
        email = "sridevi@indpro.se"
        password = "Sana@123"
        
        try:
            # Navigate to the login page
            self.driver.get(login_url)
            print(f"Navigated to login page: {login_url}")
            
            # Wait for page to be fully loaded
            if not self.wait_for_page_load():
                print("Warning: Page did not fully load within timeout")
            
            print("Page load wait complete")
            print(f"Current URL: {self.driver.current_url}")
            
            # Try multiple selectors for email field
            print("Attempting to find email field...")
            email_selectors = [
                (By.ID, "Email"),
                (By.NAME, "Email"),
                (By.CSS_SELECTOR, "input[type='email']"),
                (By.CSS_SELECTOR, "input[name='Email']"),
                (By.CSS_SELECTOR, "input[id='Email']"),
                (By.XPATH, "//input[@type='email']"),
                (By.XPATH, "//input[contains(@placeholder, 'email')]"),
                (By.XPATH, "//input[contains(@placeholder, 'Email')]"),
                (By.XPATH, "//input[contains(@class, 'email')]"),
                (By.XPATH, "//input[contains(@class, 'Email')]"),
                (By.XPATH, "//input[contains(@id, 'email')]"),
                (By.XPATH, "//input[contains(@id, 'Email')]"),
                (By.XPATH, "//input[contains(@name, 'email')]"),
                (By.XPATH, "//input[contains(@name, 'Email')]"),
                (By.XPATH, "//input[contains(@type, 'email')]"),
                (By.XPATH, "//input[contains(@type, 'Email')]")
            ]
            email_field = self.find_element_with_multiple_selectors(email_selectors)
            
            # Try to interact with email field in multiple ways
            self.driver.execute_script("arguments[0].value = '';", email_field)
            email_field.clear()
            ActionChains(self.driver).move_to_element(email_field).click().perform()
            email_field.send_keys(email)
            print("Email entered successfully")
            
            # Try multiple selectors for password field
            print("Attempting to find password field...")
            password_selectors = [
                (By.ID, "Password"),
                (By.NAME, "Password"),
                (By.CSS_SELECTOR, "input[type='password']"),
                (By.CSS_SELECTOR, "input[name='Password']"),
                (By.CSS_SELECTOR, "input[id='Password']"),
                (By.XPATH, "//input[@type='password']"),
                (By.XPATH, "//input[contains(@placeholder, 'password')]"),
                (By.XPATH, "//input[contains(@placeholder, 'Password')]"),
                (By.XPATH, "//input[contains(@class, 'password')]"),
                (By.XPATH, "//input[contains(@class, 'Password')]"),
                (By.XPATH, "//input[contains(@id, 'password')]"),
                (By.XPATH, "//input[contains(@id, 'Password')]"),
                (By.XPATH, "//input[contains(@name, 'password')]"),
                (By.XPATH, "//input[contains(@name, 'Password')]"),
                (By.XPATH, "//input[contains(@type, 'password')]"),
                (By.XPATH, "//input[contains(@type, 'Password')]")
            ]
            password_field = self.find_element_with_multiple_selectors(password_selectors)
            
            # Try to interact with password field in multiple ways
            self.driver.execute_script("arguments[0].value = '';", password_field)
            password_field.clear()
            ActionChains(self.driver).move_to_element(password_field).click().perform()
            password_field.send_keys(password)
            print("Password entered successfully")
            
            # Try multiple selectors for login button
            print("Attempting to find login button...")
            button_selectors = [
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[@type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Login')]"),
                (By.XPATH, "//button[contains(text(), 'Sign in')]"),
                (By.XPATH, "//button[contains(text(), 'Sign In')]"),
                (By.XPATH, "//button[contains(@class, 'login')]"),
                (By.XPATH, "//button[contains(@class, 'signin')]"),
                (By.XPATH, "//input[@type='submit']"),
                (By.CSS_SELECTOR, "button.login-button"),
                (By.CSS_SELECTOR, "button.submit-button"),
                (By.CSS_SELECTOR, "input[type='submit']"),
                (By.XPATH, "//button[contains(@class, 'btn')]"),
                (By.XPATH, "//button[contains(@class, 'button')]"),
                (By.XPATH, "//input[contains(@class, 'btn')]"),
                (By.XPATH, "//input[contains(@class, 'button')]")
            ]
            login_button = self.find_element_with_multiple_selectors(button_selectors)
            print("Found login button, attempting to click...")
            
            # Try multiple ways to click the button
            try:
                login_button.click()
            except:
                try:
                    ActionChains(self.driver).move_to_element(login_button).click().perform()
                except:
                    self.driver.execute_script("arguments[0].click();", login_button)
            
            print("Login button clicked")
            
            # Wait for successful login
            print("Waiting for redirect after login...")
            WebDriverWait(self.driver, 30).until(
                EC.url_contains("test-my.ibinder.com")
            )
            
            # Verify successful login
            assert "test-my.ibinder.com" in self.driver.current_url, "Login failed - Not redirected to dashboard"
            print("Login successful!")
            
        except TimeoutException as e:
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page source: {self.driver.page_source[:2000]}...")  # Print more of the page source
            raise AssertionError(f"Login test failed - Timeout waiting for element: {str(e)}")
        except Exception as e:
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page source: {self.driver.page_source[:2000]}...")
            raise AssertionError(f"Login test failed: {str(e)}")

if __name__ == "__main__":
    # Manual test execution
    test = TestIBinderLogin()
    try:
        test.setup_method()
        test.test_successful_login()
        print("Login test passed successfully!")
    except AssertionError as e:
        print(f"Test failed: {str(e)}")
    finally:
        test.teardown_method() 