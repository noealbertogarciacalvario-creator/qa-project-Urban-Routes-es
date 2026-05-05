import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time as t


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


# Clase POM
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
    confirm_code_button = (By.XPATH, ".//button[@type='submit' and @class='button full' and contains(.,'Confirmar')]")
    add_payment_button = (By.XPATH, "//div[@class='pp-button filled']")
    add_card_button = (By.CSS_SELECTOR, 'img.pp-plus')
    card_number_input = (By.XPATH, "//input[@type='text' and @id='number']")
    card_code_input = (By.XPATH, ".//input[@id='code' and @type='text' and @name='code']")
    form_button = (By.XPATH, "//div[@class='pp-buttons']")
    add_button_card = (By.XPATH, "//button[@type='submit' and @class='button full' and contains(., 'Agregar')]")
    close_payment_method_window_button = (By.XPATH, ".//button[@class='close-button section-close']")
    message_driver_input = (By.XPATH, ".//input[@id='comment']")
    drop_menu_requirements_button = (By.XPATH, ".//img[@alt='Arrow']")
    icecream_requirement_button = (By.XPATH, "//div[@class='r-link-sublabel']")
    blanket_switch_button = (By.XPATH, ".//span[@class='slider round']")
    blanket_switch_checkbox = (By.XPATH, ".//input[contains(@class,'switch-input')]")
    icecream_counter_button = (By.XPATH, ".//div[@class='counter-plus' and contains(., '+')]")
    icecream_counter_value = (By.XPATH, ".//div[contains(@class,'counter-value')]")
    reservation_button = (By.XPATH, "//button[@type='button' and @class='smart-button']")
    order_search_title = (By.XPATH, "//div[@class='order-header-title' and text()='Buscar automóvil']")
    driver_header = (By.XPATH,
                     "//div[contains(@class,'order-header-title') and contains(text(),'El conductor llegará')]")

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.from_field)
        )
        element.clear()
        element.send_keys(from_address)

    def set_to(self, to_address):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.to_field)
        )
        element.clear()
        element.send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    # Métodos para clickear elementos y enviar texto a un campo de entrada de manera mas simple.
    def click_element(self, locator):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def send_keys(self, locator, text):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(locator)

        )
        element.send_keys(text)

    def setup_route(self):
        self.set_from(data.address_from)
        self.set_to(data.address_to)

    def open_comfort_fee(self):
        self.click_element(self.order_a_taxi)
        self.click_element(self.comfort_fee)


# Clase para las pruebas
class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        cls.driver = webdriver.Chrome(options=options)

    def setup_method(self):
        self.driver.get(data.urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)

    def test_set_route(self):
        self.routes_page.setup_route()

        assert self.routes_page.get_from() == data.address_from
        assert self.routes_page.get_to() == data.address_to

    def test_set_fee(self):
        self.routes_page.setup_route()
        self.routes_page.click_element(self.routes_page.order_a_taxi)

        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.routes_page.comfort_fee)
        )
        assert element.is_enabled()

        element.click()

    def test_input_phone_number(self):
        self.routes_page.setup_route()
        self.routes_page.open_comfort_fee()

        self.routes_page.click_element(self.routes_page.phone_number_button)
        self.routes_page.send_keys(self.routes_page.phone_number_input, data.phone_number)
        self.routes_page.click_element(self.routes_page.next_phone_number_format_button)

        code = retrieve_phone_code(self.driver)
        self.routes_page.send_keys(self.routes_page.phone_number_code_input, code)
        t.sleep(1)
        self.routes_page.click_element(self.routes_page.confirm_code_button)

        assert self.driver.find_element(*self.routes_page.phone_number_code_input).get_property("value") == code

    def test_add_credit_card(self):
        self.routes_page.setup_route()
        self.routes_page.open_comfort_fee()
        self.routes_page.click_element(self.routes_page.add_payment_button)
        self.routes_page.click_element(self.routes_page.add_card_button)
        self.routes_page.send_keys(self.routes_page.card_number_input, data.card_number)
        self.routes_page.send_keys(self.routes_page.card_code_input, data.card_code)
        self.routes_page.click_element(self.routes_page.form_button)
        self.routes_page.click_element(self.routes_page.add_button_card)

        assert self.driver.find_element(*self.routes_page.card_code_input).get_property("value") == data.card_code

    def test_send_message_to_driver(self):
        self.routes_page.setup_route()
        self.routes_page.open_comfort_fee()

        message = "Hola, Señor conductor..!"
        self.routes_page.send_keys(self.routes_page.message_driver_input, message, )

        assert self.driver.find_element(*self.routes_page.message_driver_input).get_property("value") == message

    def test_order_requirements(self):
        self.routes_page.setup_route()
        self.routes_page.open_comfort_fee()
        self.routes_page.click_element(self.routes_page.drop_menu_requirements_button)
        self.routes_page.click_element(self.routes_page.icecream_requirement_button)
        self.routes_page.click_element(self.routes_page.blanket_switch_button)

        checkbox = self.driver.find_element(*self.routes_page.blanket_switch_checkbox)
        assert checkbox.is_selected(), "El switch de blanket no se activó"

    def test_ask_for_icecream(self):
        self.routes_page.setup_route()
        self.routes_page.open_comfort_fee()
        self.routes_page.click_element(self.routes_page.drop_menu_requirements_button)
        self.routes_page.click_element(self.routes_page.icecream_requirement_button)
        self.routes_page.click_element(self.routes_page.icecream_counter_button)
        t.sleep(1)
        self.routes_page.click_element(self.routes_page.icecream_counter_button)
        t.sleep(1)

        counter = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.routes_page.icecream_counter_value)
        )

        assert counter.text == "2"

    # Estas últimas dos pruebas reutilizan diseño de la prueba para agregar un número de telfono sin llamarla, para separar las pruebas como buena practica..
    def test_modal_window_appears(self):
        self.routes_page.setup_route()
        self.routes_page.open_comfort_fee()

        self.routes_page.click_element(self.routes_page.phone_number_button)
        self.routes_page.send_keys(self.routes_page.phone_number_input, data.phone_number)
        self.routes_page.click_element(self.routes_page.next_phone_number_format_button)

        code = retrieve_phone_code(self.driver)
        self.routes_page.send_keys(self.routes_page.phone_number_code_input, code)
        t.sleep(1)
        self.routes_page.click_element(self.routes_page.confirm_code_button)
        self.routes_page.click_element(self.routes_page.reservation_button)

        order_window = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.routes_page.order_search_title)
        )

        assert order_window.text == "Buscar automóvil", "No apareció la ventana de espera del conductor"

    def test_name_of_conductor_appears(self):
        self.routes_page.setup_route()
        self.routes_page.open_comfort_fee()

        self.routes_page.click_element(self.routes_page.phone_number_button)
        self.routes_page.send_keys(self.routes_page.phone_number_input, data.phone_number)
        self.routes_page.click_element(self.routes_page.next_phone_number_format_button)

        code = retrieve_phone_code(self.driver)
        self.routes_page.send_keys(self.routes_page.phone_number_code_input, code)
        t.sleep(1)
        self.routes_page.click_element(self.routes_page.confirm_code_button)
        self.routes_page.click_element(self.routes_page.reservation_button)

        driver_name = WebDriverWait(self.driver, 60).until(
            EC.visibility_of_element_located(self.routes_page.driver_header))

        assert "El conductor llegará" in driver_name.text

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
