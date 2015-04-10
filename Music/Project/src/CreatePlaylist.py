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
    
if not os.path.isdir(source_path):
    print("Usage: %s -s -d" % sys.argv[0],a )
    sys.exit(2)
if playlist == '':
    playlist=os.path.basename(source_path) +'.m3u8'
os.chdir(source_path)
newlist = myplaylist(playlist)
newlist.readmu3(source_path)
newlist.writemu3()
#listname = newlist.name + '.m3u'
#fname = os.path.join(basedir,listname)
#if fname != source_path:
#    shutil.move(fname,source_path)