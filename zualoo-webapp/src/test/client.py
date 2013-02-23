from pyamf.remoting.client import RemotingService
import urllib
import urllib2
import cookielib

def connect(email=None, base_url=None):
    if not base_url: base_url = 'http://localhost:8080'
    gw = RemotingService(base_url + '/gateway')
    if email: gw.addHTTPHeader('Cookie', login_cookie(email, base_url))
    return gw.getService('grocery')

def login_cookie(email, base_url):
    query = dict(email=email, action='Login')
    data = urllib.urlencode(query)
    jar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
    resp = opener.open(base_url + '/_ah/login', data)
    login_cookie = None
    for cookie in jar:
        if cookie.name in ['ACSID', 'dev_appserver_login']:
            login_cookie = '%s=%s' % (cookie.name, cookie.value)
            break
    if not login_cookie: raise Exception('Could not login.')
    return login_cookie
