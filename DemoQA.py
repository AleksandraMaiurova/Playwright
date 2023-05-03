from playwright.sync_api import sync_playwright

def test_demoQA_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width':1280, 'height':1080}
        )
        page = context.new_page()

        page.goto('https://demoqa.com/automation-practice-form')
        # page.fill('//input')
