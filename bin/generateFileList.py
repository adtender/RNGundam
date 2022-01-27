import config
import glob

def generate_file_list():
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

    return mediaList