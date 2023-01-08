from urllib.parse import quote, urlencode, urlparse #python 3
from urllib.request import Request, urlopen, URLError  # Python 3
from io import BytesIO as StringIO ## for Python 3
import gzip
import re
import json
import random


def getRequest(url,origin=False,referer=False,post=False):
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

def filmebrasil(url):
    url_parsed = urlparse(url) 
    hostname = '%s://%s'%(url_parsed.scheme,url_parsed.netloc)
    referer = hostname + '/'
    data = getRequest(url,referer=referer)
    player = re.compile('<div id="player">(.*?)</div>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    get_player = re.compile('get_player.+?"(.*?)","(.*?)".+?;', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(str(player))
    stream_360p = ''
    stream_480p = ''
    stream_720p = ''
    stream_1080p = ''
    if get_player:
        url2 = hostname + '/function.php'
        referer2 = url
        try:
            url_post = get_player[0][0]
            img_post = get_player[0][1]
        except:
            url_post = ''
            img_post = ''
        if url_post and img_post:
            post = {'url': url_post, 'thumb': img_post}
            data2 = getRequest(url2,referer=referer2,post=post)
            setup = re.compile('jwplayer.+?setup(.*?);', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)
            if setup:
                try:
                    data3 = setup[0].replace('(', '').replace('\n', '').replace('\t', '').replace(')', '')
                except:
                    data3 = ''
                sources = re.compile('{"file":.+?"(.*?)".+?"label": "(.*?)"}', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data3)
                if sources:
                    for source, quality in sources:
                        try:
                            source = source.encode('utf-8').decode('unicode_escape')
                        except:
                            source = source                       
                        if '360p' in quality:
                            stream_360p += source
                        elif '480p' in quality:
                            stream_480p += source
                        elif '720p' in quality:
                            stream_720p += source
                        elif '1080p' in quality:
                            stream_1080p += source
    if stream_1080p:
        stream = stream_1080p + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    elif stream_720p:
        stream = stream_720p + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    elif stream_480p:
        stream = stream_480p + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    elif stream_360p:
        stream = stream_360p + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    else:
        stream = ''
    dt = {}
    dt['page'] = str(url)
    dt['stream'] = str(stream)
    js = json.dumps(dt)
    result = js
    return result