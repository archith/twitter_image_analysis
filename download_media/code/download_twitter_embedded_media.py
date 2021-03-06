import sys, os
import pickle
import json
import util
import requests
from PIL import Image
from StringIO import StringIO
import tweepy

# This code is not yet integrated with the 'read_apollo_dump' script as this depends on twitter rate limits
# Load  Twitter API credentials
key_dict = pickle.load(open("./myTwitterKeys.p", "rb"))

apollo_dump_file = '../primaries_4/tweets_500samples.json'
apollo_dump_file = os.path.abspath(apollo_dump_file)
apollo_dump_w_emb_media_file = apollo_dump_file.strip('.json') + '_w_emb_media_file.json'
complete_twitter_data_file = apollo_dump_file.strip('.json') + '_complete_twitter_data.json'

_, out_img_folder, out_video_folder, _ = util.get_media_file_paths(apollo_dump_file)
config = util.Config(overwrite_media=False)
util.create_media_folders(out_img_folder, out_video_folder, config)

consumer_key = key_dict['consumer_key']
consumer_secret = key_dict['consumer_secret']
access_key = key_dict['access_key']
access_secret = key_dict['access_secret']

# Authenticate me
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# print user stats
user = api.me()
print('Name: ' + user.name)
print('Location: ' + user.location)
print('Friends: ' + str(user.friends_count))


def save_embd_image(url, folder_loc):
    url = url.strip('/')  # if there is a trailiing '/', important to do this is to get valid img_name
    img_name = [x for x in url.split('/') if x is not ''][-1]

    file_path = os.path.abspath(os.path.join(folder_loc, img_name))

    # Download data from url
    try:
        response = requests.get(url)
    except:
        e = sys.exc_info()[0]
        print('Error in save_embd_image with code : ' + e)

    # Save data as Image files
    try:
        img = Image.open(StringIO(response.content))
    except:
        print 'Invalid image downloaded from url : ' + url
        print 'Recieved response: ' + str(response.status_code)
        img = None

    if img is not None:
        img.save(file_path)
    else:
        print 'Image fetch failed from : ' + url
        file_path = None
    return file_path



with open(apollo_dump_file, 'r') as f:
    lines = f.readlines()

emb_media_json_fid = open(apollo_dump_w_emb_media_file, 'w')
comp_twit_data_file = open(complete_twitter_data_file, 'w')

for idx, l in enumerate(lines):
    j = json.loads(l)

    t_id = j['id']

    try:
        tweet = api.get_status(t_id)
    except:
        e = sys.exc_info()[0]
        print(e)
        print 'Failed to download tweet for line number : %d' % idx
        continue

    media_links = tweet.entities.get('media', [])
    if len(media_links) == 0:
        # No extended entities/media url found
        continue
    j['media_links'] = []
    for link_obj in media_links:
        media_url = link_obj['media_url']
        print('Link found : %s'% media_url)
        save_embd_image(media_url, out_img_folder)
        j['media_links'].append(media_url)

    l_media = json.dumps(j)
    emb_media_json_fid.write(l_media)

    l_comp = json.dumps(tweet._json)
    comp_twit_data_file.write(l_comp)

comp_twit_data_file.close()
emb_media_json_fid.close()















