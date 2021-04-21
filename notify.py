from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import pickle
import re
import ast
import yaml

timeout = 8

def notify(data, mac=True):
    if not data:
        cmd = "osascript -e 'display notification \"No updates!\" with title \"Aeries\"'"
        os.system(cmd)
        return
    for title, bodyList in data.items(): 
        for body in bodyList:
            cmd = "osascript -e 'display notification \"" + body + "\" with title \"" + title + "\"'"
            os.system(cmd)

def retrieveNewData():
    with open("./configs/config.yaml", 'r') as stream:
        cfg = yaml.safe_load(stream)
    gradeBookSelector = cfg['classes']

    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    #options.add_argument('window-size=1200x600')
    driver = webdriver.Chrome('./chromedriver',options=options)
    driver.get('https://parentnet.tustin.k12.ca.us/ParentPortal/LoginParent.aspx')
    username = driver.find_element_by_id('portalAccountUsername')
    username.send_keys(cfg['username'])
    driver.find_element_by_id('next').click()

    time.sleep(1)

    password = driver.find_element_by_id('portalAccountPassword')
    password.send_keys(cfg['password'])
    driver.find_element_by_id('LoginButton').click()

    try:
        #element_present = EC.presence_of_element_located((By.CLASS_NAME, 'GradebookLink'))
        element_present = EC.presence_of_element_located((By.XPATH, "//a[@class='GradebookLink']"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        cmd = "osascript -e 'display notification \"Script failed on timeout!\" with title \"Aeries\"'"
        os.system(cmd)
        return
    time.sleep(2)
    #list_of_gradebooks = driver.find_elements_by_class_name('GradebookLink')
    #list_of_gradebooks = [i for i in list_of_gradebooks if i.text in gradeBookSelector]

    #time.sleep(1)
    count = 1
    updates = 0
    notisDict = {}
    for i in range(len(gradeBookSelector)):
        new_assignment_list = []
        list_of_gradebooks = driver.find_elements_by_xpath("//a[@class='GradebookLink']")
        list_of_gradebooks = [i for i in list_of_gradebooks if i.text in gradeBookSelector]
        print('Period '+ str(i + 1) + ' Checked')
        period = list_of_gradebooks[i].text
        list_of_gradebooks[i].click()

        #i.click()
        try:
            element_present = EC.presence_of_element_located((By.XPATH, "//tr[@class='tinymode FullWidth CardView forceShow']"))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            cmd = "osascript -e 'display notification \"Script failed on timeout!\" with title \"Aeries\"'"
            os.system(cmd)
            return
        time.sleep(1)
        grades_list = driver.find_elements_by_xpath("//tr[@class='tinymode FullWidth CardView forceShow']")

        path = './data/' + 'period' + str(count) + '.p'
        with open(path,'rb') as handle:
            checked_grades = pickle.load(handle)

        for j in grades_list:
            element = j.find_element_by_class_name('FullWidthAutoHeight').text
            #element = j.find_element_by_class_name('Card').text
            #print(element)
            score = re.search(r'(.+) / .+', element)
            if score == None:
                continue
            score = score.group(0)
            grading_status = re.search(r'True|False',element)
            grading_status = ast.literal_eval(grading_status.group(0))
            assignment = j.find_element_by_class_name('TextHeading').text
            if assignment not in checked_grades and grading_status:
                checked_grades.append(assignment)
                assign_name = str(assignment).split(' - ')[1]
                #SMSBody += assign_name + '\n' + str(score) + '\n\n'
                body = assign_name + '\n' + str(score)
                new_assignment_list.append(body)
                updates += 1
            #element = j.find_element_by_xpath("//td//span[@class='TextSubSection']").text
        with open(path,'wb') as handle:
            pickle.dump(checked_grades,handle)
        #print(assignment_list)
        title = str(period)
        if len(new_assignment_list) > 0:   
            notisDict[title] = new_assignment_list
        count += 1
        driver.execute_script("window.history.go(-1)")
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'GradebookLink'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            cmd = "osascript -e 'display notification \"Script failed on timeout!\" with title \"Aeries\"'"
            os.system(cmd)
            return
        time.sleep(3)
        checked_grades = []
    
    driver.quit()
    #print('Finished')
    return notisDict

data = retrieveNewData()
notify(data)
