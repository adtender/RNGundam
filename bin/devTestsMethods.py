import config
import glob
import os

def list_video_files():
    wildcardString = "*/*"
    for _ in range(config.Subfolders):
        wildcardString += "/*"
        
    wildcard = [wildcardString]
    for i in range(config.Subfolders_Deep):
        wildcard.append(wildcard[i] + "/*")

    mediaList = []
    for i in range(len(wildcard)):
        mediaListUnfiltered = glob.glob(config.Media_Location + wildcard[i])
        mediaList += [file for file in mediaListUnfiltered if 
                            ( file.endswith(".mkv") or 
                            file.endswith(".mp4") or
                            file.endswith(".mov") or
                            file.endswith(".avi"))]
    if not os.path.isfile("./data/text/videoFileList.txt"):
        f = open("./data/text/videoFileList.txt", "x")
        f.close()
    f = open("./data/text/videoFileList.txt", "w")
    f.write("")
    f.close()
    f = open("./data/text/videoFileList.txt", "a")
    for i in range(len(mediaList)):
        f.write(str(i) + ": " + mediaList[i] + "\n")
    f.close()
    return "Video file list written to /RNGundam/bin/data/text/videoFileList.txt"