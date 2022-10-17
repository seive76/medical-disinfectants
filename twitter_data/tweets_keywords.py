from classes import tweet_api
import tweepy
import pandas as pd
import schedule
import time

auth = tweepy.OAuthHandler(tweet_api.API_KEY, tweet_api.API_SECRET)
auth.set_access_token(tweet_api.ACCESS_TOKEN, tweet_api.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def tweets_keywords_parsing():
    # bring on the present data
    df_1 = pd.read_csv('dat/disin_keywords.csv', usecols=['Time', 'User', 'Tweet'])

    # tweets keywords list
    keywords = ['병원감염', '병원 소독제', '병원소독제', '내시경소독제', '내시경 소독제']
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

    df_2=pd.DataFrame(data, columns=columns)
    df = pd.concat([df_1, df_2])
    df.drop_duplicates(inplace=True)
    # print(df.shape)
    # df.head()

    df.to_csv('dat/disin_keywords.csv')

# 매주 금요일 오후 12:30분에 수집개시
schedule.every().friday.at("12:30").do(tweets_keywords_parsing)

#
while true:
    schedule.run_pending()
    time.sleep(1)