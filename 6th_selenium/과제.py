from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time

path = os.getcwd() + "/6th_selenium/chromedriver.exe" # for window
driver=webdriver.Chrome(path)

try : 
    driver.get("https://www.naver.com/")
    time.sleep(1)

    
    element = driver.find_element_by_css_selector("input#query.input_text")
    element.send_keys("슬기로운 의사생활") 
    element.submit()
    driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/div[2]/a').click()
   
   
    title=[]
    for i in range(3):  
        time.sleep(1)    

        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")

        conts = bs.find_all("ul", class_="type01")[0].find("li", id="sp_nws1")
        title.append("page" + str(i+1))

        for c in conts :
            title.append(c.find("a", class_=" _sp_each_title").text)

    
        driver.find_element_by_xpath('//*[@id="main_pack"]/div[1]/div[2]/a[10]').click()
    
finally:
    print(title)
    time.sleep(1)
    driver.quit()
   