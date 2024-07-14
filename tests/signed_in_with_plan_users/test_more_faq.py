import json

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.utils import click_skip_button, wait_and_click


# Click on 'Permission Allow' button
def test_handle_allow_button(driver):
    allow_button_xpath = ('//android.widget.Button[@resource-id="com.android.permissioncontroller:id'
                          '/permission_allow_button"]')
    wait_and_click(driver, AppiumBy.XPATH, allow_button_xpath)

    # Click on 'Skip' button
    click_skip_button(driver)


def test_more(driver):
    # More screen locator
    more = '//android.widget.ImageView[@content-desc="More"]'
    wait_and_click(driver, AppiumBy.XPATH, value=more
                   )
    scroll_element_xpath = 'new UiSelector().className("android.view.View").instance(8)'
    scroll_element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_element_xpath)

    # Perform the scroll down action
    driver.execute_script('mobile: scrollGesture', {
        'elementId': scroll_element.id,
        'direction': 'down',
        'percent': 0.7
    })


# Login
# def test_login(driver):
#     perform_login(driver)


# # Select profile
# def test_select_profile(driver):
#     # Select user profile
#     select_profile(driver, 'Sameer')
#
#     # More screen locator
#     scroll_element_xpath = 'new UiSelector().className("android.view.View").instance(8)'
#     scroll_element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_element_xpath)
#
#     # Perform the scroll down action
#     driver.execute_script('mobile: scrollGesture', {
#         'elementId': scroll_element.id,
#         'direction': 'down',
#         'percent': 0.7
#     })
#
#
# Click on 'Settings'
def test_click_on_settings(driver):
    # Settings locator
    locator = '//android.widget.ImageView[@content-desc="Settings"]'
    wait_and_click(driver, AppiumBy.XPATH, locator)


#
#
# Click on 'FAQ'
def test_faq(driver):
    # Manage Devices locator
    manage_device_locator = '//android.view.View[@content-desc="FAQ"]'
    wait_and_click(driver, AppiumBy.XPATH, value=manage_device_locator)
    print('Clicked on FAQ')
    # time.sleep(5)


def test_scroll(driver):
    faqs_locator = '//android.widget.ScrollView/android.view.View/android.view.View/android.view.View[@content-desc]'

    previous_elements = set()
    all_elements = set()
    element_data = {}

    while True:
        # Wait for elements to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, faqs_locator))
        )

        # Find all current elements
        elements = driver.find_elements(by=AppiumBy.XPATH, value=faqs_locator)

        # Add new elements to all_elements set
        current_elements = set(elements)
        new_elements = current_elements - previous_elements
        all_elements.update(new_elements)

        # If no new elements, we've reached the end of the scroll
        if not new_elements:
            break

        # Scroll down
        driver.swipe(500, 1000, 500, 200, 500)  # Adjust coordinates as needed

        previous_elements = current_elements

    # Store all collected elements
    for index, element in enumerate(all_elements):
        try:
            content_desc = element.get_attribute('content-desc')
            element_data[index] = content_desc
        except NoSuchElementException:
            element_data[index] = "Element no longer available"

    # Write the data to a JSON file
    with open('FAQ_DATA.json', 'w') as json_file:
        json.dump(element_data, json_file, indent=4)

    print("FAQ_DATA.json file has been created with the content descriptions.")