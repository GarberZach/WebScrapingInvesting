# WebScrapingInvesting

#### This project aims to gather articles (tweets, news articles) from internet sources and classify the sentiment of these articles in attempt to gain meaninful insight on market direction.

## Note

This project will not run if downloaded as all API credentials have been removed to preserve security.


## Organization

  Project isn't perfect but does return quantifiable results.

  * data

     This purpose of this subdirectory is to store csv files that contain: index, sentiment score, datetime

  * AWS_Handler.py
  
     Stores and retrieves csv files from AWS. Also converts from Pandas dataframe to csv.

  * Webscraper.py
  
     Scrapes popular news sites for articles relating to a specified keyword (company or product). Next, parses articles so they can be analyzed by the natural language processor. Analyzer then creates a sentiment score for each article and stores them in a Pandas data frame.

  * Twitter_Stream.py and Tweet_Analyzer.py
  
     Preforms tasks very similar to WebScraper.py except using twitter as an article source.

  * BackTraderCerebro.py

    Utilizes the framework backtrader built by Backtrader, basically it allows one to make a strategy that uses data (in this case using sentiment scores) to make buy/sell decisions. Then the preformance of the strategy can be compared to historical stock data to gain a metric of success.
  
     