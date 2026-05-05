from pages.urban_routes_page import UrbanRoutesPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data
import json
import time
from selenium.common import WebDriverException


def retrieve_phone_code(driver) -> str:
    code = None

    for _ in range(10):
        try:
            logs = [
                log["message"]
                for log in driver.get_log("performance")
                if log.get("message") and "api/v1/number?number" in log.get("message")
            ]

            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd(
                    "Network.getResponseBody",
                    {"requestId": message_data["params"]["requestId"]},
                )
                code = "".join([x for x in body["body"] if x.isdigit()])

        except WebDriverException:
            time.sleep(1)
            continue

        if code:
            return code

    raise Exception("No se encontró el código de confirmación del teléfono.")


def open_page(driver):
    driver.get(data.urban_routes_url)
    return UrbanRoutesPage(driver)


def prepare_comfort_order(driver):
    page = open_page(driver)
    page.set_route(data.address_from, data.address_to)
    page.open_comfort_fee()
    return page


def add_phone_number(driver, page):
    page.open_phone_modal()
    page.set_phone_number(data.phone_number)

    code = retrieve_phone_code(driver)
    page.set_phone_code(code)
    page.wait_clickable(page.reservation_button)

    return code


def test_set_route(driver):
    page = open_page(driver)

    page.set_route(data.address_from, data.address_to)

    assert page.get_from() == data.address_from
    assert page.get_to() == data.address_to


def test_set_fee(driver):
    page = open_page(driver)

    page.set_route(data.address_from, data.address_to)
    page.click_element(page.order_a_taxi)

    comfort_option = page.wait_clickable(page.comfort_fee)

    assert comfort_option.is_enabled()


def test_input_phone_number(driver):
    page = prepare_comfort_order(driver)

    code = add_phone_number(driver, page)

    assert code is not None


def test_add_credit_card(driver):
    page = prepare_comfort_order(driver)

    page.add_credit_card(data.card_number, data.card_code)

    assert "Tarjeta" in page.get_payment_method_text()

def test_send_message_to_driver(driver):
    page = prepare_comfort_order(driver)

    message = "Hola, Señor conductor..!"
    page.send_message_to_driver(message)

    assert page.wait_visible(page.message_driver_input).get_property("value") == message


def test_order_requirements(driver):
    page = prepare_comfort_order(driver)

    page.open_requirements()
    page.select_icecream_requirement()
    page.activate_blanket_and_scarves()

    assert page.is_blanket_selected(), "El switch de manta y pañuelos no se activó"


def test_ask_for_icecream(driver):
    page = prepare_comfort_order(driver)

    page.open_requirements()
    page.select_icecream_requirement()
    page.add_icecream(quantity=2)

    assert page.get_icecream_counter_value() == "2"


def test_modal_window_appears(driver):
    page = prepare_comfort_order(driver)

    add_phone_number(driver, page)
    page.click_reservation_button()

    assert page.get_order_search_title() == "Buscar automóvil"


def test_name_of_conductor_appears(driver):
    page = prepare_comfort_order(driver)

    add_phone_number(driver, page)
    page.click_reservation_button()


    WebDriverWait(driver, 60).until(
        EC.text_to_be_present_in_element(page.driver_header, "El conductor llegará")
)

    assert "El conductor llegará" in page.get_driver_header_text()