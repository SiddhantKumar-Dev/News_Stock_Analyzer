#pip3 install newsapi-python
from newsapi import NewsApiClient
#pip3 install pandas_datareader
import pandas_datareader as pdr 
import json
from textblob import TextBlob
import csv


# print(testimonial.sentiment)
# print(testimonial.sentiment.polarity)

#API Key: 93f50165099047b19a1de1f5b2382950
#GET https://newsapi.org/v2/everything?q=bitcoin&apiKey=93f50165099047b19a1de1f5b2382950




def get_stock_data(ticker):
    #Get the data for the stock the user wants to analyze
    stock_data = pdr.get_data_yahoo(ticker)
    return stock_data


#Create NewsApiClient object with API Key
newsapi = NewsApiClient(api_key='93f50165099047b19a1de1f5b2382950')


def get_articles(stock_name, latest_date, page_input):
    #Get all the articles that reference the inputted company name, and set
    #the upper bound for the date as the latest stock date (we don't need any
    #articles after taht date, as we don't have stock data)
    all_articles = newsapi.get_everything(q=stock_name,
                                        #   sources='bbc-news,the-verge',
                                        #   domains='bbc.co.uk,techcrunch.com',
                                        to=latest_date,
                                        language='en',
                                        sort_by='relevancy',
                                        page=page_input)
    return all_articles

# print(all_articles)
# with open('data.json', 'w') as f:
#     json.dump(all_articles, f)

# f = open('data.json')
# all_articles = json.load(f)
def get_impact_array(stock_data, all_articles):
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

    return impact_array

def get_sentiment(impact_array):
    sentiment_array = []
    for pair in impact_array:
        value = TextBlob(pair[0])
        sentiment_array.append([value.sentiment.polarity, pair[1]])
    return sentiment_array
    # print(sentiment_array)

def combine_i_and_s(impact, sentiment):
    for i in range(len(impact)):
        impact[i].append(sentiment[i][0])
    return impact
def write_to_file(impact_sentiment_array):
    with open('text_stock_sentiment.txt', 'w') as f:
        mid_string = " !@#$%^&*() "
        f.write("Text &&&&& Stock Change &&&&& Sentiment\n")
        for i in impact_sentiment_array:
            line = "{" + i[0] + mid_string + str(i[1]) + mid_string + str(i[2]) + "}" + "\n\n"
            f.write(line)
    with open('stock_sentiment.txt', 'w') as f2:
        f2.write("Stock Change &&&& Sentiment\n")
        for i in impact_sentiment_array:
            line = str(i[1]) + " " + str(i[2]) + "\n"
            f2.write(line)
    
        
        # csv.writer(f, delimiter=' ').writerows(impact_sentiment_array)

#Get the name of the stock the user wants to analyze
##### print("what is the stock name: ")
##### stock_name = input()
#Get the name of the company the user wants to analyze
##### print("what is the company name: ")
#####comp_name = input()
#####stock_data = get_stock_data(stock_name)

# latest_stock_date = str(stock_data.iloc[-1].name)[0:10]

# article_data = get_articles(comp_name, latest_stock_date, 1)
# impact_array = get_impact_array(stock_data, article_data)
# sentiment = get_sentiment(impact_array)
# print(stock_data)
# print("--------------------")
# print(article_data)
# print("--------------------")
# print(impact_array)
# print("--------------------")
# print(sentiment)

# impact_sentiment_array = combine_i_and_s(impact_array, sentiment)
# write_to_file(impact_sentiment_array)



stock_list_array = [['Apple', 'AAPL'], ['Microsoft', 'MSFT'], ['Google', 'GOOG'], ['Amazon', 'AMZN'], ['Tesla', 'TSLA'], ['Facebook', 'FB'], ['Meta', 'FB'], ['NVIDIA', 'NVDA'], ['TSMC', 'TSM'], ['Tencent', 'TCEHY'], ['ASML', 'ASML'], ['Broadcom', 'AVGO'], ['Cisco', 'CSCO'], ['Oracle', 'ORCL'], ['Adobe', 'ADBE'], ['Intel', 'INTC'], ['Salesforce', 'CRM'], ['QUALCOMM', 'QCOM'], ['AMD', 'AMD'], ['Netflix', 'NFLX'], ['Intuit', 'INTU']]
impact_array = []
sentiment = []
for stock_set in stock_list_array:
    stock_name = stock_set[0]
    stock_ticker = stock_set[1]

    print("Parsing " + stock_name)

    stock_data = get_stock_data(stock_ticker)
    latest_stock_date = str(stock_data.iloc[-1].name)[0:10]
    
    for page_number_iter in range(1,4):
        print("On page: " + str(page_number_iter))
        article_data = get_articles(stock_name, latest_stock_date, page_number_iter)
        impact_array += get_impact_array(stock_data, article_data)
        sentiment += get_sentiment(impact_array)

impact_sentiment_array = combine_i_and_s(impact_array, sentiment)
write_to_file(impact_sentiment_array)




# print(all_articles)
# print(single_day_info)
# print(percent_change)
# for i in range(len(data)):
#     print(data.iloc[i][0])



