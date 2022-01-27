import config
import generateFileList
import os
import sqlite3
import subprocess
import pandas as pd

def list_video_files():
    mediaList = generateFileList.generate_file_list()
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

def video_file_subtitle_list(arg):
    check = True
    checkIndv = True
    if len(arg) == 3:
        check = True
    else:
        check = False
    if len(arg) == 1:
        checkIndv == True

    def normalize(input):
        output = input.splitlines()
        outputListIndv = []
        for i, j in enumerate(output):
            outputListIndv.append([i, j])
            print (i, j)
        print()
        return(outputListIndv)
        

    def logic(start, end):
        print()
        mediaList = generateFileList.generate_file_list()
        outputList = []
        for x in range(int(start), int(end) + int(1)):
            print(mediaList[x])
            subtitleOutput = 'ffprobe -hide_banner -loglevel error -select_streams s -show_entries stream=codec_name:stream_tags=language,title,codec_name -of compact=p=0:nk=1 "{}"'.format(
                mediaList[x]
            )
            bytes = subprocess.check_output(subtitleOutput, shell=True)
            output = bytes.decode('UTF-8')
            outputList.append(normalize(output))
        return(outputList)

    if check:
        return(logic(int(arg[1]), int(arg[2])))
    elif checkIndv and not arg[0] == 'devTests.py':
        return(logic((arg[0]), (arg[0])))
    else:
        start, end = input("Enter a starting index and an ending index for the videos you'd like to see\n"+
                        "If you don't know which values to enter, press ctrl+c and run list_video_files in devTests.py\n").split()
        return(logic(start, end))

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