from urllib.parse import quote, urlencode, urlparse #python 3
from urllib.request import Request, urlopen, URLError  # Python 3
from io import BytesIO as StringIO ## for Python 3
import gzip
import re
import json

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

qual_map = {'ultra': '2160', 'quad': '1440', 'full': '1080', 'hd': '720', 'sd': '480', 'low': '360', 'lowest': '240', 'mobile': '144'}

def __replaceQuality(qual):
    return qual_map.get(qual.lower(), '000')

def pick_source(sources):
    if len(sources) == 1:
        return sources[0][1]
    elif len(sources) > 1:
        return sources[0][1]
    else:
        return ''

def ok_ru(url):
    if 'ok.ru' in url and '/video/' in url or 'odnoklassniki.ru' in url and '/video/' in url:
        url = url.replace('/video/', '/videoembed/')
        ok = True
    elif 'ok.ru' in url and '/videoembed/' in url or 'odnoklassniki.ru' in url and '/videoembed/' in url:
        ok = True
    else:
        ok = False
    try:
        media_id = url.split('/videoembed/')[1]
    except:
        media_id = ''
    if ok and media_id:
        post = {'cmd': 'videoPlayerMetadata', 'mid': media_id}
        data = getRequest('http://www.ok.ru/dk',post=post)
        json_data = json.loads(data)
        try:
            if len(json_data['videos']) > 0:
                info = dict()
                info['urls'] = []
                for entry in json_data['videos']:
                    info['urls'].append(entry)
            else:  # Live Stream
                info = json_data['hlsMasterPlaylistUrl']
            if type(info) == dict:
                sources = []
                for entry in info['urls']:
                    quality = __replaceQuality(entry['name'])
                    sources.append((quality, entry['url']))
                try:
                    sources.sort(key=lambda x: int(x[0]), reverse=True)
                except:
                    pass
                if sources:
                    stream = pick_source(sources)
                    stream = stream + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
                else:
                    stream = ''
            else:
                stream = info + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        except:
            stream = ''
    else:
        stream = ''
    dt = {}
    dt['page'] = str(url)
    dt['stream'] = str(stream)
    js = json.dumps(dt)
    result = js    
    return result