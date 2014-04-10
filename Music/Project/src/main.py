# cases to cover
# 1. read files from a formatted directory and create a playlist and print
# input folder-path
#       playlist name
#       playlist folder default root of input folder.
#
# 2. read a playlist and check if objects are in the destination folder create a playlist of objects not found
# input folder-path
#       playlist name
# 3. copy files from a playlist to the destination folder
#
# 4. compare 2 playlists
#       create diff lists
# 5. find duplicatessys.exit(2)if a == '':
i=0
j=0
#print ('Number of arguments:', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))


# -------------------------------

# this is just a place holder for junk 
from cvstest import *


#songs = myplaylist(inputfile)
#missinglocation = myplaylist('broken')
allsongs = myplaylist ('ALL')
readlist(listname,allsongs)
#readlist('4 Star.txt',missinglocation)
allsongs.writemu3('ALL')
#print (allsongs.maxsongs,missinglocation.maxsongs )
#for songa in missinglocation.songlist:
    #print (songa.title,songa.artist,songa.album)
    #for songb in allsongs.songlist:
        #result = songs_match (songa,songb)
        #if result == 6 or result == 3:
            #newlist.add (songb)
        #if result == 2 or result == 5:
            ##newlist3.add (songb)
        #if result >1: 
            #print(result)
#newlist.writemu3('new')
#newlist3.writemu3('new3')       
import tkinter as tk
import tkinter.ttk as ttk
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "MY Song"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.QUIT = tk.Button(self, text="QUIT", fg="red",bg ="blue",
                                            command=root.destroy)
        self.QUIT.pack(side="bottom")

       
    def say_hi(self):
        print(allsongs.songlist[0].title)
        

root = tk.Tk()
app = Application(master=root)
app.mainloop()


# split artist and create all permutations to find a song
# e.g. The Beatles
# - /root/The Beatles/
# - / root/Beatles/
# - /root/B/The beatles
# - /root/B/Beatles
# - /root/T/ The Beatles
# - /root/T/Beatles

#for item in broken:
#    print (item)