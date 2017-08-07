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
full_list   = myplaylist('full_list.m3u8')
no_match_list = myplaylist('no_match_list.m3u8')
partial_list = myplaylist('partial_list.m3u8')

os.chdir(source_path)
srclist.checkmu3(source_path)
print (srclist.maxsongs," Songs have been added to playlist", source_path,"/",srclist.name)
srclist.writem3u8('')
os.chdir(dest_path)
destlist.checkmu3(dest_path)
print (destlist.maxsongs," Songs have been added to playlist", dest_path,"/",destlist.name)
destlist.writem3u8('')
import string
def equal(a, b):
    x = re.sub('[^a-zA-Z0-9öäüÖÄÜß\n\(\)\[\]\{\}\,\&\$\!\+]', '', a).title()
    y = re.sub('[^a-zA-Z0-9öäüÖÄÜß\n\(\)\[\]\{\}\,\&\$\!\+]', '', b).title()
    try:
        return x.lower() == y.lower()
    except AttributeError:
        return x == y

for song in srclist.songlist:
    if song.artist == "":
       print ('artist:',song.location)
       song.artist = 'Unknown'
    if song.album == "":
       print ('album:',song.location)
       song.album = 'Unknown'
    if song.title == "":
       print ('title:',song.location)
       song.title = 'Unknown'
os.chdir(dest_path)
for song in srclist.songlist:
    found = ''
    for current_song in destlist.songlist:
      if equal (song.title, current_song.title):
        if equal (song.artist , current_song.artist):
          if equal (song.album, current_song.album):
             #print ("full match ",current_song.location)
             full_list.add(current_song)
             found = 'full'
             break
          else:
            if song.artist == 'Ellie Goulding':
              print (song.album, current_song.album)
            found = 'artist'
            tmp_song = current_song

    if found == '':
      no_match_list.add(song)
    if found == 'artist':
      partial_list.add(tmp_song)




full_list.writem3u8('')
partial_list.writem3u8('')
no_match_list.writem3u8('')
print (full_list.maxsongs," Songs have been added to playlist", dest_path,"/",full_list.name)
print (partial_list.maxsongs," Songs have been added to playlist", dest_path,"/",partial_list.name)
print (no_match_list.maxsongs," Songs have been added to playlist", dest_path,"/",no_match_list.name)
