import re
import requests
import random
import json
import base64

setproxy = ''

def browser(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    try:
        resp = requests.get(url,headers=headers)
        html = resp.text
    except:
        html = ''
    return html


def proxy_https():
    url = 'http://proxydb.net/?protocol=https&country=BR'
    proxies = []
def proxy_https():
    url = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all'
    proxies = []
    try:
        list_proxies = browser(url)
        list_proxies = list_proxies.replace('\n', '').replace('\r', '')
        list_proxies = re.compile('<tbody>(.*?)</tbody>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(list_proxies)
        list_proxies = re.compile('<tr>.+?<td>.+?<a href.+?https">(.*?)</a>.+?</td>.+?</td>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(str(list_proxies))

        count = 0
        for proxie in list_proxies:
            count += 1
            if '.' in proxie:
                if verify_proxy(proxie,'https') and verify_redecanais_https(proxie) and count < 6:
                   proxies.append(proxie)
                elif count < 6:
                    continue
                else:
                    break
    except:
        pass
    if proxies:
        proxy = random.choice(proxies)
        proxy = 'https://' + proxy
    else:
        proxy = False
    return proxy

def proxy_http():
    url = 'http://proxydb.net/?protocol=http&country=BR'
    proxies = []
    try:
        list_proxies = browser(url)
        list_proxies = list_proxies.replace('\n', '').replace('\r', '')
        list_proxies = re.compile('<tbody>(.*?)</tbody>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(list_proxies)
        list_proxies = re.compile('<tr>.+?<td>.+?<a href.+?https">(.*?)</a>.+?</td>.+?</td>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(str(list_proxies))

        count = 0
        for proxie in list_proxies:
            count += 1
            if '.' in proxie:
                if verify_proxy(proxie,'https') and count < 6:
                   proxies.append(proxie)
                elif count < 6:
                    continue
                else:
                    break
    except:
        pass
    if proxies:
        proxy = random.choice(proxies)
        proxy = 'http://' + proxy
    else:
        proxy = False
    return proxy


def verify_proxy(proxie,type):
    if type == 'http':
        px = 'http://' + proxie
        api = 'http://api.ipify.org/'
    elif type == 'https':
        px = 'https://' + proxie
        api = 'https://api.ipify.org/'
    else:
        px = False
        api = False
    if px and proxie and api:
        try:
            check = proxie.split(':')[0]
        except:
            pass
        try:
            ip = getRequest(api,proxy=px)
        except:
            ip = ''
        ip = ip.replace(' ', '').replace('\n', '').replace('\r', '')
        if check in ip:
            #print('proxy valido: ', ip)
            status = True
        else:
            status = False
    else:
        status = False
    return status

def verify_redecanais_https(proxy):
    proxy = 'https://' + proxy
    url_test = 'https://sinalpublico.com/player3/ch.php?canal=amc&img=amc'
    origin='https://redecanaistv.net'
    referer='https://redecanaistv.net/'
    try:
        html = getRequest(url_test,origin=origin,referer=referer,proxy=proxy)
    except:
        html = ''
    source = re.compile('source.+?src="(.*?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(html)
    if source:
        status = True
    else:
        status = False
    return status


def verify_player.aovivotv.xyz/channels_https(proxy):
    proxy = 'https://' + proxy
    url_test = 'https://player.aovivotv.xyz/channels/'
    origin='https://aovivo.pro/tv'
    referer='https://aovivo.pro/tv/'
    try:
        html = getRequest(url_test,origin=origin,referer=referer,proxy=proxy)
    except:
        html = ''
    source = re.compile('source.+?src="(.*?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(html)
    if source:
        status = True
    else:
        status = False
    return status


def getRequest(url,origin=False,referer=False,post=False,proxy=False):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"}
    if origin:
        headers.update({"Origin": origin})
    if referer:
        headers.update({"Referer": referer})
    if post:
        if proxy:
            if 'http://' in url:
                proxyDict = {'http': proxy}
            elif 'https://' in url:
                proxyDict = {'https': proxy}
            else:
                proxyDict = {'https': proxy}
            response = requests.post(url, headers=headers, proxies=proxyDict, data=post, verify=False)
        else:
            response = requests.post(url, headers=headers, data=post, verify=False)
    else:
        if proxy:
            if 'http://' in url:
                proxyDict = {'http': proxy}
            elif 'https://' in url:
                proxyDict = {'https': proxy}
            else:
                proxyDict = {'https': proxy}
            response = requests.get(url, headers=headers, proxies=proxyDict, verify=False)
        else:
            response = requests.get(url, headers=headers, verify=False)
    html = response.text
    return html
          

#pip install urllib3==1.25.8
def test_proxy():
    #https_proxy = proxy_https()
    https_proxy = 'https://131.255.239.38:3128'
    if https_proxy:
        px = https_proxy.replace('https://', '')
        print('Proxy setado: ',px)
        html = getRequest('https://api.ipify.org/',proxy=https_proxy)
        html = html.replace(' ', '').replace('\n', '').replace('\r', '')
        print('Ip do site é ', html)
        if html in str(px):
            status = 'Proxy {0} funcionando'.format(html)
        else:
            status = 'O Proxie {0} é invalido'.format(px)
    else:
        status = 'não foi possivel usar proxy'
    print(status)


def proxy_web2(url,origin=False,referer=False,post=False):
    global setproxy
    if not setproxy:
        proxy = proxy_https()
        setproxy +=proxy
    if setproxy:
        try:
            html = getRequest(url,origin=origin,referer=referer,post=post,proxy=setproxy)
        except:
            html = ''
    else:
        html = ''
    return html

def proxy_web(url,origin=False,referer=False,post=False):
    try:
        html = getRequest(url,origin=origin,referer=referer,post=post)
    except:
        html = ''
    return html
#print(proxy_web('https://sinalpublico.com/player3/ch.php?canal=amc&img=amc',origin='https://redecanaistv.net',referer='https://redecanaistv.net/'))
