from playwright.sync_api import sync_playwright, expect
import re
import time

def test_successful_login():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Navigate to the login page
            page.goto("https://test-signin.ibinder.com/Account/Login")
            
            # Wait for the page to load
            page.wait_for_load_state("networkidle")
            time.sleep(5)  # Give extra time for dynamic content
            
            # Try multiple selectors for email field
            email_selectors = [
                page.get_by_label("Email"),
                page.get_by_placeholder("Email"),
                page.get_by_placeholder("email"),
                page.locator("input[type='email']"),
                page.locator("input[name='Email']"),
                page.locator("input[id='Email']"),
                page.locator("input[type='text']").first,
                page.locator("input").first
            ]
            
            email_field = None
            for selector in email_selectors:
                try:
                    if selector.is_visible():
                        email_field = selector
                        break
                except:
                    continue
            
            if not email_field:
                raise Exception("Could not find email field with any selector")
                
            email_field.fill("sridevi@indpro.se")
            print("Email entered successfully")
            
            # Try multiple selectors for password field
            password_selectors = [
                page.get_by_label("Password"),
                page.get_by_placeholder("Password"),
                page.get_by_placeholder("password"),
                page.locator("input[type='password']"),
                page.locator("input[name='Password']"),
                page.locator("input[id='Password']")
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    if selector.is_visible():
                        password_field = selector
                        break
                except:
                    continue
            
            if not password_field:
                raise Exception("Could not find password field with any selector")
                
            password_field.fill("Sana@123")
            print("Password entered successfully")
            
            # Try multiple selectors for login button
            button_selectors = [
                page.get_by_role("button", name="Login"),
                page.get_by_role("button", name="Sign in"),
                page.get_by_role("button", name="Sign In"),
                page.locator("button[type='submit']"),
                page.locator("input[type='submit']"),
                page.locator("button").first
            ]
            
            login_button = None
            for selector in button_selectors:
                try:
                    if selector.is_visible():
                        login_button = selector
                        break
                except:
                    continue
            
            if not login_button:
                raise Exception("Could not find login button with any selector")
                
            login_button.click()
            print("Login button clicked")
            
            # Wait for successful login
            page.wait_for_url("**/test-my.ibinder.com/**", timeout=30000)
            print("Login successful!")
            
            # Verify we're on the dashboard or any valid post-login page
            expect(page).to_have_url(re.compile(r"https://test-my\.ibinder\.com/.*"))
            print("Successfully verified post-login URL")
            
        except Exception as e:
            print(f"Test failed with error: {str(e)}")
            print(f"Current URL: {page.url}")
            print(f"Page content: {page.content()[:2000]}")
            raise
            
        finally:
            # Close the browser
            browser.close()

if __name__ == "__main__":
    test_successful_login() 