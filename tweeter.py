import os
import twitter

class HedgehogTweeter(object):
    
    def __init__(self):
        consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
        access_token = os.environ['TWITTER_ACCESS_TOKEN']
        access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        self.api = twitter.Api(consumer_key=consumer_key, \
                               consumer_secret=consumer_secret, \
                               access_token_key=access_token,
                               access_token_secret=access_token_secret)

    def tweet(self, text):
        self.api.PostUpdate(text)
