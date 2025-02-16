from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()
COOKIE = os.getenv('COOKIE')

def getOptions():
  chrome_options = Options()
  # chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-gpu')
  chrome_options.add_argument('--disable-extensions')
  # chrome_options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
  chrome_options.add_argument('--use-gl=desktop')
  # chrome_options.add_argument('--single-process')
  chrome_options.add_argument('--disable-infobars')
  chrome_options.add_argument('--disable-notifications')
  chrome_options.add_argument('--window-size=1280,720')

  return chrome_options

def checkNSFW(driver: webdriver.Chrome):

  twitch_frame = driver.find_element(By.TAG_NAME, "iframe")
  driver.switch_to.frame(twitch_frame)

  # Skip NSFW popup
  buttons = driver.find_elements(By.TAG_NAME, "button")
  for button in buttons:
    if button.text == 'Start Watching':
      button.click()

  driver.switch_to.default_content()

def checkForInactiveStream(driver: webdriver.Chrome):
  captcha_button = driver.find_element(By.ID, "g-recaptcha-span")
  if captcha_button and captcha_button.is_displayed():
    captcha_button.click()
    sleep(5)

  credits_per_minute = float(driver.find_element(By.ID, 'credits-per-minute').text)
  if credits_per_minute == 0:
    driver.refresh()

def main():
  svc = webdriver.ChromeService(executable_path=binary_path)
  driver = webdriver.Chrome(service=svc, options=getOptions())

  driver.get("https://stream-booster.ru/i/gold-pack-1.png")

  driver.add_cookie({
                    "name": "PHPSESSID",
                    "value": COOKIE,
                    "domain": "stream-booster.ru"
                    })

  driver.get("https://stream-booster.ru/en/dashboard/watch")

  balance_element = driver.find_element(By.ID, "current-credits")

  if not balance_element:
    print("not logged in")

  print("Current balance", balance_element.text)

  checkNSFW()

  while True:
    sleep(5)

    checkNSFW(driver)
    checkForInactiveStream(driver)

    pass

if __name__ == "__main__":
  main()
