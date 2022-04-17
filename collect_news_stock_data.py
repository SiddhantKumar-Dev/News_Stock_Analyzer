#pip3 install newsapi-python
from newsapi import NewsApiClient
#pip3 install pandas_datareader
import pandas_datareader as pdr 
import json
from textblob import TextBlob


# print(testimonial.sentiment)
# print(testimonial.sentiment.polarity)

#API Key: 93f50165099047b19a1de1f5b2382950
#GET https://newsapi.org/v2/everything?q=bitcoin&apiKey=93f50165099047b19a1de1f5b2382950

#Get the name of the stock the user wants to analyze
print("what is the stock name: ")
stock_name = input()
#Get the name of the company the user wants to analyze
print("what is the company name: ")
comp_name = input()

#Get the data for the stock the user wants to analyze
stock_data = pdr.get_data_yahoo(stock_name)
# print(stock_data)

#Get the date of the most updated stock
latest_stock_date = str(stock_data.iloc[-1].name)[0:10]

#Create NewsApiClient object with API Key
newsapi = NewsApiClient(api_key='93f50165099047b19a1de1f5b2382950')

#Get all the articles that reference the inputted company name, and set
#the upper bound for the date as the latest stock date (we don't need any
#articles after taht date, as we don't have stock data)
all_articles = newsapi.get_everything(q=comp_name,
                                    #   sources='bbc-news,the-verge',
                                    #   domains='bbc.co.uk,techcrunch.com',
                                      to=latest_stock_date,
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)

# print(all_articles)
# with open('data.json', 'w') as f:
#     json.dump(all_articles, f)

# f = open('data.json')
# all_articles = json.load(f)

#Get the dates the stock information covers
dates = stock_data.index
#Create a list of the dates in string format
dates_list = [str(i)[:10] for i in dates]
# print(dates_list)
#Create a set with the dates (it is a hash object so searching will be O(1))
date_set = set(dates_list)

#Create the array that will store the article information
impact_array = []

#Go through each article
for i in all_articles['articles']:
    #Get the date the article was published
    date = i['publishedAt'][0:10]
    #Create the article's information string (title and description will be
    #used in the analysis)
    article_string = i['title'] + " " + i['description']

    #Check if the date exists within the stock data
    if date in date_set:

        #Get the stock information for the date
        date_stock = stock_data.loc[date]
        #Find the percent change of the stock (between opening and closing)
        percent_change = ((date_stock[3] - date_stock[2])/date_stock[2])*100

        impact_array.append([article_string, percent_change])

# print(impact_array)

sentiment_array = []
for pair in impact_array:
    value = TextBlob(pair[0])
    sentiment_array.append([value.sentiment.polarity, pair[1]])
print(sentiment_array)



# print(all_articles)
# print(single_day_info)
# print(percent_change)
# for i in range(len(data)):
#     print(data.iloc[i][0])