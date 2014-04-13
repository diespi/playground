import sys,getopt
#import readline, 
import glob
import os
import errno
import shutil
from cvstest import get_initial,is_available,myplaylist,songs_match






def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

def mkdir_recursive( path):
        try:
                print(path)
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



#readline.set_completer_delims(' \t\n;')
#readline.parse_and_bind("tab: complete")
#readline.set_completer(complete)
try:
    #print (sys.argv)
    myoptions, myargs = getopt.getopt(sys.argv[2:],"p:s:d:a:m:q:")
except getopt.GetoptError as e:
    print (str(e))
    print("Usage: %s -s -d" % sys.argv[0])
    sys.exit(2)
if len(sys.argv) < 2:
    print("Usage:  %s <cmd> -s -d" % sys.argv[0])
    sys.exit(2)
cmd = sys.argv[1]


if cmd in ('create','copy', 'compare', 'check'): 
    
    playlist = ''
    playlistq = ''
    source_path = ''
    dest_path =''
    cmp_mode = ''
    
    for o, a in myoptions:
        if o == '-s':
            if a != '':
                source_path = a
            else:
                source_path=input('Path to source folder? ')
            #if not os.path.isdir(source_path):    
                #print("no such folder: Usage: %s -s -d" % sys.argv[0],a )
                #sys.exit(2)
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
            if os.path.isfile(playlist):
                print (playlist ,"exists and will be overwritten")
        elif o == '-q':
            playlistq = a 
            if os.path.isfile(playlistq):
                print (playlist ,"exists and will be overwritten")
        elif o == '-m':
            cmp_mode = a 
            if not cmp_mode in ('dsk2dsk', 'dsk2plist', 'plist2dsk', 'plist2plist'):
                print ( "please provide a valid mode ")
            if playlist == '' or playlistq =='':
                print ( "please provide a valid playlist names ",playlist,playlistq)
else:
    print("Usage:<command> %s -s -d" % sys.argv[0])
    sys.exit(2)
from cvstest import basedir

if cmd == 'check':
    is_available("The Beatles",basedir)
    sys.exit(1)
    
if cmd == 'compare':
    if cmp_mode =='':
        print ( "please provide a valid mode ")
        sys.exit(2)
    # compare 2 dirs or csvs
    
    
    if cmp_mode in ('dsk2dsk', 'dsk2plist'):
        if source_path == '':
            print ("this operation requires a valid directory")
            sys.exit(2)
        if not os.path.isdir(source_path):
            print ("this operation requires a valid directory")
            sys.exit(2)
        playlista = myplaylist(playlist)
        playlista.readmu3(source_path)
        
        
    if cmp_mode in('dsk2dsk','plist2dsk'):
        if dest_path == '':
            print ("this operation requires a valid directory")
            sys.exit(2)
        if not os.path.isdir(dest_path):
            print ("this operation requires a valid directory")
            sys.exit(2)
        playlistb = myplaylist(playlistq)
        playlistb.readmu3(dest_path)
    
    if cmp_mode in ('plist2plist', 'plist2dsk'):
        if playlist == '':
            print ("this operation requires a valid playlist")
            sys.exit(2)
        if not os.path.isfile(source_path):
            print ("this operation requires a valid path to the cvs file")
            sys.exit(2)
        playlista = myplaylist(playlist)
        playlista.readlist(source_path,playlista)
        
    if cmp_mode in('plist2plist','dsk2plist'):
        if dest_path == '':
            print ("this operation requires a valid playlist")
            sys.exit(2)
        if not os.path.isfile(dest_path):
            print ("this operation requires a valid path to the cvs file")
            sys.exit(2)
    
        playlistb = myplaylist(playlistq)
        playlistb.readlist(dest_path,playlistb)
        
    
    missinga = myplaylist(playlist +"missing")
    missingb = myplaylist(playlistq +"missing")
    
    match = 0
    for songa in playlista.songlist:
        for songb in playlistb.songlist:
            ret = songs_match(songa,songb)
            if  ret == 6:
                #print ("match-a",songa.title,songb.title)
                match =1
                break
            else:
                if ret > 1:
                    print (ret)
        if match == 0:
            missinga.songlist.append(songa)
        else:
            match =0
                #playlista.songlist.remove(songa)

                #playlistb.songlist.remove(songb)
                #print ("song missing",songb.location)
    for songb in playlistb.songlist:
        for songa in playlista.songlist:
            if songs_match(songa,songb) == 6:
                #print ("match-a",songa.title,songb.title)
                match =1
                break
        if match == 0:
            missingb.songlist.append(songb)
        else:
            match =0        
    #playlista.writemu3()
    #playlistb.writemu3()
    missinga.writemu3()
    missingb.writemu3()
    sys.exit()
            
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
        filename = song.track +" - " + song.title +".mp3"
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
            #print ("filepath",file_path)
            mkdir_recursive(file_path)
            filename = os.path.join(file_path,filename)
            #names = os.listdir(song.location )
            #print ("os.listdir",names)
            if os.path.isfile(song.location):
                copy(song.location,filename)
                song.location = filename
            else:
                print ("missing source file :",song.location)
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
