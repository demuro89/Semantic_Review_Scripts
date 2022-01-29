#!/usr/bin/env python3

import sys
import os
import urllib
import requests

from os import getcwd
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display

i = 0

with open("citationsDois.txt") as file:
    lines = [line.rstrip() for line in file]


for url in lines:
    print("Downloading URL = "+url+" RIGA:"+str(i))

    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", getcwd()+"/articles")
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    fp.set_preference("pdfjs.disabled", True)

    browser = webdriver.Firefox(fp)
    browser.get(url)

    time.sleep(1)

    #EZPROXY creds
    user = browser.find_element_by_id("userNameInput")
    user.send_keys("")

    pwd = browser.find_element_by_id("passwordInput")
    pwd.send_keys("")

    browser.find_element_by_id("submitButton").click()

    i=i+1
