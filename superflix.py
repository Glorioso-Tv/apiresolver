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

#<div id='Link2' Class='Link2'><a href='https://superflix.cc/filme/tt6920084' allowFullScreen mozallowfullscreen msallowfullscreen oallowfullscreen webkitallowfullscreen sandbox='allow-forms allow-pointer-lock allow-same-origin allow-scripts allow-top-navigation' referrerpolicy='no-referrer'>
#referer = https://superflix.cc/

def superflix_club(url):
    url_parsed = urlparse(url) 
    hostname = '%s://%s'%(url_parsed.scheme,url_parsed.netloc)
    referer = hostname + '/'
    referer_player = 'https://redeliteral.com/'   
    data = getRequest(url,referer=referer)
    players = re.compile("<div id='Link.+?' Class='Link.+?'><a href='(.*?)'.+?allowFullScreen.+?>", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    #print(players)
    servers = ['https://superflix.cc/filme/tt6920084/']
    if servers:
        server = random.choice(servers)
        if 'superflix.club' in server and 'filme.php' in server:
            data2 = getRequest(server,referer=referer_player)
            iframe = re.compile('<iframe.+?src="(.*?)".+?></iframe>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)
            if iframe:
                server2 = iframe[0]
                data3 = getRequest(server2,referer=server)
                #print(data3)
                #callplayer = https://player.uauflix.online//CallPlayer HTTP/1.1
                #post- id = ids
                #https://uauplayer.com/player/IgvQX8Hclugx9IS/
                #print(data3)
                server_id = re.compile('idS: "(.*?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data3)
                #print(server2)
                script = re.compile('<script>(.*?)</script>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data3)
                eval = [js.replace('\r', '').replace('\n', '') for js in script if 'p,a,c,k,e,d' in js]
                if eval:
                    eval = eval[-1]
                    try:
                        import jsunpack
                        html = jsunpack.unpack(eval).replace("\\'", "'")
                    except:
                        html = ''
                    print(html)
                if server_id:
                    url_parsed2 = urlparse(server2) 
                    hostname2 = '%s://%s'%(url_parsed2.scheme,url_parsed2.netloc)
                    origin = hostname2
                    call_player = origin + '//CallPlayer'
                    #print(call_player)
                    server3 = call_player
                    post = {'id': server_id[0]}
                    #print(server_id[0])
                    #data4 = getRequest(server3,origin=origin,referer=server2,post=post)
                    #print(data4)








#superflix_club('https://supertela.in/filmes/resident-evil-bem-vindo-a-raccoon-city/')
#play.php?vid=legendado
#filme.php?id=alternativo
#se_player.php?video_id=us
