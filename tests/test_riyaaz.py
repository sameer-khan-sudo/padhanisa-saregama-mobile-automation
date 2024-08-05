import json
import time

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.actions import interaction

from utils.utils import select_mode, search_song, wait_for_video_completion, scroll_to_bottom, report_actions
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
    # Select Riyaaz module
    select_mode(driver, 'Riyaaz')


# Select workout type
workout_type = 'Range'


# Scroll to a selected workout type
def test_scroll_to_specific_workout(driver):
    # Locator for the specific workout we're looking for
    workout_locator = f'new UiSelector().description("{workout_type}")'

    try:
        # Use UiScrollable to scroll to the specific workout
        element = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView('
            f'{workout_locator})'
        )
        print(f"'{workout_type}' found. Stopping scroll.")
        return element
    except TimeoutException:
        print(f"'{workout_type}' not found after maximum number of attempts.")
        return None


# Scroll the content inside the selected workout
def test_perform_workout(driver):
    print(f"Attempting to scroll within the {workout_type} workout container")

    # Locator for the specific workout container
    container_locator = f'//android.view.View[@content-desc="{workout_type}"]/android.view.View/android.view.View'

    try:
        # Wait for the workout container to be visible
        container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, container_locator))
        )
    except TimeoutException:
        print(f"Could not find the container for {workout_type}")
        return

    if len(container_locator) > 3:
        # Calculate swipe coordinates within the container
        container_rect = container.rect
        start_x = container_rect['x'] + container_rect['width'] * 0.9
        end_x = container_rect['x'] + container_rect['width'] * 0.1
        y = container_rect['y'] + container_rect['height'] * 0.5

        # Perform horizontal swipes within the workout container
        for _ in range(3):
            driver.swipe(start_x, y, end_x, y, 100)

        print(f"Completed scrolling within the {workout_type} workout container")


# Click on See all button if the button is present
def test_click_see_all(driver):
    # Try to find the 'See All' button
    try:
        see_all_btn_locator = '//android.view.View[@content-desc="See All"]'

        # Click on 'See All' button
        wait_and_click(driver, AppiumBy.XPATH, value=see_all_btn_locator)
        print("Successfully clicked the 'See All' button.")

    except NoSuchElementException:

        # Handle the case where the 'See All' button is not found
        print("The 'See All' button is not present. Failing the test case.")
        # You can raise an exception to explicitly fail the test
        raise Exception("The 'See All' button is not present.")


@pytest.mark.skip()
#  Scroll down and get all the see all content text
def test_scroll_and_get_see_all_content(driver, direction='down'):
    all_texts = set()
    count = 1

    while True:
        # Find elements and print their texts
        wait = WebDriverWait(driver, 4)
        elements = wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,
                                                                   '//android.widget.FrameLayout['
                                                                   '@resource-id="android:id/content"]/android.widget'
                                                                   '.FrameLayout/android.view'
                                                                   '.View/android.view.View/android.view.View/android'
                                                                   '.view.View/android.view.View/android.view.View['
                                                                   '2]/android.view.View//*[@content-desc]')))
        new_text_found = False
        for element in elements:
            text = element.get_attribute('content-desc')
            if text and text not in all_texts:
                if direction == 'down':  # Only print when direction is down
                    print(f"{count}. {text}")
                all_texts.add(text)
                new_text_found = True
                count += 1

        # If no new texts were found, break the loop
        if not new_text_found:
            break

        # Perform scroll action based on the direction parameter
        try:
            if direction == 'down':
                driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                    'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollForward()')
            elif direction == 'up':
                driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                    'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollBackward()')
            else:
                raise ValueError("Invalid scroll direction. Use 'up' or 'down'.")
        except TimeoutException:
            print("Reached the end of the scrollable view.")
            break


# Search the content

video_name = 'Singing High Notes - Fast Speed '


def test_search_workout_video(driver):
    # Search video
    search_song(driver, video_name)
    time.sleep(2)

    # Close keyboard
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(519, 434)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()


def test_play_video(driver):
    # Click on searched video
    video_locator = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=f"{video_name}")
    video_locator.click()


def test_video_session(driver):
    sdk_identification_locator = driver.find_element(by=AppiumBy.ID,
                                                     value='com.android.permissioncontroller:id/grant_dialog')
    if sdk_identification_locator.is_displayed():
        el1 = driver.find_element(by=AppiumBy.ID,
                                  value="com.android.permissioncontroller:id/permission_allow_foreground_only_button")
        el1.click()
        time.sleep(2)

        # Tap on the screen
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(444, 155)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        # Click on Play button
        click_btn_locator = 'com.saregama.edutech.uat:id/ib_play'
        wait_and_click(driver, AppiumBy.ID, click_btn_locator)

        # Get the video time and wait for completion
        wait_for_video_completion(driver)
        # el1 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
        #                           value="new UiSelector().className(\"android.widget.ImageView\").instance(10)")
        # el1.click()


def test_scroll_report(driver):
    scroll_to_bottom(driver)

# Report actions -> Save, Done & Retry
def test_report_btn_action(driver):
    report_actions(driver, 'Save')
    report_actions(driver, 'Done')
