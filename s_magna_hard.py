from gbfauto import *
from config import *
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions();
options.add_argument("user-data-dir=" + PROFILE);

driver = webdriver.Chrome(chrome_options=options)
driver.get("http://game.granbluefantasy.jp/#mypage")
time.sleep(3)

url_magna = [
        'http://game.granbluefantasy.jp/#quest/supporter/300251/1',
        'http://game.granbluefantasy.jp/#quest/supporter/300041/1',
        'http://game.granbluefantasy.jp/#quest/supporter/300091/1',
        'http://game.granbluefantasy.jp/#quest/supporter/300151/1',
        'http://game.granbluefantasy.jp/#quest/supporter/300191/1',
        'http://game.granbluefantasy.jp/#quest/supporter/300221/1']

summons = [
    '2040114000',
    '2030026000']

def run_magna(url, summons):
    if not enter_quest(driver, url, summons):
        return False

    wait_for_displayed(driver, By.CSS_SELECTOR,
            'div[class="btn-attack-start display-on"]', delay=1)
    activate_skill(driver, 0, [8000, 222]);
    activate_skill(driver, 2, [1099, 5446]);
    activate_skill(driver, 1, [6199, 2822, 2340]);
    activate_skill(driver, 3, [5453, 2229]);

    attack(driver, auto=True)

    while True:
        if "result" in driver.current_url:
            time.sleep(delay_sequence)
            break
        time.sleep(3)
    
    return True

print "STARTING magna_hard SEQUENCE"
print ""

for magna in range(len(url_magna)):
    print "CURRENT MAGNA: " + url_magna[magna]
    for i in range(3):
        print "CURRENT ROUND: " + str(i)
        if not run_magna(url_magna[magna], summons):
            break
        time.sleep(5)
