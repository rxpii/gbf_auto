from selenium.common.exceptions import NoSuchElementException
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoSuchElementException
 
EMAIL = "xianhaic@gmail.com"
PASS = "153968Pa"
RESIZE = "0.4"
 
def click_by(by, name, locate_delay=3, click_delay=1):
    print("Attempting to retrive:", name)
    while True:
        try:
            element = WebDriverWait(driver, locate_delay).until(
                EC.presence_of_element_located((by, name))
            )
            print("Found:", name)
            break
        except NoSuchElementException:
            print("Retrying:", name, "NoSuchElementException")
            continue
        except TimeoutException:
            print("Retrying:", name, "TimeoutException")
            continue
        except NoSuchWindowException:
            driver.switch_to_window(driver.window_handles[0])
            print("Retrying:", name, "NoSuchWindowException")
            continue
 
    #driver.execute_script("document.body.style.zoom = '" + RESIZE + "'");
    time.sleep(click_delay)
    #driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(click_delay) 
    print(element.location)
    print(element.width)
    print(element.height)
    #click_retry(element)
    webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
 
def get_element_by(by, name, locate_delay=3):
    print("Attempting to retrive:", name)
 
    while True:
        try:
            element = WebDriverWait(driver, locate_delay).until(
                EC.presence_of_element_located((by, name))
            )
            print("Found:", name)
            return element
        except NoSuchElementException:
            print("Retrying:", name, "NoSuchElementException")
            continue
        except TimeoutException:
            print("Retrying:", name, "TimeoutException")
            continue
        except NoSuchWindowException:
            driver.switch_to_window(driver.window_handles[0])
            print("Retrying:", name, "NoSuchWindowException")
            continue

def click_retry(element, retry_delay=3):
    while True:
        try:
            element.click()
            break
        except Exception as e:
            print(e)
            time.sleep(retry_delay)
            continue

 
driver = webdriver.Chrome()
driver.get("http://game.granbluefantasy.jp")
time.sleep(3)
click_by(By.ID, "login-auth")
'''
WebDriverWait(driver, 3).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div[class="cnt-presetting"]')))
click_by(By.XPATH, '//*[@id="mobage-login"]/img')

current_handle = driver.window_handles[0]
driver.switch_to_window(driver.window_handles[-1])
 
input_email = get_element_by(By.ID, "subject-id")
input_pass = get_element_by(By.ID, "subject-password")
input_email.send_keys(EMAIL)
input_pass.send_keys(PASS)

print("Home page recognized!")

time.sleep(10)

#trial battles
click_by(By.CSS_SELECTOR, 'div[class="btn-campaign-toggle"]')
click_by(By.XPATH, '//*[@id="wrapper"]/div[3]/div[2]/div[5]/div[2]/div[3]/img')
click_by(By.CSS_SELECTOR, 'div[data-group-title="Test Machina Alpha"]')
click_by(By.CSS_SELECTOR, 'div[data-quest-id="990011"]')
'''
'''

while True:
    current_css = get_element_by(By.ID, "asset-css")
    if current_css.get_attribute("data-css") == "/quest/supporter.css":
        break
    time.sleep(3)
click_by(By.CLASS_NAME, "icon-supporter-type-6")
click_by(By.XPATH, '//*[@id="cnt-quest"]/div[2]/div[9]/div[1]/div[4]')

while True:
    confirmation = get_element_by(By.CSS_SELECTOR, 'div[class="pop-deck supporter"]')
    if "display" in confirmation.get_attribute("style"):
        break
    time.sleep(3)
click_by(By.XPATH, '//*[@id="wrapper"]/div[3]/div[3]/div[3]/div[2]')
'''
while True:
    current_css = get_element_by(By.ID, "asset-css")
    if current_css.get_attribute("data-css") == "/raid/index.css":
        break
    time.sleep(3)
click_by(By.XPATH, '//*[@id="pop"]/div/div[3]/div')
click_by(By.CSS_SELECTOR, 'div[class="lis-character2 btn-command-character"]')
click_by(By.CSS_SELECTOR, 'div[class="ico-pre"]')
#raid stuff
'''
click_by(By.CLASS_NAME, "prt-link-quest")
click_by(By.XPATH, '//*[@id="initMoves"]')
click_by(By.XPATH, '//*[@id="cnt-quest"]/div[2]/div[2]/div[4]/div[1]/div/div[7]/div[2]/div[2]')
click_by(By.XPATH, '//*[@id="pop"]/div/div[3]/div[2]')
while True:
    current_css = get_element_by(By.ID, "asset-css")
    if current_css.get_attribute("data-css") == "/quest/supporter.css":
        break
    time.sleep(3)

click_by(By.XPATH, '//*[@id="cnt-quest"]/div[2]/div[9]/div[1]/div[4]')
while True:
    confirmation = get_element_by(By.CSS_SELECTOR, 'div[class="pop-deck supporter"]')
    if "display" in confirmation.get_attribute("style"):
        break
    time.sleep(3)
click_by(By.XPATH, '//*[@id="wrapper"]/div[3]/div[3]/div[3]/div[2]')

while True:
    current_css = get_element_by(By.ID, "asset-css")
    if current_css.get_attribute("data-css") == "/raid/multi.css":
        break
    time.sleep(3)

click_by(By.CSS_SELECTOR, 'div[class="lis-character2 btn-command-character"]')
click_by(By.CSS_SELECTOR, 'div[ability-id="1099"]')
click_by(By.CSS_SELECTOR, 'div[class="ico-pre"]')
click_by(By.CSS_SELECTOR, 'div[ability-id="6199"]')
click_by(By.CSS_SELECTOR, 'div[class="ico-pre"]')
click_by(By.CSS_SELECTOR, 'div[ability-id="1600"]')
click_by(By.CSS_SELECTOR, 'div[ability-id="6199"]')
click_by(By.CSS_SELECTOR, 'div[ability-id="8000"]')
click_by(By.CSS_SELECTOR, 'div[class="ico-next"]')
click_by(By.CSS_SELECTOR, 'div[ability-id="2340"]')
click_by(By.CSS_SELECTOR, 'div[ability-id="2822"]')
click_by(By.CSS_SELECTOR, 'div[class="btn-attack-start display-on"]')
'''
