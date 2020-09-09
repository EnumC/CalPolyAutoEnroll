# Copyright 2020 Eric Qian.
# All rights reserved.
import time
import signal
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

opts = Options()
# opts.add_argument("user-data-dir=")

driver_path = "C:/Users/Eric/OneDrive - California Polytechnic State University/Documents/chromedriver84.exe"
# brave_path = "C:/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe"

opts.add_argument("user-data-dir=chrome-user-data")
opts.add_argument("profile-directory='Profile 1'")
# opts.binary_location = brave_path
browser = webdriver.Chrome(executable_path=driver_path, options=opts)


def signal_handler(sig, frame):
    print('Exiting...')
    browser.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to stop')

def press_next_btn():
    browser.find_element_by_css_selector('[id^=DERIVED_CLS_DTL_NEXT_PB]').click()
    print ("next button pressed.")

def confirm_class_add():
    while len(browser.find_elements_by_css_selector("[value='Proceed to Step 2 of 3']")) == 0:
        time.sleep(1)
    browser.find_element_by_css_selector("[value='Proceed to Step 2 of 3']").click()
    print ("commited all classes.")

def errors_exists():
    if len(browser.find_elements_by_css_selector("[id^='DERIVED_SASSMSG_ERROR_TEXT']")) > 0:
        # there are errors!
        errMsg = ""
        for err in browser.find_elements_by_css_selector("[id^='DERIVED_SASSMSG_ERROR_TEXT']"):
            errMsg += err.text
        browser.execute_script("document.querySelectorAll('[id^=DERIVED_SASSMSG_ERROR_TEXT]').forEach(elem => elem.remove())")
        return [True, errMsg]
    else:
        return [False, ""]
def add_class(sectionNum, laboratoryNum=-1):
    while len(browser.find_elements_by_id('DERIVED_REGFRM1_CLASS_NBR')) == 0:
        time.sleep(1)

    browser.find_element_by_id('DERIVED_REGFRM1_CLASS_NBR').clear()
    browser.find_element_by_id('DERIVED_REGFRM1_CLASS_NBR').send_keys(sectionNum)
    
    browser.find_element_by_css_selector("[title='Add a class using class number']").click()

    if laboratoryNum != -1:
        # if lab section is required/passed in.

        while len(browser.find_elements_by_css_selector('[id^=trSSR_CLS_TBL_R1]')) == 0:
            time.sleep(1)
            # ERR: class already in cart
            errStatus, errMsg = errors_exists()
            if errStatus is True:
                print ("ERROR IN ADDING CLASS: " + sectionNum + ". " + errMsg)
                return
        labsections = browser.find_elements_by_css_selector('[id^=trSSR_CLS_TBL_R1]')

        for labsection in labsections:

            while len(labsection.find_elements_by_css_selector('[id^=SSR_CLS_TBL_R1_RELATE_CLASS_NBR]')) == 0:
                time.sleep(1)
            for section in labsection.find_elements_by_css_selector('[id^=SSR_CLS_TBL_R1_RELATE_CLASS_NBR]'):
                if section.text == laboratoryNum:
                    print ("found lab section!")
                    labsection.find_element_by_css_selector('[class=PSRADIOBUTTON]').click()
                    print ("selected lab section.")
                    # time.sleep(2)
                    press_next_btn()
                    break
    while len(browser.find_elements_by_css_selector('[id^=DERIVED_CLS_DTL_WAIT_LIST_OKAY]')) == 0:
        time.sleep(1)
        errStatus, errMsg = errors_exists()
        if errStatus is True:
            print ("ERROR IN ADDING CLASS: " + sectionNum + ". " + errMsg)
            return
    browser.find_element_by_css_selector('[id^=DERIVED_CLS_DTL_WAIT_LIST_OKAY].PSCHECKBOX').click()
    press_next_btn()

    print ("added class.")



browser.get('https://myportal.calpoly.edu')

print(browser.current_url)
if browser.current_url.startswith('https://idp.calpoly.edu/idp/profile/cas/login'):
    print("login required.")
    while browser.current_url.startswith('https://idp.calpoly.edu/idp/profile/cas/login'):
        time.sleep(3)
else:
    print("already logged in.")

print("logged in.")
navLinks = browser.find_elements_by_class_name("singleclick-link")
for link in navLinks:
    if link.text == "Student Center":
        link.click()
        break
    if link == navLinks[len(navLinks) - 1]:
        print ("Student center not found in nav panel. Aborting.")
        sys.exit(1)
browser.switch_to.window(browser.window_handles[1])
if (browser.current_url.startswith("https://cmsweb.pscs.calpoly.edu/psp/CSLOPRD/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL")):
    print ("now in student center.")

# print(browser.current_url)
browser.switch_to.frame(browser.find_element_by_id('ptifrmtgtframe'))
enrollBtn = browser.find_element_by_css_selector("[aria-label='Enroll']")
enrollBtn.click()

add_class('9672', '9673')
add_class('3971')
confirm_class_add()

time.sleep(30)