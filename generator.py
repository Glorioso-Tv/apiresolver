import hashlib
p = input('Text: ')
try:
    p = p.encode('utf-8')
except:
    pass
try:
    d = hashlib.md5(p)
    d = d.hexdigest()
except:
    d = ''
#d = hashlib.sha1(p)
print('Your hash is: ',d)
