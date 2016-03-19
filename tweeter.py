import os
import twitter

class HedgehogTweeter(object):
    
    def __init__(self):
        consumer_key = "nKc10yARss9L0g31nhZdwDb0g"
        consumer_secret = "xu1WufVmo3EXbJMWtTUZgIcN0H24cFjQWkZ8ngxqvt36BMeasx"
        access_token = "708645319899107330-ylDlxe6H9k9himdp5eijwGWxnEUv9jl"
        access_token_secret = "3kMOweuDjOPksWYfHuVU5cOsELU9bTYBLVJmJjH3flA7K"
        self.api = twitter.Api(consumer_key=consumer_key, \
                               consumer_secret=consumer_secret, \
                               access_token_key=access_token,
                               access_token_secret=access_token_secret)

    def tweet(self, distance, speed):
        converted_distance = self.convertFeetToMiles(distance)
        
        if int(distance) < 5280:
            distance_tweet = 'I felt lazy. I only ran ' + converted_distance + ' miles... '
        else:
            distance_tweet = 'Whew! I ran ' + converted_distance + ' miles last night! '

        speed_tweet = 'My top speed was ' + str(speed) + ' mi/hr.'
        
        self.api.PostUpdate(distance_tweet + speed_tweet)

        

    def convertFeetToMiles(self, feet):
        return str(float(feet) / 5280.0)[:5]
