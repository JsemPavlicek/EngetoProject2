# Pavel Formánek
# testovací scénář, zda bude na webové stránce přítomný HTML element s textem "Chybný email anebo heslo" nebo "Neznáma chyba" při chybně zadaných údajích
import pytest
from playwright.sync_api import sync_playwright
import time

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.mark.parametrize("user_email,user_password", [
    ("PepaEngeto@zavináč.cézet", "SpatneHeslo"),
    ("123456@seznam.cz", "01234567"), 
    ("Engeto@engeto.cz", "Engetoskoleni"),
    ("MůjPravýEmail@seznam.cz", "MojePravéHeslo")]) # např. zde bych zadal skutečné údaje pro přihlášení, abych zjistil, jak proběhne přihlášení a že poslední test skončí FAILED. Z důvodu pozdějšího zveřejnení kódu a bezpečnosti mého účtu toto netestuji

def test_login_engeto(browser, user_email, user_password):
    context = browser.new_context()
    page = context.new_page()
    
    page.goto("https://engeto.cz")
    
    page.wait_for_timeout(3000)
    
    cookies = page.locator('#cookiescript_accept')
    cookies.click()
    
    with context.expect_page() as new_page_info:
        do_portalu = page.locator('a[href="https://learn.engeto.com/cs/prihlaseni"]').first
        do_portalu.click()
    
    new_page = new_page_info.value
    new_page.wait_for_load_state()

    again_cookies = new_page.locator('#cookiescript_accept')
    again_cookies.click()
    new_page.wait_for_load_state("load")
    first_input = new_page.locator('input[name="email"]')
    second_input = new_page.locator('input[name="password"]')
    first_input.fill(user_email)
    second_input.fill(user_password)
    login = new_page.locator('span:text("Přihlásit")')
    login.click()
    new_page.wait_for_timeout(10000)
    forgotten_password_or_email = new_page.locator('text ="Chybný email anebo heslo"')
    unknown_password_or_email = new_page.locator('text="Neznáma chyba"')

    assert forgotten_password_or_email.is_visible() or unknown_password_or_email.is_visible()

    