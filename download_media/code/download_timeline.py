# Download a timeline of some user to gather toy twitter data
import os
import pickle
import json
import wget
# http://www.tweepy.org/
import tweepy

# Load  Twitter API credentials
key_dict= pickle.load(open("/home/archith/work/twitter_image_analysis/download_media/code/myTwitterKeys.p","rb" ))

consumer_key = key_dict['consumer_key']
consumer_secret = key_dict['consumer_secret']
access_key = key_dict['access_key']
access_secret = key_dict['access_secret']


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# print user stats
user = api.me()
print('Name: ' + user.name)
print('Location: ' + user.location)
print('Friends: ' + str(user.friends_count))

screen_name = 'TexasSheBandit'

media_set = set()

tweets = api.user_timeline(screen_name=screen_name, count=100)

for status in tweets:
    media = status.entities.get('media', [])
    if len(media) > 0:
        print(len(media))
        media_set.add(media[0]['media_url'])

for link in media_set:
    print(link)
    wget.download(link)



tweets_json = [t._json for t in tweets]

with open('timeline_sample.json', 'w') as f:
    for j in tweets_json:
        json.dump(j, f)
        f.write('\n')
