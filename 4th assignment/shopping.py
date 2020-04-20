
import requests
from bs4 import BeautifulSoup
import csv

# 브랜디 상품 크롤링하기 

class pScrapper():

    def __init__(self):
        self.url = "https://www.brandi.co.kr/"

    def getHTML(self):
        res = requests.get(self.url)

        if res.status_code != 200: # 코드가 정상적으로 안들어가졌으면 
            print("request error : ", res.status_code) #request error

        html = res.text
        #soup만들기 
        soup = BeautifulSoup(html, "html.parser") #html문서와, 해석기가 인자로 들어간다.
        return soup

    def getproduct(self,soup):

        
        product=[]
        price=[]
        total=[]

        soup=self.getHTML()
       

        product_box = soup.find_all("ul", class_="lilst2")
       
        
        for p in product_box:
            
            if p.find("li", class_="list_title")!= None:
                product.append(p.find("li", class_="list_title").text)
            if p.find("li", class_="list_price")!= None:
                price.append(p.find("li", class_="list_price").text)
            if p.find("li", class_="list_count") != None :
                total.append(p.find("li", class_="list_count").text)

            self.writeCSV(product,price,total)

    def writeCSV(self,product, price, total):
        file = open("shopping.csv", "a", newline='')

        wr = csv.writer(file)

        for i in range(len(product)):
            wr.writerow([product[i],price[i],total[i]] )

        file.close()

    def scrap(self):
      

        file = open("shopping.csv", "w", newline='')
        wr = csv.writer(file)
        wr.writerow([ "title", "price", "count"])
        file.close()

       

       

if __name__ == "__main__":
    s = pScrapper()
    s.scrap()