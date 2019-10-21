import os
import sys
import re
import unicodedata
import time
import urllib2
import json

DECADES = [(1950, 1959), (1960, 1969),(1970, 1979),
               (1980, 1989), (1990, 1999), (2000, 2009), (2010, 2019)]

def split_albums_by_decade(path):    
    dirs_splitted_by_decades = {}

    for decade in DECADES:
        dirs_splitted_by_decades[decade] = []

    dirs = os.walk(path)

    for album in dirs:
        match = re.search('\d{4}', album[0])
        year = match.group(0) if match else None

        # if not year:
        #     match = re.search('\d{2}', album[0])
        #     year = match.group(0) if match else None

        if year:
            for decade in DECADES:
                if int(year) in range(decade[0], decade[1]):
                    dirs_splitted_by_decades[decade].append(album[0])

    return dirs_splitted_by_decades

def order_songs_by_play_count(albums):
    songs_with_play_count = []

    for album in albums:
        artist = strip_accents(os.path.basename(album).split("-")[0]).strip()
        for dir_file in os.listdir(album):
            full_path = os.path.join(album, dir_file)
            if dir_file.endswith("mp3") or dir_file.endswith("wma"):                
                dir_file = dir_file.replace(".mp3", "").replace(".wma","").replace("Faixa","").replace(artist, "")
                dir_file = strip_accents(dir_file)
                dir_file = re.sub(r"[^a-zA-Z ]+", '', dir_file).strip()
                print "fetching info for: %s - %s" % (artist, dir_file)

                while True:
                    try:
                        json_contents = json.loads(urllib2.urlopen("http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=8c3cf884c8cfe14691f364f1776a5408&artist=%s&track=%s&format=json" % (artist.lower(), dir_file.lower())).read())

                        if 'message' in json_contents.keys():
                            print "no info"
                            break
                        print "found info!"
                        songs_with_play_count.append((full_path, int(json_contents['track']['playcount'])))
                        break
                    except Exception, e:  
                        print "error but will try again"
                        print "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=8c3cf884c8cfe14691f364f1776a5408&artist=%s&track=%s&format=json" %  (artist, dir_file)      
                        print str(e)
                        time.sleep(1)
                        pass
    
    return sorted(songs_with_play_count, key=lambda tup: tup[1], reverse=True) 


def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return str(text)

def write_ordered_to_file(ordered_list, decade, n):
    with open('top %i - %i.txt' % (int(n), int(decade)), "w") as ranking_file:
        for song_info in ordered_list[0:n]:
            ranking_file.write("%s | %i\n" % (song_info[0], int(song_info[1])))


if __name__ == '__main__':
    # print(split_albums_by_decade('/home/felipev/datasets/forro em vinil').keys())
    albums_by_decade = split_albums_by_decade('/home/felipev/datasets/forro em vinil')
    
    for decade in DECADES:
        write_ordered_to_file(order_songs_by_play_count(albums_by_decade[decade]), decade[0], 500)