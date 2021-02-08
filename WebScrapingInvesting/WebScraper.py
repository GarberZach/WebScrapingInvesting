from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import datetime
import os
import nltk
import warnings
import pandas
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import AWS_Handler

class webScraper():
    def __init__(self, keyword, date):
        self.urlList = self.getAllLinks(keyword, date)
        os.remove("tempPage.html")

    # Returns a BeautifulSoup Object for a given keyword and page number
    def savePageSoup(self, keyword, page):
        # Gets the url of a MarketWatch search for the keyword
        if page == 0:
            URL = "https://www.marketwatch.com/search?q={}&m=Keyword&rpp=100&mp=0&bd=false&rs=true".format(keyword)
        else:
            URL = "https://www.marketwatch.com/search?q={}&m=Keyword&rpp=100&mp=0&bd=false&rs=true&o={}".format(keyword, 100*page+page)

        response = urllib.request.urlopen(URL)
        webContent = response.read()

        # Save a temporary HTML file of the search to be able to create a BeautifulSoup object later
        f = open("tempPage.html", 'wb')
        f.write(webContent)
        f.close()

        # Create and return the BeautifulSoup object
        with open("tempPage.html") as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            return soup

    # Turn a date string of the form
    # H:MM a.m. Month. Day Year
    # Into a Datetime object
    def parseDate(self, dateString):
        date = dateString.split(" ")
        time = date[0].split(":")
        time[0] = int(time[0])
        time[1] = int(time[1])
        if date[1] == "p.m." and time[0] != 12:
            time[0] += 12
        months = {
            "Jan.":1,
            "Feb.":2,
            "Mar.":3,
            "Apr.":4,
            "May.":5,
            "June.":6,
            "July.":7,
            "Aug.":8,
            "Sept.":9,
            "Oct.":10,
            "Nov.":11,
            "Dec.":12
        }
        month = months[date[2]]
        day = int(date[3][:-1])
        year = int(date[4])

        return datetime.datetime(year, month, day, hour=time[0], minute=time[1])

    def getResultList(self, keyword, soup, dateLimit):
        # Get the list of results and dates
        resultList = soup.find_all("div", class_="searchresult")
        dates = soup.find_all("div", class_="deemphasized")

        lastIndex = -1 
        curList = []

        for i, (result, date) in enumerate(zip(resultList, dates)):
            # For each result check to see if keyword is in title
            curResult = BeautifulSoup(str(result), 'html.parser')
            curTitle = BeautifulSoup(str(curResult.a), features='html.parser').string
            contains = False
            if (keyword.lower() in curTitle.lower()):
                contains = True

            # Get the link that corresponds to the result
            curLink = curResult.a['href']
            if curLink[0] == "/":
                curLink = "http://www.marketwatch.com" + curLink

            # Get the date that corresponds with the result
            tempDate = BeautifulSoup(str(date), 'html.parser')
            spans = tempDate.find("span", class_="invisible")
            if spans==None:
                spans = tempDate.find("span")
            spans = BeautifulSoup(str(spans), 'html.parser').string

            # Format date
            curDate = self.parseDate(str(spans))

            # Check to see if result is outside of date range
            if curDate > dateLimit:
                lastIndex = i
            
            # Add the result to the list of results if the title contians keyword
            if (contains):
                print(curTitle)
                curList.append([curLink, curDate])
            
        return curList, lastIndex

    def getAllLinks(self, keyword, date):
        page = 0
        pastDate = True
        linkList = []
        while pastDate:
            # Create BeautifulSoup for the page
            soup = self.savePageSoup(keyword, page)

            # Get all results on page
            curList, lastIndex = self.getResultList(keyword, soup, date)

            # Get all results in date range
            if lastIndex == -1:
                linkList.extend(curList)
            else:
                linkList.extend(curList[:lastIndex])
                pastDate = False

            page += 1 

        return linkList

    def getSentiments(self, years = 0, months = 0, days = 0, hours = 0, minutes = 0, seconds = 0):
        sentimentScores = []

        # For each result calculate Vader sentiment score
        for linkPair in self.urlList:
            # Open page and read all text
            page = urllib.request.urlopen(linkPair[0])
            soup = BeautifulSoup(page, 'html.parser')
            body = soup.find_all("div", class_="column column--full article__content")
            textSoup = BeautifulSoup(str(body), 'html.parser')
            sentences = textSoup.find_all("p")
            passage = ""
            for sentence in sentences:
                passage += str(sentence)

            # Create sentiment analyzer and get score for page
            sia = SentimentIntensityAnalyzer()
            sentiment = sia.polarity_scores(passage)['compound']

            pageTimeSpan = linkPair[1]

            """
            # Turn result date into bar form
            pageTimeSpan = pageTimeSpan.replace(year=linkPair[1].year-(linkPair[1].year % years) if years != 0 else linkPair[1].year)
            pageTimeSpan = pageTimeSpan.replace(month=linkPair[1].month-(linkPair[1].month % months) if months != 0 else linkPair[1].month)
            pageTimeSpan = pageTimeSpan.replace(day=linkPair[1].day-(linkPair[1].day % days) if days != 0 else linkPair[1].day)
            pageTimeSpan = pageTimeSpan.replace(hour=linkPair[1].hour-(linkPair[1].hour % hours) if hours != 0 else linkPair[1].hour)
            pageTimeSpan = pageTimeSpan.replace(minute=linkPair[1].minute-(linkPair[1].minute % minutes) if minutes != 0 else linkPair[1].minute)
            pageTimeSpan = pageTimeSpan.replace(second=linkPair[1].second-(linkPair[1].second % seconds) if seconds != 0 else linkPair[1].second)

            """

            sentimentScores.append([sentiment, pageTimeSpan])

        sentimentScores = pandas.DataFrame(sentimentScores, columns=['Score', 'Date'])
        print(sentimentScores)

        return sentimentScores

    def put_aws(self, data_frame, ticker):
        handler = AWS_Handler()
        handler.put_data(data_frame= data_frame, ticker= ticker)