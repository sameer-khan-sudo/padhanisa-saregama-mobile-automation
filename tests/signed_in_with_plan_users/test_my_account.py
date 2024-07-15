import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.utils import click_skip_button, wait_and_click, perform_login, select_profile, scroll_horizontal, \
    tap_on_screen


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
    # Click on My Account
    locator = '//android.widget.ImageView[@content-desc="My Account"]'
    wait_and_click(driver, AppiumBy.XPATH, locator)

    # Scroll the account options
    scroll_horizontal(driver, 'right')
    time.sleep(0.5)
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

    # Get the pre-filled username
    profile_name_locator = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@text][1]')
    profile_name_text = profile_name_locator.get_attribute('text')
    print(f'Profile Name : {profile_name_text}')

    # Enter new username
    new_user_name = "Sohail"
    profile_name_locator.click()
    time.sleep(1)
    profile_name_locator.clear()
    time.sleep(1)
    profile_name_locator.send_keys(new_user_name)
    print(f'New Username : {new_user_name}')

    # Click on the screen to close the keyboard
    tap_on_screen(driver)

    # Verify right tick should be visible
    tick_locator = driver.find_element(by=AppiumBy.XPATH,
                                       value='//android.widget.ScrollView/android.widget.ImageView[3]')
    assert tick_locator.is_displayed(), "The right tick (checkmark) is not visible"

    # Gender selection
    user_gender_selection = 'Female'
    gender_options_locator = '//android.view.View[contains(@content-desc,"Identify")]/android.view.View[@content-desc]'
    gender_options = driver.find_elements(by=AppiumBy.XPATH, value=gender_options_locator)

    # Print content-desc of each gender option
    for index, option in enumerate(gender_options, 1):
        content_desc = option.get_attribute('content-desc')
        print(f'{index}: {content_desc}')

        if content_desc == user_gender_selection:
            wait_and_click(driver, AppiumBy.XPATH, value=f'({gender_options_locator})[{index}]')
            break

    # # Click on (i) icon info_button_locator =  driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new
    # UiSelector().className(\"android.view.View\").instance(12)") info_button_locator.click() time.sleep(1)

    # Tap to close info
    tap_on_screen(driver)

    # Scroll down
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiScrollable(new UiSelector().scrollable(true)).scrollForward()')

    time.sleep(1)

    # Select Learner's Age
    age_dropdown_locator = driver.find_element(by=AppiumBy.XPATH, value="//android.widget.ImageView[@content-desc][1]")
    age_dropdown_locator.click()
    time.sleep(1)

    age_selection = '25 - 35'
    # Get dropdown data
    xpath_locator = '//android.widget.Button[@content-desc]'

    # Find elements using the XPath locator
    elements = driver.find_elements(by=AppiumBy.XPATH, value=xpath_locator)

    # Print the content-desc attribute of each element
    for element in elements:
        content_desc = element.get_attribute("content-desc")
        print(content_desc)

        # Select user age
        if content_desc == user_gender_selection:
            element.click()

    # Enter email
    email_address_locator = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@text][2]')

    # Get the current value of the email field
    current_value = email_address_locator.text

    # If there's text in the field, clear it
    if current_value:
        email_address_locator.clear()
        print("Existing data cleared from the email field.")

    # Enter new data
    new_email = "newemail@example.com"  # Replace with the email you want to enter
    email_address_locator.send_keys(new_email)
    print(f"Entered new email: {new_email}")

