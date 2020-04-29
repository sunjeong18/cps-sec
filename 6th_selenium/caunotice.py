from selenium import webdriver # web페이지에 있는 정보 받아오기 
from bs4 import BeautifulSoup
import os  # 파이썬 내장 모듈 
import time # 파이썬 내장 모듈 
#request.get 하면 빈 html 갖고 오게 됨 
# c:\Users\chj09\Desktop\3학년 1학기\사이버 물리 시스템 보안\6th_selenium
path = os.getcwd() + "/6th_selenium/chromedriver.exe" # for window

driver = webdriver.Chrome(path)

try : #try밑에 있는 코드가 실행이 되고 
    driver.get("https://www.cau.ac.kr/cms/FR_CON/index.do?MENU_ID=100#page1")
    time.sleep(1)
    

    html = driver.page_source 
    bs= BeautifulSoup(html, "html.parser")

    pages = bs.find("div", class_="pagination").find_all("a")[-1]["href"].split("page")[1] #이렇게 하면 숫자만 나옴 page 248
    pages = int(pages)

    title=[]
    for i in range(3): #url뒤 페이지 1씩 증가하기 
        driver.get("https://www.cau.ac.kr/cms/FR_CON/index.do?MENU_ID=100#page" + str(i+1)) #0번부터 시작해서 1더해줌
        time.sleep(3)

        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")

        conts = bs.find_all("div", class_="txtL")
        title.append("page"+str(i+1))
        for c in conts :
           title.append(c.find("a").text) #a tag의 값

    

finally : #정상적으로 완료가 됐으면 finally code 실행
    #time.sleep(3)
    for t in title:
        if t.find("page")!=-1: #페이지가 없지 않은 경우에만 
            print()    
            print(t)
        else:
            print(t)
    driver.quit()