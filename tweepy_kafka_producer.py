
'''
    Author: Prakhar Mishra
    Date: 9/01/2016
'''

# Importing Packages
import sys
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaClient
from kafka import SimpleProducer
from kafka import SimpleConsumer

# Twitter Credentials
atoken = "285448554-osg0LhexfV1TdpSItHw1EedtPxoGZKl0ZV37Xoqr"
asecret = "jFyLKFzsxi7TrGfcdDoSOJRO1Q9mBOKMLT02tgr0UAwKu"
ckey = "q4KenWrrF0t4BAnVDh5b2AxRX"
csecret = "eYDV5vQVe6E4RP9wrNIez8KSgyI9baBJWGxOPnAmKTsxjBY7UI"

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)


class listener(StreamListener):
    # When data
    def on_data(self, data):
        try:
            # 1st parameter is the kafka topic
            producer.send_messages("socialcops", str(data))
            print 'Sent to producer'           
        except Exception as e:
            print e
    # When error
    def on_error(self, status):
        print status

# Create a stream of data
twitterStream = Stream(auth,listener())

if __name__ == "__main__":
    
    # Create producer and set filters on stream
    kafka = KafkaClient("localhost:9092")
    producer = SimpleProducer(kafka)
    twitterStream.filter(languages = ['en'], track=['the','i','to','an','and','is','e','a','u','o'])
