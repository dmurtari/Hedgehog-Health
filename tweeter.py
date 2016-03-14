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

    def tweet(self, distance, speed):
        converted_distance = convertFeetToMiles(distance)
        
        if int(distance) < 5280:
            distance_tweet = 'I felt lazy. I only ran ' + converted_distance + ' miles... '
        else:
            distance_tweet = 'Whew! I ran ' + converted_distance + ' miles! '

        speed_tweet = 'My top speed was ' + speed + ' mi/hr.'
        
        self.api.PostUpdate(distance_tweet + speed_tweet)

        

    def convertFeetToMiles(self, feet):
        return str(float(feet) / 5280.0)[:5]
