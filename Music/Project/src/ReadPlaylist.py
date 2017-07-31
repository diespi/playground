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
        elif o == '-p':
            playlist = a 
            print(playlist)
            if os.path.isdir(playlist):
                print (playlist ,"exists and will be overwritten")



if playlist == '':
    playlist=os.path.basename(source_path) +'.m3u8'

oldlist = myplaylist(playlist)
full_list = myplaylist('full_list.m3u8')
partial_list = myplaylist('partial_list.m3u8')
title_list = myplaylist('title_list.m3u8')
no_match_list = myplaylist('no_match_list.m3u8')
os.chdir(source_path)
oldlist.checkmu3(source_path)
for song in oldlist.songlist:
    if song.artist == "":
       print (song.location)
       song.artist = 'Unknown'
os.chdir(dest_path)
current_list=myplaylist('current.m3u8')
if os.path.isfile('current.m3u8'):
  print ('checkmu3',dest_path)
  current_list.checkmu3(dest_path)
else:
  print('read files and tags')
  current_list.readFilesTom3u(dest_path.rstrip('/'),0)
for song in oldlist.songlist:
  found = ''
  for current_song in current_list.songlist:
    if song.title == current_song.title:
       if song.artist == current_song.artist:
          if song.album == current_song.album:
             #print ("full match ",current_song.location)
             full_list.add(current_song)
             found = 'full'
             break
          else:
             print (song.album, current_song.album)
             found = 'artist'
             tmp_song = current_song	
          
  if found == '':
    no_match_list.add(song)
  if found == 'artist':
    partial_list.add(tmp_song)
    
    
oldlist.writem3u8()
if os.path.isfile('current.m3u8'):
    print('Keep exiting current.m3u8')
else:
    current_list.writem3u8()
full_list.writem3u8()
partial_list.writem3u8()
title_list.writem3u8()
no_match_list.writem3u8()
