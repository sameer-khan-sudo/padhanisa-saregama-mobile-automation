import time

from appium.webdriver.common.appiumby import AppiumBy

# from utils import wait_and_click, click_terms_and_privacy
from utils.utils import wait_and_click, click_skip_button, select_profile, perform_login, click_learn_to_sing, \
    scroll_song_list, select_mode, handle_skip_button


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
    select_profile(driver, 'Sameer Khan')

    # Click on 'Home' button
    home_locator = '//android.widget.ImageView[@content-desc="Home"]'
    wait_and_click(driver, AppiumBy.XPATH, home_locator)


def test_click_on_learn_to_sing(driver):
    click_learn_to_sing(driver)


# Click on 'Learn Songs' tab
def test_select_mode(driver):
    select_mode(driver, "Learn Songs")
    handle_skip_button(driver)
    time.sleep(1)


# @pytest.mark.skip(reason='TEST')
# # Scroll song list
def test_scroll_song_list(driver):
    scroll_song_list(driver)


# @pytest.mark.skip(reason='TEST')
# # Scroll song categories
# def test_horizontal_category_scroll(driver):
#     horizontal_category_scroll(driver)
#
#
# @pytest.mark.skip()
# # Search song
# def test_search_song(driver):
#     search_song(driver, 'Haal Kaisa')
#
#
# @pytest.mark.skip(reason="Skipping this test for now")
# # Play the song
# def test_play_song(driver):
#     play_song(driver)
#
#
# @pytest.mark.skip(reason="Skipping this test for now")
# # Seek the seekbar
# def test_scroll_song_seekbar(driver):
#     scroll_song_seekbar(driver)
#
#
# # @pytest.mark.skip(reason="Skipping this test for now")
# # Music control
# def test_music_control(driver):
#     music_control(driver, 'Pause')
#
#
# # @pytest.mark.skip(reason="Skipping this test for now")
# # Close the bottom player
# def test_close_song_preview(driver):
#     close_song_preview(driver)
#
#
# # Download lyrics
# @pytest.mark.skip(reason="Skipping this test for now")
# def test_download_lyrics(driver):
#     download_lyrics(driver)
#
#
# @pytest.mark.skip(reason="Skipping this test for now")
# # Click on Sing button
# def test_click_on_sing_button(driver):
#     click_on_sing(driver)
#
#
# # @pytest.mark.skip(reason="Skipping this test for now")
# # Selection audio language
# def test_select_audio_language(driver):
#     language_selection(driver, 'Hindi')
#
#
# @pytest.mark.skip(reason="Skipping this test for now")
# # Allow audio permission
# def test_allow_audio_permission(driver):
#     time.sleep(5)
#     allow_device_permissions(driver, 'audio')
#
#
# def test_filter_selection(driver):
#     def wait_and_click_by_locator(by, value):
#         wait_and_click(driver, getattr(AppiumBy, by.upper()), value=value)
#
#     def find_and_click(locator, target_text):
#         elements = driver.find_elements(by=AppiumBy.XPATH, value=locator)
#         for index, element in enumerate(elements, 1):
#             content_desc = element.get_attribute('content-desc')
#             if content_desc:
#                 print(f"{index}. {content_desc}")
#                 if content_desc == target_text:
#                     element.click()
#                     print(f"Clicked on: {content_desc}")
#                     return True
#         return False
#
#     # Click initial buttons
#     wait_and_click_by_locator('android_uiautomator', 'new UiSelector().className("android.widget.ImageView").instance(0)')
#     wait_and_click_by_locator('xpath', '//android.widget.ImageView[@content-desc="Filter"]')
#     wait_and_click_by_locator('xpath', '//android.view.View[@content-desc="Category"]')
#
#     # Find and click category options
#     category_options_locator = ('//android.view.View[@content-desc="Filter"]/android.view.View['
#                                 '2]/android.view.View//*[@content-desc]')
#     for category in ["Happy Songs"]:
#         find_and_click(category_options_locator, category)
#
#     # Click difficulty level and find options
#     wait_and_click_by_locator('xpath', '//android.view.View[@content-desc="Difficulty Level"]')
#     for level in ["Easy", "Medium"]:
#         find_and_click(category_options_locator, level)
#
#     # Click tags and find options
#     wait_and_click_by_locator('xpath', '//android.view.View[@content-desc="Tags"]')
#     for tags in ["All"]:
#         find_and_click(category_options_locator, tags)
#
#
# @pytest.mark.skip(reason="Skipping this test for now")
# def test_filter_selection_button(driver):
#     filter_selection = "Apply"
#     if filter_selection == "Apply":
#         apply_button_locator = '//android.widget.Button[@content-desc="Apply"]'
#         wait_and_click(driver, AppiumBy.XPATH, value=apply_button_locator)
#
#     elif filter_selection == "Clear":
#         apply_button_locator = '//android.widget.Button[@content-desc="Clear"]'
#         wait_and_click(driver, AppiumBy.XPATH, value=apply_button_locator)
