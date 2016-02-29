# Read the json dump from apollo and generate a hdf5 file with urls extracted and un-shortened
import json, time, sys
from pprint import pprint
from urlparse import urlparse
import collections
import re, os
from unshorted_url import unshorten_url_converge, unshorten_url2
from url_table import UrlTable, UrlEntry
from analyze_url_hdf5 import download_media, download_media_per_entry
import util
from multiprocessing import Process, Manager
import multiprocessing
import render_xlsx


valid_url_netlocs = ['t.co']

json_file = '../primaries_1/tweets_5000samples.json'

# each line is a json entry
with open(json_file) as f:
    lines = f.readlines()

media_hdf5_file_path,  \
out_img_folder, out_video_folder, db_xl_file_path = util.get_media_file_paths(json_file)

# Config parameters
config = util.Config(overwrite_media=True)
config.set_verbose_debug(False)


util.create_media_folders(out_img_folder, out_video_folder, config)

url_domains = list()
url_list = list()

# HDF5 table params
url_table = UrlTable(file_name=media_hdf5_file_path, mode='w', title=os.path.basename(media_hdf5_file_path))
url_entry = url_table.table.row

start_time = time.time()
redirection_time = 0

# Multi Processing Parameters
manager = Manager()
url_info_dict = manager.dict()
num_proc = 200  # multiprocessing.cpu_count()


def parse_json_dump(entry_num, json_entry_line, config=util.Config()):
    data = json.loads(json_entry_line)
    tweet_string = data['text']
    # Split tweet into words
    tweet_words = tweet_string.split(' ')

    # Prune out URL
    try:
        url = re.search("(?P<url>https?://[^\s]+)", tweet_string).group("url")
    except:
        url = ''
        # print 'No URL found :: ' + tweet_string
        pass
    # Convert from Unicode to string
    url = url.encode('ascii', 'ignore')

    # if there is an @ in the url, remove trailiing chars
    tmp_url = url.split('@')[0]
    url = tmp_url

    url_info = urlparse(url)

    if config.verbose_debug:
        print 'Before unshortening : ' + str(entry_num)

    # if the url is shortened, then un-shorten it
    if url_info.netloc in valid_url_netlocs:
        # long_url = unshorten_url_converge(url)
        long_url = unshorten_url2(url)

    else:
        long_url = url

    if config.verbose_debug:
         print 'After unshortening : ' + str(entry_num)


    long_url_info = urlparse(long_url)

    media_downloaded, media_path = download_media_per_entry(long_url, long_url_info.netloc, out_img_folder,
                                                            out_video_folder,
                                                            config)

    info_entry = dict()

    # fill up the URL table
    info_entry['tweet_string'] = tweet_string.encode('ascii', 'ignore')
    info_entry['tweet_id'] = data['id']
    info_entry['url_domain'] = long_url_info.netloc.encode('ascii', 'ignore')
    info_entry['long_url'] = long_url.encode('ascii', 'ignore')
    info_entry['short_url'] = url
    info_entry['screen_name'] = data['user']['screen_name'].encode('ascii', 'ignore')
    info_entry['media_downloaded'] = bool(media_downloaded)
    info_entry['media_file_paths'] = media_path

    url_info_dict[entry_num] = info_entry


print('Parsing JSON dump with %d lines' % len(lines))

for blk_idx in range(0, len(lines), num_proc):

    blk_lines = lines[blk_idx:min(blk_idx + num_proc, len(lines))]

    jobs = []

    t1 = time.time()
    for idx, line in enumerate(blk_lines):
        entry_num = idx + blk_idx
        p = Process(target=parse_json_dump, args=(entry_num, line, config))
        jobs.append(p)

    for idx, p in enumerate(jobs):
        entry_num = idx + blk_idx
        if config.verbose_debug:
            print('Launching Process for line' + str(entry_num))
        else:
            print('Launching Process for line' + str(entry_num))
            #print('Launching Process for line' + str(entry_num) + '\r'),
        p.start()
        # parse_json_dump(entry_num, line)

    for idx, p in enumerate(jobs):
        entry_num = idx + blk_idx
        if config.verbose_debug:
            print('Finishing Process for line' + str(entry_num))
        else:
            print('Finishing Process for line' + str(entry_num))
            #print('Finishing Process for line' + str(entry_num) + '\r'),
        p.join()

    t2 = time.time()

    print '###########Jobs running at %s links per sec##############' % str(len(blk_lines) / (t2 - t1))

for idx in range(len(url_info_dict)):
    try:
        url_entry['tweet_string'] = url_info_dict[idx]['tweet_string']
        url_entry['tweet_id'] = url_info_dict[idx]['tweet_id']
        url_entry['url_domain'] = url_info_dict[idx]['url_domain']
        url_entry['long_url'] = url_info_dict[idx]['long_url']
        url_entry['short_url'] = url_info_dict[idx]['short_url']
        url_entry['screen_name'] = url_info_dict[idx]['screen_name']
        url_entry['media_downloaded'] = url_info_dict[idx]['media_downloaded']
        url_entry['media_file_paths'] = url_info_dict[idx]['media_file_paths']
        url_entry.append()
    except:
        e = sys.exc_info()[0]
        print 'Error in url_entry with ' + str(idx) + ' with error ' + str(e)

url_table.table.flush()

print('Images will be available at :' + out_img_folder)
print('Videos will be available at :' + out_video_folder)

# Download image from URLs mined from tweets

# url_media_df = download_media(hdf5_file_path, out_img_folder, out_video_folder, config)
# print('Saving hdf5 file with Media data in :' + media_hdf5_file_path)
# updated url dataframe
# url_media_df.to_hdf(media_hdf5_file_path, 'df')

#Generating debug excel file
render_xlsx.render_dbg_xls(json_file, db_xl_file_path, config)
print('Debug Excel file available at : ' + db_xl_file_path)
