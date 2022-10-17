from classes import tweet_api
import tweepy
import pandas as pd

auth = tweepy.OAuthHandler(tweet_api.API_KEY, tweet_api.API_SECRET)
auth.set_access_token(tweet_api.ACCESS_TOKEN, tweet_api.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# user tweets

user = 'KSGEendoscopy' # 소화기내시경학회 트위터 이름
limit = 300 # 추출데이터 300회

tweets = tweepy.Cursor(api.user_timeline, 
                       screen_name=user,
                       count=200,
                       tweet_mode = 'extended').items(limit)

# Create DataFrame
columns = ['Time', 'User', 'Tweet']
data = []

for tweet in tweets:
    data.append([tweet.created_at, tweet.user.screen_name, tweet.full_text])

df=pd.DataFrame(data, columns=columns)
df.to_csv('dat/소화기내시경학회트윗.csv')