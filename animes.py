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

#url
#item[random]?token=aHR0cHM6Ly9hbmltZXNvbmxpbmUuY2x1Yi9wbGF5ZXIvMzAvMTJISjNKQVowNFFFRDg3&origin=aHR0cHM6Ly9hbmltZXNvbmxpbmUuY2x1Yi9hbmltZS9ib3J1dG8tbmFydXRvLW5leHQtZ2VuZXJhdGlvbnMvZXBpc29kaW8vNzAyOTI=
#<a id="openPlayer1" data-iframe="https://animesonclub.com/player/30/12HJ3JAZ04QED87" href="#Player1"><i class="fa fa-play"></i>Opção 1</a>

def animesonline_club(url):
    referer_home = 'https://animesonclub.com/'
    referer_player = 'https://deliciareceitas.com/'
    data = getRequest(url,referer=referer_home)
    links_720p = []
    links_480p = []
    players = re.compile('<a id="openPlayer.+?" data-iframe="(.*?)" href="#Player.+?"><i class="fa fa-play"></i>.+?</a>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    if players:
        for player in players:
            data2 = getRequest(player,referer=referer_player)
            iframe = re.compile('<iframe src="(.*?)" frameborder="0" scrolling="no" allowfullscreen="" mozallowfullscreen="" msallowfullscreen="" webkitallowfullscreen=""></iframe>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)
            if iframe:
                data3 = getRequest(iframe[0],referer=player)
                script = re.compile('<script type="text/javascript">(.*?)</script>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data3)
                eval = [js.replace('\r', '').replace('\n', '') for js in script if 'p,a,c,k,e,d' in js]
                if eval:
                    packed = eval[0]
                else:
                    packed = ''
                try:
                    import jsunpack
                    html = jsunpack.unpack(packed).replace("\\'", "'")
                except:
                    html = ''
                sources =  re.compile('{type:"video/mp4",file:"(.*?)",label:"(.*?)","default":"true",}', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(str(html))
                if sources:
                    for src, quality in sources:
                        if '480p' in quality:
                            links_480p.append(src)
                        elif '720p' in quality:
                            links_720p.append(src)

    if links_720p:
        stream = random.choice(links_720p)
        stream = stream + '|Referer=' + referer_home
    elif links_480p:
        stream = random.choice(links_480p)
        stream = stream + '|Referer=' + referer_home
    else:
        stream = ''
    dt = {}
    dt['page'] = str(url)
    dt['stream'] = str(stream)
    js = json.dumps(dt)
    result = js
    return result    

#animesonline_club('https://animesonclub.com/anime/boruto-naruto-next-generations/episodio/70292')
