import os
startpath ="/Users/dieter"
fullpath="/Users/dieter/Music/a/bla/xxx/1-dddd.mp3"
print(fullpath)
rootpath=os.path.dirname(fullpath)
mypath=os.path.basename(fullpath)
while os.path.dirname(rootpath) != startpath:
    rootpath=os.path.dirname(rootpath)
    mypath=os.path.join(os.path.basename(rootpath),mypath)
    print(mypath)
 

