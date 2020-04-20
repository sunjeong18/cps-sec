import requests
from bs4 import BeautifulSoup
import csv

# 삼성 노트북 모델명, 사양, 리뷰 크롤링 하기. 

class Scrapper():

    def __init__(self):
        self.url = "https://www.samsung.com/sec/notebook/all-notebook/?notebook-7"

    
    def getHTML(self, cnt):
        res = requests.get(self.url + "&start=" + str(cnt * 50))

        if res.status_code != 200: # 코드가 정상적으로 안들어가졌으면 
            print("request error : ", res.status_code) #request error

        html = res.text
        #soup만들기 
        soup = BeautifulSoup(html, "html.parser") #html문서와, 해석기가 인자로 들어간다.
        return soup

    def getproduct(self, soup, cnt):

        
        specification=[]
        model=[]
        review=[]
       

        product_box = soup.find_all("div", class_="product-card__prd-info-title-wrap js-align-h")
        review_box= soup.find_all("div", class_="product-card__detail-marketing-message")
        
        for p in product_box:
            
            if p.find("h3", class_ = "product-card__prd-info-title-name") != None:
                specification.append(p.find("h3", class_ = "product-card__prd-info-title-name").text)
           
            if p.find("div", class_ = "product-card__prd-info-title-serial") != None:
                model.append(p.find("div", class_ = "product-card__prd-info-title-serial").text)
            
        
        for r in review_box:
             if r.find("li", class_="message_list_item") !=None:
                review.append(r.find("li", class_="message_list_item").text)

            
           
        self.writeCSV(specification, model, review)

    def writeCSV(self, specification,model, review):
        file = open("4th assignment.csv", "a", newline="", encoding='UTF8')

        wr = csv.writer(file)
        for i in range(len(model)):
            wr.writerow([str(i+1),specification[i],model[i],review[i]] )

        file.close()

    def scrap(self):
        soupPage = self.getHTML(0)

        file = open("4th assignment.csv", "w", newline="", encoding='UTF8')
        wr = csv.writer(file)
        wr.writerow([ "specification", "model", "review"])
        file.close()

       

if __name__ == "__main__":
    s = Scrapper()
    s.scrap()