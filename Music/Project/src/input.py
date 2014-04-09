import sys,getopt
import readline, glob
import os
import errno

def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

def mkdir_recursive( path):
        try:
                os.makedirs(path)
        except os.error, e:
                if e.errno != errno.EEXIST:
                        raise

def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
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



readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)
try:
    myoptions, myargs = getopt.getopt(sys.argv[1:],"sda:")
except getopt.GetoptError as e:
    print (str(e))
    print("Usage: %s -s -d" % sys.argv[0])
    sys.exit(2)
 
for o, a in myoptions:
    if o == '-s':
        source_path=raw_input('Path to source folder? ')
        if os.path.isdir(source_path):
                print (source_path, "exists")
    elif o == '-d':
        dest_path=raw_input('Path to destination folder? ')
    elif o == '-a':
        artist = a
print(artist)
print (get_initial(artist))


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
