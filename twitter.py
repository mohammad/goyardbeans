import tweepy
import os
import re
import json
import psycopg2
from photoshop import crop_photo

# Twitter Client Setup
twitter_consumer_key = os.environ['TWITTER_CONSUMER_KEY']
twitter_consumer_key_secret = os.environ['TWITTER_CONSUMER_KEY_SECRET']

twitter_access_token = os.environ['TWITTER_ACCESS_TOKEN']
twitter_access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_key_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)

api = tweepy.API(auth)

# DB Setup
psql_host = os.environ['PSQL_HOST']
psql_db = os.environ['PSQL_DB']
psql_user = os.environ['PSQL_USER']
psql_password = os.environ['PSQL_PASSWORD']


conn = psycopg2.connect(host=psql_host,database=psql_db, user=psql_user, password=psql_password)

db = conn.cursor()
since_query = "select * from tweet_tracker"
db.execute(since_query)
since = int(db.fetchone()[0])

def crop_and_upload_media(url, author, reply_id):
    cropped_photo = crop_photo(url)
    media = api.media_upload(filename="goyard.jpeg", file = cropped_photo)
    status = "GOYA BEANS IS NOT MY BEST FRIEND ANYMORE! @" + author
    api.update_status(status = status, in_reply_to_status_id=reply_id, media_ids=[media.media_id])


def process_mention(tweet):
    tweet_id = tweet.id
    try:    
        screen_name = tweet.user.screen_name
        media_url = tweet.entities['media'][0]['media_url']
        crop_and_upload_media(url = media_url, author=screen_name, reply_id = tweet_id)
    except:
        print("Unable to process tweet")
    
    return tweet_id

def get_mentions(since):
    # Hacky way of reversing tweets
    tweets = api.mentions_timeline(since_id = since + 1)[::-1]
    new_since = since
    if(len(tweets) == 0):
        print('No tweets to process')
    else:
        print(str(len(tweets)) + " tweets to process")
        for tweet in tweets:
            new_since = process_mention(tweet)
        
    return new_since


since = get_mentions(since)
update_query = "UPDATE tweet_tracker SET last_processed_tweet = (%s);"
db.execute(update_query, [since])
conn.commit()

db.close()
conn.close()

    

