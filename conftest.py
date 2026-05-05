import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from api.client import APIClient


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    yield driver

    driver.quit()


@pytest.fixture
def api_client():
    return APIClient()
