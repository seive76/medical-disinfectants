from classes import tweet_api
import tweepy
import pandas as pd
import schedule
import time

auth = tweepy.OAuthHandler(tweet_api.API_KEY, tweet_api.API_SECRET)
auth.set_access_token(tweet_api.ACCESS_TOKEN, tweet_api.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# bring on the present data
# df_1 = pd.read_csv('dat/disin_keywords.csv', usecols=['Time', 'User', 'Tweet'])

# tweets keywords list
keywords = ['휴온스메디케어', '사라야', '퍼슨', '엠에이치헬스케어', '나노팜', '에이치피엔씨', '디엠파이오', '그린제약', '구미제약', '월드씨그룹', '동인당제약', '노보메드']
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
# df = pd.concat([df_1, df_2])
# df.drop_duplicates(inplace=True)
# print(df.shape)
# df.head()

df.to_csv('dat/disin_competitors.csv')

# 매주 금요일 오후 12:30분에 수집개시
# schedule.every().friday.at("12:30").do(tweets_keywords_parsing)

# 
# while true:
#     schedule.run_pending()
#     time.sleep(1)