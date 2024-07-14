from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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

    # More screen locator
    scroll_element_xpath = 'new UiSelector().className("android.view.View").instance(8)'
    scroll_element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_element_xpath)

    # Perform the scroll down action
    driver.execute_script('mobile: scrollGesture', {
        'elementId': scroll_element.id,
        'direction': 'down',
        'percent': 0.7
    })


# Click on 'My Account'
def test_click_on_my_account(driver):
    locator = '//android.widget.ImageView[@content-desc="My Account"]'
    wait_and_click(driver, AppiumBy.XPATH, locator)


def test_scroll_and_click_my_order(driver):
    # Define the locators
    scroll_container_locator = (AppiumBy.XPATH, '//android.widget.HorizontalScrollView')
    container_category_text_locator = (
        AppiumBy.XPATH, '//android.widget.HorizontalScrollView/android.view.View[@content-desc]')

    # Wait until the scroll container is visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(scroll_container_locator)
    )

    # Find the scroll container element
    scroll_container = driver.find_element(*scroll_container_locator)

    # Perform horizontal scroll and check for 'My Order'
    for _ in range(2):  # Scroll 2 times
        elements = driver.find_elements(*container_category_text_locator)
        for element in elements:
            content_desc = element.get_attribute('content-desc')
            if 'My Order' in content_desc:
                ele = driver.find_element(by=AppiumBy.XPATH,value='//android.view.View[contains(@content-desc,"My Orders")]')
                ele.click()
                return True  # 'My Order' found and clicked

        # If 'My Order' not found, scroll
        start_x = scroll_container.location['x'] + int(scroll_container.size['width'] * 0.8)
        end_x = scroll_container.location['x'] + int(scroll_container.size['width'] * 0.2)
        y = scroll_container.location['y'] + int(scroll_container.size['height'] / 2)

        actions = ActionChains(driver)
        actions.w3c_actions.pointer_action.move_to_location(start_x, y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(end_x, y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    return False  # 'My Order' not found after scrolling
