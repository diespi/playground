#from ID3 import *
#try:
    #id3info = ID3(r'')
    #print (id3info)
    # Change the tags
    #id3info['TITLE'] = "Green Eggs and Ham"
    #id3info['ARTIST'] = "Dr. Seuss"
    #for k, v in id3info.items():
        #print (k, ":", v)
#except InvalidTagError as message:
    #print ("Invalid ID3 tag:", message)
    
    
import stagger
import os
from stagger.id3 import  *
tag = stagger.read_tag(r"C:\Users\Dieter\Music\Amazon MP3\Pink\The Truth About Love [Explicit]\01-03- Try.mp3")
print (tag[TIT2 ])
print (tag.title)
print (tag.artist)
track = str.format('%02d' % tag.track)

print (track)

file_location = r"C:\Users\Dieter\Music\Amazon MP3\Pink\The Truth About Love [Explicit]\01-03- Try.mp3"
def create_rel_path(filename):
    line = os.path.basename(filename)
    folder = os.path.dirname(filename)
    folders = os.path.split(folder)
    folder1 = folders[1]
    folder2 = os.path.split(folders[0])[1]


    rel_path = os.path.join('.',folder1,folder2,line)
    return(rel_path)

print(create_rel_path(file_location))