from classes import tweet_api
import tweepy
import pandas as pd

auth = tweepy.OAuthHandler(tweet_api.API_KEY, tweet_api.API_SECRET)
auth.set_access_token(tweet_api.ACCESS_TOKEN, tweet_api.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# user tweets

keywords = ['페라세이프', '에이치엠씨엔에프산', '사이덱스', '싸이덱스']
limit = 300

# Create DataFrame
columns = ['Time', 'User', 'Tweet']
data = []

for keyword in keywords:
    tweets = tweepy.Cursor(api.search_tweets, 
                       q=keyword,
                       count=100,
                       tweet_mode = 'extended').items(limit)

    for tweet in tweets:
        data.append([tweet.created_at, tweet.user.screen_name, tweet.full_text])

    df=pd.DataFrame(data, columns=columns)
# print(df.shape)
# df.head()

    df.to_csv('dat/disin_mentioned.csv')