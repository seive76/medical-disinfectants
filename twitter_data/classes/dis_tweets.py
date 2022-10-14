import config

def parse_dis_tweets():
    # what if want to store them in txt
    
    client = tweepy.Client(bearer_token=config.BEARER_TOKEN)

    query = '소독제 -is:retweet'
    
    file_name = 'disinfectants_tweets_text.txt'

    with open(file_name, 'a+') as filehandler:
        for tweet in tweepy.Paginator(client.search_recent_tweets, query = query, max_results=100).flatten(limit=1000):
            filehandler.write('%s\n' % tweet.text)