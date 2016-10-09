from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re
import json
from translate import translate_string

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="WDn0HTvNEi6RiQEN4I1NVRRxZ"
consumer_secret="TPYkUh1yfaTbA8O723Evgz39SjqEc9XDuSdk1iZtCYIjJ20kwr"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="123434884-dlmAaFEkRKOt1rgj8bQ3ss4R9qX7Lyh5IeCKIiiV"
access_token_secret="STSuBDvC6IfHEhpZXZbfvRyHCez93KHMtWvXQt8nYFByS"

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        try:
            decoded = json.loads(data) 
            #print(decoded)
            text = decoded['user']["screen_name"]
            print('@'+text+' - '+decoded["text"])
            translate_string('@'+text, 7)
            return True
        except:
            pass

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['opencam'])