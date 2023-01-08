from urllib.parse import quote, urlencode, urlparse, parse_qs #python 3
from urllib.request import Request, urlopen, URLError  # Python 3
from io import BytesIO as StringIO ## for Python 3
import gzip
import re
import json
import random
import base64

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

def pick_source(sources):
    if len(sources) > 1 or len(sources) == 1:        
        q1080p = []
        q720p = []
        q480p = []
        q380p = []
        q240p = []
        for quality, url in sources:
            #if quality == '1080':
            #    q1080p.append((quality,url))
            if quality == '720':
                q720p.append((quality,url))
            elif quality == '480':
                q480p.append((quality,url))
            elif quality == '380':
                q380p.append((quality,url))
            elif quality == '240':
                q240p.append((quality,url))
        if q1080p:
            stream = q1080p
        elif q720p:
            stream = q720p
        elif q480p:
            stream = q480p
        elif q380p:
            stream = q380p
        elif q240p:
            stream = q240p
        else:
            stream = []
        if stream:
            result = stream[0][1]
        else:
            result = ''
    else:
        result = ''
    return result

def DailymotionResolver(url):
    if 'dai.ly' in url or 'dailymotion.com' in url:
        try:
            media_id = url.split('/video/')[1]
        except:
            media_id = False
        if media_id:
            try:
                media_id = media_id.split('?')[0]
            except:
                pass
            player = f'https://www.dailymotion.com/player/metadata/video/{media_id}'          
            try:
                origin = 'https://www.dailymotion.com'
                referer = origin + '/'
                html = getRequest(player,origin=origin,referer=referer)
                js_result = json.loads(html)
                quals = js_result.get('qualities')
                if quals:
                    mbtext = quals.get('auto')[0].get('url')
                    mbtext = getRequest(mbtext,origin=origin,referer=referer)
                    sources = re.findall('NAME="(?P<label>[^"]+)"(?:,PROGRESSIVE-URI="|\n)?(?P<url>[^#]+)', mbtext)
                    if sources:
                        stream = pick_source(sources)
                    else:
                        stream = ''
                else:
                    stream = ''
            except:
                stream = ''
        else:
            stream = ''
    else:
        stream = ''
    dt = {}
    dt['page'] = str(url)
    dt['stream'] = str(stream)
    js = json.dumps(dt)
    result = js    
    return result


#print(DailymotionResolver('https://www.dailymotion.com/embed/video/x7txn7q?autoplay=1'))

