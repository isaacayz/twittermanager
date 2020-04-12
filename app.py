import tweepy
import time
import keys as key


access_secret = key.ACCESS_SECRET
consumer_key = key.CONSUMER_KEY
consumer_secret = key.CONSUMER_SECRET
access_key = key.ACCESS_KEY

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweet():
    print("Replying to tweet...")
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended') 

    for mention in reversed(mentions):
        print(str(mention.id) +' _ ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        #if '#isaac' in mention.full_text.lower():
        api.update_status('@' + mention.user.screen_name +' You have reached daddy Isaac, and has it is I am currently unavailable. So, drop your message and I will surely get back to you. You are doing well. Beep where I am tweeting from (｡♥‿♥｡)', mention.id)

while True:
    reply_to_tweet()
    time.sleep(15)