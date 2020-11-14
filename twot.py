from helper_functions import clean_tweet
from tweepy import OAuthHandler
from tweepy import Cursor
import numpy as np
import pandas as pd
from time import sleep
import twitter_credentials
import tweepy
import json
from notify_run import Notify

auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)  # YIKES so twitter doesnt ban me

search_terms1 = ['Nike', 'Adidas', 'Netflix', 'Amazon', 'Starbucks', 'Apple', 'Dell', 'Ford', 'Ubisoft', 'Nintendo',
                 'Sony', 'EasyJet', 'Pfizer']
search_terms2 = ['Microsoft', 'Disney', 'Guardian', 'EA', 'Samsung',
                 'FedEx', 'AIG', 'Activision']


def stream_tweets(search_term):
    data = []  # empty list to which tweet_details obj will be added
    counter = 0  # counter to keep track of each iteration
    for tweet in tweepy.Cursor(api.search, q='\"{}\" -filter:retweets'.format(search_term), count=100, lang='en',
                               tweet_mode='extended').items():

        tweet_details = {}
        tweet_details['tag'] = search_term
        tweet_details['tweet'] = tweet.full_text
        tweet_details['created'] = tweet.created_at.strftime("%d-%b-%Y")  # Want timestamps to match to stock price
        clean_t = clean_tweet(tweet_details['tweet'])  # Gets rid of hyperlinks
        tweet_details['tweet'] = clean_t
        print(tweet_details)
        data.append(tweet_details)
        counter += 1
        if counter == 100:  # Api.search only runs 100 times so add a loop
            break
        else:
            pass
    with open('data/{}.json'.format(search_term), 'a') as f:
        json.dump(data, f)
    print('done!')


if __name__ == "__main__":
    notify = Notify()
    notify.send('Starting stream')
    print('Starting to stream...')
    counter = 0
    try:
        while counter != 10:  # Infinite loop
            for search_term in search_terms1:
                stream_tweets(search_term)
                print('finished!')
                counter += 1
    except:
        notify.send('Eoghan your twitter scraping program has failed')  # Send me an android notification
    finally:
        notify.send('Eoghan your twitter scraping program has finally failed')  # Send me an android notification
