import errno
import glob
import os.path
import shutil
import sys, getopt

from cvstest import myplaylist
from cvstest import basedir
from cvstest import copy

#import readline, 
playlist = 'NewMusic'
source_path = ''
dest_path =''
source_path=input('Path to source folder? ')
if os.path.isdir(source_path):
    print (source_path, "exists")
else:
    print("Usage: %s -s -d" % sys.argv[0],a )
    sys.exit(2)

newlist = myplaylist(playlist)
newlist.readmu3(source_path)
newlist.writemu3()
listname = newlist.name + '.m3u'
fname = os.path.join(basedir,listname)
copy(fname,source_path)