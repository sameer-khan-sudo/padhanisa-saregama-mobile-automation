import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

# from utils import click_button, click_terms_and_privacy
from utils.utils import click_button, click_skip_button, select_profile, perform_login, click_learn_to_sing, \
    select_mode, handle_skip_button, scroll_song_listing


# Click on 'Permission Allow' button
def test_handle_allow_button(driver):
    allow_button_xpath = ('//android.widget.Button[@resource-id="com.android.permissioncontroller:id'
                          '/permission_allow_button"]')
    click_button(driver, AppiumBy.XPATH, allow_button_xpath)

    # Click on 'Skip' button
    click_skip_button(driver)


# Login
def test_login(driver):
    perform_login(driver)


# Select profile
def test_select_profile(driver):
    select_profile(driver, 'Sameer Khan')

    # Click on 'Home' button
    home_locator = '//android.widget.ImageView[@content-desc="Home"]'
    click_button(driver, AppiumBy.XPATH, home_locator)


def test_click_on_learn_to_sing(driver):
    click_learn_to_sing(driver)


# Click on 'Learn Songs' tab
def test_click_on_learn_song_tab(driver):
    learn_to_sing_locator = '//android.widget.ImageView[starts-with(@content-desc,"Learn To Sing")]'
    click_button(driver, AppiumBy.XPATH, value=learn_to_sing_locator)


def test_scroll_down(driver):
    # Find the ScrollView
    scroll_view = driver.find_element(AppiumBy.XPATH, '//android.widget.ScrollView')

    # Get the dimensions of the ScrollView
    scroll_view_size = scroll_view.size
    scroll_view_location = scroll_view.location

    # Initialize variables for scrolling
    start_x = scroll_view_location['x'] + scroll_view_size['width'] // 2
    start_y = scroll_view_location['y'] + scroll_view_size['height'] * 0.8
    end_y = scroll_view_location['y'] + scroll_view_size['height'] * 0.2

    # Perform the scroll down action
    actions = ActionBuilder(driver)
    finger = PointerInput(interaction.POINTER_TOUCH, "finger")
    actions.add_pointer_input(finger)
    actions.pointer_action.move_to_location(start_x, start_y)
    actions.pointer_action.pointer_down()
    actions.pointer_action.move_to_location(start_x, end_y)
    actions.pointer_action.release()
    actions.perform()

    print("Scroll down action performed")

# Usage
# Assuming you have already initialized your Appium driver
# scroll_to_all_image_views(driver)

