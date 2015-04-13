playground
==========
checkplaylist
	takes a playlist
	compares the files in that playlist with a destination path
		file and pathnames are formated from ID tag
		"<inital>/<Artist>/<Album>/<track#> - <Title>"
	creates two new playlist:
		new - files are not in the destination path
		duplicate - files are already there
		
	-s <source path> # where the orignal files are located
	-p <playlist>
	-d <destination path>
	
	if playlist is not specified it defaults to the folder name of the source path
	if destination path is not specified check is made against the source path
	if files in the destination path are not formatted correctlys duplicates may occur
	
CreatePlaylist
	scans the path given recursivly for mp3 files tries to read the tags and creates a playlist on the top level
	
	-s <source path> # where the orignal files are located
	-p <playlist>
	
	if playlist is not specified it defaults to the folder name of the source path
	
CopyPlaylist
	takes a playlist formats the filenames to the standart format and copies them to the destination folder.
	creates a playlist 'new' of the files copied files already in the new destination are ignored
	
	-s <source path> # where the orignal files are located
	-p <playlist>
	-d <destination path>
	