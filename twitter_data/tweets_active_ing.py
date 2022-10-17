from classes import tweet_api
import tweepy
import pandas as pd

auth = tweepy.OAuthHandler(tweet_api.API_KEY, tweet_api.API_SECRET)
auth.set_access_token(tweet_api.ACCESS_TOKEN, tweet_api.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# user tweets

keywords = ['과산화수소', '과아세트산', '오피에이', '과초산', 'GA소독제', 'PAA소독제', 'OPA소독제', 'OPA 소독제', 'GA 소독제', 'PAA 소독제']
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

    df.to_csv('dat/ingredients_mentioned.csv')