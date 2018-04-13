from selenium.common.exceptions import NoSuchElementException
import time
import random
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
 
def click_by(driver, ref, by, name, locate_delay=3, click_delay=1,
        random_time=True):
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
 
    print(element.location)
    if (random_time):
        time.sleep(random.uniform(0.2, 2))
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
            time.sleep(locate_delay)
            continue
        except TimeoutException:
            print("Retrying:", name, "TimeoutException")
            time.sleep(locate_delay)
            continue


def click_retry(driver, element, retry_delay=3, click_delay=1, force=False):
    while True:
        try:
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

def wait_for_displayed(driver, by, name, delay=3):
    while True:
        print("Waiting for:", name)
        try:
            element = driver.find_element(by, name)
            if element.is_displayed():
                break
                print("Done waiting")
        except:
            pass
        time.sleep(delay)



def load_wait(driver, url, delay=3):
    driver.get(url)
    time.sleep(delay)

def select_summon(driver, summons):
    
    
    # get divs that contain summons
    attributes = driver.find_elements(By.CLASS_NAME, "prt-supporter-attribute")

    found = False
    
    # find preferred summon
    for summon in summons:
        for i in range(len(attributes)):
            # find summon elements
            summons_found = attributes[i].find_elements(By.CSS_SELECTOR,
                'img[alt="' + str(summon) + '"]')
            
            if len(summons_found) != 0:
                
                # click the given color element
                if (i == 7):
                    click_by(driver, driver, By.CSS_SELECTOR, 'div[data-type="'
                            + str(0) + '"]')
                    
                else:
                    click_by(driver, driver, By.CSS_SELECTOR, 'div[data-type="'
                            + str(i) + '"]')
                
                click_retry(driver, summons_found[0], force=True)
                found = True
                break
            
            # check next summon if there's none of this one
            else:
                continue

        if found:
            break

    # click default summon
    if not found:
        click_retry(driver,
                attributes[element].find_elements(By.CLASS_NAME,
                "prt-button-cover")[0])

# returns a list of visible popups, length zero if none
def checkfor_popups(driver, popup_type="NONE"):
    if popup_type == "NONE":
        popups = driver.find_elements(By.CLASS_NAME, "pop-usual")
    else:
        popups = driver.find_elements(By.CLASS_NAME, popup_type)
    
    popups_visible = []

    for popup in popups:
        if "display: block;" in popup.get_attribute("style"):
            popups_visible.append(popup)
    return popups_visible


# returns a list of popups upon fail, an empty list otherwise
def enter_quest(driver, url, summons):
    
    while True:
        # load into the quest support page
        load_wait(driver, url)
        
        select_summon(driver, summons)

        # wait for popup
        while True:
            confirmation = get_element_by(driver, driver, By.CLASS_NAME, "pop-deck")
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
        
        time.sleep(2)

        popups_visible = checkfor_popups(driver)

        if len(popups_visible) != 0:
            return popups_visible

        break

    return []


def fill_ap(driver, num_pots=1, finish_delay=3):
    url = "http://game.granbluefantasy.jp/#item"
    
    load_wait(driver, url)
    
    click_by(driver, driver, By.CSS_SELECTOR, 'div[class="btn-item-tabs items"]')

    '''
    items = WebDriverWait(driver, 3).until(
       EC.presence_of_element_located((By.CSS_SELECTOR,
       'div[class="btn-item-tabs items active"]'))
    )
    '''
    time.sleep(5)
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
    party = get_element_by(driver, driver, By.CLASS_NAME, "prt-member",
            locate_delay=0.5)
    
    click_char(driver, char_index)

    # retrive char relative to party element (index is +1)
    char = get_element_by(driver, driver, By.CSS_SELECTOR,
            'div[class="prt-command-chara chara' +
            str(char_index + 1) + '"]', locate_delay=0.5)

    # click on char's skills
    for skill in skill_list:
        click_by(driver, char, By.CSS_SELECTOR, 'div[ability-id="' + str(skill) +
        '"]')
    
    # click back button
    click_by(driver, driver, By.CLASS_NAME, "btn-command-back")

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
            print("auto visible")
            break
        time.sleep(0.3)

    time.sleep(1)
    click_by(driver, driver, By.CSS_SELECTOR, 
                'div[class="btn-auto"]', random_time=False)

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


def quest_sequence(driver, time_hrs=1.0, delay_sequence=5):
    time_s = 1.0 * 60 * 60
    time_start = time.time()

    while time.time() < time_start + time_s:
        enter_quest(driver,
                'http://game.granbluefantasy.jp/#quest/supporter/728111/5', [2040003000])

        wait_for_displayed(driver, By.CSS_SELECTOR, 'div[class="btn-attack-start display-on"]')
        
        activate_skill(driver, 1, [4003])
        activate_skill(driver, 2, [1021, 36])

        attack(driver, auto=True)

        while True:
            if "result" in driver.current_url:
                time.sleep(delay_sequence)
                break
            time.sleep(3)
        

def get_raid_id(driver, raid_options, refresh_delay=3):
    url_raid = "https://www.gbfraiders.com/?"
    url_complete = url_raid
    
    for i in range(len(raid_options)):
        url_complete += "raid=" + raid_options[i]
        if i != len(raid_options) - 1:
            url += "&"

    create_raid_tab = True

    for handle in driver.window_handles:
        driver.switch_to_window(handle)
        if "gbfraiders" not in driver.current_url:
            continue
        create_raid_tab = False
        break

    if create_raid_tab:
        driver.execute_script("window.open()")
        print "new tab"
        driver.switch_to_window(driver.window_handles[-1])
        driver.get(url_complete)
    elif driver.current_url != url_complete:
        driver.get(url_complete)

    time.sleep(refresh_delay)

    selected_raid = get_element_by(driver, driver, By.CLASS_NAME,
            "copy-div")
    
    raid_id = selected_raid.get_attribute("id")        
    driver.switch_to_window(driver.window_handles[0])
    return raid_id

def clear_pending_battles(driver):
    url_unclaimed = "http://game.granbluefantasy.jp/#quest/assist/unclaimed"
    
    raids_unclaimed = True
    
    while raids_unclaimed:

        load_wait(driver, url_unclaimed)
        raids = driver.find_elements(By.CSS_SELECTOR, 
                'div[class="btn-multi-raid lis-raid"]')
        if len(raids) == 0:
            raids_unclaimed = False
        else:
            click_by(driver, raids[0], By.CLASS_NAME, "prt-button-cover")
            time.sleep(4)


def join_raid(driver, raid_options, summons):
    url_raid = "http://game.granbluefantasy.jp/#quest/assist"
    load_wait(driver, url_raid)
    click_by(driver, driver, By.ID, "tab-id")
    
    raid_id = get_raid_id(driver, raid_options)

    get_element_by(driver, driver, By.CLASS_NAME, 
            "frm-battle-key").send_keys(raid_id)
    click_by(driver, driver, By.CLASS_NAME, "btn-post-key")
    
    time.sleep(2)
    popups_visible = checkfor_popups(driver, popup_type="common-pop-error")

    if len(popups_visible) != 0:
        popup_txt = get_element_by(driver, popups_visible[0], By.CLASS_NAME,
                "txt-popup-body")
        if popup_txt.text == "Check your pending battles.":
            clear_pending_battles(driver)

        join_raid(driver, raid_options, summons)
        return

    time.sleep(3)

    popups_visible = enter_quest(driver, driver.current_url, summons)

    time.sleep(2)

    if len(popups_visible) != 0:
        join_raid(driver, raid_options, summons)
        return

    if "empty" in driver.current_url:
        join_raid(driver, raid_options, summons)
        return

def raid_sequence(driver, raid_options, summons):
    while True:
        join_raid(driver, raid_options, summons)

        wait_for_displayed(driver, By.CSS_SELECTOR, 'div[class="btn-attack-start display-on"]')

        activate_skill(driver, 1, [4003])
        time.sleep(7)
        
