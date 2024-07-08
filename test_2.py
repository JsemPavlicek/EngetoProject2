# Pavel Formánek
# přihlášení se na webovou stránku engeta.cz, kliknutí na tlačítko do portálu 
# s následným přesměrováním na https://learn.engeto.com/cs/prihlaseni
import pytest
from playwright.sync_api import sync_playwright

tested_website = "https://engeto.cz"

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

def test_kontakt(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(tested_website)
    cookies = page.locator('#cookiescript_accept')
    cookies.click()
    kontakt_locator = page.locator('a[href="https://engeto.cz/kontakt/"]')
    kontakt = kontakt_locator.first
    kontakt.click()
    page.wait_for_load_state('networkidle')
    page_content = page.content().lower()
    page.screenshot(path = "fakturacni_udaje.png")
    assert "fakturační údaje" in page_content
    

    

  

    