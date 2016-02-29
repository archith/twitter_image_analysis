import sys, requests, os
from PIL import Image
from StringIO import StringIO


# borrowed code from http://stackoverflow.com/questions/12682039/how-can-i-get-an-direct-instagram-link-from-a-twitter-entity
# access_token = '492728d12db64bfd9aa9e03146651f83'
# client_secret = 'ce7ece028ae34ae997dcafec5d0bcf0b'

# url should be of the form 'https://www.instagram.com/p/BBqlTzTR5qy/'
def get_inst_image(url, image_size='l'):
    # image size can be  t (thumbnail), m (medium), l (large)
    # file_loc is the folder location where you want the image
    url = url.strip()  # remove trailing whitespaces
    if url[-1] == '/':
        image_url = url + 'media/?size=' + image_size
    else:
        image_url = url + '/media/?size=' + image_size

    try:
        response = requests.get(image_url)
    except:
        e = sys.exc_info()[0]
        print(e)
        print 'Response code in get_inst_image: ' + str(response.status_code)
        return response.status_code, None
    try:
        img = Image.open(StringIO(response.content))
    except:
        print 'Invalid image downloaded from url : ' + image_url
        print 'Recieved response: ' + str(response.status_code)
        img = None

    return response.status_code, img


def save_inst_image(url, folder_loc, image_size='l'):
    url = url.strip('/')  # if there is a trailiing '/', important to do this is to get valid img_name
    img_name = [x for x in url.split('/') if x is not ''][-1]
    r, img = get_inst_image(url, image_size)

    file_path = os.path.abspath(os.path.join(folder_loc, img_name + '.jpg'))

    if img is not None:
        img.save(file_path)
    else:
        print 'Image fetch failed from : ' + url
        file_path = None
    return file_path


if __name__ == "__main__":
    inst_link = 'https://www.instagram.com/p/BBqlTzTR5qy/'

    save_inst_image(inst_link, './')
    x = 2
