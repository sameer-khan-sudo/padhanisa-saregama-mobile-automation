import time

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
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
    desired_dropdown_value = 'Payment Error'

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

    # Print dropdown options and select the desired one
    desired_option_found = False
    for index, option in enumerate(dropdown_options, start=1):
        text = option.get_attribute('content-desc')
        print(f'{index}. {text}')

        if text == desired_dropdown_value:
            option.click()
            desired_option_found = True
            break

    # Assert that the desired option was found and clicked
    assert desired_option_found, f"Desired dropdown value '{desired_dropdown_value}' not found"


# More about issue
def test_more_about_issue(driver):
    # More about field locator
    more_about_field_locator = '//android.widget.EditText'
    wait_and_click(driver, AppiumBy.XPATH, value=more_about_field_locator)

    fill_data = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText')
    data = ("Saregama India Ltd., formerly known as The Gramophone Company of India Ltd., is India's oldest music "
            "label company, owned by the RP-Sanjiv Goenka Group of companies. The company is listed on the NSE and "
            "the BSE with its head office located in Kolkata and other offices in Mumbai, Chennai and Delhi.")
    fill_data.send_keys(data)
    time.sleep(1)

    # Click on the screen to close the keyboard
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(814, 805)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()


def test_upload_media(driver):
    # Upload media
    upload_field_locator = '//android.widget.ImageView[@content-desc="Upload media"]'
    wait_and_click(driver, AppiumBy.XPATH, value=upload_field_locator)

    # Media/Image/Video permission
    allow_all_btn_locator = ('//android.widget.Button[@resource-id="com.android.permissioncontroller:id'
                             '/permission_allow_all_button"]')
    wait_and_click(driver, AppiumBy.XPATH, value=allow_all_btn_locator)

    # Upload image
    image_locator = 'new UiSelector().className("android.widget.LinearLayout").instance(13)'
    try:
        # First, check if the element exists
        if driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, image_locator):
            wait_and_click(driver, AppiumBy.ANDROID_UIAUTOMATOR, value=image_locator)
            print("Image uploaded successfully!")
        else:
            print("No Image found!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("No Image found!")

    return driver


# @pytest.mark.skip('Not Needed')
def test_click_on_submit(driver):
    time.sleep(1)

    direction = 'down'

    # FIND THE CONTAINER ELEMENT
    container = driver.find_element(AppiumBy.XPATH, value='//android.widget.ScrollView')

    # GET THE DIMENSIONS OF THE CONTAINER
    container_rect = container.rect

    # CALCULATE START AND END POINTS FOR THE SCROLL
    start_x = container_rect['x'] + container_rect['width'] // 2

    if direction.lower() == 'down':
        start_y = container_rect['y'] + container_rect['height'] * 0.8
        end_y = container_rect['y'] + container_rect['height'] * 0.2
    elif direction.lower() == 'up':
        start_y = container_rect['y'] + container_rect['height'] * 0.2
        end_y = container_rect['y'] + container_rect['height'] * 0.8
    else:
        raise ValueError("Direction must be either 'up' or 'down'")

    # CREATE A POINTER INPUT OBJECT FOR TOUCH EVENTS
    finger = PointerInput(interaction.POINTER_TOUCH, "finger")

    # BUILD THE ACTION SEQUENCE
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=finger)

    # PERFORM THE SCROLL ACTION
    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
    actions.w3c_actions.pointer_action.release()

    # PERFORM THE ACTION
    actions.perform()

    # Submit button
    submit_btn_locator = '//android.widget.ImageView[@content-desc="Submit"]'
    wait_and_click(driver, AppiumBy.XPATH, value=submit_btn_locator)
    print('Click on Submit button')


# Thanks Popup screen
# @pytest.mark.skip('Not Needed')
def test_handle_tanks_popup(driver):
    thanks_screen_locator = driver.find_element(by=AppiumBy.XPATH,
                                                value='//android.view.View[contains(@content-desc,"Thank you")]')
    get_text = thanks_screen_locator.get_attribute('content-desc')
    print(f'Extracted Text : {get_text}')
    expected_text = 'Thank you for sharing your concern. We will contact you within 24-48 working hours'

    assert get_text == expected_text


# Remove uploaded media
@pytest.mark.skip('Not Needed')
def test_remove_media(driver):
    # Remove button
    remove_btn_locator = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                             value="new UiSelector().className(\"android.view.View\").instance(10)")
    remove_btn_locator.click()
    print('Uploaded image removed')


# Click on Okay button
def test_click_on_okay(driver):
    okay_btn = '//android.widget.ImageView[@content-desc="Okay"]'
    wait_and_click(driver, AppiumBy.XPATH, value=okay_btn)
    print('Click on Okay button')
