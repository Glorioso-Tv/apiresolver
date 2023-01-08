import os
import sys
import time 
from flask import Flask, Response, session, url_for, send_file, send_from_directory, redirect, render_template, request, stream_with_context
#from threading import Thread
import hashlib
from rcresolver import rcsolve, rcchannel, rcchannel2, rcchannel3, rcchannel4
from aovivogratis import aovivo
from streamtape import streamtaperesolve, stream, streamtape2
from gg import gblogger
from animes import animesonline_club
from filmebrasil import filmebrasil
from filmeflix import filmeflix
from videobin import videobin
from canalricos import canalricos
from jovempan import jovempannews
from pandafiles import pandafiles
from ok import ok_ru
from dailymotion import DailymotionResolver
from regexgenerator import regex

app = Flask(__name__, static_url_path='')

#forçar https
#@app.before_request
#def before_request():
#    if not request.is_secure:
#        url = request.url.replace('http://', 'https://', 1)
#        code = 301
#        return redirect(url, code=code)



#enviar arquivos pra download se houver
@app.route('/download/<path:path>')
def send_js(path):
    return send_from_directory('download', path)

#index do site
@app.route('/')
def index():
    #download example
    #path = "/Examples.pdf"
    #return send_file(path, as_attachment=True)
    #servir static files    
    return render_template('index.html')

@app.route('/resolver',methods=['GET', 'POST'])
def resolver():
    url = request.args.get('url')
    if url:
        if 'http' in url and 'player.aovivotv.xyz/channels/' in url:
            result = aovivo(url)
        elif 'http' in url and 'redecanais' in url:
            result = rcsolve(url)
        elif 'http' in url and 'streamtape' in url:
            result = streamtaperesolve(url)
        elif 'http' in url and 'blogger' in url:
            result = gblogger(url)
        elif 'http' in url and 'animesonline.club' in url:
            result = animesonline_club(url)
        elif 'http' in url and 'ok.ru' in url and '/video/' in url or 'http' in url and 'odnoklassniki.ru' in url and '/video/' in url or 'http' in url and 'ok.ru' in url and '/videoembed/' in url or 'http' in url and 'odnoklassniki.ru' in url and '/videoembed/' in url:
            result = ok_ru(url)
        elif 'http' in url and 'filmebrasil.com' in url:
            result = filmebrasil(url)
        elif 'http' in url and 'flashcode' in url and 'auth' in url:
            result = filmeflix(url)
        elif 'http' in url and 'videobin.co' in url:
            result = videobin(url)
        elif 'http' in url and 'canalricos' in url:
            result = canalricos(url)
        elif 'http' in url and 'jovempan' in url:
            result = jovempannews(url)            
        elif 'http' in url and 'pandafiles' in url:
            result = pandafiles(url)
        elif 'http' in url and 'dai.ly' in url or 'http' in url and 'dailymotion.com' in url:
            result = DailymotionResolver(url)
        else:
            result = '{}'
    else:
        result = '{}'
    return result

@app.route('/rcapi',methods=['GET', 'POST'])
def rcapi():
    ch = request.args.get('ch')
    if ch:
        result = rcchannel4(ch)
    else:
        result = '{}'
    return result

@app.route('/regex',methods=['GET', 'POST'])
def getregex():
    url = request.args.get('url')
    if url:
        if 'http' in url:
            result = regex(url)
        else:
            result = ''
    else:
        result = ''
    return Response(result, mimetype='text/plain')
    #return result, 200, {'Content-Type': 'text/css; charset=utf-8'}


def start_flaskapp():
	app.run(host='0.0.0.0', port=80)


if __name__ == '__main__':
    start_flaskapp()