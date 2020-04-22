import tweepy
import time
import keys as key
import json
import pandas as pd
import csv
import re
from textblob import TextBlob
import string
import preprocessor as p
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import sys

#Get access key from a file
access_secret = key.ACCESS_SECRET
consumer_key = key.CONSUMER_KEY
consumer_secret = key.CONSUMER_SECRET
access_key = key.ACCESS_KEY

#set two date variables for date range
start_date = '2020-01-01'
#end_date = '2018-10-31'

#authenticate and connect
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#Declare path to csv file
sexual_harrass_tweets = "sexual_harrass_data.csv"

#columns of the csv file
COLS = ['id', 'created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang',
'favorite_count', 'retweet_count', 'original_author', 'possibly_sensitive', 'hashtags',
'user_mentions', 'place', 'place_coord_boundaries']

#HappyEmoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])

# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])

#Emoji patterns
emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)

#combine the two set together - sad + happy
emoticons = emoticons_happy.union(emoticons_sad)

#cleans tweets passed by tweet-preprocessor
def clean_tweets(tweet): 
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(tweet)
#after tweepy preprocessing the colon symbol left remain after      #removing mentions
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
#replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)
#remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)
#drop tweets outside nigeria
    tweet = re.findall(r'[\w\.-]+Nigeria[\w\.-]+', tweet)
#filter using NLTK library append it to a string
    filtered_tweet = [w for w in word_tokens if not w in stop_words]
    filtered_tweet = []
#looping through conditions
    for w in word_tokens:
#check tokens against stop words , emoticons and punctuations
        if w not in stop_words and w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)
    return ' '.join(filtered_tweet)
    #print(word_tokens)
    #print(filtered_sentence)return tweet

#write method
def write_tweets(keyword, file):
    #if file exists, then read else write
    if os.path.exists(file):
        #time.sleep(5)
        df = pd.read_csv(file, header=0)
    else:
        #time.sleep(5)
        df = pd.DataFrame(columns=COLS)
    #page attribute in tweepy.cursor and iteration
    for page in tweepy.Cursor(api.search, q=keyword, count=200, geocode="7.71971, 4.49041, 1km", include_rts=False, since=start_date).pages(50):
        for status in page:
            new_entry = []
            status = status._json
            if status['lang'] != 'en':
                continue
            #replace the number of rts and favs        
            if status['created_at'] in df['created_at'].values:
                i = df.loc[df['created_at'] == status['created_at']].index[0]
                if status['favorite_count'] != df.at[i, 'favorite_count'] or \
                status['retweet_count'] != df.at[i, 'retweet_count']:
                    df.at[i, 'favorite_count'] = status['favorite_count']
                    df.at[i, 'retweet_count'] = status['retweet_count']
                continue

            clean_text = p.clean(status['text'])  

            filtered_tweet = clean_tweets(clean_text)

            blob = TextBlob(filtered_tweet)
            Sentiment = blob.sentiment
            polarity = Sentiment.polarity
            subjectivity = Sentiment.subjectivity

            #append the JSON parsed data to the string array created
            new_entry += [status['id'], status['created_at'],
                    status['source'], status['text'],filtered_tweet, Sentiment,polarity,subjectivity, status['lang'],
                    status['favorite_count'], status['retweet_count']]
            new_entry.append(status['user']['screen_name'])
            try:
                is_sensitive = status['possibly_sensitive']
            except KeyError:
                is_sensitive = None
            new_entry.append(is_sensitive)
            #get all hashtags and user mentions in tweets
            hashtags = ", ".join([hashtag_item['text'] for hashtag_item in status['entities']['hashtags']])
            new_entry.append(hashtags) #append the hashtags
            mentions = ", ".join([mention['screen_name'] for mention in status['entities']['user_mentions']])
            new_entry.append(mentions) #append the user mentions
            #get current tweet location from live tweet
            try:
                coordinates = [coord for loc in status['place']['bounding_box']['coordinates'] for coord in loc]
            except TypeError:
                coordinates = None
            new_entry.append(coordinates)
            #get users location as saved by the user
            try:
                location = status['user']['location']
            except TypeError:
                location = ''
            new_entry.append(location)
            #wrap the data gathered into a Pandas DataFrame
            single_tweet_df = pd.DataFrame([new_entry], columns=COLS)
            df = df.append(single_tweet_df, ignore_index=True)

            #append or write to a CSV file
            csvFile = open(file, 'a' ,encoding='utf-8')
            df.to_csv(csvFile, mode='a', columns=COLS, index=False, encoding="utf-8")

#declare keywords to look out for
sexual_harrassment_keywords = '#abusesexually OR #sexualabuse OR #sexualabuse OR #abusedsexually \
                                OR #childabuse OR #childabuse OR #homeviolence OR #rape OR #raped OR #abusivehusband'

#call method
#write_tweets(sexual_harrassment_keywords, sexual_harrass_tweets)

while True: 
    write_tweets(sexual_harrassment_keywords, sexual_harrass_tweets)
    print("Writing data...")
    time.sleep(30)