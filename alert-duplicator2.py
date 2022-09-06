import os
import re
import time
import sys
from selenium import webdriver
from selenium.common import exceptions
from selenium.common.exceptions import WebDriverException, ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import logging
from webdriver_manager.chrome import ChromeDriverManager
import json
import requests

os.environ['PATH'] += r"C:/SeleniumDrivers"
os.environ['WDM_LOG_LEVEL'] = '0'
options = Options()
options.add_argument(r"--user-data-dir=C:\Users\Corbin\AppData\Local\Google\Chrome\User Data")
options.add_argument(r'--profile-directory=Profile 2')
options.add_argument("window-size=1920x1080")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.set_capability('goog:loggingPrefs', {'performance': 'ALL', 'browser': 'ALL'})
options.add_experimental_option("detach", True)
wait_duration = 5


class DuplicateAlertSettings(object):

    def __init__(self):
        self.driver = None
        self.platform_name = None
        self.language = None
        self.alert_settings = None
        self.start_time = None
        self.init_time = None
        self.theme_name = None
        self.username = None

    def start(self):
        # Launch webdriver to Streamlabs Alert Box Page
        logging.basicConfig(filename='alert-duplicator.log', encoding='utf-8', level=logging.INFO)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def launch_alert_box(self):
        driver = self.driver
        driver.get('https://streamlabs.com/dashboard#/alertbox')
        driver.maximize_window()
        time.sleep(2)

    def assert_platforms(self):
        driver = self.driver
        self.platform_name = driver.find_element(By.XPATH, "(//div[@class='top-nav__item-text'])[1]").get_attribute('innerHTML').split("\n", 2)[1].strip()
        self.language = driver.find_element(By.XPATH, "(//div[@class='top-nav__item-text'])[2]").get_attribute('innerHTML').split("\n", 2)[1].strip()

        if self.language != 'English':
            # Navigate to dropdown and switch platforms to the event
            header_elem = driver.find_element(By.XPATH, "//nav[@role='navigation']")
            driver.execute_script("arguments[0].style.display = 'Block';", header_elem)
            driver.implicitly_wait(wait_duration)
            user_dropdown = driver.find_element(By.XPATH, "//div[@class='s-pane-dropdown top-nav__item top-nav-user']")
            user_dropdown.click()
            driver.implicitly_wait(wait_duration)
            lang_dropdown = driver.find_element(By.XPATH, "(//div[@class='s-pane-dropdown top-nav__lang-menu']/div[1])[1]")
            lang_dropdown.click()
            driver.implicitly_wait(wait_duration)
            lang = driver.find_element(By.XPATH, "//div[@class='s-pane-dropdown top-nav__lang-menu']/div[1]/following-sibling::div/div/a[contains(text(), 'English')]")
            lang.click()
            self.language = 'English'
            print(f"--- Language switched to English ---")
            logging.info(f"--- Language switched to English ---")
            time.sleep(2)

    def get_widgetthemes(self):
        driver = self.driver
        driver.get('https://streamlabs.com/dashboard#/widgetthemes')
        time.sleep(8)

        widgetthemes_list = driver.find_elements(By.XPATH, "//div[@class='content-row__group']/h4")
        for i in widgetthemes_list:
            inner_name = i.get_attribute('innerHTML')

            print('a.duplicate_settings("' + inner_name + '", False, False, False, False, True, False)')
            # print(inner_name)

    def duplicate_settings(self, desired_theme_name, streamlabs, twitch, youtube, facebook, trovo, thirdparty):
        driver = self.driver
        driver.implicitly_wait(wait_duration)
        self.init_time = time.time()
        self.theme_name = driver.find_element(By.XPATH, "//span[@class='theme-name']").text

        if desired_theme_name != 'active':
            if self.theme_name != desired_theme_name:
                self.switch_themes(desired_theme_name)

        self.get_settings()

        if streamlabs:
            # self.import_event('Streamlabs', 'Donations')
            self.import_event('Streamlabs', 'Merch')
            self.import_event('Streamlabs', 'Cloudbot Redemption')
            self.import_event('Streamlabs', 'Streamlabs Prime Gift')
            self.import_event('Streamlabs', 'Streamlabs Charity Donations')

        if twitch:
            self.import_event('Twitch', 'Follows')
            self.import_event('Twitch', 'Subscriptions')
            self.import_event('Twitch', 'Hosts')
            self.import_event('Twitch', 'Bits')
            self.import_event('Twitch', 'Raids')

        if youtube:
            self.import_event('YouTube', 'Subscribers')
            self.import_event('YouTube', 'Members')
            self.import_event('YouTube', 'Super Chats')

        if facebook:
            self.import_event('Facebook', 'Follows')
            self.import_event('Facebook', 'Stars')
            self.import_event('Facebook', 'Likes')
            self.import_event('Facebook', 'Supports')
            self.import_event('Facebook', 'Support Gifters')
            self.import_event('Facebook', 'Shares')

        if trovo:
            self.import_event('Trovo', 'Follows')
            self.import_event('Trovo', 'Subscriptions')
            self.import_event('Trovo', 'Raids')

        if thirdparty:
            self.import_event('Third Party', 'Pledges')
            self.import_event('Third Party', 'Sponsored Campaign')
            self.import_event('Third Party', 'Charity Streaming Donations')
            self.import_event('Third Party', 'Extra Life Donations')
            self.import_event('Third Party', 'Tiltify Donations')
            self.import_event('Third Party', 'Treats')
            self.import_event('Third Party', 'JustGiving')

        total_time = round(time.time() - self.init_time, 2)
        print(f"'{self.theme_name}' Theme events updated. [{total_time}s]")
        logging.info(f"'{self.theme_name}' Theme events updated. [{total_time}s]")

    def duplicate_settings_request(self, desired_theme_name, streamlabs, twitch, youtube, facebook, trovo, thirdparty):
        driver = self.driver
        driver.implicitly_wait(wait_duration)
        self.init_time = time.time()
        self.theme_name = driver.find_element(By.XPATH, "//span[@class='theme-name']").text

        if desired_theme_name != 'active':
            if self.theme_name != desired_theme_name:
                self.switch_themes(desired_theme_name)

        # self.alert_settings['settings']
        # self.get_settings_request()

        # json_dict = {'trovo_raid_image_href': 'https://test.com/test.png'}
        # cookies_dict = {'sl-ab-t': 'B', 'slobs_user': 'eyJpdiI6InlpeGQ4XC9pMXJMWUhMUjd4NUk0dndBPT0iLCJ2YWx1ZSI6IlBwcXdteU1JQTNwNkxmek9YcElhOGc9PSIsIm1hYyI6ImVjY2U2ODBlODc3Y2MyY2UzMTNjZTBmNjEyOTY2NGUyM2NmNjUzODg2OWEyYWUxMDVmZDgxNWM2ZjMxZGI1MDUifQ==', '__sla-uuid': '4939230e-1e94-428f-b2f2-ae33e061c9bd', '__stripe_mid': '0253932f-bc5c-4a15-8f32-608440a079f35fd61e', 'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Aug+23+2022+20:07:10+GMT-0400+(Eastern+Daylight+Time)&version=6.33.0&isIABGlobal=false&hosts=&consentId=90fceeb6-e5e6-4714-990f-4d9af3ed998f&interactionCount=1&landingPath=NotLandingPage&groups=C0001:1,C0002:1,C0003:1,C0004:0&AwaitingReconsent=false', '__stripe_sid': '042aac0c-f0c5-4a1b-a75a-f7eb6ee8e4a311a6b5', 'intercom-session-h78qaj1s': 'SEI3aDVhQ1Z2clZZZHFmNHJ3VFNDbjFlMnpHdUtlTFErclNtcXEzMGVoQ21PNWlUY2dGdnZpR08zVkhCemZZMC0tOUo4UDhUOWhadCtKUzZRNGhpMnV4dz09--f68a94f2e5d022274210cd13a2a86301b6b20b17', 'XSRF-TOKEN': 'eyJpdiI6IkpFTmk4VlwvRG5WSXpWemZsc2pqdzZnPT0iLCJ2YWx1ZSI6IlkyYUZpbEkyYkJIZnEyWVFIeWVCTk1LaG83cnBIQnlFaW5oVUZ5VFk0cGRqUXRYc3o5R2tqdWE3RmlOR2xwNTErQnJKVlc5Z3N3WGZSSjVRUmlDZGF3PT0iLCJtYWMiOiIzMjBiZDMxZDhiMDNjMmYxMmMzZWY3YzkxNDQ5MWM4Yzk2OTFjNzVjY2Y0ZWE0OGI5OWRlMWIyMmVjMjY0NmZmIn0=', 'slsid': 'eyJpdiI6ImNcL29oN1VoSk1tRE1yMloxTHV6NjV3PT0iLCJ2YWx1ZSI6IlpSTndxVUd6KzlWWFwvVFZNNjZQSlZQRVgxMVh0QXRjWFBKUGVPN2ZER0h3RnhpXC9KVko4XC9rSFV2T0Z5Q1F4T2NMRzNMSVRFbmdOZ2ljSVdsODM4VkZRPT0iLCJtYWMiOiI1MWEzN2JlNzNlZGM2NmZhODcyZDI4M2Y3OTI2MTFkNzJmYjFjMTNmYmVkNTEwOWZhZjUwODQ1YTg4Nzg4OTc2In0=' }
        # x = requests.post('https://streamlabs.com/api/v5/widget/alertbox', json=json_dict, cookies=cookies_dict)
        # print(x.text)
        headers_dict = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': 'sl-ab-t=B; slobs_user=eyJpdiI6InlpeGQ4XC9pMXJMWUhMUjd4NUk0dndBPT0iLCJ2YWx1ZSI6IlBwcXdteU1JQTNwNkxmek9YcElhOGc9PSIsIm1hYyI6ImVjY2U2ODBlODc3Y2MyY2UzMTNjZTBmNjEyOTY2NGUyM2NmNjUzODg2OWEyYWUxMDVmZDgxNWM2ZjMxZGI1MDUifQ%3D%3D; __sla-uuid=4939230e-1e94-428f-b2f2-ae33e061c9bd; __stripe_mid=0253932f-bc5c-4a15-8f32-608440a079f35fd61e; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Aug+23+2022+20%3A07%3A10+GMT-0400+(Eastern+Daylight+Time)&version=6.33.0&isIABGlobal=false&hosts=&consentId=90fceeb6-e5e6-4714-990f-4d9af3ed998f&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A0&AwaitingReconsent=false; __stripe_sid=042aac0c-f0c5-4a1b-a75a-f7eb6ee8e4a311a6b5; intercom-session-h78qaj1s=c3N2eUh4ZGJhSTcrQzR2Z3YwTTdSMXRDVnhEenhpbE1zcGJJNnVhSGxFd2dyazRvaFlWU3IvRXJoUUlPZmpQaC0tQ0Y4N2o2c0FyQVRBYzM2ZFNEbklKQT09--31884645f2d03efe97ff10a25d3e202868b5a7ed; XSRF-TOKEN=eyJpdiI6IkxlRTJTR0VSSUpFQnMzQ0hMbGlEeVE9PSIsInZhbHVlIjoiQUhxNmJSd0pDejd3eG5uNkNCMm9Id0tPcDVoaTNOa01LNGFZYTJxcG8ybWt2ZkFWbVpcLzZUOWNmaVVzczRPd0Nwb1A1SGF1Q1Jia2VudEV5aXg3V3dnPT0iLCJtYWMiOiJiNjJmMjkzYmEyMDc2NDUyMDNjZjJhMTRiNGE2NTlkMmJkMTY5OGE5MGVmYzE2YmExMWIwZWQ2NmIzYmViZjY2In0%3D; slsid=eyJpdiI6IldZSCtHcGl3OXZFejR1cjZRTVJCZ3c9PSIsInZhbHVlIjoicERNSW1TVmxVMGtIajJnandSQnBkZWlVU1NEWitKazVZdFl3U21qV1RyeTd2d2hvVnNJZ0JoVThGMGUydjR3REt4UmR6T3JyeDRESmtpYjdlRjYzN1E9PSIsIm1hYyI6IjMzYWVlNjE2ZGQwOTA3OTAzNzQ2MWIzODM5ZTA2NGYzY2Y1OGQ2NTU2OTZjODYwYzQ3ODA0MWEzOTkzOThmNGYifQ%3D%3D',
            'dnt': '1',
            'referer': 'https://streamlabs.com/dashboard',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'x-csrf-token': 'OebWpr7OnHbk4rLMm36ZKeWKC9ShgwIGmvDQLahK',
            'x-requested-with': 'XMLHttpRequest'
        }
        y = requests.get('https://streamlabs.com/api/v5/widget/alertbox', headers=headers_dict)
        print(y.text)

        total_time = round(time.time() - self.init_time, 2)
        print(f"'{self.theme_name}' Theme events updated. [{total_time}s]")

    def get_settings_request(self):
        driver = self.driver
        dashboard_info = driver.find_element(By.XPATH, "//script[text()[contains(., 'dashboardInfo')]]").get_attribute('innerHTML').split("\n", 2)[1].replace('window.dashboardInfo = ', '').replace(';', '').strip()
        dashboard_info_dict = json.loads(dashboard_info)
        self.username = dashboard_info_dict['user']['display_name']
        self.theme_name = driver.find_element(By.XPATH, "//span[@class='theme-name']").text

        time.sleep(6)
        logs_raw = driver.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

        def log_filter(log_):
            return (
                    log_["method"] == "Network.responseReceived"
                    and "json" in log_["params"]["response"]["mimeType"]
            )

        for log in filter(log_filter, logs):
            request_id = log["params"]["requestId"]
            resp_url = log["params"]["response"]["url"]
            if resp_url == 'https://streamlabs.com/api/v5/widget/alertbox':
                try:
                    network_log = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
                    self.alert_settings = json.loads(network_log['body'])
                    print(self.alert_settings['settings'])
                except exceptions.WebDriverException:
                   print('response.body is null')

        print(f"Settings received.")

    def import_event(self, platform, eventname):
        driver = self.driver
        actions = ActionChains(driver)
        dropdown_platform = driver.find_element(By.XPATH, "(//div[@class='top-nav__item-text'])[1]").get_attribute('innerHTML').split("\n", 2)[1].strip()
        self.start_time = time.time()
        if platform == "Twitch" or platform == "Facebook" or platform == "YouTube" or platform == "Trovo":
            if platform != dropdown_platform:
                # Navigate to dropdown and switch platforms to the event
                header_elem = driver.find_element(By.XPATH, "//nav[@role='navigation']")
                driver.execute_script("arguments[0].style.display = 'Block';", header_elem)
                driver.implicitly_wait(wait_duration)
                user_dropdown = driver.find_element(By.XPATH, "//div[@class='s-pane-dropdown top-nav__item top-nav-user']")
                user_dropdown.click()
                driver.implicitly_wait(wait_duration)
                platform_dropdown = driver.find_element(By.XPATH, "(//div[@class='s-pane-dropdown']/div[1])[1]")
                platform_dropdown.click()
                driver.implicitly_wait(wait_duration)
                platform_dropdown_item = driver.find_element(By.XPATH, "(//div[@class='s-pane-dropdown']/div[2])[1]/div/a[contains(text(), '" + platform + "')]")
                platform_dropdown_item.click()
                self.platform_name = platform
                print(f"--- Platform switched to {platform} ---")
                logging.info(f"--- Platform switched to {platform} ---")
                time.sleep(5)

        event_path = "//li/a[contains(text(), '" + eventname + "')]"
        if driver.find_elements(By.XPATH, event_path):
            event_tab = driver.find_element(By.XPATH, "//li/a[contains(text(), '" + eventname + "')]/parent::li")
            event_button = driver.find_element(By.XPATH, event_path)
            driver.execute_script("arguments[0].style.display = 'Block';", event_tab)
            event_name = event_button.get_attribute('innerText')
            actions.move_to_element(event_button).perform()
            event_button.click()

        if "sub" in eventname.lower():
            master_event = "sub"
        elif "follow" in eventname.lower():
            master_event = "follow"
        elif "raid" in eventname.lower():
            master_event = "raid"
        else:
            master_event = "donation"

        # Hide the top nav
        header_elem = driver.find_element(By.XPATH, "//nav[@role='navigation']")
        driver.execute_script("arguments[0].style.display = 'none';", header_elem)
        time.sleep(3)

        # Event Layout
        driver.implicitly_wait(wait_duration)
        if self.alert_settings['settings'][master_event + '_layout'] is None or self.alert_settings['settings'][master_event + '_layout'] == "":
            self.alert_settings['settings'][master_event + '_layout'] = self.alert_settings['settings']['layout']

        driver.execute_script("arguments[0].style.display = 'block';", driver.find_element(By.XPATH, "(//input[@value='above'])[2]"))
        driver.execute_script("arguments[0].style.display = 'block';", driver.find_element(By.XPATH, "(//input[@value='banner'])[2]"))
        driver.execute_script("arguments[0].style.display = 'block';", driver.find_element(By.XPATH, "(//input[@value='side'])[2]"))

        layout_label = '(//label[@data-value=\'' + self.alert_settings['settings'][master_event + '_layout'] + '\'])[2]'
        layout_input = '(//input[@value=\'' + self.alert_settings['settings'][master_event + '_layout'] + '\'])[2]'
        if driver.find_element(By.XPATH, layout_input).get_attribute('checked') is None:
            driver.find_element(By.XPATH, layout_label).click()

        # Event Animation
        show_animation_str = driver.find_element(By.XPATH, "//span[contains(@id, 'show_animation')]").text.replace(" ", "").lower()
        if show_animation_str != self.alert_settings['settings'][master_event + '_show_animation'].lower():
            driver.implicitly_wait(wait_duration)
            driver.find_element(By.XPATH, "//span[contains(@id, 'show_animation')]").click()
            driver.find_element(By.XPATH, "//input[@class='select2-search__field']").send_keys(re.sub(r"(\w)([A-Z])", r"\1 \2", self.alert_settings['settings'][master_event + '_show_animation']))
            driver.find_element(By.XPATH, "//input[@class='select2-search__field']").send_keys(Keys.ENTER)

        hide_animation_str = driver.find_element(By.XPATH, "//span[contains(@id, 'hide_animation')]").text.replace(" ", "").lower()
        if hide_animation_str != self.alert_settings['settings'][master_event + '_hide_animation'].lower():
            driver.implicitly_wait(wait_duration)
            driver.find_element(By.XPATH, "//span[contains(@id, 'hide_animation')]").click()
            driver.find_element(By.XPATH, "//input[@class='select2-search__field']").send_keys(re.sub(r"(\w)([A-Z])", r"\1 \2", self.alert_settings['settings'][master_event + '_hide_animation']))
            driver.find_element(By.XPATH, "//input[@class='select2-search__field']").send_keys(Keys.ENTER)

        # Event Text Animation
        text_animation_str = driver.find_element(By.XPATH, "//span[contains(@id, 'text_animation')]").text.replace(" ", "").lower()
        if text_animation_str != self.alert_settings['settings'][master_event + '_text_animation'].lower():
            driver.implicitly_wait(wait_duration)
            text_animation_window = driver.find_element(By.XPATH, "//span[contains(@id, 'text_animation')]")
            actions.move_to_element(text_animation_window).perform()
            if text_animation_window.get_attribute('innerHTML') == "":
                # doesn't work
                print(text_animation_window.get_attribute('innerHTML'))
                # driver.execute_script("arguments[0].textContent=arguments[1];", text_animation_window, "None")

            text_animation_window.click()
            driver.find_element(By.XPATH, "//input[@class='select2-search__field']").send_keys(re.sub(r"(\w)([A-Z])", r"\1 \2", self.alert_settings['settings'][master_event + '_text_animation']))
            driver.find_element(By.XPATH, "//input[@class='select2-search__field']").send_keys(Keys.ENTER)

        # Replace Product Image
        if driver.find_elements(By.XPATH, "//div/label[contains(text(), 'Image')]/parent::div/following-sibling::div/div/div[1]/input"):
            driver.implicitly_wait(wait_duration)
            enable_product_image_button = driver.find_element(By.XPATH, "//div/label[contains(text(), 'Image')]/parent::div/following-sibling::div/div/div[1]/input")
            actions.move_to_element(enable_product_image_button).perform()
            enable_product_image_button.click()

        # Event Image URL
        if self.alert_settings['settings'][master_event + '_image_href']:
            if self.alert_settings['settings'][master_event + '_image_href'] == '/images/gallery/default.gif':
                self.alert_settings['settings'][master_event + '_image_href'] = 'https://streamlabs.com/images/gallery/default.gif'

            if "http://" in self.alert_settings['settings'][master_event + '_image_href']:
                alert_image_url = self.alert_settings['settings'][master_event + '_image_href'].replace("http://", "https://")
            else:
                alert_image_url = self.alert_settings['settings'][master_event + '_image_href']
            if driver.find_elements(By.XPATH, "//a[@title='Link Image']/i[@class='icon-link']"):
                driver.implicitly_wait(wait_duration)
                actions.move_to_element(driver.find_element(By.XPATH, "//a[@title='Link Image']/i[@class='icon-link']")).perform()
                driver.find_element(By.XPATH, "//a[@title='Link Image']/i[@class='icon-link']").click()
                driver.implicitly_wait(wait_duration)
                driver.find_element(By.XPATH, "//input[@placeholder='https://yoururl.com/image/Streamlabs']").click()
                driver.find_element(By.XPATH, "//input[@placeholder='https://yoururl.com/image/Streamlabs']").send_keys(alert_image_url)
                driver.find_element(By.XPATH, "//div[@class='reveal__footer']/button[@title='Submit']").click()
        else:
            self.remove_media("Image")

        # Event Sound URL
        if self.alert_settings['settings'][master_event + '_sound_href']:
            if self.alert_settings['settings'][master_event + '_sound_href'] == '/sounds/gallery/default.ogg':
                self.alert_settings['settings'][master_event + '_sound_href'] = 'https://streamlabs.com/sounds/gallery/default.ogg'

            if "http://" in self.alert_settings['settings'][master_event + '_sound_href']:
                alert_sound_url = self.alert_settings['settings'][master_event + '_sound_href'].replace("http://", "https://")
            else:
                alert_sound_url = self.alert_settings['settings'][master_event + '_sound_href']

            if driver.find_elements(By.XPATH, "//a[@title='Link Audio']/i[@class='icon-link']"):
                driver.implicitly_wait(wait_duration)
                actions.move_to_element(driver.find_element(By.XPATH, "//a[@title='Link Audio']/i[@class='icon-link']")).perform()
                driver.find_element(By.XPATH, "//a[@title='Link Audio']/i[@class='icon-link']").click()
                driver.implicitly_wait(wait_duration)
                driver.find_element(By.XPATH, "//input[@placeholder='https://yoururl.com/audio/Streamlabs']").click()
                driver.find_element(By.XPATH, "//input[@placeholder='https://yoururl.com/audio/Streamlabs']").send_keys(alert_sound_url)
                driver.find_element(By.XPATH, "//div[@class='reveal__footer']/button[@title='Submit']").click()
        else:
            self.remove_media("Audio")

        # Event Sound Volume
        if driver.find_element(By.XPATH, "//div[contains(@name, 'sound_volume')]/span[1]/span").text.replace("%", "") != str(self.alert_settings['settings'][master_event + '_sound_volume']):
            desired_value_str = 'ui-slider-pip-' + str(self.alert_settings['settings'][master_event + '_sound_volume'])
            driver.implicitly_wait(wait_duration)
            sound_volume_handle = driver.find_element(By.XPATH, "//div[contains(@name, 'sound_volume')]/span[1]")
            desired_handle = driver.find_element(By.XPATH, "//div[contains(@name, 'sound_volume')]/span[contains(@class, '" + desired_value_str + "')]")

            driver.implicitly_wait(wait_duration)
            driver.execute_script("arguments[0].style.display = 'block';", desired_handle)
            actions.move_to_element(sound_volume_handle).perform()

            driver.implicitly_wait(wait_duration)
            actions.drag_and_drop(sound_volume_handle, desired_handle).perform()

        # Event Duration
        if driver.find_element(By.XPATH, "//div[contains(@name, 'alert_duration')]/span[1]/span").text.replace("s", "") != str(round(self.alert_settings['settings'][master_event + '_alert_duration'] / 1000)):
            desired_value_str = 'ui-slider-pip-' + str(round(self.alert_settings['settings'][master_event + '_alert_duration'] / 1000))
            driver.implicitly_wait(wait_duration)
            duration_handle = driver.find_element(By.XPATH, "//div[contains(@name, 'alert_duration')]/span[1]")
            desired_handle = driver.find_element(By.XPATH, "//div[contains(@name, 'alert_duration')]/span[contains(@class, '" + desired_value_str + "')]")

            driver.implicitly_wait(wait_duration)
            driver.execute_script("arguments[0].style.display = 'block';", desired_handle)
            actions.move_to_element(duration_handle).perform()

            driver.implicitly_wait(wait_duration)
            actions.drag_and_drop(duration_handle, desired_handle).perform()

        # Event Text Delay
        if driver.find_element(By.XPATH, "//div[contains(@name, 'text_delay')]/span[1]/span").text.replace("s", "") != str(round(self.alert_settings['settings'][master_event + '_text_delay'] / 1000)):
            desired_value_str = 'ui-slider-pip-' + str(round(self.alert_settings['settings'][master_event + '_text_delay'] / 1000))

            driver.implicitly_wait(wait_duration)
            text_delay_handle = driver.find_element(By.XPATH, "//div[contains(@name, 'text_delay')]/span[1]")
            desired_handle = driver.find_element(By.XPATH, "//div[contains(@name, 'text_delay')]/span[contains(@class, '" + desired_value_str + "')]")

            driver.implicitly_wait(wait_duration)
            driver.execute_script("arguments[0].style.display = 'block';", desired_handle)
            actions.move_to_element(text_delay_handle).perform()

            driver.implicitly_wait(wait_duration)
            actions.drag_and_drop(text_delay_handle, desired_handle).perform()

        # Custom Code
        if self.alert_settings['settings'][master_event + '_custom_html_enabled'] is False:
            driver.implicitly_wait(wait_duration)
            if driver.find_element(By.XPATH, "//div/label[contains(text(), 'Enable Custom HTML/CSS')]/parent::div/following-sibling::div/div/div[1]/input").get_attribute( 'checked') == 'true':
                driver.find_element(By.XPATH, "//div/label[contains(text(), 'Enable Custom HTML/CSS')]/parent::div/following-sibling::div/div/div[2]/input").click()

        if self.alert_settings['settings'][master_event + '_custom_html_enabled'] is True:
            driver.implicitly_wait(wait_duration)
            actions.move_to_element(driver.find_element(By.XPATH, "//div/label[contains(text(), 'Enable Custom HTML/CSS')]/parent::div/following-sibling::div/div/div[2]/input")).perform()
            if driver.find_element(By.XPATH, "//div/label[contains(text(), 'Enable Custom HTML/CSS')]/parent::div/following-sibling::div/div/div[2]/input").get_attribute('checked') == 'true':
                driver.find_element(By.XPATH, "//div/label[contains(text(), 'Enable Custom HTML/CSS')]/parent::div/following-sibling::div/div/div[1]/input").click()

            self.add_custom_code("//a[contains(text(), 'HTML')]/parent::li/parent::ul/following-sibling::div/div/div[1]", self.alert_settings['settings'][master_event + '_custom_js'], "js")
            self.add_custom_code("//a[contains(text(), 'HTML')]/parent::li/parent::ul/following-sibling::div/div/div[2]", self.alert_settings['settings'][master_event + '_custom_html'], "html")
            self.add_custom_code("//a[contains(text(), 'HTML')]/parent::li/parent::ul/following-sibling::div/div/div[3]", self.alert_settings['settings'][master_event + '_custom_css'], "css")

            if self.alert_settings['settings'][master_event + '_custom_json']:
                if driver.find_elements(By.XPATH, "//div[@class='row']/ul[@class='tabs']/li[@class='tabs-title'][4]"):
                    # If there's a Custom Fields tab
                    custom_fields_tab = driver.find_element(By.XPATH, "//div[@class='row']/ul[@class='tabs']/li[@class='tabs-title'][4]")
                    custom_fields_tab.click()
                    driver.implicitly_wait(wait_duration)
                    custom_fields_edit_button = driver.find_element(By.XPATH, "//input[@value='Edit Custom Fields']")
                    custom_fields_edit_button.click()
                else:
                    # If there's no Custom Fields tab, add it
                    custom_fields_add_button = driver.find_element(By.XPATH, "//input[@value='Add Custom Fields']")
                    custom_fields_add_button.click()

                    driver.implicitly_wait(wait_duration)
                    custom_fields_edit_button = driver.find_element(By.XPATH, "//input[@value='Edit Custom Fields']")
                    custom_fields_edit_button.click()

                # Add custom field code in editor here
                self.add_custom_code("//a[contains(text(), 'HTML')]/parent::li/parent::ul/following-sibling::div/div/div[5]", json.dumps(self.alert_settings['settings'][master_event + '_custom_json']), "json")
                custom_fields_update_button = driver.find_element(By.XPATH, "//input[@value='Update']")
                custom_fields_update_button.click()

            else:
                # If custom fields are not in the json template, remove it from the page if it exists
                if driver.find_elements(By.XPATH, "//div[@class='row']/ul[@class='tabs']/li[@class='tabs-title'][4]"):
                    actions.move_to_element(driver.find_element(By.XPATH, "//div[@class='row']/ul[@class='tabs']/li[@class='tabs-title'][4]")).perform()
                    custom_fields_tab = driver.find_element(By.XPATH, "//div[@class='row']/ul[@class='tabs']/li[@class='tabs-title'][4]")
                    custom_fields_tab.click()

                    driver.implicitly_wait(wait_duration)
                    custom_fields_remove_button = driver.find_element(By.XPATH, "//input[@value='Remove Custom Fields']")
                    custom_fields_remove_button.click()

        # Open Font Settings
        driver.implicitly_wait(wait_duration)
        base_alert_font_button = driver.find_element(By.XPATH, "//div[@class='s-accordion--title' and contains(text(), 'Open Font Settings')]")
        base_alert_font_button.click()

        # Font Typeface
        if driver.find_element(By.XPATH, "//span[contains(@id, '_font-')]").text != self.alert_settings['settings'][master_event + '_font']:
            driver.implicitly_wait(wait_duration)
            driver.find_element(By.XPATH, "//span[contains(@id, '_font-')]").click()
            driver.find_element(By.XPATH, "//input[@class='select2-search__field']").send_keys(self.alert_settings['settings'][master_event + '_font'])
            driver.find_element(By.XPATH, "//input[@class='select2-search__field']").send_keys(Keys.ENTER)

        # Font Size
        if driver.find_element(By.XPATH, "//div/label[contains(text(), 'Font Size')]/parent::div/following-sibling::div/div/span[1]/span").text != self.alert_settings['settings'][master_event + '_font_size']:
            driver.implicitly_wait(wait_duration)
            desired_value_str = 'ui-slider-pip-' + self.alert_settings['settings'][master_event + '_font_size'].replace("px","")

            driver.implicitly_wait(wait_duration)
            font_size_handle = driver.find_element(By.XPATH, "//div/label[contains(text(), 'Font Size')]/parent::div/following-sibling::div/div/span[1]")
            desired_handle = driver.find_element(By.XPATH, "//div/label[contains(text(), 'Font Size')]/parent::div/following-sibling::div/div/span[contains(@class, '" + desired_value_str + "')]")

            driver.implicitly_wait(wait_duration)
            driver.execute_script("arguments[0].style.display = 'block';", desired_handle)
            actions.move_to_element(font_size_handle).perform()

            driver.implicitly_wait(wait_duration)
            actions.drag_and_drop(font_size_handle, desired_handle).perform()

        # Font Weight
        if driver.find_element(By.XPATH, "//div[contains(@name, 'font_weight')]/span[1]/span").text != str(self.alert_settings['settings'][master_event + '_font_weight']):
            driver.implicitly_wait(wait_duration)
            desired_value_str = 'ui-slider-pip-' + str(self.alert_settings['settings'][master_event + '_font_weight'])

            driver.implicitly_wait(wait_duration)
            font_weight_handle = driver.find_element(By.XPATH, "//div[contains(@name, 'font_weight')]/span[1]")
            if driver.find_elements(By.XPATH, "//div[contains(@name, 'font_weight')]/span[contains(@class, '" + desired_value_str + "')]"):
                desired_handle = driver.find_element(By.XPATH, "//div[contains(@name, 'font_weight')]/span[contains(@class, '" + desired_value_str + "')]")
                driver.execute_script("arguments[0].style.display = 'block';", desired_handle)

            driver.implicitly_wait(wait_duration)
            actions.move_to_element(font_weight_handle).perform()
            driver.implicitly_wait(wait_duration)
            actions.drag_and_drop(font_weight_handle, desired_handle).perform()

        # Text Color
        if driver.find_element(By.XPATH, "//div[contains(@name, 'font_color')][1]/input").get_attribute('value') != self.alert_settings['settings'][master_event + '_font_color']:
            driver.implicitly_wait(wait_duration)
            driver.find_element(By.XPATH, "//div[contains(@name, 'font_color')][1]/input").click()
            actions.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()
            actions.key_down(Keys.DELETE).key_up(Keys.DELETE).perform()
            driver.find_element(By.XPATH, "//div[contains(@name, 'font_color')][1]/input").send_keys(self.alert_settings['settings'][master_event + '_font_color'])

        # Text Highlight Color
        if driver.find_element(By.XPATH, "//div[contains(@name, 'font_color2')][1]/input").get_attribute('value') != self.alert_settings['settings'][master_event + '_font_color2']:
            driver.implicitly_wait(wait_duration)
            driver.find_element(By.XPATH, "//div[contains(@name, 'font_color2')][1]/input").click()
            actions.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()
            actions.key_down(Keys.DELETE).key_up(Keys.DELETE).perform()
            driver.find_element(By.XPATH, "//div[contains(@name, 'font_color2')][1]/input").send_keys(self.alert_settings['settings'][master_event + '_font_color2'])

        # Save Settings
        save_settings_button = driver.find_element(By.XPATH, "(//button[contains(text(), 'Save settings')])[2]")
        actions.move_to_element(save_settings_button).perform()
        save_settings_button.click()
        time.sleep(1)
        actions.key_down(Keys.CONTROL).key_down(Keys.HOME).key_up(Keys.CONTROL).key_up(Keys.HOME).perform()
        actions.key_down(Keys.CONTROL).key_down(Keys.HOME).key_up(Keys.CONTROL).key_up(Keys.HOME).perform()
        finish_time = round(time.time() - self.start_time, 2)
        print(f"{platform} {event_name} updated. [{finish_time}s]")
        logging.info(f"{platform} {event_name} updated. [{finish_time}s]")
        driver.execute_script("arguments[0].style.display = 'block';", header_elem)
        time.sleep(4)

    def browser_close(self):
        print(f"Closing browser.")
        logging.info(f"Closing browser.")
        self.driver.close()

    def check_exists_by_xpath(self, xpath):
        driver = self.driver
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def get_settings(self):
        driver = self.driver
        dashboard_info = driver.find_element(By.XPATH, "//script[text()[contains(., 'dashboardInfo')]]").get_attribute('innerHTML').split("\n", 2)[1].replace('window.dashboardInfo = ', '').replace(';', '').strip()
        dashboard_info_dict = json.loads(dashboard_info)
        self.username = dashboard_info_dict['user']['display_name']
        self.theme_name = driver.find_element(By.XPATH, "//span[@class='theme-name']").text

        current_platform = driver.find_element(By.XPATH, "(//div[@class='top-nav__item-text'])[1]").get_attribute('innerHTML').split("\n", 2)[1].strip()
        if current_platform != "Twitch":
            # Switch to Twitch to grab alert settings
            # Navigate to dropdown and switch platforms to the event
            header_elem = driver.find_element(By.XPATH, "//nav[@role='navigation']")
            driver.execute_script("arguments[0].style.display = 'Block';", header_elem)
            driver.implicitly_wait(wait_duration)
            user_dropdown = driver.find_element(By.XPATH, "//div[@class='s-pane-dropdown top-nav__item top-nav-user']")
            user_dropdown.click()
            driver.implicitly_wait(wait_duration)
            platform_dropdown = driver.find_element(By.XPATH, "(//div[@class='s-pane-dropdown']/div[1])[1]")
            platform_dropdown.click()
            driver.implicitly_wait(wait_duration)
            platform_dropdown_item = driver.find_element(By.XPATH, "(//div[@class='s-pane-dropdown']/div[2])[1]/div/a[contains(text(), 'Twitch')]")
            platform_dropdown_item.click()

        time.sleep(6)
        logs_raw = driver.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

        def log_filter(log_):
            return (
                    log_["method"] == "Network.responseReceived"
                    and "json" in log_["params"]["response"]["mimeType"]
            )

        for log in filter(log_filter, logs):
            request_id = log["params"]["requestId"]
            resp_url = log["params"]["response"]["url"]
            if resp_url == 'https://streamlabs.com/api/v5/widget/alertbox':
                try:
                    network_log = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
                    self.alert_settings = json.loads(network_log['body'])
                except exceptions.WebDriverException:
                   # print('response.body is null')
                   logging.info('WebDriverException when getting settings')

        print(f"Duplicating '{self.alert_settings['active_profile']['name']}' Theme's events...")
        logging.info(f"Duplicating '{self.alert_settings['active_profile']['name']}' Theme's events...")


    def make_textarea_visible(self, xpath):
        driver = self.driver
        element = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].style.overflow = 'visible';", element)
        driver.execute_script("arguments[0].style.width = '50px';", element)
        driver.execute_script("arguments[0].style.height = '10px';", element)
        driver.execute_script("arguments[0].style.top = '0px';", element)
        driver.execute_script("arguments[0].style.left = '0px';", element)

    def switch_themes(self, desired_theme_name):
        driver = self.driver
        driver.get('https://streamlabs.com/dashboard#/widgetthemes')
        time.sleep(10)

        try:
            theme_button = driver.find_element(By.XPATH, "//div[@class='content-row__group']/h4[contains(text(), '" + desired_theme_name + "')]/parent::div/following-sibling::div/button")
            driver.implicitly_wait(wait_duration)
            theme_button.click()
            print(f"--- Theme activated: '{desired_theme_name}' ---")
            logging.info(f"--- Theme activated: '{desired_theme_name}' ---")
            time.sleep(5)

            driver.get('https://streamlabs.com/dashboard#/alertbox')
            time.sleep(3)
            self.theme_name = driver.find_element(By.XPATH, "//span[@class='theme-name']").text

        except ElementClickInterceptedException:
            print("Failed to activate new theme")
            logging.info("Failed to activate new theme")


    def delete_word_textarea(self, xpath):
        driver = self.driver
        actions = ActionChains(driver)
        element = driver.find_element(By.XPATH, xpath)
        
        actions.click(element).click(element).perform()
        actions.key_down(Keys.BACKSPACE).key_up(Keys.BACKSPACE).perform()

    def remove_media(self, mediatype):
        driver = self.driver
        actions = ActionChains(driver)
        if driver.find_elements(By.XPATH, "//a[@title='Remove" + mediatype + "']/i[@class='icon-close']"):
            driver.implicitly_wait(wait_duration)
            actions.move_to_element(
                driver.find_element(By.XPATH, "//a[@title='Remove" + mediatype + "']/i[@class='icon-close']")).perform()
            driver.find_element(By.XPATH, "//a[@title='Remove" + mediatype + "']/i[@class='icon-close']").click()

    def add_custom_code(self, xpath, code, lang):
        driver = self.driver
        actions = ActionChains(driver)

        # Make code wrapper element visible and move to it
        element = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].style.display = 'block';", element)
        actions.move_to_element(element).perform()
        driver.implicitly_wait(wait_duration)

        # Reveal text area
        element_window = driver.find_element(By.XPATH, xpath + "//div/div/div/div[1]")
        self.make_textarea_visible(xpath + "//div/div/div/div[1]")
        actions.move_to_element(element_window).perform()

        actions.click(element_window).perform()
        element_textarea = driver.find_element(By.XPATH, xpath + "//div/div/div/div[1]/textarea")
        actions.click(element_textarea).perform()

        # Select first word, ctrl + a and delete
        for word in driver.find_elements(By.XPATH, "(" + xpath + "//pre[@class=' CodeMirror-line ']/span/span)[1]"):
            driver.implicitly_wait(wait_duration)
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            actions.key_down(Keys.BACKSPACE).key_up(Keys.BACKSPACE).perform()

        driver.execute_script("arguments[0].value=arguments[1];", element_textarea, code)
        driver.implicitly_wait(wait_duration)
        actions.click(element_window).perform()


def duplicate_alert_settings(arg):
    enabled_list = []
    enable_streamlabs = False
    enable_twitch = False
    enable_youtube = False
    enable_facebook = False
    enable_trovo = False
    enable_thirdparty = False
    theme_name = arg[0]

    if arg[1].lower() == "y":
        enable_streamlabs = True
        enabled_list.append("Streamlabs")
    if arg[2].lower() == "y":
        enable_twitch = True
        enabled_list.append("Twitch")
    if arg[3].lower() == "y":
        enable_youtube = True
        enabled_list.append("YouTube")
    if arg[4].lower() == "y":
        enable_facebook = True
        enabled_list.append("Facebook")
    if arg[5].lower() == "y":
        enable_trovo = True
        enabled_list.append("Trovo")
    if arg[6].lower() == "y":
        enable_thirdparty = True
        enabled_list.append("Third Party Integrations")

    print(f"Duplicating settings to: " + ", ".join(enabled_list))
    logging.info(f"Duplicating settings to: " + ", ".join(enabled_list))
        
    a = DuplicateAlertSettings()
    a.start()
    a.launch_alert_box()
    a.assert_platforms()

    a.duplicate_settings(theme_name, enable_streamlabs, enable_twitch, enable_youtube, enable_facebook, enable_trovo, enable_thirdparty)
    # a.browser_close()


def duplicate_alerts_quickstart():
    a = DuplicateAlertSettings()
    a.start()
    a.launch_alert_box()
    a.assert_platforms()

    a.duplicate_settings_request("Default", False, False, False, False, True, False)


def get_widgetthemes_start():
    a = DuplicateAlertSettings()
    a.start()
    a.get_widgetthemes()


duplicate_alerts_quickstart()
# get_widgetthemes_start()


#duplicate_alert_settings(sys.argv)