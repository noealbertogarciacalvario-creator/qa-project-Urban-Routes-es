from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    # Locators
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    order_a_taxi = (By.CSS_SELECTOR, 'button.button.round')
    comfort_fee = (By.CLASS_NAME, 'tcard-icon')
    phone_number_button = (By.CLASS_NAME, 'np-text')
    phone_number_input = (By.ID, 'phone')
    next_phone_number_format_button = (By.CSS_SELECTOR, 'button.button.full')
    phone_number_code_input = (By.ID, 'code')
    confirm_code_button = (
        By.XPATH,
        ".//button[@type='submit' and @class='button full' and contains(.,'Confirmar')]"
    )
    add_payment_button = (By.XPATH, "//div[@class='pp-button filled']")
    add_card_button = (By.CSS_SELECTOR, 'img.pp-plus')
    card_number_input = (By.XPATH, "//input[@type='text' and @id='number']")
    card_code_input = (By.XPATH, ".//input[@id='code' and @type='text' and @name='code']")
    form_button = (By.XPATH, "//div[@class='pp-buttons']")
    add_button_card = (
        By.XPATH,
        "//button[@type='submit' and @class='button full' and contains(., 'Agregar')]"
    )
    close_payment_method_window_button = (
        By.XPATH,
        ".//button[@class='close-button section-close']"
    )
    message_driver_input = (By.XPATH, ".//input[@id='comment']")
    drop_menu_requirements_button = (By.XPATH, ".//img[@alt='Arrow']")
    icecream_requirement_button = (By.XPATH, "//div[@class='r-link-sublabel']")
    blanket_switch_button = (By.XPATH, ".//span[@class='slider round']")
    blanket_switch_checkbox = (By.XPATH, ".//input[contains(@class,'switch-input')]")
    icecream_counter_button = (
        By.XPATH,
        ".//div[@class='counter-plus' and contains(., '+')]"
    )
    icecream_counter_value = (By.XPATH, ".//div[contains(@class,'counter-value')]")
    reservation_button = (By.XPATH, "//button[@type='button' and @class='smart-button']")
    order_search_title = (
        By.XPATH,
        "//div[@class='order-header-title' and text()='Buscar automóvil']"
    )
    driver_header = (
        By.XPATH,
        "//div[contains(@class,'order-header-title') and contains(text(),'El conductor llegará')]"
    )
    payment_method_text = (By.CLASS_NAME, "pp-value-text")

    def __init__(self, driver):
        self.driver = driver

    def wait_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def click_element(self, locator):
        self.wait_clickable(locator).click()

    def send_keys(self, locator, text):
        self.wait_visible(locator).send_keys(text)

    def set_from(self, from_address):
        element = self.wait_visible(self.from_field)
        element.clear()
        element.send_keys(from_address)

    def set_to(self, to_address):
        element = self.wait_visible(self.to_field)
        element.clear()
        element.send_keys(to_address)

    def get_from(self):
        return self.wait_visible(self.from_field).get_property("value")

    def get_to(self):
        return self.wait_visible(self.to_field).get_property("value")

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def open_comfort_fee(self):
        self.click_element(self.order_a_taxi)
        self.click_element(self.comfort_fee)

    def open_phone_modal(self):
        self.click_element(self.phone_number_button)

    def set_phone_number(self, phone_number):
        self.send_keys(self.phone_number_input, phone_number)
        self.click_element(self.next_phone_number_format_button)

    def set_phone_code(self, code):
        self.send_keys(self.phone_number_code_input, code)
        self.click_element(self.confirm_code_button)

    def add_credit_card(self, card_number, card_code):
        self.click_element(self.add_payment_button)
        self.click_element(self.add_card_button)
        self.send_keys(self.card_number_input, card_number)
        self.send_keys(self.card_code_input, card_code)
        self.click_element(self.form_button)
        self.click_element(self.add_button_card)

    def send_message_to_driver(self, message):
        self.send_keys(self.message_driver_input, message)

    def open_requirements(self):
        self.click_element(self.drop_menu_requirements_button)

    def select_icecream_requirement(self):
        self.click_element(self.icecream_requirement_button)

    def activate_blanket_and_scarves(self):
        self.click_element(self.blanket_switch_button)

    def add_icecream(self, quantity=1):
        for _ in range(quantity):
            self.click_element(self.icecream_counter_button)

    def click_reservation_button(self):
        self.click_element(self.reservation_button)

    def get_icecream_counter_value(self):
        return self.wait_visible(self.icecream_counter_value).text

    def is_blanket_selected(self):
        checkbox = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.blanket_switch_checkbox)
        )
        return checkbox.is_selected()

    def get_order_search_title(self):
        return self.wait_visible(self.order_search_title).text

    def get_driver_header_text(self):
        return self.wait_visible(self.driver_header, timeout=60).text

    def get_payment_method_text(self):
        return self.wait_visible(self.payment_method_text).text
