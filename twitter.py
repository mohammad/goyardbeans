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

api = tweepy.API(auth)
since = 0

def get_mentions(since):
    try:
        tweet = api.mentions_timeline(since_id = since + 1)[0]
        tweet_id = tweet.id
        screen_name = tweet.user.screen_name
        media_url = tweet.entities['media'][0]['media_url']
        crop_and_upload_media(url = media_url, author=screen_name, reply_id = tweet_id)
        return tweet_id
    except:
        print("No recent photos to update")

    
def crop_and_upload_media(url, author, reply_id):
    cropped_photo = crop_photo(url)
    media = api.media_upload(filename="goyard.jpeg", file = cropped_photo)
    status = "GOYA BEANS IS NOT MY BEST FRIEND ANYMORE! @" + author
    api.update_status(status = status, in_reply_to_status_id=reply_id, media_ids=[media.media_id])


new_since = get_mentions(since)


    

