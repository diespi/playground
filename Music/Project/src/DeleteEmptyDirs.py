import errno
import glob
import os
import shutil
import sys, getopt
import glob

from cvstest import myplaylist
from cvstest import copy
from cvstest import get_initial
from cvstest import is_available
from macpath import dirname
from pathlib import Path
from cvstest import mkdir_recursive
from os.path import join
#import readline, 
playlist = ''
source_path = ''
dest_path =''
def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))
def remEmptyDir(mypath):
    for root, dirs, files in os.walk(mypath,topdown=False):
        for name in dirs:
         #print ('dir',name)
         fname = join(root,name)
         #print('fname',fname)
         if not os.path.isdir(fname):
             print('rmEmptyDir',fname)
             continue
         if not os.listdir(fname): #to check wither the dir is empty
             #print ('list', item)
             print ('removing ',fname)
             os.removedirs(fname)
         else:
            #print('rmEmptyDir not empty',fname)
            for item in os.listdir(fname):
                if item.startswith('.'):
                    hidden_fname = join(fname,item)
                    print (hidden_fname)
                    os.remove (hidden_fname)
                else:
                    break
            if not os.listdir(fname):
                print('Removing dir ',fname)
                #os.removedirs(fname)
                    
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
path=source_path

print (path)
os.chdir(path)
        
#os.removedirs(path)
remEmptyDir(source_path)
