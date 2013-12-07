import os
import re
pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")

def parsefile(path):
    f=open(path, 'r')
    for line in f:
        words = line.split()
        if len(words) > 1:
            if  words[0] == 'From:':
                for word in words:
                    if pattern.match(word):
                        #print word
                        f.close()
                        return
    print 'NO THING TO PARSE HERE: ' + path
    f.close()

    

for root,dirs,files in os.walk('.'):
    for afile in files:
        parsefile(root + '/' + afile)
