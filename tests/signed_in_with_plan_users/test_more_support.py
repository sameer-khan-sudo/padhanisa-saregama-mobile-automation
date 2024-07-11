import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.utils import click_skip_button, wait_and_click, perform_login


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
    # select_profile(driver, 'Sameer')

    # More screen locator
    scroll_element_xpath = 'new UiSelector().className("android.view.View").instance(8)'
    scroll_element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_element_xpath)

    # Perform the scroll down action
    driver.execute_script('mobile: scrollGesture', {
        'elementId': scroll_element.id,
        'direction': 'down',
        'percent': 0.7
    })


# Click on 'Help Videos'
def test_click_on_support(driver):
    locator = '//android.widget.ImageView[@content-desc="Support"]'
    wait_and_click(driver, AppiumBy.XPATH, locator)


# Email and Phone assertion
def test_assert_email_and_phone(driver):
    # Assert email field is present and has correct content
    email_address_locator = '//android.widget.ImageView[contains(@content-desc,"padhanisa@saregama.com")]'
    email_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.XPATH, email_address_locator))
    )
    assert "padhanisa@saregama.com" in email_element.get_attribute("content-desc")

    # Assert phone number field is present and has correct content
    phone_number_locator = '//android.widget.ImageView[contains(@content-desc,"18001027799")]'
    phone_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.XPATH, phone_number_locator))
    )
    assert "18001027799" in phone_element.get_attribute("content-desc")


# Dropdown concern selection
def test_dropdown_selection(driver):
    time.sleep(2)

    desired_dropdown_value = 'Booking Issue'
    # Dropdown locator
    dropdown_locator = '//android.widget.ImageView[@content-desc="Select"]'
    wait_and_click(driver, AppiumBy.XPATH, dropdown_locator)

    # Wait for dropdown options to be visible
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((AppiumBy.XPATH, '//android.widget.Button[@content-desc]'))
    )

    # Dropdown values
    dropdown_data_locator = '//android.widget.Button[@content-desc]'
    dropdown_options = driver.find_elements(AppiumBy.XPATH, dropdown_data_locator)

    # Print dropdown options
    for index, option in enumerate(dropdown_options, start=1):
        text = option.get_attribute('content-desc')
        print(f'{index}. {text}')

        if text == desired_dropdown_value:
            desired_option_found = True
            break

    # Assert that the desired option was found and clicked
    assert desired_option_found, f"Desired dropdown value '{desired_dropdown_value}' not found"




