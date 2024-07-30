import time

import pytest
from appium.webdriver.common.appiumby import AppiumBy

from utils.utils import select_mode, select_songs_by_character, scroll_song_list, difficulty_level_selection
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
    select_profile(driver, 'Franklin')


# Click on 'Singing Classes' tab
def test_click_on_singing_classes(driver):
    singing_classes_locator = '//android.widget.ImageView[contains(@content-desc,"Singing Classes")]'
    wait_and_click(driver, AppiumBy.XPATH, value=singing_classes_locator)


# Module selection
def test_select_module(driver):
    # Select 15 min class module
    select_mode(driver, 'Class')


# Difficulty level selection
def test_level_selection(driver):
    mode = 'Medium'
    difficulty_level_selection(driver, mode)
    time.sleep(4)


# Perform song list scroll
def test_character_scroll(driver):
    # Scroll down
    scroll_song_list(driver, 'down')
#
#     # Scroll up
#     scroll_song_list(driver, 'up')
#
#
# # Get songs by given character
# @pytest.mark.skip()
# def test_songs_by_character(driver):
#     letter = "S"
#     try:
#         select_songs_by_character(driver, letter)
#         print(f"Successfully selected character '{letter}'")
#     except Exception as e:
#         print(f"Failed to select character: {str(e)}")
