import os
import re
pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
pattern2 = re.compile(r"^[a-z'A-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
twoperiods = re.compile(r"\.\.")
emails_list = re.compile(r"', '|' \r\n'")
cnt = 0
shit = 0

def clean_email_list(wordlist):
    toRet = []
    for word in wordlist:
        if pattern.match(word):
            if word[:2] == "<.":
                word = word[2:]
            if word[-1] == ',':
                word = word[:-1]
            if word[-1] == '>':
                word = word[:-1]

            toRet.append(word)
        #else:
        #    print "dropped " + word
    return toRet

def parsetime(words):
    if not words[-1] == '(PST)' and not words[-1] == '(PDT)':
        print words
    return True

def parsefrom(line, path):
    words = clean_email_list(line.split())
    if len(words) == 1:
        return words[0]
    else:
        print line
        #assert(False)

def parse_multiline_to(line, f, path): #TODO delete path
    recipients = []
    go = True
    num = 0
    while go:
        num += 1
        recipients += (clean_email_list(line.split()))
        line = f.readline()
        if line[:9] == 'Subject: ':
            break
    return recipients

def parsefile(path):
    global cnt
    global shit
    f=open(path, 'r')
    f.readline() # ignore first line

    date = f.readline()
    assert(date[:6]  == 'Date: ') # second line is date
    parsetime(date.split())

    fromline = f.readline()
    assert(fromline[:6]  == 'From: ') # third line is From
    source = parsefrom(fromline[6:], path)

    fourthline = f.readline() # fourth line is To or Subject
    if fourthline[:4] == 'To: ':
        sinks = parse_multiline_to(fourthline[4:], f, path)
    elif fourthline[:9] == 'Subject: ':
        shit += 1
        if shit % 1000 == 0:
            print shit
    else:
        assert(False)

    f.close()
    cnt += 1

    

for root,dirs,files in os.walk('enron_email_full'):
    for afile in files:
        parsefile(root + '/' + afile)
print cnt
