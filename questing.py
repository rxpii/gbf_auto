from gbfauto import *
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

robomi_sequence(driver)
