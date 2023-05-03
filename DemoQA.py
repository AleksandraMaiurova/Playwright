from playwright.sync_api import sync_playwright

def test_demoQA_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width':1280, 'height':1200}
        )
        page = context.new_page()

        page.goto('https://demoqa.com/automation-practice-form')
        page.fill('//input[@id="firstName"]', 'Aleksandra')
        page.fill('//input[@id="lastName"]', 'Maiurova')
        page.fill('//input[@id="userEmail"]', 'asmaiurova@itmo.ru')
        page.click('//label[@for="gender-radio-2"]')
        page.fill('//input[@id="userNumber"]', '1234567899')
        page.fill('//input[@id="dateOfBirthInput"]', '13 Jul 1993')
        page.click('//div[contains(@class, "react-datepicker__day--selected")]')
        page.fill('//input[@id="subjectsInput"]', 'english')
        page.click('//*[text()="English"]') #.nth(1) - если элементов несколько
        page.click('//label[@for="hobbies-checkbox-1"]')
        page.click('//label[@for="hobbies-checkbox-2"]')
        page.locator('//input[@id="uploadPicture"]').set_input_files('vbUrzS0RtIg.jpg')
        page.fill('//textarea[@id="currentAddress"]', 'This is my address where I can cry if I wanna')
        page.click('//div[@id="state"]')
        page.click('//*[text()="Uttar Pradesh"]')
        page.click('//div[@id="city"]')
        page.click('//*[text()="Agra"]')
        page.click('//button[@id="submit"]')
        assert 'Thanks for submitting the form' in page.inner_text('//div[@class="modal-content"]')










        page.wait_for_timeout(3000)
