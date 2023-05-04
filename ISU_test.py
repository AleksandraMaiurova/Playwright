from playwright.sync_api import sync_playwright

def test_papers():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width':1280, 'height':1080}
        )
        page = context.new_page()

        page.goto('https://id.itmo.ru/auth/realms/itmo/protocol/openid-connect/auth?response_type=code&scope=openid&client_id=isu&redirect_uri=https://isu.ifmo.ru/api/sso/v1/public/login?apex_params=p=2143:LOGIN:105983405529584')
        page.fill('//input[@id="username"]', 'LOGIN')
        page.fill('//input[@id="password"]', 'PASSWORD')
        page.click('//input[@id="kc-login"]')
        page.click('//*[text()="Личный кабинет"]')
        page.click('//*[text()="Результаты и достижения"]')
        page.click('//*[text()="Публикации"]')
        page.click('//button[@id="B4433377515183783526"]')
        page.click('//span[@id="select2-chosen-1"]')
        page.fill('//input[@id="s2id_autogen1_search"]', 'Статья')
        page.keyboard.press("Enter")
        page.fill('//input[@id="P3_ACTION"]', 'Это самое крутое наименование статьи, оно чуть длиннее чем обычно, но все равно крутое')
        page.click('//select[@id="P3_YEAR"]')
        page.keyboard.press("ArrowDown")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.click('//button[@id="B1781660956466320586"]')

        assert 'Редактирование карточки результата' in page.inner_text('//span[@class="panel-title"]')
        page.wait_for_timeout(5000)