import errno
import glob
import os
import shutil
import sys, getopt


from cvstest import myplaylist
from cvstest import copy
from cvstest import get_initial
from cvstest import is_available
from macpath import dirname
from pathlib import Path
from cvstest import mkdir_recursive

#import readline, 
playlist = ''
source_path = '/Users/dieter/Music/NewMusic.m3u8'
dest_path ='/Users/dieter/Music-new'
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

#source_path=input('Path to source folder? ')
#if os.path.isfile(source_path):
#    print (source_path, "exists")
#else:
#    print("Usage: %s -s -d" % sys.argv[0],a )
#    sys.exit(2)

newlist = myplaylist(playlist)
destlist = myplaylist('new.m3u8')
duplist = myplaylist('duplicate.m3u8')

os.chdir(source_path)
newlist.checkmu3(source_path)
for song in newlist.songlist:
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
        #print("new",filename) 
        mkdir_recursive(file_path)
        copy(song.location,filename)
        song.location = filename
destlist.writem3u8()
duplist.writem3u8()
print (destlist.maxsongs," Songs have been copied -ckeck playlist", destlist.name)
print (duplist.maxsongs," Songs have not been copied -ckeck playlist", duplist.name)
