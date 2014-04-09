import sys,getopt
#import readline, 
import glob
import os
import errno
import shutil
from cvstest import myplaylist




def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

def mkdir_recursive( path):
        try:
                os.makedirs(path)
        except os.error as e:
                if e.errno != errno.EEXIST:
                        raise

def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)

# smart artist:
#       if artist starts with 'The ' 'Die' 'Der' 'Das'
#       if artist starts with 'A '
#       if artist starts with # 10CC TenCC ?? 4 four ...
#               get the inital from the second token
def get_initial (artist):
        words = artist.split()
        if any(words[0].upper() == x for x in ('THE','A','DER','DIE')):
                initial = words[1][0].upper()
        else:
                initial = words[0][0].upper()
        return(initial)



#readline.set_completer_delims(' \t\n;')
#readline.parse_and_bind("tab: complete")
#readline.set_completer(complete)
try:
    myoptions, myargs = getopt.getopt(sys.argv[2:],"p:s:d:a:")
except getopt.GetoptError as e:
    print (str(e))
    print("Usage: %s -s -d" % sys.argv[0])
    sys.exit(2)
cmd = sys.argv[1]
print(sys.argv)

if cmd in ('create','copy', 'compare', 'check'): 
    
    playlist = ''
    source_path = ''
    dest_path =''
    
    for o, a in myoptions:
        print(o,a)
        if o == '-s':
            if a != '':
                source_path = a
            else:
                source_path=input('Path to source folder? ')
            if os.path.isdir(source_path):
                print (source_path, "exists")
            else:
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
else:
    print("Usage:<command> %s -s -d" % sys.argv[0])
    sys.exit(2)

if cmd == 'create' or cmd == 'copy':
    if playlist != '':
        newlist = myplaylist(playlist)
    else:
        print ("playlist name required - use -p <playlist>")
        sys.exit(2)
    if source_path == '':
        print ("this operation requires a valid directory")
        sys.exit(2)
        
    newlist.readmu3(source_path)
    newlist.writemu3()
    if cmd == 'copy':
        if dest_path == '':
            print ("this operation requires a valid directory")
            sys.exit(2)
        if os.path.isdir(dest_path):
            print (dest_path, "exists")
        else:
            print("creating" ,dest_path)
    for song in newlist.songlist:
        initial = get_initial(song.artist)
        #print(initial, song.artist)
        filename = song.track +" -" + song.title +".mp3"
        file_path = os.path.join(dest_path, initial,song.artist,song.album)
        filename = os.path.join(file_path,filename)
        if os.path.isdir(file_path):
            if os.path.isfile(filename):
                print (filename, "aleady exists")
            else:
                copy(song.location,filename)
        else:
            mkdir_recursive(file_path)
            copy(song.location,filename)
            
        #copy(song.location,filepath)
        
# music folder structure:
#       /root_path/%Inital%/%artist%/%album%/%tracknr% - %title%.mp3
#       /root_path/Various/%album%/%track% - %artist% - %title%.mp3
#
#  functions
#  - read a directory with formated mp3 files into a playlist
#    check the files not in the destination folder and create a missing playlist
#    copy the missing files to destination folder
#  - check if a file is in the detination folder

#       strip root_path
#      try dest_path,dest_path/%initial%,dest_path/%artist[0]%/, Various/...
