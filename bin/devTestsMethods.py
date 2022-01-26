import config
import glob
import os
import sqlite3
import pandas as pd

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

def drop_table():
    conn = sqlite3.connect(config.Text_Location + 'history.db')
    cursor = conn.cursor()
    table = "DROP TABLE HISTORY"
    cursor.execute(table)
    conn.commit()
    conn.close()

def db_to_xlsx():
    x = sqlite3.connect(config.Text_Location + 'history.db')
    df = pd.read_sql_query("SELECT * FROM HISTORY", x)
    x.commit()
    x.close
    #print(df.to_string())
    df.to_excel(config.Text_Location + "history.xlsx")