from urllib.parse import quote, urlencode, urlparse #python 3
from urllib.request import Request, urlopen, URLError  # Python 3
from io import BytesIO as StringIO ## for Python 3
import gzip
import re
import requests
#import random
#import json








def open_url(url,origin=False,referer=False,post=False):
    req = Request(url)
    req.add_header('sec-ch-ua', '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"')
    req.add_header('sec-ch-ua-mobile', '?0')
    req.add_header('sec-ch-ua-platform', '"Windows"')
    req.add_header('Upgrade-Insecure-Requests', '1')    
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
    req.add_header('Sec-Fetch-Site', 'none')
    req.add_header('Sec-Fetch-Mode', 'navigate')
    req.add_header('Sec-Fetch-User', '?1')
    req.add_header('Sec-Fetch-Dest', 'document')
    req.add_header('Accept-Encoding', 'gzip')
    req.add_header('Accept-Language', 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7')
    if origin:
        req.add_header('Origin', origin)    
    if referer:    
        req.add_header('Referer', referer)
    #req.set_proxy(proxy_host, 'https')
    try:
        if post:
            post = urlencode(post)
            try:
                response = urlopen(req,data=post.encode('utf-8'))
                code = response.getcode()
                encoding = response.info().get('Content-Encoding')
            except:
                response = urlopen(req,data=post)
                code = response.getcode()
                encoding = response.info().get('Content-Encoding')
        else:
            try:
                response = urlopen(req)
                code = response.getcode()
                encoding = response.info().get('Content-Encoding')
            except:
                code = 401
                encoding = 'none'
    except:
        code = 401
        encoding = 'none'
    if code == 200:
        if encoding == 'gzip':
            try:
                buf = StringIO(response.read())
                f = gzip.GzipFile(fileobj=buf)
                content = f.read()
            except:
                content = ''
        else:
            try:
                content = response.read()
            except:
                content = ''
    else:
        content = ''
    try:
        content = content.decode('utf-8')
    except:
        pass
    return content



def last_url(url,referer=False,timeout=12):
    req = Request(url)
    req.add_header('sec-ch-ua', '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"')
    req.add_header('sec-ch-ua-mobile', '?0')
    req.add_header('sec-ch-ua-platform', '"Windows"')
    req.add_header('Upgrade-Insecure-Requests', '1')    
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
    req.add_header('Sec-Fetch-Site', 'none')
    req.add_header('Sec-Fetch-Mode', 'navigate')
    req.add_header('Sec-Fetch-User', '?1')
    req.add_header('Sec-Fetch-Dest', 'document')
    req.add_header('Accept-Encoding', 'gzip')
    req.add_header('Accept-Language', 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7')   
    if referer:    
        req.add_header('Referer', referer)
    try:
        response = urlopen(req,timeout=timeout)
        lasturl = response.geturl()
    except:
        lasturl = ''
    return lasturl

def headers(referer=False):
    if referer:
        headers = '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36&Referer=%s'%referer
    else:
        headers = '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    return headers

def streamtape(url):
    correct_url = url.replace('/v/', '/e/')
    parsed_uri = urlparse(url)
    protocol = parsed_uri.scheme
    host = parsed_uri.netloc
    referer = '%s://%s'%(protocol,host)
    data = open_url(correct_url,referer=referer)
    link_part1_re = re.compile('<div.+?style="display:none;">(.*?)&token=.+?</div>').findall(data)
    link_part2_re = re.compile("&token=(.*?)'").findall(data)
    if link_part1_re and link_part2_re:
        part1 = link_part1_re[0]
        part2 = link_part2_re[-1]
        part1 = part1.replace(' ', '')
        if 'streamtape' in part1:
            try:
                part1 = part1.split('streamtape')[1]
                final = 'streamtape' + part1 + '&token=' + part2
                stream = 'https://' + final + '&stream=1'
                link = last_url(stream,referer=referer)                
                link = link + headers(referer=stream)
            except:
                link = False
        elif 'get_video' in part1:
            try:
                part1_1 = part1.split('get_video')[0]
                part1_2 = part1.split('get_video')[1]
                part1_1 = part1_1.replace('/', '')
                part1 = part1_1 + '/get_video' + part1_2
                final = part1 + '&token=' + part2
                stream = 'https://' + final + '&stream=1'
                link = last_url(stream,referer=referer)
                link = link + headers(referer=stream)
            except:
                link = False
        else:
            link = False
    else:
        link = False
    return link

def streamtape2(url):
    correct_url = url.replace('/v/', '/e/')
    parsed_uri = urlparse(url)
    protocol = parsed_uri.scheme
    host = parsed_uri.netloc
    referer = '%s://%s'%(protocol,host)
    data = open_url(correct_url,referer=referer)
    link_part1_re = re.compile('<div.+?style="display:none;">(.*?)&token=.+?</div>').findall(data)
    link_part2_re = re.compile("&token=(.*?)'").findall(data)
    if link_part1_re and link_part2_re:
        part1 = link_part1_re[0]
        part2 = link_part2_re[-1]
        part1 = part1.replace(' ', '')
        if 'streamtape' in part1:
            try:
                part1 = part1.split('streamtape')[1]
                final = 'streamtape' + part1 + '&token=' + part2
                stream = 'https://' + final + '&stream=1'
                link = last_url(stream,referer=referer)                
                #link = link + headers(referer=stream)
            except:
                link = False
        elif 'get_video' in part1:
            try:
                part1_1 = part1.split('get_video')[0]
                part1_2 = part1.split('get_video')[1]
                part1_1 = part1_1.replace('/', '')
                part1 = part1_1 + '/get_video' + part1_2
                final = part1 + '&token=' + part2
                stream = 'https://' + final + '&stream=1'
                link = last_url(stream,referer=referer)
                #link = link + headers(referer=stream)
            except:
                link = False
        else:
            link = False
    else:
        link = False
    if link:
        stream = link
    else:
        stream = 'empty'
    return stream

def stream(url):
    try:
        url = streamtape2(url)
        r = requests.get(url,stream=True)
        return r
    except:
        return 'empty'


def streamtaperesolve(url):
    st = streamtape(url)
    if st:
        result = '{"page": "%s", "stream": "%s"}'%(str(url),str(st))
    else:
        result = '{}'
    return result


#print(streamtaperesolve('https://streamtape.com/e/dRGAvXoDvMukVK6/V3N0RPKDUB.mp4'))