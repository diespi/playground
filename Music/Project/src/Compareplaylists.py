# check if songs from a playlist are  available in the destiantion playlist
#encoding: utf-8
import errno
import glob
import os
import shutil
import sys, getopt
import re
from cvstest import myplaylist
from cvstest import get_initial
from cvstest import is_available
from macpath import dirname
from pathlib import Path


#import readline, 
playlist = ''
source_path = ''
dest_path =''
try:
    #print (sys.argv)
    myoptions, myargs = getopt.getopt(sys.argv[1:],"r:p:s:d:a:")
except getopt.GetoptError as e:
    print (str(e))
    print("Usage: %s -s" % sys.argv[0])
    sys.exit(2)
for o, a in myoptions:
        if o == '-s':
            if a != '':
                source_path = a
            else:
                source_path=input('Path to source folder? ')
            if not os.path.isdir(source_path):
                print("Usage: %s -s -d" % sys.argv[0],a )
                sys.exit(2)
        elif o == '-d':
            if a != '':
                dest_path =a
            else:
                dest_path=input('Path to destination folder? ')
        elif o == '-a':
            artist = a
            print(artist)
            print (get_initial(artist))
        elif o == '-r':
            playlist2 = a 
            print(playlist2)
        elif o == '-p':
            playlist1 = a 
            print(playlist)



if playlist1 == '':
     sys.exit(2)
if playlist2 == '':
     sys.exit(2)
if dest_path == '':
    dest_path = source_path 

srclist    = myplaylist(playlist1)
destlist   = myplaylist(playlist2)
matchall   = myplaylist('matchall.m3u8')
matchartist = myplaylist('matchartist.m3u8')
matchtitle = myplaylist('matchtitle.m3u8')

os.chdir(source_path)
srclist.checkmu3(source_path)
print (srclist.maxsongs," Songs have been added to playlist", source_path,"/",srclist.name)

os.chdir(dest_path)
destlist.checkmu3(dest_path)
print (destlist.maxsongs," Songs have been added to playlist", dest_path,"/",destlist.name)

for song in srclist.songlist:
    song.artist = re.sub('[^a-zA-Z0-9öäüÖÄÜß \n\.\-\'\(\)\[\]\{\}\,\&\$\!\+]', '',song.artist).title()
    song.album  = re.sub('[^a-zA-Z0-9öäüÖÄÜß \n\.\-\'\(\)\[\]\{\}\,\&\$\!\+]', '',song.album).title()
    song.title  = re.sub('[^a-zA-Z0-9öäüÖÄÜß \n\.\-\'\(\)\[\]\{\}\,\&\$\!\+]', '',song.title).title()
    if song.artist == "":
       song.artist = 'Unknown'
    if song.album == "":
       song.album = 'Unknown'
    if song.title == "":
       song.title = 'Unknown'
    
for song in destlist.songlist:
    song.artist = re.sub('[^a-zA-Z0-9öäüÖÄÜß \n\.\-\'\(\)\[\]\{\}\,\&\$\!\+]', '',song.artist).title()
    song.album  = re.sub('[^a-zA-Z0-9öäüÖÄÜß \n\.\-\'\(\)\[\]\{\}\,\&\$\!\+]', '',song.album).title()
    song.title  = re.sub('[^a-zA-Z0-9öäüÖÄÜß \n\.\-\'\(\)\[\]\{\}\,\&\$\!\+]', '',song.title).title()
    if song.artist == "":
       song.artist = 'Unknown'
    if song.album == "":
       song.album = 'Unknown'
    if song.title == "":
       song.title = 'Unknown'

for song in srclist.songlist:    
    for song2 in destlist.songlist:
        if song.title == song2.tile:
            if song.artist == song2.artist:
                if song.album == song2.album:
                    matchall.add(song2)
                else:
                    matchartist.add(song2)
            else:
                matchtitle.add(song2)
            if not os.path.isfile(song2.location):
                if not os.path.isfile(song.location):
                    print ("song's missing",song2.location)
                else:
                    print ("song's only in source location",song.location)

matchall.writem3u8()
matchartist.writem3u8()
matchtitle.writem3u8()
print (matchall.maxsongs," Songs have been added to playlist", dest_path,"/",matchall.name)
print (matchartist.maxsongs," Songs have been added to playlist", dest_path,"/",matchartist.name)
print (matchtitle.maxsongs," Songs have been added to playlist", dest_path,"/",matchtitle.name)
