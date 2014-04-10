#!/usr/bin/python
import codecs, os
from os import path
#from fuzzywuzzy import fuzz
broken =[]
import configparser
config = configparser.ConfigParser()
config.read('.\myconfig')
basedir =  config['default']['basedir']
listname = config['default']['ituneslist']
rconf = config['ratings']
Onestar = rconf['Onestar']
Twostar = rconf['Twostar']
Threestar = rconf['Threestar']
Fourstar = rconf['Fourstar']
Fivestar = rconf['Fivestar']
Notrated = rconf['Notrated']
delimiter = config['file format']['delimiter']
rowlen = int (config['file format']['default rowlen'])

#-------------------------------------------------------------------------------------------------    
class myplaylist(object):
    
    def __init__(self,playlist_name): 
        self.name =  playlist_name
        self.songlist = []
        self.count =0
        self.maxsongs = 0
    def __iter__(self):
        return self.songlist[self.count]
    def __next__(self):
        if self.count > self.maxsongs:
            raise StopIteration 
        self.count +=1
        return self.songlist[self.count]         
    def add (self,song):
        self.songlist.append(song)
        self.maxsongs+=1
        
    def listsong (self):
        for i in self.songlist:
            print (i.title)
    def writemu3 (self):
        listname = self.name + '.m3u'
        fname = path.join(basedir,listname)
        ID = 0
        mu3file=open(fname,'w')
        old = []
        slist=sorted (self.songlist, key=lambda songt: songt.title)
        for element in slist:
            if 'Paint' in element.title:
                print (old.title,old.artist,element.title,element.artist)
            if old != []:
                if old.title == element.title and old.artist == element.artist:
                    if 'Paint' in element.title:
                        print (element.title,element.artist,'cont')
                    continue
                
            if 'Paint' in element.title:
                print('write')
            ID =ID+1
            mu3file.write("#EXTINF:%d," % ID)
            mu3file.write("%s - " % element.title)
            mu3file.write("%s\n" % element.artist)
            mu3file.write("%s\n" % element.location)
            old = element
        mu3file.close() 
    def readmu3 (self,mypath):
        
        file_paths = [] 
        for dirpath, dirnames, files in os.walk(mypath):
            for filename in files:
                filepath = os.path.join(dirpath,filename)
                file_paths.append(filepath) 
        
        for item in file_paths:
            line = os.path.basename(item)
            # only if its an mp3 file
            if '.mp3' in line:
                # format is rootpath/artist/album 
                tracknr =line.split('-')
                line = os.path.dirname(item)
                albumpath = line.split('\\')
                album = albumpath[len(albumpath)-1]
                #support 3 formats
                # track - title -> len == 2
                # disk-track - title
                # track - artist - title
                if len(tracknr) == 2:
                    disknr = 0
                    track = tracknr[0]
                    artist = albumpath[len(albumpath)-2]
                else:
                    if tracknr[1].isdigit():
                        track = tracknr[1]
                        disknr = tracknr[0]
                        artist = albumpath[len(albumpath)-2]
                    else:
                        track = tracknr[0]
                        artist = tracknr[1]
                title = tracknr[len(tracknr)-1].strip('.mp3')
                newsong=songt('')
                newsong.title = title
                newsong.artist = artist
                newsong.album = album
                newsong.track = track
                newsong.disk = disknr
                newsong.location = item
                self.songlist.append(newsong)
        #return (self.songlist)                
                
class songt(object):
          
        def __init__(self,songlist):

            if songlist:
                self.artist = songlist[1]
                self.title = songlist[0]
                self.album = songlist[3]
                self.disk = songlist[8]
                self.track = songlist[10]
                self.rating = songlist[25]
                if len (songlist) == rowlen:
                    self.location = songlist[26]
                else:
                    self.location =''

        def viewsong(self):
            print (self.location)
def songs_match(song1,song2):
    #print(song1.title,song2.title)
    #if fuzz.token_set_ratio(song1.title,song2.title) >90:
    if song1.title == song2.title:
        #if fuzz.token_set_ratio(song1.artist,song2.artist) >90:
        if song1.artist == song2.artist:
            #if fuzz.token_set_ratio(song1.album,song2.album) >90:
            if song1.album == song2.album:
                if song2.location != '':
                    if song2.rating != Fourstar:
                        #print(song1.title, song1.artist,song1.album)
                        return(6)
                    else:
                        #print(song2.title,song2.artist,'rating')
                        return (5)
                else:
                    return(4)
            else:
                return(3)
        else:
            return(2)
    else:
        return(1)


    return (0)

def readlist(filename,playlistname):
    i=0
    fname = path.join(basedir,filename)
    print(fname)
    songreader = codecs.open(fname,'r',encoding='utf-8',errors='ignore')
    for line in songreader:
        try:
            row = line.split('\t')
            if len(row) >= rowlen-1:
                if i > 0:
                    mysong = songt(row)
                    playlistname.add(mysong)
                i+=1
        except UnicodeDecodeError:
            continue      
                    
    return()