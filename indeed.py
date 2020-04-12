import requests
from bs4 import BeautifulSoup
import csv

class Scrapper() :
    def __init__(self):
        self.url = "https://kr.indeed.com/jobs?q=python"

    def getHTML(self, cnt):
        res = requests.get(self.url + "&start=" + str(cnt * 50))

        if res.status_code != 200:
            print("request error : ", res.status_code)

        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def getPages(self, soup):
        pages = soup.select(".pagination > a")
        return len(pages)

    def getCards(self, soup, cnt):
        jobCards = soup.find_all("div", class_="jobsearch-SerpJobCard")
        jobID = []
        jobTitle = []
        jobLocation = []

        for j in jobCards:
            jobID.append("https://kr.indeed.com/viewjob?jk=" + j["data-jk"])
            jobTitle.append(j.find("a").text.replace("\n", ""))
            if j.find("div", class_ = "location") != None:
                jobLocation.append(j.find("div", class_ = "location").text)
            elif j.find("span", class_ = "location") != None:
                jobLocation.append(j.find("span", class_="location").text)

        self.writeCSV(jobID, jobTitle, jobLocation, cnt)

    def writeCSV(self, ID, Title, Location, cnt):
        file = open("indeed.csv", "a", newline="")

        wr = csv.writer(file)
        for i in range(len(ID)):
            wr.writerow([str(i+1+(cnt*50)), ID[i], Title[i], Location[i]])

        file.close()

    def scrap(self):
        soupPage = self.getHTML(0)
        pages = self.getPages(soupPage)

        file = open("indeed.csv", "w", newline="")
        wr = csv.writer(file)
        wr.writerow(["No. ", "Link", "Title", "Location"])
        file.close()

        for i in range(pages):ss
           soupCard = self.getHTML(i)
           self.getCards(soupCard, i)
           print(i+1, "번째 페이지 Done")

if __name__ == "__main__":
    s = Scrapper()
    s.scrap()