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


def test_enter_username(driver):
    # Get the pre-filled username
    profile_name_locator = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@text][1]')
    profile_name_text = profile_name_locator.get_attribute('text')
    print(f'Profile Name : {profile_name_text}')

    # Enter new username
    new_user_name = "Sohail"
    profile_name_locator.click()

    profile_name_locator.clear()
    profile_name_locator.send_keys(new_user_name)
    print(f'New Username : {new_user_name}')

    # Click on the screen to close the keyboard
    tap_on_screen(driver)

    # Verify right tick should be visible
    tick_locator = driver.find_element(by=AppiumBy.XPATH,
                                       value='//android.widget.ScrollView/android.widget.ImageView[3]')
    assert tick_locator.is_displayed(), "The right tick (checkmark) is not visible"


def test_gender_selection(driver):  # Gender selection
    user_gender_selection = 'Male'
    gender_options_locator = '//android.view.View[contains(@content-desc,"Identify")]/android.view.View[@content-desc]'
    gender_options = driver.find_elements(by=AppiumBy.XPATH, value=gender_options_locator)

    # Print content-desc of each gender option
    for index, option in enumerate(gender_options, 1):
        content_desc = option.get_attribute('content-desc')
        print(f'{index}: {content_desc}')

        if content_desc == user_gender_selection:
            wait_and_click(driver, AppiumBy.XPATH, value=f'({gender_options_locator})[{index}]')
            break

    # Tap to close info
    tap_on_screen(driver)

    # Scroll down
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiScrollable(new UiSelector().scrollable(true)).scrollForward()')


@pytest.mark.skip()
def test_age_selection(driver):
    # Select Learner's Age age_dropdown_locator = driver.find_element(by=AppiumBy.XPATH,
    # value="//android.widget.ImageView[@content-desc][1]") age_dropdown_locator.click() time.sleep(1)

    age_selection = '25 - 35'
    # Get dropdown data
    xpath_locator = '//android.widget.Button[@content-desc]'

    # Find elements using the XPath locator
    elements = driver.find_elements(by=AppiumBy.XPATH, value=xpath_locator)

    # Print the content-desc attribute of each element
    # for element in elements:
    #     content_desc = element.get_attribute("content-desc")
    #     print(content_desc)
    #
    #     # Select user age
    #     if content_desc == age_selection:
    #         element.click()


def test_enter_email(driver):
    # Get the current value of the email field
    email_address_locator = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@text][2]')
    email_address_text = email_address_locator.get_attribute('text')
    print(f'Email Address : {email_address_text}')

    new_email = 'khan.sameer301999@gmail.com'
    if email_address_text == '':
        email_address_locator.click()
        # Enter the new email address
        email_address_locator.send_keys(new_email)

        # Click on the screen to close the keyboard
        tap_on_screen(driver)

    else:
        email_address_locator.click()
        email_address_locator.clear()
        email_address_locator.send_keys(new_email)

        # Click on the screen to close the keyboard
        tap_on_screen(driver)


def test_click_on_save_changes_btn(driver):
    # Click on Save Changes button
    save_changes_btn_locator = '//android.widget.ImageView[@content-desc="Save Changes"]'
    wait_and_click(driver, AppiumBy.XPATH, value=save_changes_btn_locator)
