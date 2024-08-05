import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging


# REUSABLE METHOD TO CLICK A BUTTON IDENTIFIED BY ITS LOCATOR
def wait_and_click(driver, by, value, timeout=180):
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
    except TimeoutException:
        logging.error(f"Element with {by}='{value}' not clickable after {timeout} seconds")
        raise


# CLICK ON THE TERMS & CONDITIONS AND PRIVACY POLICY LINKS
def click_terms_and_privacy(driver):
    terms_and_conditions_id = "Terms & Conditions"
    wait_and_click(driver, AppiumBy.ACCESSIBILITY_ID, terms_and_conditions_id)
    time.sleep(1)

    back_button_xpath = '//android.widget.Button'
    wait_and_click(driver, AppiumBy.XPATH, back_button_xpath)

    privacy_policy_id = "Privacy Policy"
    wait_and_click(driver, AppiumBy.ACCESSIBILITY_ID, privacy_policy_id)
    time.sleep(1)

    wait_and_click(driver, AppiumBy.XPATH, back_button_xpath)


# HANDLE VOCAL TEST
def handle_skip_button(driver):
    try:
        skip_button_vocal = driver.find_element(by=AppiumBy.XPATH,
                                                value='//android.widget.ImageView[@content-desc="Skip "]')
        if skip_button_vocal.is_displayed():
            skip_button_vocal.click()
    except NoSuchElementException:
        pass


# CLICK ON THE SKIP & START BUTTON
def click_get_started_button(driver):
    skip_button_accessibility_id = 'Get Started'
    wait_and_click(driver, AppiumBy.ACCESSIBILITY_ID, skip_button_accessibility_id)


# CLICK ON THE BACK BUTTON
def click_back_button(driver):
    back_button_xpath = '//android.widget.Button'
    wait_and_click(driver, AppiumBy.XPATH, back_button_xpath)


# PERFORM LOGIN BY ENTERING THE MOBILE NUMBER AND CLICKING NECESSARY BUTTONS
def perform_login(driver):
    login_field_xpath = "//android.widget.EditText"
    login_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((AppiumBy.XPATH, login_field_xpath)))
    login_field.click()
    login_field.send_keys('8888888888')

    # Close the Keyboard
    screen_click(driver)

    # Tick the checkbox
    check_box_xpath = "//android.widget.CheckBox"
    wait_and_click(driver, AppiumBy.XPATH, check_box_xpath)

    get_otp_btn_locator = '//android.widget.ImageView[@content-desc="Get OTP"]'
    wait_and_click(driver, AppiumBy.XPATH, get_otp_btn_locator)


# SELECT USER PROFILE BY CLICKING ON THE APPROPRIATE ELEMENT
def select_profile(driver, user_name):
    user_profile_xpath = f"//*[contains(@content-desc, '{user_name}')]"

    # Wait until the element is present
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((AppiumBy.XPATH, user_profile_xpath)))

    # Find the element and click it
    driver.find_element(AppiumBy.XPATH, user_profile_xpath).click()


# CLICK ON 'LEARN TO SING' TAB
def click_learn_to_sing(driver):
    learn_to_sing_xpath = '//android.widget.ImageView[starts-with(@content-desc,"Learn To Sing")]'
    module_mode = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((AppiumBy.XPATH, learn_to_sing_xpath)))
    module_mode.click()


def select_mode(driver, mode):
    mode_locator = f'//android.widget.ImageView[contains(@content-desc,"{mode}")]'
    wait_and_click(driver, AppiumBy.XPATH, mode_locator)
    # time.sleep(1)


# Scroll song listing vertical
def scroll_song_listing(driver, list_container_locator, direction):
    # FIND THE CONTAINER ELEMENT
    container = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, value=list_container_locator)

    # GET THE DIMENSIONS OF THE CONTAINER
    container_rect = container.rect

    # CALCULATE START AND END POINTS FOR THE SCROLL
    start_x = container_rect['x'] + container_rect['width'] // 2

    if direction.lower() == 'down':
        start_y = container_rect['y'] + container_rect['height'] * 0.8
        end_y = container_rect['y'] + container_rect['height'] * 0.2
    elif direction.lower() == 'up':
        start_y = container_rect['y'] + container_rect['height'] * 0.2
        end_y = container_rect['y'] + container_rect['height'] * 0.8
    else:
        raise ValueError("Direction must be either 'up' or 'down'")

    # CREATE A POINTER INPUT OBJECT FOR TOUCH EVENTS
    finger = PointerInput(interaction.POINTER_TOUCH, "finger")

    # BUILD THE ACTION SEQUENCE
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=finger)

    # PERFORM THE SCROLL ACTION
    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
    actions.w3c_actions.pointer_action.release()

    # PERFORM THE ACTION
    actions.perform()


# Scroll vertical song category
def scroll_horizontally_to_end(driver, scroll_container, direction='right', max_scrolls=2):
    last_page_source = ""
    scroll_count = 0

    while scroll_count < max_scrolls:
        # Find the scroll container
        try:
            container = driver.find_element(AppiumBy.XPATH, scroll_container)
        except StaleElementReferenceException:
            print("The element is no longer attached to the DOM.")
            break

        # Get the dimensions of the container
        container_location = container.location
        container_size = container.size

        # Calculate start and end points for the scroll
        start_x = container_location['x'] + (container_size['width'] * (0.1 if direction == 'right' else 0.9))
        start_y = container_location['y'] + (container_size['height'] // 2)
        end_x = container_location['x'] + (container_size['width'] * (0.9 if direction == 'right' else 0.1))
        end_y = start_y

        # Create a PointerInput object for touch events
        finger = PointerInput(interaction.POINTER_TOUCH, "finger")

        # Build the action sequence
        actions = ActionBuilder(driver, mouse=finger)
        actions.pointer_action.move_to_location(start_x, start_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.move_to_location(end_x, end_y)
        actions.pointer_action.release()

        # Perform the action
        actions.perform()

        # Check if the page source has changed
        current_page_source = driver.page_source
        if current_page_source == last_page_source:
            print(f"Reached the end after {scroll_count + 1} scrolls.")
            break

        last_page_source = current_page_source
        scroll_count += 1

    if scroll_count == max_scrolls:
        print(f"Reached maximum number of scrolls ({max_scrolls}).")


# SEARCH SONG
def search_song(driver, song_name):
    # CLICK ON 'SEARCH' BUTTON
    song_name = song_name
    search_btn = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                     value="new UiSelector().className(\"android.widget.ImageView\").instance(0)")
    search_btn.click()
    search_field = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
    search_field.click()
    search_field.send_keys(song_name)


def play_song(driver):
    # RETRIEVE SONG LIST
    search_data = ('//android.view.View[@content-desc="Search Results"]/android.view.View['
                   '2]/android.view.View/android.view.View[@content-desc]')
    # ele = driver.find_elements(by=AppiumBy.XPATH, value=search_data)

    song_list = driver.find_elements(AppiumBy.XPATH, search_data)
    print('Songs count : ', len(song_list))

    # EXTRACT SONG TEXT
    song_data = [song.get_attribute('content-desc') for song in song_list]

    if len(song_list) >= 5:
        size = driver.get_window_size()

        # SCROLL TO THE END (SWIPE FROM BOTTOM TO TOP)
        start_y = size['height'] * 0.8
        end_y = size['height'] * 0.2
        driver.swipe(size['width'] // 2, start_y, size['width'] // 2, end_y, 800)

        driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollBackward()')
    else:
        pass

    for i, song_name in enumerate(song_data, start=1):
        print(f"{i}. {song_name}")
        print('index : ', i)
        print("-" * len(song_name))

    # PLAY THE SONG
    elements = driver.find_elements(by=AppiumBy.XPATH, value='//android.view.View/android.widget.ImageView[1]')
    if len(elements) >= 2:
        # CLICK ON THE SECOND ELEMENT (INDEX 1, AS LIST INDICES START AT 0)
        elements[1].click()
    else:
        print("Not enough elements found")


# SCROLL SONG SEEKBAR
def scroll_seekbar(driver, scroll_amount):
    # FIND THE SEEKBAR ELEMENT
    seekbar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.SeekBar[@content-desc]'))
    )

    # GET THE SEEKBAR'S LOCATION AND SIZE
    location = seekbar.location
    size = seekbar.size

    # CALCULATE START AND END POINTS FOR THE SWIPE
    start_x = location['x']
    end_x = start_x + (size['width'] * scroll_amount)  # % OF THE WIDTH
    y = location['y'] + (size['height'] // 2)

    # CREATE A POINTER INPUT OBJECT FOR TOUCH EVENTS
    finger = PointerInput(interaction.POINTER_TOUCH, "finger")

    # BUILD THE ACTION SEQUENCE
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=finger)
    actions.w3c_actions.pointer_action.move_to_location(start_x, y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(end_x, y)
    actions.w3c_actions.pointer_action.release()

    # PERFORM THE ACTION
    actions.perform()


# SONG CONTROLS PLAY/PAUSE
def music_control(driver, control):
    # time.sleep(3)

    song_control = control
    if song_control == 'Play':
        # PLAY BUTTON LOCATOR
        play_btn_locator = "(//android.widget.ImageView)[15]"
        wait_and_click(driver, AppiumBy.XPATH, play_btn_locator)

    elif song_control == 'Pause':
        # PAUSE BUTTON LOCATOR
        pause_btn_locator = "(//android.widget.ImageView)[15]"
        wait_and_click(driver, AppiumBy.XPATH, value=pause_btn_locator)


# CLOSE BOTTOM PLAYER SCREEN
def close_song_preview(driver):
    # CROSS BUTTON
    cross_btn_locator = '//android.view.View[@content-desc]/android.widget.Button'
    wait_and_click(driver, AppiumBy.XPATH, value=cross_btn_locator)


# DOWNLOAD LYRICS
def download_lyrics(driver):
    # LYRICS BUTTON LOCATOR
    lyrics_btn_locator = '(//android.widget.ImageView[@content-desc="Lyrics"])[1]'
    wait_and_click(driver, AppiumBy.XPATH, value=lyrics_btn_locator)

    #  ALLOW MEDIA PERMISSION
    allow_all_btn_xpath = ('//android.widget.Button[@resource-id="com.android.permissioncontroller:id'
                           '/permission_allow_all_button"]')
    wait_and_click(driver, AppiumBy.XPATH, value=allow_all_btn_xpath)

    # CLICK ON BACK BUTTON FROM PDF VIEW
    pdf_back_btn = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.ImageButton").instance(0)'
        ))
    )

    pdf_back_btn.click()


# CLICK ON SING BUTTON
def click_on_sing(driver):
    sing_btn_locator = '(//android.widget.ImageView[@content-desc="Sing"])[1]'
    wait_and_click(driver, AppiumBy.XPATH, value=sing_btn_locator)


# LANGUAGE SELECTION
def language_selection(driver, language_type):
    try:
        language_header = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (AppiumBy.XPATH, '//android.view.View[@content-desc="Choose Your Preferred Audio Language"]'))
        )

        proceed_btn_locator = '//android.widget.Button[@content-desc="Proceed"]'

        if language_header.is_displayed():
            if language_type == 'Hindi':
                locator = 'new UiSelector().className("android.widget.ImageView").instance(1)'
                wait_and_click(driver, AppiumBy.ANDROID_UIAUTOMATOR, locator)
                wait_and_click(driver, AppiumBy.XPATH, proceed_btn_locator)
            elif language_type == 'English':
                locator = 'new UiSelector().className("android.widget.ImageView").instance(0)'
                wait_and_click(driver, AppiumBy.ANDROID_UIAUTOMATOR, locator)
                wait_and_click(driver, AppiumBy.XPATH, proceed_btn_locator)

    except NoSuchElementException:
        print('Language selection is already done.')
    except Exception as e:
        print(f'Error occurred: {str(e)}')


# ALLOW NECESSARY DEVICE PERMISSIONS SUCH AS AUDIO AND VIDEO
def allow_device_permissions(driver, permission_type):
    audio_button_locator = "com.android.permissioncontroller:id/permission_allow_foreground_only_button"
    video_button_locator = "com.android.permissioncontroller:id/permission_allow_camera_button"

    if permission_type == 'audio' or permission_type == 'both':
        el2 = driver.find_element(by=AppiumBy.ID, value=audio_button_locator)
        el2.click()

    if permission_type == 'video' or permission_type == 'both':
        video_button = driver.find_element(by=AppiumBy.ID, value=video_button_locator)
        video_button.click()


# CLICK ON START BUTTON
def click_on_start_button(driver):
    start_button_xpath = '//android.widget.ImageView[@content-desc="Start"]'
    wait_and_click(driver, AppiumBy.XPATH, start_button_xpath)


# CLICK ON CONTINUE BUTTON
def click_on_continue_button(driver):
    continue_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Continue"))
    )
    continue_button.click()


# CLICK ON SCREEN
def screen_click(driver):
    # actions = ActionChains(driver)
    # actions.w3c_actions.pointer_action.move_to_location(492, 944).click()
    # actions.perform()
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(492, 944)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()


# CLICK ON PAUSE BUTTON
def click_on_pause_btn(driver):
    # Click on Pause button
    pause_btn_locator = '//android.view.View[@content-desc="Pause"]'
    wait_and_click(driver, AppiumBy.XPATH, value=pause_btn_locator)


def handle_setting(driver, setting_name, target_value):
    # setting_locator = f'//android.widget.ImageView[@content-desc="{setting_name}"]'
    setting_locator = f'new UiSelector().description("{setting_name}")'
    wait_and_click(driver, AppiumBy.ANDROID_UIAUTOMATOR, value=setting_locator)

    options_locator = ('//android.view.View[@content-desc]/android.view.View[2]/android.view.View//*['
                       '@content-desc]')

    elements = driver.find_elements(by=AppiumBy.XPATH, value=options_locator)
    for index, element in enumerate(elements, 1):
        content_desc_value = element.get_attribute('content-desc')
        if content_desc_value:
            print(f"{index}. {content_desc_value}")

            if content_desc_value == target_value:
                element.click()
                print(f"Clicked on: {content_desc_value}")
                break


def scroll_horizontal(driver, direction):
    scroll_container_locator = (AppiumBy.XPATH, '//android.widget.HorizontalScrollView')
    # Wait until the scroll container is visible
    scroll_container = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(scroll_container_locator)
    )
    container_location = scroll_container.location
    container_size = scroll_container.size

    if direction == 'right':
        start_x = container_location['x'] + (container_size['width'] * 0.9)
        end_x = container_location['x'] + (container_size['width'] * 0.1)
    elif direction == 'left':
        start_x = container_location['x'] + (container_size['width'] * 0.1)
        end_x = container_location['x'] + (container_size['width'] * 0.9)
    else:
        raise ValueError("Direction must be 'left' or 'right'")

    center_y = container_location['y'] + (container_size['height'] / 2)

    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(start_x, center_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(end_x, center_y)
    actions.w3c_actions.pointer_action.release()
    actions.perform()


# Close Keyboard

def tap_on_screen(driver):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(814, 805)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()


def select_songs_by_character(driver, target_char):
    scroll_bar_locator = (AppiumBy.XPATH, '//android.view.View[contains(@content-desc, "A\nB\nC")]')

    scroll_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located(scroll_bar_locator))

    char_list = scroll_bar.get_attribute('content-desc').split('\n')

    if target_char not in char_list:
        raise ValueError(f"Character '{target_char}' not found in the scroll bar")

    char_index = char_list.index(target_char)
    total_chars = len(char_list)

    location = scroll_bar.location
    size = scroll_bar.size

    x = location['x'] + size['width'] // 2
    y = location['y'] + (size['height'] * char_index // total_chars)

    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "finger"))

    (actions.w3c_actions.pointer_action
     .move_to_location(x, y)
     .pointer_down()
     .pause(0.1)
     .release())

    actions.perform()


def scroll_song_list(driver, direction):
    scroll_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.XPATH,
                                        '//android.view.View[@content-desc="A B C D E G H I K L M P R S T V W Y"]'))
    )

    # Get the location and size of the scroll bar
    location = scroll_bar.location
    size = scroll_bar.size

    # Calculate the coordinates
    start_x = location['x'] + (size['width'] // 2)

    if direction.lower() == 'down':
        start_y = location['y'] + 10
        end_y = location['y'] + size['height'] - 10
    elif direction.lower() == 'up':
        start_y = location['y'] + size['height'] - 10
        end_y = location['y'] + 10
    else:
        raise ValueError("Direction must be 'up' or 'down'")

    # Create a PointerInput object for touch events
    finger = PointerInput(interaction.POINTER_TOUCH, "finger")

    # Create an ActionChains object
    actions = ActionChains(driver)

    # Add actions to the chain
    actions.w3c_actions = ActionBuilder(driver, mouse=finger)
    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.5)  # Press and hold for 500ms

    steps = 20  # Number of steps for smooth scroll
    for i in range(1, steps + 1):
        if direction.lower() == 'down':
            new_y = start_y + (end_y - start_y) * i / steps
        else:  # 'up'
            new_y = start_y - (start_y - end_y) * i / steps

        actions.w3c_actions.pointer_action.move_to_location(start_x, new_y)
        actions.w3c_actions.pointer_action.pause(0.05)  # Short pause between movements

    # Release at the end
    actions.w3c_actions.pointer_action.release()

    # Perform the action
    actions.perform()

    if direction.lower() == 'up':
        scroll_bar.click()


# Difficulty Level Selection
def difficulty_level_selection(driver, level):
    mode = level
    level_locator = (f"//android.widget.FrameLayout[@resource-id='android:id/content']/android.widget.FrameLayout"
                     f"/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View["
                     f"5]//android.view.View[@content-desc='{mode}']")

    wait_and_click(driver, AppiumBy.XPATH, value=level_locator)


# Apply Song Filter
def song_filter_selection(driver, setting_name, target_values):
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{setting_name}")').click()

    target_values = list(target_values)
    clicked_values = []

    while target_values:
        elements = driver.find_elements(AppiumBy.XPATH,
                                        '//android.view.View[@content-desc]/android.view.View[2]/android.view.View//*[@content-desc]')
        for element in elements:
            content_desc = element.get_attribute('content-desc')
            if content_desc in target_values:
                element.click()
                clicked_values.append(content_desc)
                target_values.remove(content_desc)
                break
        else:
            break

    print(f"Clicked: {clicked_values}")
    print(f"Not found: {target_values}")


# Filter button selection
def filter_btn_selection(driver, btn_selection):
    if btn_selection == 'Apply':
        # Click on Apply button
        apply_btn_locator = '//android.widget.Button[@content-desc="Apply"]'
        wait_and_click(driver, AppiumBy.XPATH, apply_btn_locator)
    elif btn_selection == 'Clear':
        # Click on Clear button
        clear_btn_locator = '//android.widget.Button[@content-desc="Clear"]'
        wait_and_click(driver, AppiumBy.XPATH, clear_btn_locator)

    print(f"Button selected: {btn_selection}")


# Get video time and wait for video completion
def wait_for_video_completion(driver):
    try:
        video_timer = driver.find_element(by=AppiumBy.ID, value='com.saregama.edutech.uat:id/tv_total_time')
        get_video_timer = video_timer.get_attribute('text')
        print(f'Video timer : {get_video_timer}')

        minutes, seconds = map(int, get_video_timer.split(':'))
        total_seconds = minutes * 60 + seconds

        print(f'Waiting for video to complete. Duration: {total_seconds} seconds')
        time.sleep(total_seconds)
        print("Video playback time completed")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Scroll the report to Save button
def scroll_to_bottom(driver, max_attempts=3, timeout=2):
    # Scroll indicator
    scroll_indicator_locator = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.ImageView").instance(10)'
    )
    # Save button locator
    save_button_locator = (AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="Save"]')

    for _ in range(max_attempts):
        try:
            # Check if the Save button is already visible
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(save_button_locator))
            print("Save button found!")
            return True
        except TimeoutException:
            # If Save button is not found, click on the scroll indicator
            try:
                scroll_indicator = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located(scroll_indicator_locator)
                )
                scroll_indicator.click()
                print("Clicked on scroll indicator")
            except TimeoutException:
                print("Scroll indicator not found")
                return False

    print("Save button not found after maximum attempts")
    return False


# Report actions -> Save, Done & Retry
def report_actions(driver, action_type):
    btn_locator = f'{action_type}'
    wait_and_click(driver, AppiumBy.ACCESSIBILITY_ID, value=btn_locator)


# Preview recording action Save / Skip
def preview_recording_action(driver, action_type):
    btn_locator = f'{action_type}'
    wait_and_click(driver, AppiumBy.ACCESSIBILITY_ID, value=btn_locator)


def sdk_filter_selection(driver, setting_name, target_values):
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{setting_name}")').click()

    target_values = list(target_values)
    clicked_values = []

    while target_values:
        elements = driver.find_elements(AppiumBy.XPATH,
                                        '//android.view.View[@content-desc]/android.view.View[2]/android.view.View//*[@content-desc]')
        for element in elements:
            content_desc = element.get_attribute('content-desc')
            if content_desc in target_values:
                element.click()
                clicked_values.append(content_desc)
                target_values.remove(content_desc)
                break
        else:
            break

    print(f"Clicked: {clicked_values}")
    print(f"Not found: {target_values}")
