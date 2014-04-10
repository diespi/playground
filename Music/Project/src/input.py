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

def is_available (path,artist,file):
    initial1 = get_initial(artist)
    file1 =  os.path.join(path,artist,file)
    file2 =  os.path.join(path,initial1,artist,file)
    initial2 = artist [0]
    file3 = os.path.join(path,initial2,artist,file)
    if os.path.isfile(file1):
        return (file1)
    if os.path.isfile(file2):
        return(file2)
    if os.path.isfile(file3):
        return(file3)
    
    name = artist.split(' ',1)
    if len(name) > 1:
        artist = name[1]
    else:
        return('')
    if is_available (path,artist,file):
            return (file)
    return ('')

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


if cmd in ('create','copy', 'compare', 'check'): 
    
    playlist = ''
    source_path = ''
    dest_path =''
    
    for o, a in myoptions:
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
from cvstest import basedir

if cmd == 'check':
    is_available("The Beatles",basedir)
    sys.exit(1)
    

if cmd == 'create' or cmd == 'copy':
    if playlist != '':
        newlist = myplaylist(playlist)
        destlist = myplaylist(playlist +"copy")
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
        destlist.add(song)
        initial = get_initial(song.artist)
        #print(initial, song.artist)
        filename = song.track +" -" + song.title +".mp3"
        file_path = os.path.join(song.album,filename)
        
        file = is_available(dest_path,song.artist,file_path)
        if file != '':
            song.location = file
            continue
            #print (file, "aleady exists")
        else:
            # dest_path is root
            # need a subfolder with initial
            # need to create artist/ablbum
            # and copy filename
            
            file_path = os.path.join(dest_path,initial,song.artist,song.album)
            mkdir_recursive(file_path)
            filename = os.path.join(file_path,filename)
            copy(song.location,filename)
            song.location = filename
    destlist.writemu3()
            
       
        
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
