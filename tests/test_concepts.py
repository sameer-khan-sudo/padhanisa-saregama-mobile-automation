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

from utils.utils import select_mode, language_selection, screen_click, scroll_seekbar, click_on_pause_btn, \
    handle_setting
from utils.utils import wait_and_click, perform_login, select_profile, click_get_started_button


# Click on 'Permission Allow' button
def test_handle_allow_button(driver):
    allow_button_xpath = ('//android.widget.Button[@resource-id="com.android.permissioncontroller:id'
                          '/permission_allow_button"]')
    wait_and_click(driver, AppiumBy.XPATH, allow_button_xpath)

    # Click on 'Get Started' button
    click_get_started_button(driver)


# Perform login
def test_login(driver):
    # User sign in
    perform_login(driver)


# Profile selection
def test_select_profile(driver):
    # Select user's profile
    select_profile(driver, 'SAM')


# Click on 'Singing Classes' tab
def test_click_on_singing_classes(driver):
    singing_classes_locator = '//android.widget.ImageView[contains(@content-desc,"Singing Classes")]'
    wait_and_click(driver, AppiumBy.XPATH, value=singing_classes_locator)


# Module selection
def test_select_module(driver):
    # scroll down
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollForward()')

    # Select Concepts module
    select_mode(driver, 'Concepts')


# Scroll the list of video and get the text/name
# @pytest.mark.skip()
def test_scroll_and_print_texts(driver):

    # Scroll down
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollForward('
                        ').scrollForward()')

    # Scroll up
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollBackward('
                        ').scrollBackward()')


# @pytest.mark.skip()
# Search concept video
def test_search_concept_video(driver):
    search_btn_locator = (
        '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout'
        '/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View'
        '/android.view.View[1]/android.widget.ImageView')
    wait_and_click(driver, AppiumBy.XPATH, search_btn_locator)

    search_field_locator = '//android.widget.EditText'
    wait_and_click(driver, AppiumBy.XPATH, search_field_locator)
    video_name = "Sur Introduction"

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


# @pytest.mark.skip()
# Language selection
def test_language_selection(driver):
    language_selection(driver, 'Hindi')


# @pytest.mark.skip()
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


@pytest.mark.skip()
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


@pytest.mark.skip()
# Exit button
def test_exit(driver):
    # Exit button locator
    exit_btn_locator = 'new UiSelector().className("android.widget.Button").instance(0)'
    wait_and_click(driver, AppiumBy.ANDROID_UIAUTOMATOR, value=exit_btn_locator)
    print('Clicked On: Exit button')
