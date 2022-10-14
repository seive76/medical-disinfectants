import tweepy
import config

def flatten_tweets(tweets_json):
    """ Flattens out tweet dictionaries so relevant JSON
        is in a top-level dictionary."""
    tweets_list = []
    
    # Iterate through each tweet
    for tweet in tweets_json:
        tweet_obj = json.loads(tweet)
    
        # Store the user screen name in 'user-screen_name'
        tweet_obj['user-screen_name'] = tweet_obj['user']['screen_name']
    
        # Check if this is a 140+ character tweet
        if 'extended_tweet' in tweet_obj:
            # Store the extended tweet text in 'extended_tweet-full_text'
            tweet_obj['extended_tweet-full_text'] = tweet_obj['extended_tweet']['full_text']
    
        if 'retweeted_status' in tweet_obj:
            # Store the retweet user screen name in 'retweeted_status-user-screen_name'
            tweet_obj['retweeted_status-user-screen_name'] = tweet_obj['retweeted_status']['user']['screen_name']

            # Store the retweet text in 'retweeted_status-text'
            tweet_obj['retweeted_status-text'] = tweet_obj['retweeted_status']['text']
            
        tweets_list.append(tweet_obj)
    return tweets_list

def parse_disinfectants_tweets():
    """ '소독제'언급 트윗 추출(retweets 제외), 
       텍스트파일, 'disinfectants_tweets.txt', 저장하기"""
    
    client = tweepy.Client(bearer_token=config.BEARER_TOKEN)
    query = '소독제 -is:retweet'
    
    # what if want to store them in txt
    file_name = 'disinfectants_tweets_text.txt'

    with open(file_name, 'a+') as filehandler:
        for tweet in tweepy.Paginator(client.search_recent_tweets, query = query, max_results=100).flatten(limit=1000):
            filehandler.write('%s\n' % tweet.text)
    