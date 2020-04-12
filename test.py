# 실습 내용에 추가로 코드를 짜는게 어려워서 개인적으로 공부하면서 BeautifulSoup로 웹사이트 크롤링 하는 것을 해 보았습니다.
from bs4 import BeautifulSoup
import urllib.request

def get_soup(target_url):
    html = urllib.request.urlopen(target_url).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

#<table class="grid" style="width:800px"> 태그

def extract_data(soup):
    table = soup.find('table', {'class': 'grid'})
    trs = table.find_all('tr')
    for idx, tr in enumerate(trs):
        if idx > 0:
            tds = tr.find_all('td')
            sequence = tds[0].text.strip()
            description = tds[1].text.strip()
            solved_num = tds[2].text.strip()
            print(sequence, description, solved_num)

for i in range(1, 7):
    target_url = 'http://euler.synap.co.kr/prob_list.php?pg={}'.format(i)
    soup = get_soup(target_url)
    extract_data(soup)


