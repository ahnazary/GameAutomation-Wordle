import os
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
from difflib import get_close_matches


driverPath = os.path.abspath(os.path.dirname(__file__)) + '/chromedriver_linux64/chromedriver'
driver = webdriver.Chrome(driverPath)
driver.get('https://www.wordleunlimited.com/')


wordsFilePath = os.path.abspath(os.path.dirname(__file__)) + '/words'

try:
    element = WebDriverWait(driver,3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div[11]/div[1]/div[4]'))
    )
    element.click()
    element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div[11]/div[2]/div[1]'))
    )
    element.click()
    element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div[11]/div[1]/div[8]'))
    )
    element.click()
    element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div[11]/div[2]/div[2]'))
    )
    element.click()
    element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div[11]/div[1]/div[3]'))
    )
    element.click()
    element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div[11]/div[3]/div[9]'))
    )
    element.click()
except:
    raise('too long waiting time')

with open(wordsFilePath) as f:
    words = f.readlines()

r = re.compile("^.{5}$")
filtered_list = list(filter(r.match, words))

startingWord = 'raise'

# for char in startingWord:
#     driver.find_element('Rowl-letter').send_keys(char)


