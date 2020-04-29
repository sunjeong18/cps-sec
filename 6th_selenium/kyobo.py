from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time

path = os.getcwd() + "/6th_selenium/chromedriver.exe" # for window
driver=webdriver.Chrome(path)

try : 
    driver.get("http://www.kyobobook.co.kr/index.laf?OV_REFFER=https://www.google.com/")
    time.sleep(1)
    
    searchIndex = "파이썬"
    element = driver.find_element_by_class_name("main_input")
    element.send_keys(searchIndex)  # 검색창에 파이썬 입력 
    driver.find_element_by_class_name("btn_search").click() #클릭버튼 눌러주기 

    # 검색 후 도서목록 수집하기 
    html = driver.page_source
    bs= BeautifulSoup(html, "html.parser") #검색하고 검색 첫 페이지에서 찾을 수 있음 

    pages = int(bs.find("span", id="totalpage").text)
    print(pages)


    title=[]
    for i in range(3) :

        time.sleep(1) 

        html = driver.page_source
        bs=BeautifulSoup(html, "html.parser")

        conts= bs.find("div", class_ = "list_search_result" ).find_all("td", class_="detail")
        title.append("page" + str(i+1))
        for c in conts :
            title.append(c.find("div", class_="title").find("strong").text)

        


finally :
    for t in title : 
        if t.find("page") !=-1:
            print()
            print(t)
        else :
            print(t)

    driver.quit()