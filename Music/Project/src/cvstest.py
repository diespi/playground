#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs, os
from os import path
import stagger
import shutil
import errno
from stagger.id3 import  *
from _operator import itemgetter
#import audiotools
import re
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
verbose = 0
fixit = 0
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
        print (   
                song.title,
                song.artist,
                song.composer,
                song.album,
                song.disk,
                song.genre,
                song.size,
                song.time,
                song.disc_nr,
                song.disc_cnt,
                song.track,
                song.track_cnt,
                song.year,
                song.modified,
                song.added,
                song.comment,
                song.plays,
                song.last_played,
                song.skips,
                song.last_skipped,
                song.rating,
                song.location )
        self.songlist.append(song)
        self.maxsongs+=1
        
    def listsongs (self):
        # print a breif list of songs in the playlist
        for i in self.songlist:
            print (i.artist,"-",i.title)
    
    def writem3u8 (self,newname):
        # create a playlist file sorted by title
        if newname == "":
          listname = self.name
        else:
          listname = newname
        fname = path.join(os.getcwd(),listname)
        if os.path.isfile(fname):
            os.rename (listname,listname +'.org')
            print ('renamed', listname, ' to ', listname +'.org')
        ID = 0
        mu3file=open(fname,'w',encoding='utf-8')
        slist=sorted (self.songlist, key=lambda songt: songt.title)
        for element in slist:
            ID =ID+1
            #print(element.location)
            mu3file.write("#EXTINF:%d," % ID)
            mu3file.write("%s - " % element.title)
            mu3file.write("%s\n" % element.artist)
            mu3file.write("%s\n" % element.location)
        mu3file.close() 
    
    def readFilesTom3u (self,mypath,fixit):
        # walk through a given directory and find all the mp3 files.
        # append files to a given playlist
        # files and directories should have a pre defines structure
        # like amazon or itunes are organizing their folders
        #print(mypath)
        if fixit == 0:
            print ("skipping tag update")
        file_paths = [] 
        for dirpath, dirnames, files in os.walk(mypath):
            #print(files)
            for filename in files:
                #print(filename, "Dir",dirpath)
                filepath = os.path.join(dirpath,filename)
                #print(filepath)
                file_paths.append(filepath) 
        
        for item in file_paths:
            line = os.path.basename(item)
            #print(line)
            # for now force into reading mp3 tags
            # only if its an mp3 file
            if '.mp3' in line:
                try:
                    if verbose == 1:
                        print (item)
                    tag = stagger.read_tag(item)
                    print(tag)
                    print(list(tag.keys()))
                    if fixit == 1:
                      for key in list(tag.keys()):
                        if key in ('GEOB',  # General encapsulated object
                                   'MCDI',  # Music CD identifier
                                   'NCON',  # MusicMatch data
                                   'PCNT',  # Play counter
                                   'POPM',  # Popularimeter
                                   'PRIV',  # Private frame
                                   'TCOP',  # Copyright message
                                   'TDLR',  # invalid
                                   'TENC',  # Encoded by 
                                   'TEXT',  # Lyricist/Text writer
                                   'TIT3',  # Subtitle/Description refinement
                                   'TKEY',  # Initial key /^([CDEFGAB][b#]?[m]?|o)$/
                                   'TOAL',  # Original album/movie/show title
                                   'TOLY',  # Original lyricist(s)/text writer(s)
                                   'TPUB',  # Publisher
                                   'TRSN',  # Internet radio station name
                                   'TSIZ',  # Size 
                                   'TSSE',  # Software/Hardware and settings used for encoding
                                   'TT22',  # invalid
                                   'TOWN',  # File owner
                                   'TSOE',  # invalid
                                   'TXXX',  # User defined text information frame
                                   'UFI',   # Unique file identifier
                                   'UFID',  # Unique file identifier
                                   'USER',  # Terms of use
                                   'W000',  # invalid
                                   'WCOM',  # Commercial information
                                   'WOAF',  # Official audio file webpage
                                   'WOAR',  # Official artist/performer webpage
                                   'WOAS',  # Official audio source webpage
                                   'WORS',  # Official Internet radio station homepage
                                   'WXXX'   # User defined URL link frame
                                  ):
                            #print('stripping ',key,tag[key])
                            # deleting keys which are broken or not relevant
                            del tag[key]
                            
                        else:
                            if key not in (
                                           'APIC',   # Attached picture
                                           'COM',    # Comments
                                           'COMM',   # Comments
                                           'PIC',    # Attached picture
                                           'RGAD',   # Replay Gain Adjustment
                                           'RVAD',   # Relative volume adjustment Replaced by RVA2 in id3v2.4
                                           'SYLT',   # Synchronised lyric/text
                                           'TAL',    # Album/Movie/Show title
                                           'TALB',   # Album/Movie/Show title
                                           'TBPM',   # BPM (beats per minute)
                                           'TCM',    # Composer
                                           'TCMP',   # iTunes: Part of a compilation
                                           'TCO',    # Content type
                                           'TCOM',   # Composer
                                           'TCON',   # Content type
                                           'TCP',    # iTunes: Part of a compilation
                                           'TDAT',   # Date
                                           'TDRC',   # Recording time
                                           'TDRL',   # Release time
                                           'TEN',    # Encoded by
                                           'TENC',   # Encoded by
                                           'TFLT',   # File type
                                           'TIME',   # Time Replaced by TDRC in id3v2.4
                                           'TIT1',   # Content group description
                                           'TIT2',   # Title/songname/content description
                                           'TLAN',   # Language
                                           'TLEN',   # LENGTH
                                           'TMED',   # Media type
                                           'TOPE',   # Original artist(s)/performer(s)
                                           'TORY',   # Original release year Replaced by TDOR in id3v2.4
                                           'TP1',    # Lead performer(s)/Soloist(s)
                                           'TP2',    # Band/orchestra/accompaniment
                                           'TPA',    # Part of a set
                                           'TPE1',   # Lead performer(s)/Soloist(s)
                                           'TPE2',   # Band/orchestra/accompaniment
                                           'TPE3',   # Conductor/performer refinement
                                           'TPOE',   # invalid
                                           'TPOS',   # Part of a set
                                           'TRCK',   # Track number/Position in set
                                           'TRK',    # Track number/Position in set
                                           'TSO2',   # iTunes: Album Artist sort order
                                           'TSOA',   # Album sort order
                                           'TSOP',   # Performer sort order
                                           'TSOT',   # Title sort order
                                           'TT2',    # Title/songname/content description
                                           'TYE',    # Year Replaced by TDRC in id3v2.4
                                           'TYER',   # Year Replaced by TDRC in id3v2.4
                                           'USLT'    # Unsynchronised lyric/text transcription
                                          ):

                                print('key:',key,'tag[key]:',tag[key])
                        if key.endswith(" "): # iTunes
                            del tag[key]
                        if tag.version == 4 and key == "XSOP": # MusicBrainz
                            del tag[key]
                      tag.artist = tag.artist.strip()
                      tag.album = tag.album.strip()
                      tag.title = tag.title.strip()
                      if tag.artist == '':
                          tag.artist = 'Unknown'
                      if tag.album == '':
                          tag.album = 'Unknown'
                      tag.write()
                    date = tag.date
                    album_artist = tag.album_artist
                    track_total = tag.track_total
                    disc_total = tag.disc_total
                    composer = tag.composer
                    genre = tag.genre
                    comment = tag.comment
                    
                    track  = str.format("%02d" % tag.track)
                    artist = tag.artist.strip().title()
                    title = tag.title.strip().title()
                    album = tag.album.strip().title()
                    #print(title,tag.title)
                    disknr = tag.disc
                # except Error("ID3v2 tag not found"):
                except stagger.Error as e:
                    print("bad tag",line)
                    continue
                    #print(artist,album,track,title)
                    #if tracknr[1].isdigit():
                        #   track = tracknr[1].strip()
                        #  disknr = tracknr[0]
                        # artist = albumpath[len(albumpath)-2]
                    #else:
                        #track = tracknr[0].trim()
                        #artist = tracknr[1].strip()
                
                
                newsong=songt('self')
                newsong.title = title
                newsong.artist = artist
                newsong.album = album
                newsong.track = track
                newsong.composer = composer
                newsong.genre = genre
                newsong.disk = disknr
                newsong.comment = comment
                newsong.year = date
                newsong.size = 0
                rootpath=os.path.dirname(item)
                myrelpath=os.path.basename(item)
                while rootpath != mypath:
                    #print(rootpath, "mypath",mypath)
                    myrelpath=os.path.join(os.path.basename(rootpath),myrelpath)
                    rootpath=os.path.dirname(rootpath)
                newsong.location = myrelpath
                # print(myrelpath.encode("utf-8"))
                # todo: check for duplicates
                self.add(newsong)
                #self.maxsongs+=1
        #return (self.songlist)
    def checkmu3 (self,mypath):
        # open a playlist file and append the songs to playlist passed in
        # if the playlist is local the the file path should point to a physcal file 
        # so we can open that file and read the tags.
        # otherwise we can read the metadata from the playlist and create a normalized version
        listname = self.name
        print(listname)
        mu3file=open(listname,'r',encoding='utf-8')
        for fullline in mu3file:
            if '.mp3' in fullline:
                #check if file exits
                #read the tags
                #append to playlist
                fpath=fullline.rstrip('\n')
                fpath=path.join(os.getcwd(),fpath)
                #print ("path ",fpath)
                if os.path.isfile(fpath):
                    #print (fpath)
                    tag = stagger.read_tag(fpath)
                    track = str.format("%02d" % tag.track)
                    #artist = re.sub('[^a-zA-Z0-9öäüÖÄÜß\'\n\-\(\)\[\]\{\}\,\&\$\!\+ ]', '', tag.artist.strip()).title()
                    #title  = re.sub('[^a-zA-Z0-9öäüÖÄÜß\'\n\-\(\)\[\]\{\}\,\&\$\!\+ ]', '', tag.title.strip()).title()
                    #album  = re.sub('[^a-zA-Z0-9öäüÖÄÜß\'\n\-\(\)\[\]\{\}\,\&\$\!\+ ]', '', tag.album.strip()).title()
                    artist = tag.artist.strip().title()
                    title = tag.title.strip().title()
                    album = tag.album.strip().title()
                    disknr = tag.disc
                    #print(artist,album,track,title)

                else:
                    # we assume no id tags need to get information from the file
                    # format is rootpath/artist/album
		    #  there is no fixed layout for playlists. Scanning a playlist can be tricky
                    #  order artist -title vs. title - artist 
                    # ---------------
                    #  Full path
                    #  #EXTINF:11,Hide Away - Daya
                    #  /Volumes/My Passport/Music/temp/top rated/Hide Away - Daya.mp3
                    full_track = os.path.basename(fullline)
                    album_path = fullline.split('/')
                    disknr = 1
                    title = ""
                    track = 0
                    artist = ""
                    album = ""
                    if len(album_path) == 1:
                      # no '/' in the path check if it is a Windows path
                      fullline = fullline.replace ('\\','/')
                      full_track = os.path.basename(fullline)
                      album_path = fullline.split('/')
                      # print (fullline, full_track,album_path)
                    if len(album_path) == 2:
                      # ---------------
                      #  Short path: folder/title - artist/
                      #  #EXTINF:10,2 Become 1 - Spice Girls
                      #  top rated/2 Become 1 - Spice Girls.mp3
                      artist = full_track.split(' - ')[1].split('.')[0].strip()
                      title = full_track.split(' - ')[0].strip()
                      album = album_path[len(album_path) - 2].strip()
                      # print ( artist,'/',album,'/',title)
                      # print(fullline,full_track,album,title,artist)
                      track=str.format("%02d" % 1)
                      # print ( artist,'/',album,'/',track,' - ', title)
                    elif len(album_path) >= 4:
                      # ---------------
                      #  Normalized path
                      #  #EXTINF:85,'No More (I Can'T Stand It) - Maxx
                      #  M/Maxx/Dance Nrg 94/02 - 'No More (I Can'T Stand It).mp3
                      print(full_track)
                      title = full_track.split('-')[1].split('.')[0].strip()
                      if title == "":
                        title = 'unknown'
                      track = full_track.split(' - ')[0].strip()
                      album = album_path[len(album_path) - 2].strip()
                      artist = album_path[len(album_path) - 3].strip()
                      # print(fullline,full_track,album,title,artist)
                      # print ( artist,'/',album,'/',track,' - ', title)
                    else:
                       print ('len', len(album_path))
                       print (fullline)
                    # print ('initial:',initial,'filename:', filename,'path:',file_path)
                    # line is the song title plus track number
                    # track number is ususally seperated by '-' but title can contain '-' as well
                    # itunes has disk-track titel
                    # amazon has disk-track- title
                    # lets split the line
                    # tracktitle = os.path.basename(fullline)
                    # title=''
                    # tracknr =tracktitle.split('-')
                    # if len(tracknr) ==1:
                        # no dashes in the file 
                        # a) no track number
                        # b) track is seperated by space
                        # words=tracknr.split(' ')
                        # track=int(words[0])
                        # for j in range (len(words)-1):
                            # title=title+'-'+words[j+1]
                        
                    # if len(tracknr) ==2:
                        # track = tracknr[0].strip()
                        # line = os.path.dirname(fullline)
                        # albumpath = os.path.split(line)
                        # album = albumpath[len(albumpath)-1]
                        # albumpath = os.path.split(albumpath[0])
                    #support 3 formats
                    # track - title -> len == 2
                    # disk-track - title
                    # track - artist - title
                        # disknr = 0
                        # artist = albumpath[len(albumpath)-1]
                        #title = tracknr[len(tracknr)-1].strip('.mp3')
                        # for j in range (len(tracknr)-1):
                            # title=title+'-'+tracknr[j+1]
                    # if len(tracknr) ==3:
                        #todo find algorythem
                        # for j in range (len(tracknr)-1):
                            # title=title+'-'+tracknr[j+1]
                        
                    # title = title.strip ('.mp3')
                if title == '':
                    title = 'Unknown'
                filename = str(track) +" - " + title +".mp3"
                if artist == '':
                    artist = 'Unknown'
                initial = get_initial(artist)
                file_path = os.path.join(initial,artist,album,filename) 
                newsong=songt('')
                newsong.title = title
                #print(newsong.title)
                newsong.artist = artist
                newsong.album = album
                newsong.track = track
                newsong.disk = disknr
                # print (file_path)
                if mypath == '':
                    newsong.location = fpath
                else:
                    newsong.location = file_path
                self.add(newsong)

                
class songt(object):
    # a song object holds all the meta data of a song
    # it can be initialized by a CVS file exported from itunes
    # I am only interested in a few fields
    # sometimes itunes screws up the location in that case I leave it empty.
    # todo try to repair the location
    # todo normalized and non normalized locations
    # ----------------------------------------------
    # itunes export text converted to excel and exported as csv
    # 0 Name  - Title  
    # 1 Artist  
    # 2 Composer        
    # 3 Album   
    # 4 Grouping        
    # 5 Work    
    # 6 Movement Number 
    # 7 Movement Count  
    # 8 Movement Name   
    # 9 Genre   
    # 10 Size    
    # 11 Time    
    # 12 Disc Number     
    # 13 Disc Count      
    # 14 Track Number    
    # 15 Track Count     
    # 16 Year    
    # 17 Date Modified   
    # 18 Date Added      
    # 19 Bit Rate        
    # 20 Sample Rate     
    # 21 Volume Adjustment       
    # 22 Kind    
    # 23 Equalizer       
    # 24 Comments        
    # 25 Plays   
    # 26 Last Played     
    # 27 Skips   
    # 28 Last Skipped    
    # 29 My Rating       
    # 30 Location          
        def __init__(self,songlist):

            if songlist:
                self.title = ''
                self.artist = ''
                self.composer = ''
                self.album = ''
                self.disk = 0
                self.genre = ''
                self.size = 0
                self.time = 0
                self.disc_nr = 0
                self.disc_cnt = 0
                self.track = 0
                self.track_cnt = 0
                self.year = 0
                self.modified = 0
                self.added = 0
                self.comments = ''
                self.plays = 0
                self.last_played = 0
                self.skips = 0
                self.last_skipped = 0
                self.rating = 0
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
                    #if song2.rating != Fourstar:
                        print(song2.location)
                        return(6)
                    #else:
                        #print(song2.title,song2.artist,'rating')
                        #return (5)
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
def get_initial (artist):
        words = artist.split()
        #print (words)
        if words == '':
           words = "Unknown"
        if any(words[0].upper() == x for x in ('THE','A','DER','DIE')):
                initial = words[1][0].upper()
        else:
                initial = words[0][0].upper()
        return(initial)

def is_available (path,artist,file):
    initial1 = get_initial(artist)
    file1 =  os.path.join(path,artist,file)
    file2 =  os.path.join(path,initial1,artist,file)
    initial2 = artist [0]
    file3 = os.path.join(path,initial2,artist,file)
    #print(file1,file2,file3)
    if os.path.isfile(file1):
        return (file1)
    if os.path.isfile(file2):
        return(file2)
    if os.path.isfile(file3):
        return(file3)
    if initial1 == initial2:
        return ('')
    name = artist.split(' ',1)
    if len(name) > 1:
        artist = name[1]
    else:
        return('')
    if is_available (path,artist,file):
            return (file)
    return ('')

def mkdir_recursive( path):
        try:
                os.makedirs(path)
        except os.error as e:
                if e.errno != errno.EEXIST:
                        raise

def copy(src, dest):
    #print(src)
    #print(dest)
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)

def normalize_tags (input_tag):
    mapping = {ord(u"ü"): u"ue", ord(u"ä"): u"ae", ord(u"ö"): u"oe", ord(u"ß"): u"ss"}
    special_chars='éáàâà\´\’_.,;/:#<>$+%!*`|{}?"\ @\n\''
    k = (b'\xcc\x88').decode('utf-8') # special messed up umlaut
    for invalid in special_chars:
        input_tag = input_tag.replace(invalid,'')
    while '__' in input_tag:
        input_tag = input_tag.replace('__','_')
    while '&' in input_tag:
        input_tag = input_tag.replace('&', 'and')
    #for german_chars in 'üü':
        #input_tag = input_tag.replace(german_chars,'ue')
    input_tag = input_tag.replace (k,'e')
    return input_tag.lower().translate(mapping)

def my_equal(a, b):
    x = normalize_tags(a).strip('_')
    y = normalize_tags(b).strip('_')
    # print ( "compare ", x,'  vs  ',y)
    # return x == y
    if x == y:
        return 1
    else:
        print ( "compare/",x,'/ vs /',y,'/')
        return 0
