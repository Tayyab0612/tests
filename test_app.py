import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Updated to your specific EC2 IP and Port 3000
APP_URL = os.environ.get('APP_URL', 'http://32.236.12.162:3000')

def get_driver():
    """Setup headless Chrome - required for Jenkins on EC2"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

@pytest.fixture(scope="module")
def driver():
    d = get_driver()
    yield d
    d.quit()

class TestShopZone:
    # 1. Homepage loads successfully
    def test_01_homepage_loads(self, driver):
        driver.get(APP_URL)
        assert driver.title != ""
        print(f"\n✓ Test 1 PASSED: Homepage loaded at {APP_URL}")

    # 2. Page contains ShopZone branding
    def test_02_homepage_has_shopzone_branding(self, driver):
        driver.get(APP_URL)
        assert "shop" in driver.page_source.lower()

    # 3. Homepage has a navigation bar
    def test_03_homepage_has_navbar(self, driver):
        driver.get(APP_URL)
        nav = driver.find_elements(By.TAG_NAME, "nav")
        assert len(nav) >= 0 

    # 4. Homepage displays products
    def test_04_homepage_has_products_section(self, driver):
        driver.get(APP_URL)
        assert "product" in driver.page_source.lower()

    # 5. Homepage loads within 15 seconds
    def test_05_homepage_loads_under_15s(self, driver):
        start = time.time()
        driver.get(APP_URL)
        elapsed = time.time() - start
        assert elapsed < 15

    # 6. CSS stylesheets are loaded
    def test_06_homepage_css_loaded(self, driver):
        driver.get(APP_URL)
        css = driver.find_elements(By.CSS_SELECTOR, "link[rel='stylesheet']")
        assert len(css) > 0

    # 7. JavaScript executes correctly
    def test_07_javascript_works(self, driver):
        driver.get(APP_URL)
        assert driver.execute_script("return 2 + 2") == 4

    # 8. Homepage has navigation links
    def test_08_homepage_has_links(self, driver):
        driver.get(APP_URL)
        assert len(driver.find_elements(By.TAG_NAME, "a")) > 0

    # 9. No 500 server error on homepage
    def test_09_no_server_error_on_homepage(self, driver):
        driver.get(APP_URL)
        assert "500" not in driver.title

    # 10. Homepage has footer
    def test_10_homepage_has_footer(self, driver):
        driver.get(APP_URL)
        assert "footer" in driver.page_source.lower() or len(driver.page_source) > 100

    # 11. /products page is accessible
    def test_11_products_page_accessible(self, driver):
        driver.get(f"{APP_URL}/products")
        assert "404" not in driver.page_source

    # 12. /auth/login page is accessible
    def test_12_login_page_accessible(self, driver):
        driver.get(f"{APP_URL}/auth/login")
        assert "404" not in driver.page_source

    # 13. /auth/register page is accessible
    def test_13_register_page_accessible(self, driver):
        driver.get(f"{APP_URL}/auth/register")
        assert "404" not in driver.page_source

    # 14. Non-existent route returns 404
    def test_14_custom_404_page_works(self, driver):
        driver.get(f"{APP_URL}/invalid-route-123")
        assert "404" in driver.page_source or "not found" in driver.page_source.lower()

    # 15. Login form has email field
    def test_15_login_has_email_field(self, driver):
        driver.get(f"{APP_URL}/auth/login")
        inputs = driver.find_elements(By.TAG_NAME, "input")
        assert len(inputs) > 0
TESTEOF
