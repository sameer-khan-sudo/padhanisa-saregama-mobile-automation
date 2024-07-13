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
from urllib3.util import wait

from utils.utils import click_skip_button, select_profile, perform_login, screen_click, wait_and_click, \
    language_selection


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

    # More screen locator
    time.sleep(1)
    scroll_element_xpath = 'new UiSelector().className("android.view.View").instance(8)'
    scroll_element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_element_xpath)

    # Perform the scroll down action
    driver.execute_script('mobile: scrollGesture', {
        'elementId': scroll_element.id,
        'direction': 'down',
        'percent': 0.7
    })


# Click on 'Help Videos'
def test_click_on_help_videos(driver):
    locator = '//android.widget.ImageView[contains(@content-desc,"Help Videos")]'
    wait_and_click(driver, AppiumBy.XPATH, locator)


# # Scroll the video list and get the text
# def test_scroll_get_text(driver):
#     screen_size = driver.get_window_size()
#     start_x = screen_size['width'] * 0.5
#     start_y = screen_size['height'] * 0.8
#     end_y = screen_size['height'] * 0.2
#
#     all_texts = set()
#     count = 1
#
#
#     while True:
#         # Find elements and print their texts
#         wait = WebDriverWait(driver, 40)
#         videos_locator = wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH, '//android.widget.ImageView['
#                                                                                          '@content-desc]')))
#         new_text_found = False
#         for element in videos_locator:
#             global text = element.get_attribute('content-desc')
#             if text and text not in all_texts:
#                 print(f"{count}. {text}")
#                 all_texts.add(text)
#                 new_text_found = True
#                 count += 1
#                 time.sleep(2)
#                 # if text == desired_text:
#                 #     ele = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH,
#                 #                                                  f'//android.widget.ImageView[@content-desc="{desired_text}"]/android.view.View')))
#                 #     ele.click()
#                 #     return  # Exit the function after clicking the desired element
#
#         # If no new texts were found, break the loop
#         if not new_text_found:
#             break
#
#         # Perform scroll down action
#         actions = ActionChains(driver)
#         actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
#         actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
#         actions.w3c_actions.pointer_action.pointer_down()
#         actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
#         actions.w3c_actions.pointer_action.release()
#         actions.perform()
#
#
# def test_click_on_video(driver):
#     if text == desired_text:
#         ele = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH,
#                                                      f'//android.widget.ImageView[@content-desc="{desired_text}"]/android.view.View')))
#         ele.click()
#         return  # Exit the function after clicking the desired element
#     # Search
#     # concept
#     # video
#

# Define global variables at the module level
video_name = 'Test'
desired_element_found = False


# @pytest.mark.skip()
def test_scroll_get_text(driver):
    screen_size = driver.get_window_size()
    start_x = screen_size['width'] * 0.5
    start_y = screen_size['height'] * 0.8
    end_y = screen_size['height'] * 0.2

    all_texts = set()
    count = 1

    while True:
        # Find elements and print their texts
        videos_locator = WebDriverWait(driver, 40).until(
            EC.presence_of_all_elements_located((AppiumBy.XPATH, '//android.widget.ImageView[@content-desc]')))
        new_text_found = False
        for element in videos_locator:
            text = element.get_attribute('content-desc')
            if text and text not in all_texts:
                print(f"{count}. {text}")
                all_texts.add(text)
                new_text_found = True
                count += 1
                time.sleep(2)
                if text == video_name:
                    ele = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((AppiumBy.XPATH,
                                                                                      f'//android.widget.ImageView['
                                                                                      f'@content-desc="'
                                                                                      f'{video_name}"]/android.view.View')))
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


# @pytest.mark.skip()
def test_click_on_video(driver):
    # Use the global variables directly if needed
    if desired_element_found:
        ele = WebDriverWait(driver, 40).until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, f'//android.widget.ImageView[@content-desc="{video_name}"]/android.view.View')))
        ele.click()
        return  # Exit the function after clicking the desired element

    language_selection(driver,'Hindi')


@pytest.mark.skip()
def test_search_help_video(driver):
    search_field_locator = '//android.widget.EditText'
    wait_and_click(driver, AppiumBy.XPATH, search_field_locator)

    # # Enter the Video name
    fill_data = driver.find_element(by=AppiumBy.XPATH, value=search_field_locator)
    fill_data.send_keys(video_name)

    # CLOSE THE KEYBOARD
    keyboard_down_locator = 'new UiSelector().className("android.widget.FrameLayout").instance(0)'
    keyboard_down = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, keyboard_down_locator)))
    keyboard_down.click()

    # Search video locator
    search_video_locator = (
        f"//android.widget.ImageView[contains(@content-desc, '{video_name}')]/android.view.View")

    # No result found locator
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
