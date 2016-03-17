import os, sys, requests
from StringIO import StringIO
from PIL import Image
image_link_path = os.path.abspath('./image_link')
if image_link_path not in sys.path:
    sys.path.append(image_link_path)
from get_image_link import inspect_link_urllib2

import random, string

def get_arb_image(url):

    url = url.strip()  # remove trailing whitespaces

    _, img_link = inspect_link_urllib2(url)

    try:
        response = requests.get(img_link)
    except:
        e = sys.exc_info()[0]
        print(e)
        print 'Error in get_arb_image with status: ' + str(e)
        return -1, None
    try:
        img = Image.open(StringIO(response.content))
    except:
        print 'Invalid image downloaded from url : ' + img_link
        print 'Recieved response: ' + str(response.status_code)
        img = None

    return response.status_code, img


def save_arb_image(url, folder_loc):
    if not len(url):
        print 'Encountered Empty URL'
        # An empty URL has ended up here
        return None

    img_name = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
    r, img = get_arb_image(url)

    file_path = os.path.abspath(os.path.join(folder_loc, img_name + '.jpg'))

    if img is not None:
        try:
            img.save(file_path)
        except IOError:
            img.convert('RGB').save(file_path) # fix the mode P error
    else:
        print 'Image fetch failed from : ' + url
        file_path = None
    return file_path


if __name__ == "__main__":
    link = 'http://www.amazon.com/The-Great-Hampshire-Primary-Myth/dp/1494700379%3FSubscriptionId%3DAKIAI3JDYDGCDVTNWTFQ%26tag%3Dmydocpage-20%26linkCode%3Dsp1%26camp%3D2025%26creative%3D165953%26creativeASIN%3D1494700379'

    x = save_arb_image(link, './')
    print(x)

