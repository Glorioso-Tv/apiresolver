from urllib.parse import quote_plus
url_host = 'https://apiresolver.joelsilva3.repl.co'

def regex(url):
    if url:
        rg = 'Your regex:\n'
        rg += '<item>\n'
        rg += '<title>Test</title>\n'
        rg += '<link>$doregex[resolver]</link>\n'
        rg += '<regex>\n'
        rg += '<name>resolver</name>\n'
        rg += '<expres>"stream":.+?"(.*?)"</expres>\n'
        rg += '<page>{0}/resolver?url={1}</page>\n'.format(url_host,quote_plus(url))
        rg += '</regex>\n'
        rg += '<thumbnail></thumbnail>\n'
        rg += '<fanart></fanart>\n'
        rg += '<info></info>\n'
        rg += '</item>'
    else:
        rg = ''
    return rg
