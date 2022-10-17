from classes import tweet_api
import tweepy
import pandas as pd

auth = tweepy.OAuthHandler(tweet_api.API_KEY, tweet_api.API_SECRET)
auth.set_access_token(tweet_api.ACCESS_TOKEN, tweet_api.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# user tweets

keywords = '병원감염'
limit = 300

tweets = tweepy.Cursor(api.search_tweets, 
                       q=keywords,
                       count=100,
                       tweet_mode = 'extended').items(limit)

# Create DataFrame
columns = ['Time', 'User', 'Tweet']
data = []

for tweet in tweets:
    data.append([tweet.created_at, tweet.user.screen_name, tweet.full_text])

df=pd.DataFrame(data, columns=columns)
# print(df.shape)
# df.head()

df.to_csv('dat/병원감염트윗.csv')