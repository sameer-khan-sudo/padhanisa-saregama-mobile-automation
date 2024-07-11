# from utils import click_button, click_terms_and_privacy
from appium.webdriver.common.appiumby import AppiumBy

from tests.signed_in_flow.conftest import driver
# from utils import click_button, click_terms_and_privacy
from utils.utils import click_button, click_skip_button, select_profile, perform_login, \
    horizontal_category_scroll_search


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
    select_profile(driver, 'SAM')

    # Click on 'Home' button
    home_locator = '//android.widget.ImageView[@content-desc="Home"]'
    click_button(driver, AppiumBy.XPATH, home_locator)


# Click on 'Perform To Songs' tab
def test_perform_to_song(driver):
    perform_to_song_locator = ("//android.view.View[@content-desc=\"Perform To Songs\nRecord, share & get "
                               "certificates\"]")
    click_button(driver, AppiumBy.XPATH, value=perform_to_song_locator)

    # Usage example
    scroll_container = ('//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout'
                        '/android.view.View/android.view.View/android.view.View/android.view.View/android.widget'
                        '.HorizontalScrollView')


def test_scroll_category_and_search(driver):
    horizontal_category_scroll_search(driver, 2, 'Happy')

# @pytest.mark.skip
# Scroll the song list
# def test_scroll_listing(driver):
#     for i in range(2):
#         scroll_song_listing(driver, direction='down')
#         time.sleep(1)
#         scroll_song_listing(driver, direction='up')


# def test_search_song(driver):
#     # Search song
#     search_song(driver, 'Raat Kali')


# def test_click_on_sing_btn(driver):
#
#     # Click on Sing button
#     click_on_sing(driver)
#
#     sing_btn = '(//android.widget.ImageView[@content-desc="Sing"])[4]'
#     click_button(driver, AppiumBy.XPATH, sing_btn)
#     time.sleep(1)
#
#     audio_button_locator = "com.android.permissioncontroller:id/permission_allow_foreground_only_button"
#     el2 = driver.find_element(by=AppiumBy.ID, value=audio_button_locator)
#     el2.click()
#     time.sleep(10)
#
#     ele = WebDriverWait(driver,40).until(EC.p)
