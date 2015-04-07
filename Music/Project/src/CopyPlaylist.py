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
source_path = '/Users/dieter/Music/playlist.m3u'
dest_path ='/Users/dieter/Music-new'

#source_path=input('Path to source folder? ')
#if os.path.isfile(source_path):
#    print (source_path, "exists")
#else:
#    print("Usage: %s -s -d" % sys.argv[0],a )
#    sys.exit(2)
playlist = os.path.basename(source_path)
path=os.path.dirname(source_path)
newlist = myplaylist(playlist)
destlist = myplaylist('new')
print (path)
os.chdir(path)
newlist.checkmu3(source_path)
for song in newlist.songlist:
    song.title=song.title.replace('/',' ')
    initial = get_initial(song.artist)
    filename = str(song.track) +" - " + song.title +".mp3"
    file_path = os.path.join(song.album,filename.strip('/'))
        
    file = is_available(dest_path,song.artist,file_path)
    if file != '':
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
destlist.writemu3()