from gbfauto_js import *
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


EMAIL = "xianhaic+1@gmail.com"
PASS = "153968Pa"

options = webdriver.ChromeOptions();
options.add_argument("user-data-dir=/home/xianhai/.config/google-chrome");

driver = webdriver.Chrome(chrome_options=options)
driver.get("http://game.granbluefantasy.jp/#mypage")
time.sleep(3)

num_cycles = 0
time_start = time.time()
time_current = time_start
print("Starting sequence: 1hr cycle, 2hr break (randomized)")
while True:
    print("")
    print("")
    print("")
    print("Processing cycle #", num_cycles)
    print("")
    print("")
    print("")
    
    time_current = time.time()
   
    random_ontime = random.uniform(0.5, 1.5)
    print("Random ontime:", random_ontime)

    ahalo_sequence(driver, [2040225000, 2040225000, 2040056000], time_hrs=random_ontime) 
   
    print("")
    print("")
    print("")
    print("Processing cycle #", num_cycles)
    print("")
    print("")
    print("")
    print("Cycle duration:", time.time() - time_current)
    print("Total time elapsed:", time.time() - time_start)
    time_current = time.time()
    
    print("")
    
    num_cycles += 1

    random_sleeptime = random.uniform(1.5, 3)

    print("Sleeping for", random_sleeptime, "hrs")
    #time.sleep(random_sleeptime * 60 * 60)

