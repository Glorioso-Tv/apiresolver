from urllib.parse import quote, quote_plus, urlencode, urlparse #python 3
from urllib.request import Request, urlopen, URLError  # Python 3
from io import BytesIO as StringIO ## for Python 3
import gzip
import re
import requests
import random
import json
from proxy import proxy_web
proxy_host = '177.19.228.165:4153'


def getRequest8(url,origin=False,referer=False,post=False):
    if origin and referer:
        headers={'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Origin': origin,
        'Referer': referer}
    elif origin and not referer:
        headers={'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Origin': origin}
    elif referer and not origin:
        headers={'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': referer}
    else:             
        headers={'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'}
    #data_proxy_https = getRequest('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=BR&ssl=yes&anonymity=all')
    #lista = data_proxy_https.splitlines()
    #total = len(lista)
    #number_https = random.randint(0,total-1)
    #proxy_https = 'https://'+lista[number_https]
    proxy_https = '169.57.157.146:25'
    proxyDict = {"https" : proxy_https}
    #try:
    #    if post:
    #        req = requests.post(url, data=json.dumps(post), headers=headers, proxies=proxyDict)
    #    else:
    #        req = requests.get(url, headers=headers, proxies=proxyDict)
    #    req.encoding = 'utf-8'
    #    content = req.text
    #except:
    #    content = ''
    if post:
        req = requests.post(url, data=json.dumps(post), headers=headers, proxies=proxyDict,verify=False)
    else:
        req = requests.get(url, headers=headers, proxies=proxyDict,verify=False)
    req.encoding = 'utf-8'
    content = req.text        
    return content






def getRequest5(url,origin=False,referer=False,post=False):
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



def rcsolve(urlrc):
    try:
        #url = str(re.compile('rcresolver=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(urlrc)[0]) 
        url = urlrc
        url_parsed = urlparse(url) 
        hostname = '%s://%s'%(url_parsed.scheme,url_parsed.netloc)
        origin = hostname
        referer1 = hostname + '/'
        referer2 = url
        data = proxy_web(url,origin=origin,referer=referer1)
        #print(data)
        player1 = re.compile('<iframe.+?name="Player.+?".+?src="(.*?)".+?</iframe>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        player2 = re.compile('<iframe name=Player "" src="(.*?)" frameborder=.+?height=.+?scrolling=.+?width=.+?allowFullScreen>.+?</iframe>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        if player1:
            player = player1
        elif player2:
            player = player2
        else:
            player = []
        if player:
            url_player = hostname + player[0]
            data2 = proxy_web(url_player,referer=referer2)
            url_action1 = re.compile('<form.+?id="myForm".+?method="post".+?action="(.*?)".+?>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)
            url_action2 = re.compile('<form id=myForm method=post target=_parent action="(.*?)" name=assistirplayer>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)
            if url_action1:
                url_action = url_action1
            elif url_action2:
                url_action = url_action2
            else:
                url_action = []                
            post_data1 = re.compile('<input type="hidden".+?name="(.*?)".+?value="(.*?)".+?/>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)
            post_data2 = re.compile('<input type=hidden name=(.*?) value="(.*?)" />', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)
            if post_data1:
                post_data = post_data1
            elif post_data2:
                post_data = post_data2
            else:
                post_data = []
            if url_action and post_data:
                url_player2 = url_action[0]
                referer3 = url_player2
                key = post_data[0][0]
                value = post_data[0][1]
                dicionary = {key: value}            
                data3 = proxy_web(url_player2,origin=origin,referer=referer1,post=dicionary)
                url_action2 = re.compile('<form.+?id="myForm".+?method="post".+?name="sendData".+?action="(.*?)">', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data3)
                post_data2 = re.compile('<input type="hidden".+?name="(.*?)".+?value="(.*?)".+?/>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data3)
                if url_action2 and post_data2:
                    url_player3 = url_action2[0]
                    url_parsed2 = urlparse(url_player3)
                    hostname2 = '%s://%s'%(url_parsed2.scheme,url_parsed2.netloc)
                    referer_hostname2 = hostname2 + '/'
                    ads = '%s'%url_parsed2.netloc
                    origin2 = hostname2
                    page = post_data2[0][1]
                    try:
                        php = page.split('?')[0]
                    except:
                        php = ''
                    try:
                        video = page.split('?')[1]
                        video = video.replace('&=', '')
                    except:
                        video = ''
                    if php and video:
                        url_player_final = '{0}{1}?M:%%3C\%3E/i/e/s/*=&{2}&ads={3}&='.format(hostname2,php,video,ads)
                        data4 = proxy_web(url_player_final,origin=origin2,referer=referer_hostname2)
                        baixar = re.compile('baixar="(.*?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data4)
                        source = re.compile('source.+?src="(.*?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data4)
                        track = re.compile('<track kind="metadata" src="(.*?)"></track>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data4)
                        if track:
                            track = track[0].replace('./','/player3/')
                            sub = '%s%s'%(hostname2,track)
                        else:
                            sub = 'false'
                        if baixar:
                            data_source = proxy_web(baixar[0],referer=url_player_final)
                            download = re.compile("<meta http-equiv=.+?refresh.+?content=.+?URL='(.*?)'.+?/>", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data_source)
                            if download:
                                stream = '%s|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36&Referer=%s'%(download[0],referer_hostname2)
                            elif source:
                                stream = '%s|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36&Origin=%s&Referer=%s'%(source[0],origin2,referer_hostname2)
                            else:
                                stream = ''
                        elif source:
                            stream = '%s|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36&Origin=%s&Referer=%s'%(source[0],origin2,referer_hostname2)
                        else:
                            stream = ''
                    else:
                        stream = ''
                else:
                    stream = ''
            else:
                stream = ''
        else:
            stream = ''
    except:
        stream = ''
    dt = {}
    dt['page'] = str(urlrc)
    dt['stream'] = str(stream)
    js = json.dumps(dt)
    result = js
    return result

def rcchannel(channel):
    try:
        server = 'https://noticiasfix.fun'
        referer = server + '/'
        origin = server
        ads = server.replace('https://', '')
        url = '{0}/player3/canaishlbhls.php?M:%%3C\%3E/i/e/s/*=&canal={1}'.format(server,channel)
        referer_player = '{0}/player3/canaishlb.php?M:%%3C\%3E/i/e/s/*=&canal={1}&ads={2}&='.format(server,channel,ads)
        data = getRequest5(url,origin=origin,referer=referer_player)
        source = re.compile('source.+?src="(.*?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        if source:
            stream = source[0]
            stream = stream + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36&Origin={0}&Referer={1}'.format(origin,referer)
        else:
            stream = ''
    except:
        stream = ''
    dt = {}
    dt['channel'] = str(channel)
    dt['stream'] = str(stream)
    js = json.dumps(dt)
    result = js
    return result

def rcchannel2(channel):
    url = 'https://sinalpublico.com/player3/ch.php?canal={0}&img={0}'.format(channel)
    referer = 'https://redecanaistv.net/'
    url_parsed = urlparse(url) 
    hostname = '%s://%s'%(url_parsed.scheme,url_parsed.netloc)
    origin_player = hostname
    referer_player = url
    data = getRequest5(url,referer=referer)
    source = re.compile('source.+?src="(.*?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    if source:
        stream = source[0]
        stream = stream + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36&Origin={0}&Referer={1}'.format(origin_player,referer_player)
    else:
        stream = ''
    dt = {}
    dt['channel'] = str(channel)
    dt['stream'] = str(stream)
    js = json.dumps(dt)
    result = js
    return result

def rcchannel3(channel):
    try:
        UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        server = 'https://noticiasfix.fun'
        referer = server + '/'
        origin = server
        ads = server.replace('https://', '')
        url = '{0}/player3/canaishlbhls.php?M:%%3C\%3E/i/e/s/*=&canal={1}'.format(server,channel)
        referer_player = '{0}/player3/canaishlb.php?M:%%3C\%3E/i/e/s/*=&canal={1}&ads={2}&='.format(server,channel,ads)
        #novo_referer_player = 'https://sinalpublico.com/player3/ch.php?canal={0}&img={0}'.format(channel)
        novo_referer_player = 'https://sinalpublico.com/'
        url_parsed = urlparse(novo_referer_player) 
        hostname = '%s://%s'%(url_parsed.scheme,url_parsed.netloc)
        origin_player = hostname        
        data = getRequest5(url,origin=origin,referer=referer_player)
        url_parsed_test = urlparse(url)
        hostname_test = '%s://%s'%(url_parsed_test.scheme,url_parsed_test.netloc)
        origin_player_test = hostname_test
        referer_test = url        
        source = re.compile('source.+?src="(.*?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)        
        if source:
            stream = source[0]
            stream = stream + '|User-Agent={0}&Origin={1}&Referer={2}'.format(UA,origin_player_test,referer_test)
            #stream = stream + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36&Origin={0}&Referer={1}'.format(origin,referer)
            #stream = stream + '|User-Agent={0}&Origin={1}&Referer={2}'.format(quote(UA),quote(origin_player),quote(novo_referer_player))
            #stream = stream + '|User-Agent={0}&Origin={1}&Referer={2}'.format(quote(UA),quote(origin_player),quote(novo_referer_player))
            #stream = stream + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36&Referer={0}'.format(novo_referer_player)
        else:
            stream = ''
    except:
        stream = ''
    dt = {}
    dt['channel'] = str(channel)
    dt['stream'] = str(stream)
    js = json.dumps(dt)
    result = js
    return result

def rcchannel4(channel):
    try:
        UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        url = 'https://sinalpublico.com/player3/ch.php?canal={0}&img={0}'.format(channel)
        referer = 'https://redecanaistv.net/'
        url_parsed = urlparse(url) 
        hostname = '%s://%s'%(url_parsed.scheme,url_parsed.netloc)
        origin = hostname
        data = proxy_web(url,origin=origin,referer=url)
        source = re.compile('source.+?src="(.*?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        if source: 
            url2 = source[0]
            novo_referer_player = 'https://sinalpublico.com/'
            url_parsed2 = urlparse(novo_referer_player) 
            hostname2 = '%s://%s'%(url_parsed2.scheme,url_parsed2.netloc)
            origin_player = hostname
            stream = url2 + '|User-Agent={0}&Origin={1}&Referer={2}'.format(UA,origin_player,novo_referer_player)            
        else:
            stream = ''        
    except:
        stream = ''
    dt = {}
    dt['channel'] = str(channel)
    dt['stream'] = str(stream)
    js = json.dumps(dt)
    result = js
    return result


#https://apiresolver.herokuapp.com/rcapi2?ch=amc
#print(rcsolve('https://redecanais.wf/liga-da-justica-de-zack-snyder-dublado-2021-1080p_77e2db1d6.html'))

#def proxytest():
#    data = getRequest5('https://www.httpbin.org/ip')
#    print(data)
#proxytest()
#novo canal
#############################
#https://sinalpublico.com/player3/ch.php?canal=nickjr&img=nickjr 
#referer = https://redecanaistv.net/
#https://www-opensocial.googleusercontent.com/gadgets/proxy?container=focus&refresh=7200&url=http://minuano.tk/hls1/amc-48944.html 
#referer = https://sinalpublico.com/
###############################

#print(rcchannel('amc'))
#print(rcchannel2('amc'))
#print(rcchannel3('amc'))
#print(rcchannel4('amc'))

#site rc canais
#https://m3u9.ml/a2/hls1/fx.m3u8?mu3zAQc9HC3GbwJq=T5v6yQcbYQax2z_agCErsw&3U1G7qaTxrPbalZnEx=1642493060 
#Origin: https://sinalpublico.com
#Referer: https://sinalpublico.com/

#url teste:
#url=https://m3u9.ml/a2/hls1/fx.m3u8?mu3zAQc9HC3GbwJq=T5v6yQcbYQax2z_agCErsw&3U1G7qaTxrPbalZnEx=1642493060|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36&Origin=https://sinalpublico.com&Referer=https://sinalpublico.com/
