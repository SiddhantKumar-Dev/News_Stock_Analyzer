#pip3 install newsapi
from newsapi import NewsApiClient


#API Key: 93f50165099047b19a1de1f5b2382950
#GET https://newsapi.org/v2/everything?q=bitcoin&apiKey=93f50165099047b19a1de1f5b2382950

newsapi = NewsApiClient(api_key='93f50165099047b19a1de1f5b2382950')
all_articles = newsapi.get_everything(q="Tesla",
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2022-03-15',
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)

