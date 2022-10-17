from classes import tweet_api
import tweepy
import pandas as pd

auth = tweepy.OAuthHandler(tweet_api.API_KEY, tweet_api.API_SECRET)
auth.set_access_token(tweet_api.ACCESS_TOKEN, tweet_api.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

public_tweets = api.home_timeline()

columns = ['time', 'twitter', 'tweet']
data = []

for tweet in public_tweets:
    data.append([tweet.created_at, tweet.user.screen_name, tweet.text])

df=pd.DataFrame(data, columns=columns)    

df.to_csv('public_tweets.csv')