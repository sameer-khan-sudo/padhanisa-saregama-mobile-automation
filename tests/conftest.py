import pytest
from appium import webdriver
from appium.options.common import AppiumOptions


@pytest.fixture(scope="module")
def driver():
    caps = {
        'platformName': 'Android',
        'platformVersion': '14.0',
        'deviceName': 'Pixel',
        'appPackage': 'com.saregama.edutech.uat',
        'appActivity': 'com.saregama.edutech.MainActivity',
        'automationName': 'UiAutomator2',
        'noReset': False,
        "appium:ensureWebviewsHavePages": True,
        "appium:nativeWebScreenshot": True,
        "appium:newCommandTimeout": 6000,
        "appium:connectHardwareKeyboard": True
    }
    url = 'http://localhost:4723'
    driver = webdriver.Remote(url, options=AppiumOptions().load_capabilities(caps))
    driver.implicitly_wait(10)
    yield driver
    # driver.quit()
