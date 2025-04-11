const { chromium } = require('playwright');

class TestIBinderLogin {
    async setup() {
        this.browser = await chromium.launch({
            headless: false,
            args: [
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--window-size=1920,1080',
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars',
                '--start-maximized'
            ]
        });
        
        this.context = await this.browser.newContext({
            viewport: { width: 1920, height: 1080 },
            userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        });
        
        this.page = await this.context.newPage();
    }

    async teardown() {
        if (this.browser) {
            await this.browser.close();
        }
    }

    async findElement(selectors, elementType = "element") {
        for (const selector of selectors) {
            try {
                const element = selector;
                if (await element.isVisible()) {
                    return element;
                }
            } catch (error) {
                continue;
            }
        }
        throw new Error(`Could not find ${elementType}`);
    }

    async testSuccessfulLogin() {
        // Test data
        const loginUrl = "https://test-signin.ibinder.com/Account/Login";
        const email = "sridevi@indpro.se";
        const password = "Sana@123";

        try {
            // Navigate to the login page
            await this.page.goto(loginUrl);
            console.log(`Navigated to login page: ${loginUrl}`);

            // Wait for page to be fully loaded
            await this.page.waitForLoadState('networkidle');
            await this.page.waitForTimeout(3000); // Give extra time for dynamic content
            console.log("Page load complete");
            console.log(`Current URL: ${this.page.url()}`);

            // Try multiple selectors for email field
            console.log("Attempting to fill email field...");
            const emailSelectors = [
                this.page.getByLabel("Email"),
                this.page.getByPlaceholder("Email"),
                this.page.getByPlaceholder("email"),
                this.page.locator("input[type='email']"),
                this.page.locator("input[name='Email']"),
                this.page.locator("input[id='Email']"),
                this.page.locator("input[type='text']").first(),
                this.page.locator("input").first(),
                this.page.locator("#Email"),
                this.page.locator("[name='Email']"),
                this.page.locator("[id='Email']")
            ];

            const emailField = await this.findElement(emailSelectors, "email field");
            await emailField.fill(email);
            console.log("Email entered successfully");

            // Try multiple selectors for password field
            console.log("Attempting to fill password field...");
            const passwordSelectors = [
                this.page.getByLabel("Password"),
                this.page.getByPlaceholder("Password"),
                this.page.getByPlaceholder("password"),
                this.page.locator("input[type='password']"),
                this.page.locator("input[name='Password']"),
                this.page.locator("input[id='Password']"),
                this.page.locator("#Password"),
                this.page.locator("[name='Password']"),
                this.page.locator("[id='Password']")
            ];

            const passwordField = await this.findElement(passwordSelectors, "password field");
            await passwordField.fill(password);
            console.log("Password entered successfully");

            // Try multiple selectors for login button
            console.log("Attempting to click login button...");
            const buttonSelectors = [
                this.page.getByRole("button", { name: "Login" }),
                this.page.getByRole("button", { name: "Sign in" }),
                this.page.getByRole("button", { name: "Sign In" }),
                this.page.locator("button[type='submit']"),
                this.page.locator("input[type='submit']"),
                this.page.locator("button").first(),
                this.page.locator("input[type='submit']").first(),
                this.page.locator("button:has-text('Login')"),
                this.page.locator("button:has-text('Sign in')"),
                this.page.locator("button:has-text('Sign In')")
            ];

            const loginButton = await this.findElement(buttonSelectors, "login button");
            await loginButton.click();
            console.log("Login button clicked");

            // Wait for successful login
            console.log("Waiting for redirect after login...");
            await this.page.waitForURL("**/test-my.ibinder.com/**", { timeout: 30000 });

            // Verify successful login
            const currentUrl = this.page.url();
            if (!currentUrl.includes("test-my.ibinder.com")) {
                throw new Error("Login failed - Not redirected to dashboard");
            }
            console.log("Login successful!");

        } catch (error) {
            console.log(`Current URL: ${this.page.url()}`);
            try {
                console.log(`Page title: ${await this.page.title()}`);
                console.log(`Page content: ${(await this.page.content()).substring(0, 1000)}`);
            } catch (e) {
                console.log("Could not get page details");
            }
            throw new Error(`Login test failed: ${error.message}`);
        }
    }
}

// Manual test execution
async function runTest() {
    const test = new TestIBinderLogin();
    try {
        await test.setup();
        await test.testSuccessfulLogin();
        console.log("Login test passed successfully!");
    } catch (error) {
        console.log(`Test failed: ${error.message}`);
    } finally {
        await test.teardown();
    }
}

runTest(); 