import time

import pytest
from appium.webdriver.common.appiumby import AppiumBy

from utils.utils import wait_and_click, perform_login, select_profile, scroll_horizontal, \
    tap_on_screen, click_get_started_button


# Click on 'Permission Allow' button
def test_handle_allow_button(driver):
    allow_button_xpath = ('//android.widget.Button[@resource-id="com.android.permissioncontroller:id'
                          '/permission_allow_button"]')
    wait_and_click(driver, AppiumBy.XPATH, allow_button_xpath)

    # Click on 'Get Started' button
    click_get_started_button(driver)


# Login
def test_login(driver):
    perform_login(driver)


# Select profile
def test_select_profile(driver):
    # Select user profile
    select_profile(driver, 'Sohail')

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
    # Click on My Account
    locator = '//android.widget.ImageView[@content-desc="My Account"]'
    wait_and_click(driver, AppiumBy.XPATH, locator)

    # Scroll the account options
    scroll_horizontal(driver, 'right')
    scroll_horizontal(driver, 'left')


# Edit Profile
def test_edit_profile(driver):
    # Click on Edit Profile button
    edit_profile_locator = '//android.widget.ImageView[@content-desc=" Edit Profile"]'
    wait_and_click(driver, AppiumBy.XPATH, value=edit_profile_locator)

    # Verify 'Edit Profile' label
    label_locator = driver.find_element(AppiumBy.XPATH, value='//android.view.View[@content-desc="Edit Profile"]')
    label_text = label_locator.get_attribute('content-desc')
    print(f'Label : {label_text}')

    assert label_text == "Edit Profile"


def test_click_reset_profile(driver):
    # Scroll down
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiScrollable(new UiSelector().scrollable(true)).scrollForward()')

    # Click on Reset Profile button
    reset_btn_locator = '//android.widget.ImageView[@content-desc="Reset Profile"]'
    wait_and_click(driver, AppiumBy.XPATH, value=reset_btn_locator)

    # Reset Profile popup
    popup_element_line_one = driver.find_element(by=AppiumBy.XPATH,
                                                 value='//android.view.View[contains(@content-desc,"reset your '
                                                       'profile? ")]')

    popup_element_line_two = driver.find_element(by=AppiumBy.XPATH,
                                                 value='//android.widget.Button[contains(@content-desc,"This will '
                                                       'delete all your information")]')

    # Get the content-desc attributes
    content_desc_one = popup_element_line_one.get_attribute('content-desc')
    content_desc_two = popup_element_line_two.get_attribute('content-desc')

    # Concatenate the text
    confirmation_message = content_desc_one + '' + content_desc_two

    print(f'Confirmation Message :  {confirmation_message}')


def test_perform_action(driver):
    # Action
    action = 'Reset'
    action_locator = f'//android.widget.Button[@content-desc="{action}"]'

    if action == action:
        wait_and_click(driver, AppiumBy.XPATH, value=action_locator)

    # OTP Verification
    otp_field_locator = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText')
    wait_and_click(driver, AppiumBy.XPATH, otp_field_locator)
    time.sleep(2)
    # Enter OTP number
    otp_field_locator.send_keys('123456')
