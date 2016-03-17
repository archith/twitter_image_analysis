import sys, os, re, httplib, urlparse, json
from BeautifulSoup import BeautifulSoup
from StringIO import StringIO
from PIL import Image
import urllib2
import pycurl
import string, random
from StringIO import StringIO

#temp_name = 'img_temp'

#----------------------------------deprecated-------------------------------
IMG_KEYWORDS = [
"twitpic", "imgur", "postimage", "picasaweb",
"flickr", "imagehostinga", "photobucket",
"yfrog", "zooomr",
"image", "img",  "photo", "pic"
]

link_cache = {}

# don't bother to use api for each...inspected manually for each html
def get_image_hotlink(url):
    url = "http://"+url if "http" not in url else url
    try:
        dst = urllib2.urlopen(url, timeout=5)
    except Exception:
        return url

    raw_html = dst.read()
    dst.close()
    try:
        soup = BeautifulSoup(raw_html.encode('utf-8'))
    except Exception:
        return url

    image_url = url # just return pure url for other hostings...
    #print >> sys.stderr, "url::"  + image_url
    if "twitpic" in url:
        img_tag = soup.find('img', attrs = { 'id':re.compile("photo-display"), 'class' : re.compile("photo") })
    elif "yfrog" in url:
        img_tag = soup.find('img', attrs = { 'id':re.compile("main_image") })
    elif "img.ly" in url:
        img_tag = soup.find('img', attrs = { 'id':re.compile("the-image") })
    elif "flickr" in url:
        img_tag = soup.find('img', attrs = { 'alt':re.compile("photo") })
    else:
        return image_url

    if img_tag != None:
        image_url = img_tag['src']
    else:
        return "" # image not found case

    return "http:" + image_url if "http:" not in image_url else image_url

def unshorten_url(url):
    try:
        parsed = urlparse.urlparse(url)
        h = httplib.HTTPConnection(parsed.netloc, timeout=5) # modify this value at your convinience
        h.request('HEAD', parsed.path)
        response = h.getresponse()
        if response.status/100 == 3 and response.getheader('Location'):
            return unshorten_url(response.getheader('Location')) # changed to process chains of short urls
        else:
            return url
    except Exception:
        return ""

def inspect_link_httpheader(link):
    cached = link_cache.get(link)
    if cached != None:
        return cached

    u = unshorten_url(link)
    for i in IMG_KEYWORDS:
        if i in u:
            hotlink = get_image_hotlink(u)
            link_cache[link] = hotlink
            #print >> sys.stderr, hotlink
            return hotlink
    return ""

def inspect_link_pycurl(link):
    storage = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, link)
    c.setopt(c.WRITEFUNCTION, storage.write)
    c.setopt(c.FOLLOWLOCATION, 1)
    c.setopt(c.MAXREDIRS, 6)
    c.perform()
    c.close()

    # not sure how to set this: final_url
    biggest_img_link = get_biggest_img(storage.getvalue())

    return final_url, biggest_img_link

#----------------------------------deprecated ends-------------------------------

# copied from Werkzeug
import urllib
import urlparse

def url_fix(s, charset='utf-8'):
    """Sometimes you get an URL by a user that just isn't a real
    URL because it contains unsafe characters like ' ' and so on.  This
    function can fix some of the problems in a similar way browsers
    handle data entered by the user:

    :param charset: The target charset for the URL if the url was
                    given as unicode string.
    """
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

def is_wanted(dim):
    # check ratio for ad
    ratio_thres = 4
    small_thres = (300, 180) # need to be tuned

    k = (1/float(ratio_thres)) < dim[0]/float(dim[1]) < ratio_thres and\
    sum(dim) > sum(small_thres) # check if image is too small (often icon)
    return k

def get_absolute(origin, path):
    k = re.match(r'(?P<top>(https?://[a-zA-Z0-9.]+))/?\S+', path)
    if k != None:
        return path
    else:
        return k.group('top')+ path


def get_biggest_img(origin, html):
    try:
        soup = BeautifulSoup(html)
    except UnicodeDecodeError:
        print >> sys.stderr, "unable to parse URL"
        return ""
    except UnicodeEncodeError, e:
        print >> sys.stderr, e
        return ""
    ##### tanvir: added exception to debug
    except Exception, e:
        print >> sys.stderr, e, "Unknown exception for ", origin
        return ""

    img_tags = soup.findAll('img')

    if img_tags == None:
        print >> sys.stderr, "no image found"
        return ""

    max_dim_url = ""
    max_dim = (0,0)
    # download imgs and check dimension
    for i in img_tags:
        try:
            esc_url = url_fix(get_absolute(origin, i['src']))
        except:
            continue
        #print >> sys.stderr, "o: " + origin
        #print >> sys.stderr, "e: " + esc_url
        if "http" not in esc_url: # almost always web img files...so just ignore
            continue
        try:
            dst = urllib2.urlopen(esc_url)
            k = dst.read()
            dst.close()
        except: #urllib2.HTTPError, ignore 4xx errors
            # tanvir: March 21: a hack to replace %3A by :
            #esc_url = esc_url.replace('%3A',':')
            esc_url = urllib2.unquote(esc_url)
            try:
                dst = urllib2.urlopen(esc_url)
                k = dst.read()
                dst.close()
            except:
                print >> sys.stderr, "problem reading the image", esc_url
                continue

        try:
            im = Image.open(StringIO(k))
            if is_wanted(im.size):
                if im.size > max_dim:
                    max_dim = im.size
                    max_dim_url = i['src']
        except:
            print >> sys.stderr, "problem opening the image"
            continue

    #if os.path.isfile(temp_name):
    #    os.remove(temp_name)

    # handle on-site image
    return max_dim_url


def inspect_link_urllib2(link):
    original_url = "http://"+link if link[0:4] != "http" else link
    try:
        # tanvir: timeout changed from 5 to 10
        dst = urllib2.urlopen(original_url, timeout=10)
        final_url = dst.geturl()
        raw_html = dst.read()
        dst.close()
    except:
        print >> sys.stderr, "url invalid: " + repr(link)
        return link, ""

    biggest_image_link = get_biggest_img(final_url, raw_html)

    return final_url, biggest_image_link


def get_image_link(tweet):
    """
        get tweet in json format
        returns None , if link is broken
                (<final_url>, <url_to_biggest_img>), <url_to_biggest_img> can be '' if image is not found
    """
    # tanvir: unescape url because they may be in http:\/\/test.com format
    text = tweet['text'].replace('\/','/')
    urls = re.findall(r'https?://\S+', text)
    if len(urls) != 0:
        for link in urls:
            img_link = inspect_link_urllib2(link)
            print >> sys.stderr, img_link
            return img_link

if __name__ == '__main__':
#   print >> sys.stderr, inspect_link_urllib2("http://www.photozz.com/?1ixz")
    #print >> sys.stderr, inspect_link_urllib2("http://www.guardian.co.uk/commentisfree/2011/aug/18/riots-sentencing-courts?utm_source=twitterfeed&utm_medium=twitter&utm_campaign=Feed%3A+theguardian%2Fmedia%2Frss+%28Media%29")
#    #f = open("../egypt_dataset.txt")
    f = open("small_tweets")
    tweets = f.readlines()
    f.close()
    for tweet in tweets:
        try:
            print >> sys.stderr, get_image_link(json.loads(tweet.replace("\'","\"").replace("None", "\"\"")))
        except:
            print >> sys.stderr, "oh man"
