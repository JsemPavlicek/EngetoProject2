# Pavel Formánek
#testování aplikace na stránce https://test-intro.engeto.com/ s použitím pytest parametrize

import pytest
from playwright.sync_api import sync_playwright



@pytest.mark.parametrize("first_name, city, expected_result", [
    ("Pavel", "Louny", "Welcome Pavel from Louny. There are 2 vowels in your first name and 3 consonants in your first name and there are 3 vowels in your city and 2 consonants in your city."),
    ("2Pavel", "2Louny", "Welcome 2Pavel from 2Louny. There are 2 vowels in your first name and 3 consonants in your first name and there are 3 vowels in your city and 2 consonants in your city."),
    ("Pávěl", "Lóůny", "Welcome Pávěl from Lóůny. There are 2 vowels in your first name and 3 consonants in your first name and there are 3 vowels in your city and 2 consonants in your city."),
])
def test_form_submission(first_name, city, expected_result):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        
        page.goto("https://test-intro.engeto.com/") 
        page.wait_for_load_state("load")

        first_name_input = page.locator('input[name="firstname"]')
        first_name_input.fill(first_name)

        city_input = page.locator('input[name="city"]')
        city_input.fill(city)

        submit_button = page.locator('input[type="submit"]')
        submit_button.click()

        page.wait_for_load_state('load')

        actual_result = page.locator('div[style="width:8000px"]').inner_text()
        assert actual_result == expected_result

        browser.close()

