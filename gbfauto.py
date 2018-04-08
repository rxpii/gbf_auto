from selenium.common.exceptions import NoSuchElementException
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

RESIZE = "0.99"
 
def click_by(driver, ref, by, name, locate_delay=3, click_delay=1):
    print("Attempting to retrive:", name)
    while True:
        try:
            element = ref.find_element(by, name)
            if not element.is_displayed():
                continue
            #element = WebDriverWait(driver, locate_delay).until(
             #   EC.presence_of_element_located((by, name))
            #)
            print("Found:", name)
            break
        except NoSuchElementException:
            print("Retrying:", name, "NoSuchElementException")
            time.sleep(locate_delay)
            continue
        except TimeoutException:
            print("Retrying:", name, "TimeoutException")
            time.sleep(locate_delay)
            continue
        except NoSuchWindowException:
            driver.switch_to_window(driver.window_handles[0])
            print("Retrying:", name, "NoSuchWindowException")
            time.sleep(locate_delay)
            continue
 
    print(element.location)
    click_retry(driver, element)
 

def get_element_by(driver, ref, by, name, locate_delay=3):
    print("Attempting to retrive:", name)
 
    while True:
        try:
            element = ref.find_element(by, name)
            if not element.is_displayed():
                continue
            print("Found:", name)
            return element
        except NoSuchElementException:
            print("Retrying:", name, "NoSuchElementException")
            continue
        except TimeoutException:
            print("Retrying:", name, "TimeoutException")
            continue


def click_retry(driver, element, retry_delay=3, click_delay=1, force=False):
    while True:
        try:
            time.sleep(click_delay)
            webdriver.ActionChains(driver).move_to_element(element).perform()
            webdriver.ActionChains(driver).send_keys(Keys.DOWN).perform()

            time.sleep(click_delay)
            webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
            break
        except Exception as e:
            print(e)
            time.sleep(retry_delay)
            continue

def login_seq(driver, email, password):

    driver.get("http://game.granbluefantasy.jp")
    time.sleep(3)

    click_by(driver, driver, By.ID, "login-auth")
    click_by(driver, driver, By.XPATH, '//*[@id="mobage-login"]/img')

    driver.switch_to_window(driver.window_handles[-1])
     
    input_email = get_element_by(driver, driver, By.ID, "subject-id")
    input_pass = get_element_by(driver, driver, By.ID, "subject-password")
    input_email.send_keys(email)
    input_pass.send_keys(password)
    
    click_by(driver, driver, By.ID, "login")

    while True:
        try: 
            driver.find_element(By.XPATH, "null")
        except NoSuchWindowException:
            driver.switch_to_window(driver.window_handles[0])
            break
        except:
            time.sleep(3)
            continue

def wait_for_pattern(driver, pattern, delay=3):
    while True:
        if pattern in driver.current_url:
            time.sleep(delay)
            break
        time.sleep(delay)

def wait_for_displayed(driver, by, name):
    while True:
        print("Waiting for:", name)
        try:
            element = driver.find_element(by, name)
            if element.is_displayed():
                break
                print("Done waiting")
        except:
            pass



def load_wait(driver, url, delay=3):
    driver.get(url)
    time.sleep(delay)

def enter_quest(driver, url, element, summons):
    
    while True:
        # load into the quest support page
        load_wait(driver, url)
        
        # get divs that contain summons
        attributes = driver.find_elements(By.CLASS_NAME, "prt-supporter-attribute")
        
        # click the given color element
        click_by(driver, driver, By.CSS_SELECTOR, 'div[data-type="' + str(element) + '"]')
        
        found = False
        
        # find preferred summon
        for summon in summons:
            # find summon elements
            summons_found = attributes[element].find_elements(By.CSS_SELECTOR,
                    'img[alt="' + str(summon) + '"]')
            
            # check next summon if there's none of this one
            if len(summons_found) == 0:
                continue
            else:
                click_retry(driver, summons_found[0], force=True)
                found = True
                break
        # click default summon
        if not found:
            click_retry(driver,
                    attributes[element].find_elements(By.CLASS_NAME,
                    "prt-button-cover")[0])

        # wait for popup
        while True:
            confirmation = get_element_by(driver, driver, By.CSS_SELECTOR,
                    'div[class="pop-deck supporter"]')
            if "display" in confirmation.get_attribute("style"):
                print("break")
                break
            time.sleep(3)
        
        # check if need to fill stam
        stamina = get_element_by(driver, driver, By.CLASS_NAME, "txt-stamina-after")
        
        # extract int value
        current_stam = int(stamina.text)

        if (current_stam < 0):
            fill_ap(driver, num_pots=1)
            continue
        

        print("click ok")

        # enter dungeon
        button_ok = confirmation.find_element(By.CLASS_NAME, "btn-usual-ok")
        click_retry(driver, button_ok)
        
        break


def fill_ap(driver, num_pots=1, finish_delay=3):
    url = "http://game.granbluefantasy.jp/#item"
    
    load_wait(driver, url)
    
    click_by(driver, driver, By.CSS_SELECTOR, 'div[class="btn-item-tabsitems"]')

    click_by(driver, driver, By.CSS_SELECTOR, 'div[class="lis-item se"][data-index="1"]')
    
    # select number of pots to consume
    if num_pots > 1 and num_pots <= 20:
        select = Select(get_element_by(driver, driver, By.CSS_SELECTOR,
            'select[class="num-set use-item-num"]'))
        select.select_by_value(str(num_pots))
    
    # click use
    click_by(driver, driver, By.CSS_SELECTOR, 'div[class="btn-usual-use"]')
    
    time.sleep(finish_delay)
    
def click_char(driver, char_index):
    # retrieve party element
    party = get_element_by(driver, driver, By.CLASS_NAME, "prt-member")
    
    # click char relative to party element
    click_by(driver, party, By.CSS_SELECTOR, 'div[class="lis-character' +
            str(char_index) + ' btn-command-character"]')
    

def activate_skill(driver, char_index, skill_list):
    # retrieve party element
    party = get_element_by(driver, driver, By.CLASS_NAME, "prt-member")
    
    # retrive char relative to party element
    char = get_element_by(driver, party, By.CSS_SELECTOR, 'div[class="lis-character' +
            str(char_index) + ' btn-command-character"]')
    
    click_char(driver, char_index)

    # click on char's skills
    for skill in skill_list:
        click_by(driver, char, By.CSS_SELECTOR, 'div[ability-id="' + str(skill) +
        '"]')
    
    # click back button
    click_by(driver, driver, By.CSS_SELECTOR, 'div[class="btn-command-back display-off display-on"]')

def attack(driver, auto=False):
    # click attack button
    click_by(driver, driver, By.CSS_SELECTOR, 'div[class="btn-attack-start display-on"]')
    
    # return if auto off
    if not auto:
        return

    # click auto
    while True:
        auto = get_element_by(driver, driver, By.CSS_SELECTOR, 
                'div[class="btn-auto"]')
        if auto.get_attribute("style") != "display: none;":
            break
        time.sleep(1)

    click_by(driver, driver, By.CSS_SELECTOR, 
                'div[class="btn-auto"]')

def test_sequence(driver):
    enter_quest(driver,
            'http://game.granbluefantasy.jp/#quest/supporter/990011/17', 6, [2040003000])

    while True:
        popup = get_element_by(driver, driver, By.CSS_SELECTOR,
                'div[class="pop-usual pop-trialbattle-notice pop-show"]')
        if "display" in popup.get_attribute("style"):
            break
        time.sleep(3)
    click_by(driver, driver, By.XPATH, '//*[@id="pop"]/div/div[3]/div')
    click_by(driver, driver, By.XPATH, '//*[@id="prt-command-top"]/div/div/div[3]')
    click_by(driver, driver, By.XPATH,
            '//*[@id="wrapper"]/div[3]/div[2]/div[9]/div[5]/div[3]/div[1]/div[1]')


    click_by(driver, driver, By.CSS_SELECTOR, 'div[class="ico-pre"]')

    click_by(driver, driver, By.XPATH,
            '//*[@id="wrapper"]/div[3]/div[2]/div[9]/div[4]/div[3]/div[1]/div[1]')

    click_by(driver, driver, By.CSS_SELECTOR, 'div[class="btn-attack-start display-on"]')
    while True:
        auto = get_element_by(driver, driver, By.CSS_SELECTOR, 
                'div[class="btn-auto"]')
        if auto.get_attribute("style") != "display: none;":
            break
        time.sleep(1)

    click_by(driver, driver, By.CSS_SELECTOR, 
                'div[class="btn-auto"]')


def robomi_sequence(driver):
    enter_quest(driver,
            'http://game.granbluefantasy.jp/#quest/supporter/727281/3', 6,
            [2040003000])

    wait_for_displayed(driver, By.CSS_SELECTOR, 'div[class="btn-attack-start display-on"]')
    
    activate_skill(driver, 1, [1098, 5445])
    activate_skill(driver, 3, [4003])

    attack(driver, auto=True)
