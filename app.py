import tweepy
import time
import keys as key
import json
import pandas as pd
import csv
import re as reg
from textblob import TextBlob
import string
import preprocessor as p

#Get access key from a file
access_secret = key.ACCESS_SECRET
consumer_key = key.CONSUMER_KEY
consumer_secret = key.CONSUMER_SECRET
access_key = key.ACCESS_KEY

#authenticate and connect
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

FILE_NAME = 'files/last_seen_id.txt'
FILE_NAME2 = "files/raw_data.txt"
class AutoReplyTweet():

    def retrieve_last_seen_id(self, file_name):
        f_read = open(file_name, 'r')
        last_seen_id = int(f_read.read().strip())
        f_read.close()
        return last_seen_id

    def store_last_seen_id(self, last_seen_id, file_name):
        f_write = open(file_name, 'w')
        f_write.write(str(last_seen_id))
        f_write.close()
        return

    def reply_to_tweet(self,):
        print("Replying to tweet...")
        last_seen_id = self.retrieve_last_seen_id(FILE_NAME)
        mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended') 

        for mention in reversed(mentions):
            print(str(mention.id) +' _ ' + mention.full_text)
            last_seen_id = mention.id
            self.store_last_seen_id(last_seen_id, FILE_NAME)
            #if '#isaac' in mention.full_text.lower():
            api.update_status('@' + mention.user.screen_name +' You have reached daddy Isaac, and has it is I am currently unavailable. So, drop your message and I will surely get back to you. You are doing well. Beep where I am tweeting from (｡♥‿♥｡)', mention.id)

#Auto implementation
"""while True:
    reply_to_tweet()
    time.sleep(15)"""


#This section implements Twitter API scraping - Streaming

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
        self.store_raw_data(raw_data, FILE_NAME2)
    
    def on_error(self, status_code):
        if status_code == 420:
            #Return false in on data disconect the stream
            return False

#Streaming implementation continues
#Create Stream
class MaxStream():
    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    def start(self, keyword_list):
        self.stream.filter(track=keyword_list)

#Initialize stream
#Start stream
if __name__ == "__main__":
    listener = MaxListener()

    #stream = MaxStream(auth, listener)
    #stream.start(['abuse sexually', 'sexual abuse'])

#direct_messages = api.list_direct_message(count=100, cursor=-1)
direct_messages = api.get_direct_message(id=384760732-1149202744353480704, full_text=True)
print(type(direct_messages))
