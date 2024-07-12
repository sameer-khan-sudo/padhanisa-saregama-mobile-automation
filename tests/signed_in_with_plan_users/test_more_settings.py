import datetime
import json
import time

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.utils import click_skip_button, wait_and_click, perform_login, select_profile, screen_click


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


# Click on 'Settings'
def test_click_on_settings(driver):
    # Settings locator
    locator = '//android.widget.ImageView[@content-desc="Settings"]'
    wait_and_click(driver, AppiumBy.XPATH, locator)


def test_manage_devices(driver):
    # Manage Devices locator
    manage_device_locator = '//android.view.View[@content-desc="Manage Devices"]'
    wait_and_click(driver, AppiumBy.XPATH, value=manage_device_locator)
    print('Clicked on Manage Devices')


def test_scroll_and_print_devices(driver):

    # json file name - write data
    device_json_file = 'device_data.json'
    output_file = f"device_data_{device_json_file}.json"

    # Set up scrolling parameters
    screen_size = driver.get_window_size()
    start_x = screen_size['width'] * 0.5
    start_y = screen_size['height'] * 0.8
    end_y = screen_size['height'] * 0.2
    duration = 800  # milliseconds

    last_texts = set()  # To keep track of previously seen texts
    scroll_attempts = 0
    max_scroll_attempts = 1  # Adjust this value based on your needs

    all_devices = []  # List to store all device data

    while scroll_attempts < max_scroll_attempts:
        # Find all devices
        devices = driver.find_elements(AppiumBy.XPATH,
                                       '//android.widget.ScrollView/android.view.View[2]/android.view.View/android.widget.ImageView')

        current_texts = set()
        for device in devices:
            try:
                # Get the text of the device
                device_text = device.get_attribute('content-desc')
                if device_text and device_text not in last_texts:
                    # Parse and format the device information
                    lines = device_text.split('\n')
                    if len(lines) >= 4:
                        device_data = {
                            "Device Name": lines[0],
                            "Location": lines[1],
                            "Profile used": lines[2],
                            "Status": lines[3]
                        }
                        all_devices.append(device_data)

                        print(f"Device Name : {lines[0]}")
                        print(f"Location : {lines[1]}")
                        print(f"Profile used: {lines[2]}")
                        print(f"{lines[3]}")
                        print()  # Add a blank line between devices
                    else:
                        print(device_text)  # Print as-is if it doesn't match expected format
                    current_texts.add(device_text)
            except NoSuchElementException:
                print("Could not find text for a device")

        # If no new texts are found, we've probably reached the end of the list
        if not current_texts - last_texts:
            break

        last_texts.update(current_texts)

        # Perform scroll action
        driver.swipe(start_x, start_y, start_x, end_y, duration)

        # Wait for the page to load after scrolling
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.ScrollView'))
        )

        scroll_attempts += 1

    print("Finished scrolling and printing text")

    # Save all device data to JSON file
    with open(output_file, 'w') as f:
        json.dump(all_devices, f, indent=2)

    print(f"Device data saved to {output_file}")


