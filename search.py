import time
import tweepy
import keys as key
import json


access_secret = key.ACCESS_SECRET
consumer_key = key.CONSUMER_KEY
consumer_secret = key.CONSUMER_SECRET
access_key = key.ACCESS_KEY

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
FILE_NAME = "files/raw_data.txt"
lat = 6.465422
long = 3.406448
coordinate = {lat, long}


#Create a Stream listener
class MaxListener(tweepy.StreamListener):
    def on_data(self, raw_data):
        self.process_data(raw_data)

        return True


    def store_raw_data(self, raw_data, file_name):
        f_write = open(file_name, 'a')
        f_write.write(str(raw_data))
        f_write.close()
        return

    def retrieve_stored_data(self, file_name):
        f_read = open(file_name, 'r')
        raw_data = str(f_read.read().split("created_at"))
        f_read.close()
        return raw_data

    def process_data(self, raw_data):
        print(type(raw_data))
        #data = json.dumps(raw_data)
        self.store_raw_data(raw_data, FILE_NAME)
        #for mentions in data:
            #self.store_raw_data(mentions, FILE_NAME)

    
    def on_error(self, status_code):
        if status_code == 420:
            #Return false in on data disconect the stream
            return False

#Create Stream
class MaxStream():
    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    def start(self, keyword_list):
        self.stream.filter(track=keyword_list)


#Start stream
if __name__ == "__main__":
    listener = MaxListener()

    stream = MaxStream(auth, listener)
    stream.start(['abuse sexually', 'sexual abuse'])

"""for tweet in tweepy.Cursor(api.search, q='#isaac', rpp=100).items():
    # Do something
    #print("Found something...")
    #print("going back in...")
    #print(str(tweet.id) + ' ' + tweet.text)
    print(tweet)
    my_list.append(tweet.text[0]) """

    