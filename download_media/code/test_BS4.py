from urllib import urlretrieve
import urlparse
from bs4 import BeautifulSoup
import urllib2
from unshorted_url import unshorten_url_converge

#url = "https://www.youtube.com/watch?v=Gmaww5-vHFo&feature=youtu.be"
url = "https://www.washingtonpost.com/"
#url = 'https://youtu.be/TtOG-jISsig'
url_netloc = urlparse.urlparse(url).netloc


long_url = unshorten_url_converge(url)




soup = BeautifulSoup(urllib2.urlopen(long_url))
for img in soup.findAll("img",{"alt":True, "src":True}):
    img_url = urlparse.urljoin(url, img['src'])
    file_name = img['src'].split('/')[-1]
    urlretrieve(img_url, file_name)