import time

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.utils import wait_and_click, click_skip_button, perform_login, select_profile, click_learn_to_sing, \
    language_selection, screen_click, scroll_seekbar, click_on_pause_btn, handle_setting


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
    select_profile(driver, 'Sameer')

    # Click on 'Home' button
    home_locator = '//android.widget.ImageView[@content-desc="Home"]'
    wait_and_click(driver, AppiumBy.XPATH, home_locator)


# Click on 'Learn to Sing' tab
def test_click_on_learn_to_sing(driver):
    click_learn_to_sing(driver)


# Select 'Understand Concepts' mode
def test_click_on_understand_concepts(driver):
    locator = '//android.widget.ImageView[contains(@content-desc,"Understand Concepts")]'
    wait_and_click(driver, AppiumBy.XPATH, locator)


# Scroll the list of video and get the text/name
@pytest.mark.skip()
def test_scroll_and_print_texts(driver):
    screen_size = driver.get_window_size()
    start_x = screen_size['width'] * 0.5
    start_y = screen_size['height'] * 0.8
    end_y = screen_size['height'] * 0.2

    all_texts = set()
    count = 1
    desired_text = 'Mukhda Introduction'
    desired_element_found = False

    while True:
        # Find elements and print their texts
        wait = WebDriverWait(driver, 40)
        elements = wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH, '//*[@content-desc]')))
        new_text_found = False
        for element in elements:
            text = element.get_attribute('content-desc')
            if text and text not in all_texts:
                print(f"{count}. {text}")
                all_texts.add(text)
                new_text_found = True
                count += 1
                time.sleep(2)
                if text == desired_text:
                    ele = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH,
                                                                 f'//android.widget.ImageView[@content-desc="{desired_text}"]/android.view.View')))
                    ele.click()
                    return  # Exit the function after clicking the desired element

        # If no new texts were found, break the loop
        if not new_text_found:
            break

        # Perform scroll down action
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    # Perform scroll up and look for the desired element
    while not desired_element_found:
        # Find elements and check for the desired text
        elements = wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH, '//*[@content-desc]')))
        for element in elements:
            text = element.get_attribute('content-desc')
            if text == desired_text:
                ele = wait.until(EC.element_to_be_clickable(
                    (AppiumBy.XPATH, f'//android.widget.ImageView[@content-desc="{desired_text}"]/android.view.View')))
                ele.click()
                return  # Exit the function after clicking the desired element


# Search concept video
def test_search_concept_video(driver):
    search_btn_locator = (
        '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout'
        '/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View'
        '/android.view.View[1]/android.widget.ImageView')
    wait_and_click(driver, AppiumBy.XPATH, search_btn_locator)

    search_field_locator = '//android.widget.EditText'
    wait_and_click(driver, AppiumBy.XPATH, search_field_locator)
    video_name = "Sur"

    wait = WebDriverWait(driver, 40)
    search_field = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, search_field_locator)))
    search_field.send_keys(video_name)

    # CLOSE THE KEYBOARD
    keyboard_down_locator = 'new UiSelector().className("android.view.View").instance(10)'
    keyboard_down = wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, keyboard_down_locator)))
    keyboard_down.click()

    # Wait for search results to load
    search_video_locator = (
        f"//android.widget.ImageView[contains(@content-desc, '{video_name}')]/android.view.View")
    no_result_locator = '//android.view.View[@content-desc="No Result Found"]'

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (AppiumBy.XPATH, f"{search_video_locator} | {no_result_locator}")
            )
        )

        if "No Result Found" in element.get_attribute("content-desc"):
            print(f"No Data Found for '{video_name}'.")
        else:
            wait_and_click(driver, AppiumBy.XPATH, search_video_locator)

    except TimeoutException:
        print(f"No Data Found for '{video_name}'. Neither search results nor 'No Result Found' screen were found.")


# Language selection
def test_language_selection(driver):
    language_selection(driver, 'Hindi')


# Video screen actions
def test_handle_single_passive_video(driver):
    # On screen click
    screen_click(driver)

    # Scroll seekbar
    scroll_seekbar(driver, 0.5)

    # Click on pause button
    click_on_pause_btn(driver)

    # Click on Settings button
    setting_btn_locator = '//android.widget.ImageView[@content-desc="Settings"]'
    wait_and_click(driver, AppiumBy.XPATH, value=setting_btn_locator)


# Handle settings
def test_settings(driver):
    # Subtitle setting
    handle_setting(driver, "Subtitles", "On")

    # Audio/Language setting
    handle_setting(driver, "Audio", "Hindi (हिंदी)")

    # Speed setting
    handle_setting(driver, "Speed", "0.5x")
    time.sleep(2)

    # Click on Apply button
    apply_btn_locator = '//android.widget.Button[@content-desc="Apply"]'
    wait_and_click(driver, AppiumBy.XPATH, value=apply_btn_locator)
    print("Clicked on: Apply button")


# Exit button
def test_exit(driver):

    # Exit button locator
    exit_btn_locator = 'new UiSelector().className("android.widget.Button").instance(0)'
    wait_and_click(driver,AppiumBy.ANDROID_UIAUTOMATOR,value=exit_btn_locator)
    print('Clicked On: Exit button')
