import sys
from get_image_link import get_image_link
import simplejson
import glob
import re

#------------------------------------------------------------------------------
def main():
    #print inspect_link('http://t.co/EjqReQxt')
    for l in sys.stdin:
        try:
            o = simplejson.loads(l)
        except:
            o = eval(l)
        image_link = get_image_link(o)
        if image_link != '':
            print >> sys.stderr, repr(image_link), repr(o)

#------------------------------------------------------------------------------
def __get_output_file(analysis_path):
    file_paths = glob.glob(analysis_path + '/*.ranked_model.txt')
    return file_paths

#------------------------------------------------------------------------------
def get_image_link_from_tweet_text(text):
    return get_image_link({'text': text})

def is_image_page(url):
    return True
    #print 'url:', url
    #for s in IMG_KEYWORDS:
    #    if url.find(s) >= 0:
    #        return True
    #return False

def get_claim_with_image(claim):

    image_link_res = get_image_link_from_tweet_text(claim['text'])
    if image_link_res != None and is_image_page(image_link_res[0]):
        image_link = image_link_res[1]
        print >> sys.stderr, 'Found One:', repr(image_link_res[0]), repr(image_link)
    else:
        image_link = ''

    if image_link != '':
        claim['claim_img'] = image_link
        #print >> sys.stderr, "Found One:", image_link, claim['claim_desc']
    return claim

def main2():
    # if this is called as -f <path> then run for only one file
    # if this is called as <path> (without specifying -f switch, run for all files)
    # the next argument is max_depth specifying for how many
    # top claims images would be crawled
    max_depth = 0  # crawl images for all claims

    if sys.argv[1] == '-f': # run for only one file
        output_files = [sys.argv[2]]
        if len(sys.argv) > 3:
            max_depth = int(sys.argv[3])
    else: # run for the whole directory
        output_files = __get_output_file(sys.argv[1])
        if len(sys.argv) > 2:
            max_depth = int(sys.argv[2])
    for f in output_files:
        # open new output file
        input_file = open(f, 'r')
        output_file = open(f + '.with_image', 'w')
        while 1:
            meta_line = input_file.readline()
            if not meta_line:
                break
            data_line = input_file.readline()
            print >> output_file, meta_line,
            # process dataline
            tweet_data = simplejson.loads(data_line)
            get_claim_with_image(tweet_data)
            print >> output_file, simplejson.dumps(tweet_data)
        input_file.close()
        output_file.close()

if __name__ == '__main__':
    #main()
    main2()
