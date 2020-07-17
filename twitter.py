import tweepy
import os
import re
import json
from photoshop import crop_photo


twitter_consumer_key = os.environ['TWITTER_CONSUMER_KEY']
twitter_consumer_key_secret = os.environ['TWITTER_CONSUMER_KEY_SECRET']

twitter_access_token = os.environ['TWITTER_ACCESS_TOKEN']
twitter_access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_key_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)

# TODO - push to Heroku and set up Cronjob 

# Nothing better than a text file that serves as your DB
api = tweepy.API(auth)
f = open('since.txt')
since = int(f.read())
f.close()

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
    tweets = api.mentions_timeline(since_id = since + 1)
    new_since = since
    if(len(tweets) == 0):
        print('No tweets to process')
    else:
        print(str(len(tweets)) + " tweets to process")
        for tweet in tweets:
            new_since = process_mention(tweet)
        
    return new_since


since = get_mentions(since)
f = open("since.txt", "w")
f.write(str(since))
f.close()

    

