import os
import re
pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
pattern2 = re.compile(r"^[a-z'A-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
twoperiods = re.compile(r"\.\.")
emails_list = re.compile(r"', '|' \r\n'")
cnt = 0

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
        else:
            print "dropped " + word
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
    while go:
        recipients += (clean_email_list(line.split()))
        line = f.readline()
        if line[:9] == 'Subject: ':
            break
    #nextline = f.readline()
    #while not nextline.split()[0][-1] == ':':
    #    recipients.append(emails_list.split(nextline))
    #    nextline = f.readline()
    #
    #    print "FAILED ON: " + nextline 
    return recipients


def parseto(words, path):
    #for word in words:
    #    if word[-1] == ':':
    #        print path
    #        print word
    return True
    #words = line.split()
    #if len(words) > 1:
    #    if  words[0] == 'From:':
    #        for word in words:
    #            if pattern.match(word):
    #                if word[0] == '<' and word[-1] == '>':
    #                    word = word [1:-1]
    #                if twoperiods.match(word):
    #                    print path + " has bad addr: " + word
    #                return
    #print 'NO THING TO PARSE HERE: ' + path

def parsefile(path):
    global cnt
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
        2 +2 
    else:
        assert(False)

    #for line in f:
    #    line_number += 1
    #    words = line.split()
    #    if len(words) > 1:
    #        if not havetime and words[0] == 'Date:':
    #            havetime = parsetime(words)
    #            if line_number > 2:
    #                print words
    #        elif not havefrom and words[0] == 'From:':
    #            havefrom = parsefrom(words)
    #        elif words[0] == 'To:':
    #            toList = words[1:]
    #        elif len(toList) > 0:
    #            if words[0] == 'Subject:': 
    #                haveto = parseto(toList, path)
    #            else:
    #                toList.append(words)
    #        #elif not haveto and words[0] == 'X-To:':
    #            #print words

    f.close()
    #if (havefrom and havetime and haveto):
    cnt += 1
        #print 'NO THING TO PARSE HERE: ' + path

    

for root,dirs,files in os.walk('enron_email_full'):
    for afile in files:
        parsefile(root + '/' + afile)
print cnt
