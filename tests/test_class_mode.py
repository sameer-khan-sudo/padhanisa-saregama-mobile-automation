import time

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

from utils.utils import select_mode, select_songs_by_character, scroll_song_list, difficulty_level_selection, \
    song_filter_selection, filter_btn_selection, search_song, tap_on_screen, allow_device_permissions
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


@pytest.mark.skip()
# Difficulty level selection
def test_level_selection(driver):
    mode = 'Easy'
    difficulty_level_selection(driver, mode)
    time.sleep(2)


@pytest.mark.skip()
# Perform song list scroll
def test_character_scroll(driver):
    # Scroll down
    scroll_song_list(driver, 'down')

    # Scroll up
    scroll_song_list(driver, 'up')


# Get/scroll songs by given character
@pytest.mark.skip()
def test_songs_by_character(driver):
    letter = "S"
    try:
        select_songs_by_character(driver, letter)
        print(f"Successfully selected character '{letter}'")
    except Exception as e:
        print(f"Failed to select character: {str(e)}")


@pytest.mark.skip()
# Apply song filter
def test_apply_filter(driver):
    # Click on Filter button
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Filter').click()

    # Filter category and values selection
    song_filter_selection(driver, 'Mood', ['Sad', 'Happy', 'Sentimental'])
    time.sleep(0.5)
    song_filter_selection(driver, 'Artist', ['Sanam'])
    time.sleep(2)

    # Filter button action -> Apply/Clear
    filter_btn_selection(driver, 'Clear')


# Search song
def test_search_song(driver):
    # Search song
    song_name = 'Raat Kali'
    search_song(driver, song_name)
    time.sleep(1)

    # Close keyboard
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(519, 434)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()

    # Click on Start class button
    song_locator = f'//android.view.View[contains(@content-desc,"{song_name}")][1]/android.widget.ImageView[3]'
    wait_and_click(driver, AppiumBy.XPATH, value=song_locator)

    time.sleep(2)

    # Allow audio permission
    allow_permission = ('//android.widget.Button[@resource-id="com.android.permissioncontroller:id'
                        '/permission_allow_foreground_only_button"]')
    wait_and_click(driver, AppiumBy.XPATH, value=allow_permission)


# Star class
def test_start_class(driver):
    time.sleep(2)
    start_class_locator = 'Start'
    wait_and_click(driver, AppiumBy.ACCESSIBILITY_ID, value=start_class_locator)
