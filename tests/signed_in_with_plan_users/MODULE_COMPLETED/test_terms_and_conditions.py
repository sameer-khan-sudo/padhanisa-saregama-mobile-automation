from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

from utils.utils import click_skip_button, wait_and_click, perform_login, select_profile


# Click on 'Permission Allow' button
def test_handle_allow_button(driver):
    allow_button_xpath = ('//android.widget.Button[@resource-id="com.android.permissioncontroller:id'
                          '/permission_allow_button"]')
    wait_and_click(driver, AppiumBy.XPATH, allow_button_xpath)

    # Click on 'Skip' button
    click_skip_button(driver)


# Login
def test_login(driver):
    perform_login(driver)


# Select profile
def test_select_profile(driver):
    # Select user profile
    select_profile(driver, 'Sameer')


# Click on T&C
def test_click_on_terms_and_conditions(driver):
    # Settings locator
    locator = '//android.widget.ImageView[@content-desc="Settings"]'
    wait_and_click(driver, AppiumBy.XPATH, locator)

    # T&C locator
    locator = '//android.view.View[@content-desc="Terms and Conditions"]'
    wait_and_click(driver, AppiumBy.XPATH, locator)


# Scroll the T&C screen
def test_scroll_and_get_content_desc(driver):
    # Locate the container
    container = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value=
    'new UiSelector().className("android.view.View").instance(7)')

    # Get the container's dimensions
    container_rect = container.rect

    # Define scroll parameters
    start_x = container_rect['x'] + container_rect['width'] / 2
    start_y = container_rect['y'] + container_rect['height'] * 0.8
    end_y = container_rect['y'] + container_rect['height'] * 0.2

    for scroll_count in range(8):
        # Perform the scroll
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
