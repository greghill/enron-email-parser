import os
import re
import heapq
import datetime
# store a min_heap with (date, source, destination_list), pull off heap to order emails chronologically
emails = []
heapq.heapify(emails)
adjlist = dict() # addr from, addrs sent to
pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
pattern2 = re.compile(r"^[a-z'A-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
twoperiods = re.compile(r"\.\.")
emails_list = re.compile(r"', '|' \r\n'")
cnt = 0
shit = 0
name_map = dict()
max_id = 0

def get_id(name):
    global name_map
    global max_id
    if name in name_map:
        return name_map[name]
    else:
        max_id += 1
        name_map[name] = max_id
        return max_id

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

def get_hour_mins(word):
    times = word.split(':')
    assert len(times) == 3
    return (int(times[0]),int(times[1]))

def get_month(word):
    if word == 'Jan':
        return 1
    elif word == 'Feb':
        return 2
    elif word == 'Mar':
        return 3
    elif word == 'Apr':
        return 4
    elif word == 'May':
        return 5
    elif word == 'Jun':
        return 6
    elif word == 'Jul':
        return 7
    elif word == 'Aug':
        return 8
    elif word == 'Sep':
        return 9
    elif word == 'Oct':
        return 10
    elif word == 'Nov':
        return 11
    elif word == 'Dec':
        return 12
    else:
        print word
        assert False

def parsetime(words):
    assert(len(words) == 8)
    assert(words[-1] == '(PST)' or words[-1] == '(PDT)')
# ignoring timezones for now
    #if words[-1] == '(PST)':
    #    timezone = pytz.pst
    #else:
    #    timezone = pytz.pdt
    month = get_month(words[3])
    (hour, mins) =  get_hour_mins(words[5])
    return datetime.datetime(int(words[4]), month, int(words[2]), hour, mins)

def parsefrom(line, path):
    words = clean_email_list(line.split())
    if len(words) == 1:
        return words[0]
    else:
        print line

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
    global adjlist
    global cnt
    global shit
    global emails
    f=open(path, 'r')
    f.readline() # ignore first line

    date = f.readline()
    assert(date[:6]  == 'Date: ') # second line is date
    datetime = parsetime(date.split())

    fromline = f.readline()
    assert(fromline[:6]  == 'From: ') # third line is From
    source = parsefrom(fromline[6:], path)

    fourthline = f.readline() # fourth line is To or Subject
    if fourthline[:4] == 'To: ':
        sinks = parse_multiline_to(fourthline[4:], f, path)
        if source is not None and len(sinks) > 0: # ignore if source or no dest passes regex
            source_id = get_id(source)
            three_tuple = (datetime, source_id, sinks)
            heapq.heappush(emails, three_tuple)
            #if source_id not in adjlist:
            #    adjlist[source_id] = []
            #for sink in sinks:
            #    sink_id = get_id(sink)
            #    assert(sink_id is not None)
            #    adjlist[source_id].append(sink_id)

    elif fourthline[:9] == 'Subject: ': # ignore if it doesnt have a to field
        shit += 1
        if shit % 1000 == 0:
            print shit
    else:
        assert(False)
    # now look for CCs

    f.close()
    cnt += 1

for root,dirs,files in os.walk('enron_email_full'):
    for afile in files:
        parsefile(root + '/' + afile)

print cnt
fileout = open('enron-adjlist.txt', 'w')
fileout.write('# ' + str(max_id) + '\n')
for (datetime, source_id, sink_list) in sorted(emails):
    for sink in sink_list:
        fileout.write(str(source) + ' '  + str(sink) + datetime + '\n')
fileout.close()
