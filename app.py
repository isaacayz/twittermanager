import tweepy

CONSUMER_KEY = 'KnPYfM8bVxZnlouSqTVSdEPwh'
CONSUMER_SECRET = 'WfggoT2NtGAD56DDPoGubvCVWt2txDHWLjy7cwbgGf6wN7Pori'
ACCESS_KEY = '384760732-BHwopT7JoZ9AUXcBoy5C2aJtT5ZSSlNqUizQxf9O'
ACCESS_SECRET = 'mfMn84xBbmkkeeS465SOphLWVm2RGHGq55sYEOKCv0Y2C'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
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

last_seen_id = retrieve_last_seen_id(FILE_NAME)
mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended') 

for mention in reversed(mentions):
    print(str(mention.id) +' _ ' + mention.full_text)
    last_seen_id = mention.id
    store_last_seen_id(last_seen_id, FILE_NAME)
    if '#isaac' in mention.full_text.lower():
        api.update_status('@' + mention.user.screen_name +' You are doing well small girl. Beep where I am tweeting from (｡♥‿♥｡)', mention.id)