#-*-coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import os
import time

TWITTER_EMAIL = os.environ["TWITTER_EMAIL"]
TWITTER_PASS = os.environ["TWITTER_PASS"]


browser_path = '/usr/bin/chromium-browser'

opts = Options()
opts.binary_location = browser_path
opts.add_argument('--headless')
opts.add_argument('--disable-gpu')
# opts.add_argument('--no-sandbox')


def login(browser):
    browser.get("https://twitter.com/login")

    # ToDo? check if already logged in

    login_button_xpath = "//*[@id=\"page-container\"]/div/div[1]/form/div[2]/button"
    email_input_xpath = "//*[@id=\"page-container\"]/div/div[1]/form/fieldset/div[1]/input"
    pass_input_xpath = "//*[@id=\"page-container\"]/div/div[1]/form/fieldset/div[2]/input"

    email_input = browser.find_element_by_xpath(email_input_xpath)
    pass_input = browser.find_element_by_xpath(pass_input_xpath)
    login_button = browser.find_element_by_xpath(login_button_xpath)

    email_input.send_keys(TWITTER_EMAIL)
    pass_input.send_keys(TWITTER_PASS)
    login_button.click()


tweet_id = 1039490979969945600
tweet_url = "https://twitter.com/x/status/{}".format(tweet_id)

browser = webdriver.Chrome(chrome_options=opts)
login(browser)
time.sleep(1)

browser.get(tweet_url)
time.sleep(1)

tweet_xpath = "//*[@id=\"permalink-overlay-dialog\"]/div[3]/div/div/div[1]/div[1]/div"
tweet = browser.find_element_by_xpath(tweet_xpath)
tweet_html = tweet.get_attribute("")

