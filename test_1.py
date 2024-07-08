# Pavel Formánek
# test odsouhlasení cookies na webové stránce engeto.cz + vytvoření screenshotu na konci testu

import pytest
from playwright.sync_api import sync_playwright
import time

tested_webside = "https://engeto.cz"

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

def test_accept_cookies(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(tested_webside)
    page_content = page.content().upper()
    assert "COOKIES" in page_content and "CHÁPU A PŘIJÍMÁM" in page_content
    page.click("#cookiescript_accept")

    