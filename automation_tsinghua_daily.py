
# coding: utf-8

# In[16]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import os
import schedule


# In[14]:


os.makedirs('./daily_screenshot')

def job():
    submit_daily()
    print('Finished at ' + time.asctime(time.localtime(time.time())) + '\n')

def submit_daily():
    chrome_options = Options()
    chrome_options.add_argument("--headless")       # define headless
    chrome_options.add_argument('--no-sandbox') 
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)

    # will redirect to online service platform after login
    driver.get("https://id.tsinghua.edu.cn/do/off/ui/auth/login/form/a585295b8da408afdda9979801383d0c/0?/fp/")

    # fill in username and password and click login button
    username = driver.find_element_by_xpath("//input[@id='i_user']")
    username.send_keys("2017012003")
    password = driver.find_element_by_xpath("//input[@id='i_pass']")
    password.send_keys("czfqqaa1234cjwlh")
    driver.find_element_by_link_text("登录").click()

    # waiting for redirecting and image to load
    daily_img = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='formHome_serve_content'] \
        /div[@name='【日报】学生健康和出行情况报告']/div[2]/img"))
    )
    daily_img.click()

    # waiting for iframe and inside forms to load
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@id='formIframe']"))
    )
    driver.switch_to.frame("formIframe")
    form_title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h2/strong"))
    )
    driver.switch_to.default_content()

    # click the submit button
    submit_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@id='commit']"))
    )
    # submit_button.click()

    time.sleep(3)
    screenshot_name = time.asctime(time.localtime(time.time())) + '.png'
    driver.get_screenshot_as_file("./daily_screenshot/" + screenshot_name )
    driver.quit()
    return None

schedule.every(30).seconds.do(job)
# schedule.every().day.at("3:00").do(job)
    
while True:
    schedule.run_pending()
    time.sleep(1)

