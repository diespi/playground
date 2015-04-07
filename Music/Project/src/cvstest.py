#!/usr/bin/python
import codecs, os
from os import path
import stagger
from stagger.id3 import  *
#from fuzzywuzzy import fuzz
broken =[]
import configparser
config = configparser.ConfigParser()
config.read('./myconfig')
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
        
    def listsongs (self):
        # print a breif list of songs in the playlist
        for i in self.songlist:
            print (i.artist,"-",i.title)
    
    def writemu3 (self):
        # create a playlist file sorted by title
        listname = self.name + '.m3u'
        fname = path.join(basedir,listname)
        ID = 0
        mu3file=open(fname,'w',encoding='utf-8')
        slist=sorted (self.songlist, key=lambda songt: songt.title)
        for element in slist:
            ID =ID+1
            print(element.location)
            mu3file.write("#EXTINF:%d," % ID)
            mu3file.write("%s - " % element.title)
            mu3file.write("%s\n" % element.artist)
            mu3file.write("%s\n" % create_rel_path(element.location))
        mu3file.close() 
    
    def readmu3 (self,mypath):
        # walk through a given directory and find all the mp3 files.
        # append files to a given playlist
        # files and directories should have a pre defines structure
        # like amazon or itunes are organizing their folders
        
        file_paths = [] 
        for dirpath, dirnames, files in os.walk(mypath):
            for filename in files:
                filepath = os.path.join(dirpath,filename)
                file_paths.append(filepath) 
        
        for item in file_paths:
            line = os.path.basename(item)
            readmode=2
            # only if its an mp3 file
            if '.mp3' in line:
                # format is rootpath/artist/album 
                #print(line)
                tracknr =line.split('-')
                line = os.path.dirname(item)
                albumpath = os.path.split(line)
                album = albumpath[len(albumpath)-1]
                albumpath = os.path.split(albumpath[0])
                #support 3 formats
                # track - title -> len == 2
                # disk-track - title
                # track - artist - title
                if readmode == 1:
                #if len(tracknr) == 2:
                    disknr = 0
                    track = tracknr[0].strip()
                    artist = albumpath[len(albumpath)-1]
                    #title = tracknr[len(tracknr)-1].strip('.mp3')
                    title=''
                    for j in range (len(tracknr)-1):
                        title=title+'-'+tracknr[j+1]
                    title = title.strip ('.mp3')
                else:
                    # track is not formatted properly or has extra '-'
                    # try to read the id-tag from the file
                    tag = stagger.read_tag(item)
                    track = str.format("%02d" % tag.track)
                    artist = tag.artist
                    title = tag.title
                    disknr = 1
                    album = tag.album
                #print(artist,album,track,title)
                    #if tracknr[1].isdigit():
                        #   track = tracknr[1].strip()
                        #  disknr = tracknr[0]
                        # artist = albumpath[len(albumpath)-2]
                    #else:
                        #track = tracknr[0].trim()
                        #artist = tracknr[1].strip()
                
                
                newsong=songt('')
                newsong.title = title
                newsong.artist = artist
                newsong.album = album
                newsong.track = track
                newsong.disk = disknr
                newsong.location = item
                print(item)
                # todo: check for duplicates
                self.songlist.append(newsong)
        #return (self.songlist)
    def checkmu3 (self,mypath):
        listname = self.name
        mu3file=open(listname,'r',encoding='utf-8')
        for line in mu3file:
            if '.mp3' in line:
                #check if file exits
                #read the tags
                #append to playlist
                fpath=line.rstrip('\n')
                #fpath=path.join(os.getcwd(),line)
                if os.path.exists(fpath):
                    tag = stagger.read_tag(fpath)
                    track = str.format("%02d" % tag.track)
                    artist = tag.artist
                    title = tag.title
                    disknr = 1
                    album = tag.album
                    #print(artist,album,track,title)
                    newsong=songt('')
                    newsong.title = title
                    newsong.artist = artist
                    newsong.album = album
                    newsong.track = track
                    newsong.disk = disknr
                    newsong.location = fpath
                    self.songlist.append(newsong)

                else:
                    print(fpath, "is missing")

                    
                
class songt(object):
    # a song object holds all the meta data of a song
    # it can be initialized by a CVS file exported from itunes
    # I am only interested in a few fields
    # sometimes itunes screws up the location in that case I leave it empty.
    # todo try to repair the location
    # todo normalized and non normalized locations
          
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
        def check_location (self):
            if os.path.isfile(self.location):
                return (1)
            else:
                return (0)
# todo fuzzy match
def songs_match(song1,song2):
    # compare two songs
    #    0 - not used
    #    1 - no match in title
    #    2 - same title
    #    3 - same title and artist
    #    4 - same title and artist and album
    #    5 - rating is already set
    #    6 - rating has to be updated
    
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

# function to read a cvs formatted file and put all songs into a playlist
# basedir of files can be configured

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

def create_rel_path(filename):
    line = os.path.basename(filename)
    folder = os.path.dirname(filename)
    folders = os.path.split(folder)
    folder1 = folders[1]
    folder2 = os.path.split(folders[0])[1]


    rel_path = os.path.join('.',folder2,folder1,line)
    return(rel_path)
