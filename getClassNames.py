from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

status = False
timeout = 8
driver = webdriver.Chrome('/Users/alexhuang/Desktop/aeriesNotifications/chromedriver')
driver.get('https://parentnet.tustin.k12.ca.us/ParentPortal/LoginParent.aspx')
username = driver.find_element_by_id('portalAccountUsername')
username.send_keys('alexanderh0098@mytusd.org')
driver.find_element_by_id('next').click()

time.sleep(1)

password = driver.find_element_by_id('portalAccountPassword')
password.send_keys('SUP@dmin2')
driver.find_element_by_id('LoginButton').click()

try:
    element_present = EC.presence_of_element_located((By.XPATH, "//a[@class='GradebookLink']"))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print('Timeout')
    timeout = True
time.sleep(2)

names = []
list_of_gradebooks = driver.find_elements_by_xpath("//a[@class='GradebookLink']")
for i in list_of_gradebooks:
    if i.text != '':
        names.append(i.text)

print(names)
