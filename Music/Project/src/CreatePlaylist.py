# check all the file in the path pointed to with the -s option and create a playlist file named with -p
import errno
import glob
import os.path
import shutil
import sys, getopt

from cvstest import myplaylist
from cvstest import basedir
from cvstest import copy
from cvstest import get_initial

playlist = ''
source_path = ''
dest_path =''
fixit = 0
try:
    #print (sys.argv)
    myoptions, myargs = getopt.getopt(sys.argv[1:],"p:s:d:a:f")
except getopt.GetoptError as e:
    print (str(e))
    print("Usage: %s -s" % sys.argv[0])
    sys.exit(2)
for o, a in myoptions:
        if o == '-f':
           fixit = 1
       
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
            #print(playlist)
            if os.path.isdir(playlist):
                print (playlist ,"exists and will be overwritten")
    
if not os.path.isdir(source_path):
    print("Usage: %s -s -p" % sys.argv[0] )
    sys.exit(2)
if playlist == '':
    playlist=os.path.basename(source_path.rstrip('/')) +'.m3u8'
os.chdir(source_path)
#print(source_path)
print("Creating new playlist: ",playlist)
newlist = myplaylist(playlist)
print("Scanning Folder for mp3 files",source_path)
newlist.readFilesTom3u(source_path.rstrip('/'),fixit)
if dest_path != '':
    path = dest_path
    os.chdir(dest_path)
else:
    path = source_path
print("Copy playlist file to disk")
newlist.writem3u8()
print (newlist.maxsongs," Songs have been added to playlist", path,"/",newlist.name)
