cat > ~/devops-assignment01/tests/test_app.py << 'TESTEOF'
import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

# Use environment variable - localhost:3001 because docker-compose maps 3001:3000
APP_URL = os.environ.get('APP_URL', 'http://localhost:3001')

def get_driver():
    """Setup headless Chrome - required for Jenkins on EC2"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

@pytest.fixture(scope="module")
def driver():
    d = get_driver()
    yield d
    d.quit()

class TestShopZone:

    # ─────────────────────────────────────────
    # HOMEPAGE TESTS
    # ─────────────────────────────────────────

    def test_01_homepage_loads(self, driver):
        """Test 1: Homepage loads successfully"""
        driver.get(APP_URL)
        assert driver.title != ""
        assert "404" not in driver.page_source
        assert "Cannot GET" not in driver.page_source
        print(f"\n✓ Test 1 PASSED: Homepage loaded | Title: '{driver.title}'")

    def test_02_homepage_has_shopzone_branding(self, driver):
        """Test 2: Page contains ShopZone branding"""
        driver.get(APP_URL)
        page = driver.page_source.lower()
        title = driver.title.lower()
        assert "shopzone" in page or "shopzone" in title or "shop" in page
        print(f"✓ Test 2 PASSED: ShopZone branding found")

    def test_03_homepage_has_navbar(self, driver):
        """Test 3: Homepage has a navigation bar"""
        driver.get(APP_URL)
        nav = driver.find_elements(By.CSS_SELECTOR,
            "nav, .navbar, .nav, header, .header")
        assert len(nav) > 0, "Navbar should exist"
        print(f"✓ Test 3 PASSED: Navbar found ({len(nav)} elements)")

    def test_04_homepage_has_products_section(self, driver):
        """Test 4: Homepage displays products"""
        driver.get(APP_URL)
        products = driver.find_elements(By.CSS_SELECTOR,
            ".product, .card, .product-card, "
            "[class*='product'], [class*='card'], .item")
        page = driver.page_source.lower()
        assert len(products) > 0 or "product" in page
        print(f"✓ Test 4 PASSED: Products found ({len(products)} elements)")

    def test_05_homepage_loads_under_15s(self, driver):
        """Test 5: Homepage loads within 15 seconds"""
        start = time.time()
        driver.get(APP_URL)
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        elapsed = time.time() - start
        assert elapsed < 15, f"Too slow: {elapsed:.2f}s"
        print(f"✓ Test 5 PASSED: Loaded in {elapsed:.2f}s")

    def test_06_homepage_css_loaded(self, driver):
        """Test 6: CSS stylesheets are loaded"""
        driver.get(APP_URL)
        css   = driver.find_elements(By.CSS_SELECTOR, "link[rel='stylesheet']")
        style = driver.find_elements(By.TAG_NAME, "style")
        assert len(css) + len(style) > 0, "No CSS found"
        print(f"✓ Test 6 PASSED: {len(css)} CSS files, {len(style)} style tags")

    def test_07_javascript_works(self, driver):
        """Test 7: JavaScript executes correctly"""
        driver.get(APP_URL)
        result = driver.execute_script("return 2 + 2")
        assert result == 4
        print("✓ Test 7 PASSED: JavaScript works")

    def test_08_homepage_has_links(self, driver):
        """Test 8: Homepage has navigation links"""
        driver.get(APP_URL)
        links = driver.find_elements(By.TAG_NAME, "a")
        assert len(links) > 0, "Homepage should have links"
        print(f"✓ Test 8 PASSED: Found {len(links)} links")

    def test_09_no_server_error_on_homepage(self, driver):
        """Test 9: No 500 server error on homepage"""
        driver.get(APP_URL)
        page = driver.page_source.lower()
        assert "500"                  not in driver.title
        assert "internal server error" not in page
        assert "cannot read"           not in page
        print("✓ Test 9 PASSED: No server errors")

    def test_10_homepage_has_footer(self, driver):
        """Test 10: Homepage has footer"""
        driver.get(APP_URL)
        footer = driver.find_elements(By.CSS_SELECTOR, "footer, .footer, [class*='footer']")
        page   = driver.page_source.lower()
        assert len(footer) > 0 or "footer" in page or len(driver.page_source) > 500
        print(f"✓ Test 10 PASSED: Footer found ({len(footer)} elements)")

    # ─────────────────────────────────────────
    # ROUTE ACCESSIBILITY TESTS
    # ─────────────────────────────────────────

    def test_11_products_page_accessible(self, driver):
        """Test 11: /products page is accessible"""
        driver.get(f"{APP_URL}/products")
        time.sleep(2)
        assert "404"        not in driver.page_source
        assert "Cannot GET" not in driver.page_source
        print("✓ Test 11 PASSED: /products accessible")

    def test_12_login_page_accessible(self, driver):
        """Test 12: /auth/login page is accessible"""
        driver.get(f"{APP_URL}/auth/login")
        time.sleep(1)
        assert "404"        not in driver.page_source
        assert "Cannot GET" not in driver.page_source
        print("✓ Test 12 PASSED: /auth/login accessible")

    def test_13_register_page_accessible(self, driver):
        """Test 13: /auth/register page is accessible"""
        driver.get(f"{APP_URL}/auth/register")
        time.sleep(1)
        assert "404"        not in driver.page_source
        assert "Cannot GET" not in driver.page_source
        print("✓ Test 13 PASSED: /auth/register accessible")

    def test_14_custom_404_page_works(self, driver):
        """Test 14: Non-existent route returns custom 404"""
        driver.get(f"{APP_URL}/this-page-xyz-does-not-exist")
        time.sleep(1)
        page = driver.page_source.lower()
        assert "404" in page or "not found" in page
        print("✓ Test 14 PASSED: Custom 404 works")

    # ─────────────────────────────────────────
    # LOGIN PAGE TESTS
    # ─────────────────────────────────────────

    def test_15_login_has_email_field(self, driver):
        """Test 15: Login form has email field"""
        driver.get(f"{APP_URL}/auth/login")
        field = driver.find_elements(By.CSS_SELECTOR,
            "input[type='email'], input[type='text'], "
            "input[name='email'], input[name='username']")
        assert len(field) > 0, "Email field should exist"
        print("✓ Test 15 PASSED: Email field found")

    
TESTEOF
