
from newsapi import NewsApiClient
# import pandas_datareader as pdr 
from textblob import TextBlob
from tensorflow import keras
from tensorflow.keras.models import load_model
from datetime import datetime


#Create NewsApiClient object with API Key
newsapi = NewsApiClient(api_key='93f50165099047b19a1de1f5b2382950')


def sentiment_information(stock_name, latest_date, page_input):
    #Get all the articles that reference the inputted company name, and set
    #the upper bound for the date as the latest stock date (we don't need any
    #articles after taht date, as we don't have stock data)
    sentiment_array = []
    all_articles = newsapi.get_everything(q=stock_name,
                                        #   sources='bbc-news,the-verge',
                                        #   domains='bbc.co.uk,techcrunch.com',
                                        from_param=latest_date,
                                        language='en',
                                        sort_by='relevancy',
                                        page=page_input)
    
    # print(all_articles)
    for i in all_articles['articles']:
        # print(i)
        #Get the date the article was published
        date = i['publishedAt'][0:10]
        #Create the article's information string (title and description will be
        #used in the analysis)
        title = i['title']
        desc = i['description']
        if desc is None:
            desc = ""
        if title is None:
            title = ""
        article_string = title + " " + desc
        value = TextBlob(article_string)
        sentiment_array.append([value.sentiment.polarity])
    # print(sentiment_array)
    return sentiment_array
        





model = load_model('model.h5')

print("What is the stock you want to analyze?")
stock_name = input()
today_date = datetime.today().strftime('%Y-%m-%d')

sentiment_arr = []
for page_num in range(1,4):
    sentiment_arr += sentiment_information(stock_name, today_date, page_num)

sum_change = 0
sum_change2 = 0
for i in sentiment_arr:
    
    prediction = model.predict(i)[0][0]
    sum_change += prediction
    if prediction < 0:
        sum_change2 += -(prediction**0.5)
    else:
        sum_change2 += (prediction**0.5)
    

print(sum_change)
print(sum_change/len(sentiment_arr))
print(sum_change2/len(sentiment_arr))

