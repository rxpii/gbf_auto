from gbfauto_js import *
from config import *
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

num_cycles = 0
time_start = time.time()
time_current = time_start
print("Starting sequence: 1hr cycle, 2hr break (non-randomized)")
click_by(driver, driver, By.CLASS_NAME, "prt-link-quest") 
'''
while True:
    print("")
    print("")
    print("")
    print("Processing cycle #", num_cycles)
    print("")
    print("")
    print("")

    time_current = time.time()
    quest_sequence(driver, time_hrs=1.0)
    
    print("Cycle duration:", time.time() - time_current)
    print("Total time elapsed:", time.time() - time_start)
    time_current = time.time()
    
    print("")
    
    print("")
    print("")
    print("")
    print("Finished cycle #", num_cycles)
    print("")
    print("")
    print("")
    num_cycles += 1

    #print("Sleeping for 2hrs")
    #time.sleep(2 * 60 * 60)
'''
