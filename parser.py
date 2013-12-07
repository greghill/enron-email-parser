import os
import re
pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
pattern2 = re.compile(r"^[a-z'A-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
twoperiods = re.compile(r"\.\.")

def parsefile(path):
    f=open(path, 'r')
    for line in f:
        words = line.split()
        if len(words) > 1:
            if  words[0] == 'From:':
                for word in words:
                    if pattern.match(word):
                        if word[0] == '<' and word[-1] == '>':
                            word = word [1:-1]
                        if twoperiods.match(word):
                            print path + " has bad addr: " + word
                        f.close()
                        return
    print 'NO THING TO PARSE HERE: ' + path
    f.close()

    

for root,dirs,files in os.walk('enron_email_full'):
    for afile in files:
        parsefile(root + '/' + afile)
