# check if songs from a playlist are  available in the destiantion directory
# source_dir is the folder for the playlist
# if dest-dir is empty we check against source 
# prints the list of songs not in the destination folder
#encoding: utf-8
import errno
import glob
import os
import shutil
import sys, getopt

from cvstest import myplaylist
from cvstest import get_initial
from cvstest import is_available
from macpath import dirname
from pathlib import Path
from cvstest import songs_match

#import readline, 
playlist = ''
source_path = ''
dest_path =''
try:
    #print (sys.argv)
    myoptions, myargs = getopt.getopt(sys.argv[1:],"p:s:d:a:")
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
        elif o == '-p':
            playlist = a 
            print(playlist)
            if os.path.isdir(playlist):
                print (playlist ,"exists and will be overwritten")


if playlist == '':
    playlist=os.path.basename(source_path.rstrip('/')) +'.m3u8'
os.chdir(source_path)
oldlist = myplaylist(playlist)
partduplist = myplaylist('sametitle.m3u8')
duplist = myplaylist('duplicate.m3u8')
oldlist.checkmu3(source_path)
song1=''
for song in oldlist.songlist:
    #print(song.title)
    if song1:
        match = songs_match(song1,song)
        if match == 6:
            # full match
            duplist.add(song1)
            duplist.add(song)
            #print(match,song1.location,song.location)
        if match == 3:
            #title + artist match
            partduplist.add(song1)
            partduplist.add(song)
            #print(match,song1.location,song.location)
        if match == 2:
            #only title match
            print(match,song1.location,song.location)
    song1 =song

duplist.writem3u8()
partduplist.writem3u8()
if duplist.maxsongs >0:
    duplist.writem3u8()
    print (duplist.maxsongs,"Duplcate  Songs have been added to playlist", duplist.name)
if partduplist.maxsongs >0:
    partduplist.writem3u8()
    print (partduplist.maxsongs,"Duplcate  Songs have been added to playlist", partduplist.name)