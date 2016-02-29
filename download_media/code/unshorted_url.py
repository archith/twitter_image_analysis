# This is for Py2k.  For Py3k, use http.client and urllib.parse instead, and
# use // instead of / for the division
# From http://stackoverflow.com/questions/4201062/how-can-i-unshorten-a-url-using-python
import httplib
import urlparse
import requests
import sys, traceback

time_out = 5


def unshorten_url(_url):
    parsed = urlparse.urlparse(_url)
    try:
        h = httplib.HTTPConnection(parsed.netloc)
        h.request('HEAD', parsed.path)
        response = h.getresponse()
        if response.status / 100 == 3 and response.getheader('Location'):
            return response.status, response.getheader('Location')
        else:
            return response.status, _url
    except:
        _e = sys.exc_info()[0]
        raise _e
    return _url


def unshorten_url_converge(input_url):
    counter = 0
    # keep trying unshorted_url in case of multiple levels of url shortnening
    #input_url = input_url.encode('ascii', 'ignore')
    while counter < time_out:
        try:
            status, url = unshorten_url(input_url)
        except:
            e = sys.exc_info()[0]
            print 'Error in unshorten_url_converge for : ' + input_url.encode('ascii', 'ignore') + ' with error ' + str(e)
            return ''
        if (status == 301):
            # probably found the final url
            break
        else:
            input_url = url
        counter = counter + 1

    return url


def unshorten_url2(url):
    try:
        requests.packages.urllib3.disable_warnings()
        # Ignore SSL Errors
        r = requests.head(url, allow_redirects=True, verify=False, timeout=10)
    except:
        e = sys.exc_info()[0]
        print 'Error in unshorten_url2 for :' + url + ' with exception ' + str(e)
        traceback.print_exc(file=sys.stdout)
        return url

    return r.url


if __name__ == "__main__":
    short_url = u'https://t.co/J8hdQXh9Q7'

    while (1):
        # try:
        #     print(unshorten_url(short_url))
        # except Exception as e:
        #     print e

        try:
            url = unshorten_url2(short_url)
            print(url)
        except Exception as e:
            print e
