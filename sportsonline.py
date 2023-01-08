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

def sportsonline(url):
    url_parsed = urlparse(url) 
    hostname = '%s://%s'%(url_parsed.scheme,url_parsed.netloc)
    referer = hostname + '/'
    data = getRequest(url)
    iframe = re.compile('<iframe.+?src="(.*?)".+?scrolling.+?frameborder.+?allowfullscreen.+?></iframe>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    #referer = ''
    sources = []
    if iframe:
        url2 = iframe[0]
        #referer += url2
        data2 = getRequest(url2,referer=url)
        script = re.compile('<script>(.*?)</script>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)
        eval = [js.replace('\r', '').replace('\n', '') for js in script if 'p,a,c,k,e,d' in js]
        if eval:
            eval = eval[0]
            try:
                import jsunpack
                html = jsunpack.unpack(eval).replace("\\'", "'")
                src = re.compile('src="(.*?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(html)
                for s in src:
                    if '.m3u8' in s:
                        sources.append(s)
            except:
                pass
    if sources and referer:
        stream = random.choice(sources)
        #stream = sources[0]
        stream = stream + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36&Referer=' + referer
    else:
        stream = ''
    dt = {}
    dt['page'] = str(url)
    dt['stream'] = str(stream)
    js = json.dumps(dt)
    result = js
    return result

#print(sportsonline('https://sportsonline.to/channels/hd/hd1.php'))
