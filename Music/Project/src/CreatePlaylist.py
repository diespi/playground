import errno
import glob
import os
import shutil
import sys, getopt

from cvstest import myplaylist


#import readline, 
playlist = ''
source_path = ''
dest_path =''
newlist = myplaylist('playlist')
source_path=input('Path to source folder? ')
if os.path.isdir(source_path):
    print (source_path, "exists")
else:
    print("Usage: %s -s -d" % sys.argv[0],a )
    sys.exit(2)
newlist.readmu3(source_path)
newlist.writemu3()