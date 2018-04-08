from gbfauto import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL = "xianhaic@gmail.com"
PASS = "153968Pa"

driver = webdriver.Chrome()
login_seq(driver, EMAIL, PASS)

while True:
    click_by(driver, By.XPATH,
            '//*[@id="wrapper"]/div[3]/div[2]/div[4]/div[2]/div/img')

    click_by(driver, By.XPATH,
            '//*[@id="cnt-quest"]/div[1]/div[1]/div[5]/div[2]/div[1]/div[2]/div[2]') 

    time.sleep(3)
    while True:
        try:
            driver.find_element(By.CSS_SELECTOR, 'div[class="pop-usual pop-stamina pop-show"]')
            click_by(driver, By.XPATH,
            '//*[@id="pop"]/div/div[2]/div/div[2]/div[2]/div[5]/div')
            time.sleep(1)
            click_by(driver, By.CSS_SELECTOR, 
                    'div[class="btn-treasure-footer-reload"]')
                    
            click_by(driver, By.XPATH,
                    '//*[@id="cnt-quest"]/div[1]/div[1]/div[5]/div[2]/div[1]/div[2]/div[2]')
        except NoSuchElementException:
            break
        except:
            continue


    while True:
        current_css = get_element_by(driver, By.ID, "asset-css")
        if current_css.get_attribute("data-css") == "/quest/supporter.css":
            break
        time.sleep(3)
    #click_by(By.CLASS_NAME, "icon-supporter-type-5", driver)
    click_by(driver, By.XPATH,
            '//*[@id="cnt-quest"]/div[2]/div[8]/div[1]/div[4]')
    while True:
        confirmation = get_element_by(driver, By.CSS_SELECTOR,
                'div[class="pop-deck supporter"]')
        if "display" in confirmation.get_attribute("style"):
            break
        time.sleep(3)
    click_by(driver, By.XPATH,
            '//*[@id="wrapper"]/div[3]/div[3]/div[3]/div[2]')

    while True:
        current_css = get_element_by(driver, By.ID, "asset-css")
        if current_css.get_attribute("data-css") == "/raid/index.css":
            break
        time.sleep(3)

    click_by(driver, By.CSS_SELECTOR, 'div[class="lis-character1 btn-command-character"]')
    click_by(driver, By.CSS_SELECTOR, 'div[ability-id="1614"]')
    click_by(driver, By.CSS_SELECTOR, 'div[class="ico-next"]')
    click_by(driver, By.CSS_SELECTOR, 'div[ability-id="4003"]')
    click_by(driver, By.CSS_SELECTOR, 'div[class="btn-attack-start display-on"]')

    while True:
        auto = get_element_by(driver, By.CSS_SELECTOR, 
                'div[class="btn-auto"]')
        if auto.get_attribute("style") != "display: none;":
            break
        time.sleep(1)

    click_by(driver, By.CSS_SELECTOR, 
                'div[class="btn-auto"]')
    while True:
        if "result" in driver.current_url:
            time.sleep(5)
            break
        time.sleep(3)


    driver.get("http://game.granbluefantasy.jp/#mypage")
    time.sleep(3)

