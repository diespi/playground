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

import myplaylist
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
    playlist=os.path.basename(source_path) +'.m3u8'
if dest_path == '':
    dest_path = source_path 

oldlist = myplaylist(playlist)
newlist = myplaylist('new.m3u8')
duplist = myplaylist('duplicate.m3u8')

os.chdir(source_path)
oldlist.checkmu3(source_path)
for song in oldlist.songlist:
    initial = get_initial(song.artist)
    filename = str(song.track) +" - " + song.title.replace('/',' ') +".mp3"
    file_path = os.path.join(song.album,filename)
        
    file = is_available(dest_path,song.artist,file_path)
    if file != '':
        duplist.add(song)
        continue
            #print (file, "aleady exists")
    else:
        newlist.add(song)
        file_path = os.path.join(dest_path,initial,song.artist,song.album)
        filename = os.path.join(file_path,filename) 
        #print("new",filename.encode('utf-8') ) 
os.chdir(source_path)
newlist.writemu3()
duplist.writemu3()