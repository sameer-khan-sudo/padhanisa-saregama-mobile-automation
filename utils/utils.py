import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# REUSABLE METHOD TO CLICK A BUTTON IDENTIFIED BY ITS LOCATOR
def wait_and_click(driver, by, value, timeout=40):
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.element_to_be_clickable((by, value)))
    element.click()


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
def click_skip_button(driver):
    skip_button_accessibility_id = 'Skip & Start'
    wait_and_click(driver, AppiumBy.ACCESSIBILITY_ID, skip_button_accessibility_id)


# CLICK ON THE BACK BUTTON
def click_back_button(driver):
    back_button_xpath = '//android.widget.Button'
    wait_and_click(driver, AppiumBy.XPATH, back_button_xpath)


# PERFORM LOGIN BY ENTERING THE MOBILE NUMBER AND CLICKING NECESSARY BUTTONS
def perform_login(driver):
    more_locator = '//android.widget.ImageView[@content-desc="More"]'
    wait_and_click(driver, AppiumBy.XPATH, more_locator)

    sign_in_locator = '//android.view.View[@content-desc="Sign In"]'
    wait_and_click(driver, AppiumBy.XPATH, sign_in_locator)

    login_field_xpath = "//android.widget.EditText"
    login_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((AppiumBy.XPATH, login_field_xpath)))
    login_field.click()
    login_field.send_keys('8888888888')

    # CLOSE THE KEYBOARD
    keyboard_down = driver.find_element(by=AppiumBy.XPATH,
                                        value='//android.view.View[starts-with(@content-desc, "Padhanisa")]')
    keyboard_down.click()

    check_box_xpath = "//android.widget.CheckBox"
    wait_and_click(driver, AppiumBy.XPATH, check_box_xpath)

    next_button_xpath = '//android.widget.ImageView[@content-desc="Next"]'
    wait_and_click(driver, AppiumBy.XPATH, next_button_xpath)


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
    mode_locator = f'//android.widget.ImageView[starts-with(@content-desc,{mode})]'
    wait_and_click(driver, AppiumBy.XPATH, mode_locator)
    time.sleep(1)


# Scroll song listing vertical
def scroll_song_listing(driver, list_container_locator, direction):
    # FIND THE CONTAINER ELEMENT
    container = driver.find_element(AppiumBy.XPATH, value=list_container_locator)

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
    time.sleep(1)
    # CLICK ON 'SEARCH' BUTTON
    searchbar_icon_locator = "new UiSelector().className(\"android.widget.ImageView\").instance(0)"
    wait_and_click(driver, AppiumBy.ANDROID_UIAUTOMATOR, value=searchbar_icon_locator)

    search_field = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                       value="new UiSelector().className(\"android.widget.ImageView\").instance(0)")
    search_field.click()
    el2 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
    el2.click()
    search_field.send_keys(song_name)

    # CLOSE THE KEYBOARD
    keyboard_down = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                        value='new UiSelector().className("android.view.View").instance(10)')
    keyboard_down.click()


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
    actions = ActionChains(driver)
    actions.w3c_actions.pointer_action.move_to_location(1113, 402).click()
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