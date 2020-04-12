#실습한 것에 추가해서 수정하는게 어려워서 개인적으로 찾아보면서 네이버 베스트 셀러 웹 크롤링을 해보았습니다. 

# 실행하기 위해 필요한 패키지 목록

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


url = "https://book.naver.com/bestsell/bestseller_list.nhn"

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(30)


# 네이버의 베스트셀러 웹페이지를 가져오기
driver.get(url)
bsObject = BeautifulSoup(driver.page_source, 'html.parser')



# 책의 상세 웹페이지 주소를 추출하여 리스트에 저장
book_page_urls = []
for index in range(0, 25):
    dl_data = bsObject.find('dt', {'id':"book_title_"+str(index)})
    link = dl_data.select('a')[0].get('href')
    book_page_urls.append(link)



# 메타 정보와 본문에서 필요한 정보를 추출
for index, book_page_url in enumerate(book_page_urls):

    driver.get(book_page_url)
    bsObject = BeautifulSoup(driver.page_source, 'html.parser')


    title = bsObject.find('meta', {'property':'og:title'}).get('content')
    author = bsObject.find('dt', text='저자').find_next_siblings('dd')[0].text.strip()
    image = bsObject.find('meta', {'property':'og:image'}).get('content')
    url = bsObject.find('meta', {'property':'og:url'}).get('content')

    dd = bsObject.find('dt', text='가격').find_next_siblings('dd')[0]
    salePrice = dd.select('div.lowest strong')[0].text
    originalPrice = dd.select('div.lowest span.price')[0].text

    print(index+1, title, author, image, url, originalPrice, salePrice)
