import time

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.utils import select_songs_by_character, scroll_song_list, difficulty_level_selection, \
    song_filter_selection, filter_btn_selection, search_song, wait_for_video_completion, scroll_to_bottom, \
    report_actions, preview_recording_action
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


# Click on Sing A Song module
def test_select_module(driver):
    # Select sing a song/practice module
    sing_a_song_locator = '//android.view.View[contains(@content-desc,"Sing A Song")]'
    wait_and_click(driver, AppiumBy.XPATH, value=sing_a_song_locator)


# Difficulty level selection
@pytest.mark.skip()
def test_level_selection(driver):
    mode = 'Easy'
    difficulty_level_selection(driver, mode)
    time.sleep(2)


# Perform song list scroll
@pytest.mark.skip()
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


# Apply song filter
@pytest.mark.skip()
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
    song_name = 'Alvida'
    search_song(driver, song_name)
    time.sleep(2)

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


# Get the songs part name
@pytest.fixture
def get_song_parts(driver):
    # Wait for elements to be visible and store them
    parts = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((AppiumBy.XPATH, '//android.widget.ScrollView/android.view.View'))
    )

    # Print song parts
    for index, song_part_name in enumerate(parts, 1):
        part_names = song_part_name.get_attribute('content-desc')
        print(f'{index}. Song Part Name : {part_names}')
    print(f"Number of song parts: {len(parts)}")

    return parts


# Select part and play
def test_select_song_part(driver, get_song_parts):
    selected_part_name = "Mudkda 2"

    for song_part_name in get_song_parts:
        part_names = song_part_name.get_attribute('content-desc')
        if selected_part_name in part_names:
            # Perform action on the selected part (e.g., click)
            song_part_name.click()
            print(f"Selected '{selected_part_name}' part")
            break
    else:
        print(f"'{selected_part_name}' part not found")
        assert False, f"'{selected_part_name}' part was not found in the song parts"


# Allow audio and record permissions
def test_allow_permissions(driver):
    el1 = driver.find_element(by=AppiumBy.ID,
                              value="com.android.permissioncontroller:id/permission_allow_foreground_only_button")
    el1.click()
    time.sleep(2)
    el2 = driver.find_element(by=AppiumBy.ID,
                              value="com.android.permissioncontroller:id/permission_allow_foreground_only_button")
    el2.click()

    # Turn off the video
    video_btn_locator = "com.saregama.edutech.uat:id/ib_camera_on_off_toggle"
    wait_and_click(driver, AppiumBy.ID, value=video_btn_locator)

    # Click on Next button
    next_btn_locator = "com.saregama.edutech.uat:id/btn_next"
    wait_and_click(driver, AppiumBy.ID, value=next_btn_locator)


# Set active video settings
def test_select_settings_and_play_video(driver):
    # Click on Next button for 4 times
    settings_next_btn = 'com.saregama.edutech.uat:id/btn_next'

    for click in range(4):
        wait_and_click(driver, AppiumBy.ID, value=settings_next_btn)

    time.sleep(3)


# Active video play
def test_active_session(driver):
    # Tap on the screen
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(444, 155).pointer_down().pause(0.1).release()
    actions.perform()

    # Click on Play button
    wait_and_click(driver, AppiumBy.ID, 'com.saregama.edutech.uat:id/ib_play')

    # Get the video time and wait for completion
    try:
        video_timer = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.saregama.edutech.uat:id/tv_total_time'))
        )
        get_video_timer = video_timer.get_attribute('text')
        print(f'Video timer: {get_video_timer}')

        minutes, seconds = map(int, get_video_timer.split(':'))
        total_seconds = minutes * 60 + seconds

        print(f'Waiting for video to complete. Duration: {total_seconds} seconds')
        time.sleep(total_seconds)
        print("Video playback time completed")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
