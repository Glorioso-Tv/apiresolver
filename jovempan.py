from urllib.parse import quote, urlencode, urlparse, parse_qs #python 3
from urllib.request import Request, urlopen, URLError  # Python 3
from io import BytesIO as StringIO ## for Python 3
import gzip
import re
import json
import random
import base64
import os

def valida(url,origin=False,referer=False):
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36')
    if origin:
        req.add_header('Origin', origin)
    if referer:    
        req.add_header('Referer', referer)
    try:
        response = urlopen(req)
        code = response.getcode()
    except:
        code = 404
    if code == 200:
        status = True
    else:
        status = False
    return status


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


def check_server(lista,origin=False,referer=False):
    sv = []
    for server in lista:
        if not 'panflix' in server:
            status = valida(server,origin=origin,referer=referer)
            if status:
                sv.append(server)
                break
    if sv:
        s = sv[0]
    else:
        s = ''
    return s

def pick_m3u8(url,origin=False,referer=False):
    filename = os.path.basename(url)
    path_url = url.replace(filename, '')
    data = getRequest(url,origin=origin,referer=referer)
    sources = re.findall('EXT-X-STREAM-INF:BANDWIDTH.+?,AVERAGE-BANDWIDTH.+?,RESOLUTION=(.*?),FRAME-RATE.+?,CODECS.+?"\n(.*?).m3u8', data)
    index_1080 = []
    index_720 = []
    index_480 = []
    for resolution, index in sources:
        if resolution == '1920x1080':
            index_1080.append(index)
        elif resolution == '1280x720':
            index_720.append(index)
        elif resolution == '768x432':
            index_480.append(index)
    if index_1080:
        stream = path_url + index_1080[0] + '.m3u8'
    elif index_720:
        stream = path_url + index_720[0] + '.m3u8'
    elif index_480:
        stream = path_url + index_480[0] + '.m3u8'
    else:
        stream = ''
    return stream


def jovempannews(url):
    url_parsed = urlparse(url) 
    hostname = '%s://%s'%(url_parsed.scheme,url_parsed.netloc)
    origin = hostname
    referer = hostname + '/'    
    data = getRequest(url)
    #regex todos os links: http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+
    #regex somente m3u8: http\S+\.m3u8    
    link = re.compile('http\S+\.m3u8', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    if link:
            try:
                sv = check_server(link,origin=origin,referer=referer)
                if sv:
                    pick = pick_m3u8(sv,origin=origin,referer=referer)
                else:
                    pick = ''
                if pick:
                    stream = pick + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36&Origin={0}&Referer={1}'.format(origin,referer)
                else:
                    stream = ''
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

#print(jovempannews('https://jovempan.com.br/jpnews'))
