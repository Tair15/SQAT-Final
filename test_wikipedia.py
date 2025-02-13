import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Фикстура для выбора браузера
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Choose browser: chrome, firefox, edge")


@pytest.fixture
def web_driver(request):
    browser = request.config.getoption("--browser")
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "edge":
        driver = webdriver.Edge()
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()
    yield driver
    driver.quit()


# Тестирование функциональности
@pytest.mark.wikipedia
@pytest.mark.regression
def test_edit_article(web_driver):
    web_driver.get("https://en.wikipedia.org/wiki/Wikipedia:Sandbox")
    edit_btn = web_driver.find_element(By.ID, "ca-edit")
    edit_btn.click()
    time.sleep(2)
    web_driver.switch_to.active_element.send_keys(Keys.ENTER)
    time.sleep(2)
    text_area = web_driver.find_element(By.ID, "wpTextbox1")
    text_area.clear()
    text_area.send_keys("Automated test edit. This is a test.")
    preview_btn = web_driver.find_element(By.ID, "wpPreview")
    preview_btn.click()
    time.sleep(2)
    preview_header = web_driver.find_element(By.ID, "wikiPreview")
    assert "Automated test edit" in preview_header.text, "Изменения не отображаются в превью"


# Тестирование удобства использования
@pytest.mark.wikipedia
@pytest.mark.regression
def test_ui_elements(web_driver):
    web_driver.get("https://en.wikipedia.org/wiki/Main_Page")
    time.sleep(2)
    search_input = web_driver.find_element(By.NAME, "search")
    assert search_input.is_displayed(), "Поле поиска недоступно"
    search_btn = web_driver.find_element(By.NAME, "search")
    assert search_btn.is_displayed(), "Кнопка поиска недоступна"
    login_menu = WebDriverWait(web_driver, 10).until(EC.presence_of_element_located((By.ID, "pt-login-2")))
    assert login_menu.is_displayed(), "Логин меню отсутствует"


# Тестирование производительности
@pytest.mark.wikipedia
def test_page_load_time(web_driver):
    start_time = time.time()
    web_driver.get("https://en.wikipedia.org/wiki/Main_Page")
    load_time = time.time() - start_time
    assert load_time < 3, f"Главная страница загружалась слишком долго: {load_time} секунд"

    web_driver.get("https://en.wikipedia.org/wiki/Wikipedia:Sandbox")
    edit_start_time = time.time()
    edit_btn = web_driver.find_element(By.ID, "ca-edit")
    edit_btn.click()
    edit_load_time = time.time() - edit_start_time
    assert edit_load_time < 3, f"Страница редактирования загружалась слишком долго: {edit_load_time} секунд"


# Проверка отображения логотипа
@pytest.mark.wikipedia
def test_logo_visibility(web_driver):
    web_driver.get("https://en.wikipedia.org/wiki/Main_Page")
    logo_element = web_driver.find_element(By.CLASS_NAME, "mw-logo-icon")
    assert logo_element.is_displayed(), "Логотип Wikipedia не отображается"


# Тестирование перехода на случайную страницу
@pytest.mark.wikipedia
def test_random_page(web_driver):
    web_driver.get("https://en.wikipedia.org/wiki/Special:Random")
    time.sleep(2)
    assert "wikipedia" in web_driver.current_url.lower(), "Случайная страница не загрузилась"


# Проверка доступности страницы помощи
@pytest.mark.wikipedia
def test_help_page(web_driver):
    web_driver.get("https://en.wikipedia.org/wiki/Help:Contents")
    title_text = web_driver.find_element(By.ID, "firstHeading").text
    assert "Help" in title_text, "Страница помощи не загрузилась"


# Проверка доступности страницы "О Wikipedia"
@pytest.mark.wikipedia
def test_about_page(web_driver):
    web_driver.get("https://en.wikipedia.org/wiki/Wikipedia:About")
    title_text = web_driver.find_element(By.ID, "firstHeading").text
    assert "Wikipedia" in title_text, "Страница 'О Wikipedia' не загрузилась"


# Проверка отображения категорий
@pytest.mark.wikipedia
def test_categories_presence(web_driver):
    web_driver.get("https://en.wikipedia.org/wiki/Main_Page")
    category_elements = web_driver.find_elements(By.CLASS_NAME, "mw-normal-catlinks")
    assert len(category_elements) > 0, "Список категорий отсутствует"


# Проверка ссылок в футере
@pytest.mark.wikipedia
def test_footer_links(web_driver):
    web_driver.get("https://en.wikipedia.org/wiki/Main_Page")
    footer_links = web_driver.find_elements(By.CSS_SELECTOR, "#footer a")
    assert len(footer_links) > 5, "В футере недостаточно ссылок"


# Проверка истории изменений
@pytest.mark.wikipedia
def test_revision_history(web_driver):
    web_driver.get("https://en.wikipedia.org/wiki/Main_Page")
    history_btn = WebDriverWait(web_driver, 10).until(EC.element_to_be_clickable((By.ID, "ca-history")))
    history_btn.click()

    WebDriverWait(web_driver, 10).until(EC.presence_of_element_located((By.ID, "firstHeading")))
    heading_text = web_driver.find_element(By.ID, "firstHeading").text
    assert "Revision history" in heading_text or "View history" in heading_text, "Страница истории изменений не загрузилась"


# Проверка страницы контактов
@pytest.mark.wikipedia
def test_contact_page(web_driver):
    web_driver.get("https://en.wikipedia.org/wiki/Wikipedia:Contact_us")
    title_text = web_driver.find_element(By.ID, "firstHeading").text
    assert "Contact" in title_text, "Страница контактов Wikipedia не загрузилась"
