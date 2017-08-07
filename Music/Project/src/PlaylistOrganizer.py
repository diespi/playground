#!/usr/local/bin/python3
# Tasks:
# - search a folder structure for mp3 files, read the tags and create a 
#   playlist.m3u8 that points to these files. 
# - take a playlist and read tags and fix bad and broken ones.
# - take a folder and read tags and fix bad and broken ones.
# - take a playlist and check against a destination folder 
#   identify duplicates and missings files
# - take a playlist and check against another playlist 
#   identify duplicates and missings files
# - normalize a playlist for default layout. Filter special characters
#   convert windows originated. If creating filenames from tags there are
#   few limitation on allowed characters. Windows has lots of limitations.
#   ignore upper/lower case to be compatible with windows.  
# - take a playlist and copy files to a given folder. Create a playlist of
#   copied files, duplicate files

import errno
import glob
import os.path
import shutil
import sys, getopt
import re
from cvstest import myplaylist
from cvstest import basedir
from cvstest import copy
from cvstest import get_initial
from cvstest import is_available
from cvstest import mkdir_recursive
from cvstest import normalize_tags
from cvstest import my_equal
playlist = ''
source_path = ''
dest_path =''
fixit = 0
command = ''
    
try:
    #print (sys.argv)
    myoptions, myargs = getopt.getopt(sys.argv[1:],"p:r:s:d:a:c:fv")
except getopt.GetoptError as e:
    print (str(e))
    print("Usage: %s -s" % sys.argv[0])
    sys.exit(2)
for o, a in myoptions:
        # flag to turn on tag rewrite
        if o == '-f':
           fixit = 1
        # flag to turn on tag rewrite
        if o == '-v':
           verbose = 1
        # folder pointing to the source of the music folder or where 
        # the source playlists can be found
        if o == '-s':
            if a != '':
                source_path = a
            else:
                source_path=input('Path to source folder? ')
            if not os.path.isdir(source_path):
                print ("path: ",source_path," not found")
                print("Usage: %s -s -d" % sys.argv[0],a )
                sys.exit(2)
        # target folder to place results
        if o == '-d':
            if a != '':
                dest_path =a
            else:
                dest_path=input('Path to destination folder? ')
            if not os.path.isdir(dest_path):
                print ("path: ",dest_path," not found")
                print("Usage: %s -s -d" % sys.argv[0],a )
                sys.exit(2)
        # name of the the source playlist dafault is folder.m3u8
        if o == '-p':
            playlist = a
            #print(playlist)
        # name of the the target playlist default is folder.m3u8
        if o == '-r':
            target = a
            #print(target)

        if o == '-c':
            command = a

# find mp3 files and create a native playlist
if command == '1':
    print('Reading files from ', source_path ,' into new playlist ',playlist)
    os.chdir(source_path)
    newlist = myplaylist(playlist)
    newlist.readFilesTom3u(source_path.rstrip('/'),fixit)
    if dest_path != '':
        path = dest_path
        os.chdir(dest_path)
    else:
        path = source_path
    print("Copy playlist file to disk")
    newlist.writem3u8('')
    print (newlist.maxsongs," Songs have been added to playlist", path,"/",newlist.name)

# use a playlist an copy the files to the target directory
if command == '2':
    newlist = myplaylist(playlist)
    destlist = myplaylist('new.m3u8')
    duplist = myplaylist('duplicate.m3u8')

    os.chdir(source_path)
    newlist.checkmu3('')
    for song in newlist.songlist:
        # normalize and remove all invalid charactes
        song.title=song.title.replace('/',' ')
        if song.artist == '':
            song.artist = 'Unknown'
        initial = get_initial(song.artist)
        filename = str(song.track) +" - " + song.title +".mp3"
        file_path = os.path.join(song.album,filename.strip('/'))

        file = is_available(dest_path,song.artist,file_path)
        if file != '':
            duplist.add(song)
            continue
                #print (file, "aleady exists")
        else:
            destlist.add(song)
            file_path = os.path.join(dest_path,initial,song.artist,song.album)
            filename = os.path.join(file_path,filename)
            print("new",filename)
            mkdir_recursive(file_path)
            copy(song.location,filename)
            song.location = filename
    destlist.writem3u8('')
    duplist.writem3u8('')
    print (destlist.maxsongs," Songs have been copied -ckeck playlist", destlist.name)
    print (duplist.maxsongs," Songs have not been copied -ckeck playlist", duplist.name)
# use any playlist and normalze it. Strip absolute path and add default directory structure
if command == '3':
    oldlist = myplaylist(playlist)
    os.chdir(source_path)
    oldlist.checkmu3(source_path)
    base_name = playlist.split('.')[0]
    print(base_name)
    oldlist.writem3u8(base_name +'.normalized.m3u8')
# compare a playlist against another playlist 
if command == '4':
    srclist    = myplaylist(playlist)
    destlist   = myplaylist(target)
    full_list   = myplaylist('full_list.m3u8')
    no_match_list = myplaylist('no_match_list.m3u8')
    partial_list = myplaylist('partial_list.m3u8')

    os.chdir(source_path)
    srclist.checkmu3('')
    print (srclist.maxsongs," Songs have been added to playlist", source_path,"/",srclist.name)
    os.chdir(dest_path)
    destlist.checkmu3('')
    print (destlist.maxsongs," Songs have been added to playlist", dest_path,"/",destlist.name)

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
        song.artist =  song.artist.lower()
        for current_song in destlist.songlist:
          if my_equal (song.title, current_song.title):
            current_song.artist = current_song.artist.lower()
            al = song.artist.split()
            if al[0] == 'the':
                song.artist = song.artist.replace('the ','')
            al = current_song.artist.split()
            if al[0] == 'the':
                current_song.artist = current_song.artist.replace('the ','')
            if my_equal (song.artist , current_song.artist):
              if my_equal (song.album, current_song.album):
                 #print ("full match ",current_song.location)
                 full_list.add(current_song)
                 found = 'full'
                 break
              else:
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

if command == "5":
    print ("to do")
# read a playlist of folder check if 
# tag.title 
# tag.artist 
# tag.album 
# matching the folder/filenames.
# in some cases the tags contain characters that are not allowed as file/derectory names
# especially windows has a lot of restrictions.
# if we compare a song against a folder there is a mismatch due to unsupported characters.
# if we want to save tags to a file we run into OS errors.
# if we share between windows and mac we need to avoid upper lower case comparision
# also '/' verses '\' has to be addressed.
# goal is to convert tag fields to a generic form on the fly for comparison
# replace offending characters in the tags 
# make sure tag and filename match.
# it should be possible to find a song by reading the filename and scanning tags
# it should be possibel th find a song by reading a tag and searching a folder
# in addition copy the files to a NAS will create other limitations. 
# lenght of the name can become an issue 
# typical pain chars
#     "pound" -> "#",
#     "left angle bracket" -> "<",
#     "dollar sign" -> "$",
#     "plus sign" -> "+",
#     "percent" -> "%",
#     "right angle bracket" -> ">",
#     "exclamation point" -> "!",
#     "backtick" -> "`",
#     "ampersand" -> "&",
#     "asterisk" -> "*",
#     "single quotes" -> "“",
#     "pipe" -> "|",
#     "left bracket" -> "{",
#     "question mark" -> "?",
#     "double quotes" -> "”",
#     "equal sign" -> "=",
#     "right bracket" -> "}",
#     "forward slash" -> "/",
#     "colon" -> ":",
#     "back slash" -> "\",
#     "blank spaces" -> " ",
#     "at sign" -> "@"
# "&" versus "and"


