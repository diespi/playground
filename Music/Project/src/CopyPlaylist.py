import errno
import glob
import os
import shutil
import sys, getopt

from cvstest import myplaylist
from macpath import dirname
from pathlib import Path


#import readline, 
playlist = ''
source_path = '/Users/dieter/Music/playlist.m3u'
dest_path =''

#source_path=input('Path to source folder? ')
#if os.path.isfile(source_path):
#    print (source_path, "exists")
#else:
#    print("Usage: %s -s -d" % sys.argv[0],a )
#    sys.exit(2)
playlist = os.path.basename(source_path)
path=os.path.dirname(source_path)
newlist = myplaylist(playlist)
print (path)
os.chdir(path)
newlist.checkmu3(source_path)
