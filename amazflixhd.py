#https://amazflixhd.com/
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

def hex2string(string):
    import ast
    string = r'"%s"'%string
    value = ast.literal_eval(string)
    return value

def amazflixhd(url):
    #https://amzcdn.xyz/player/index.php?data=5cbdfd0dfa22a3fca7266376887f549b&do=getVideo 
    #referer = 'https://midiacamaleao.com.br/'
    if 'amzcdn' in url and '/video/' in url:
        try:
            id_data = url.split('/video/')[1]
        except:
            id_data = ''
        if id_data:
            url2 = 'https://amzcdn.xyz/player/index.php?data={0}'.format(id_data)
            data = getRequest(url2,referer=url)
            script = re.compile('<script type="text/javascript">(.*?)</script>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
            eval = [js.replace('\r', '').replace('\n', '') for js in script if 'p,a,c,k,e,d' in js]
            if eval:
                eval = eval[-1]
                try:
                    import jsunpack
                    html = jsunpack.unpack(eval).replace("\\'", "'")
                except:
                    html = ''
                ck = re.compile(',"ck":"(.*?)",', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(html)
                if ck:
                    stream = ck[0]
                    stream = stream.replace('\\\\', '\\')
                    stream = hex2string(stream)
                    stream = base64.b64decode(stream)
                    print(stream)
                    #https://reidoseriado.xyz/cdn/down/disk1/6c19b457e02db82b853bc5c1e124643a/Video/720p/720p_019.html 

    #data = getRequest(url,referer=referer)
    #print(data)
    #script = re.compile('<script type="text/javascript">(.*?)</script>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    #eval = [js.replace('\r', '').replace('\n', '') for js in script if 'p,a,c,k,e,d' in js]
    #if eval:
    #    eval = eval[-1]
    #    try:
    #        import jsunpack
    #        html = jsunpack.unpack(eval).replace("\\'", "'")
    #    except:
    #        html = ''
    #    print(html)
    #    ck = re.compile(',"ck":"(.*?)",', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(html)
    #    if ck:
    #        stream = ck[0]
    #        stream = stream.replace('\\\\', '\\')
    #        stream = hex2string(stream)
    #        stream = base64.b64decode(stream)
    #        #stream = bytes.fromhex(stream).decode('utf-8')
    #        #stream = base64.b32decode(stream)
    #        #with open('amazflix.txt', 'w') as f:
    #        #    f.write(stream.decode('utf-8'))
    #        #    f.close()

        #print(html)

amazflixhd('https://amzcdn.xyz/video/5cbdfd0dfa22a3fca7266376887f549b')