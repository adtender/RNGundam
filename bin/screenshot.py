import os
import re
import sys
import math
import random
import time
import subprocess
import glob
import config
import generateFileList
import cv2
import sqlite3
import datetime
import hashlib
from re import A, match
from time import gmtime, strftime
from pathlib import Path

class SCREENSHOT:
    
    def __init__(self) -> None:
        self.odest = config.Generated_Media_Location
        self.videoNumberSelected = 243 # change to zero before committing
        self.videoFileSelected = ""
        self.videoFileSelectedPath = ""
        self.videoFileSelectedFileName = ""
        self.videoFileSelectedFileNameNoExtension = ""
        self.totalFrames = ""
        self.totalSeconds = ""
        self.totalTime = ""
        self.frameSelected = ""
        self.frameSelectedTime = ""
        self.fps = ""
        self.gifOrNo = ""
        self.runCommand = ""
    
    def delete_files(self):

        print("Delete files")
        [f.unlink() for f in Path(self.odest).glob("output*") if f.is_file()]
        time.sleep(1)
        ("dest: ", self.odest)
        
    def select_video(self):
        
        # Within config.py, set variable Chance_Of_GIF to an interger of a percentage
        # For example Chance_Of_GIF = 33 is a 33% or 1/3 chance to choose a gif rather than a static image
        
        print("Select video")
        if random.randint(1,100) <= config.Chance_Of_GIF:
            self.gifOrNo = True
        else:
            self.gifOrNo = False
        
        mediaList = generateFileList.generate_file_list()
        
        self.videoNumberSelected = random.randint(0,len(mediaList)-1)
        #self.videoNumberSelected = 308
        self.videoFileSelected = mediaList[self.videoNumberSelected]
        self.videoFileSelectedPath, self.videoFileSelectedFileName = os.path.split(self.videoFileSelected)
        self.videoFileSelectedFileNameNoExtension = os.path.splitext(self.videoFileSelectedFileName)[0]
        cap = cv2.VideoCapture(self.videoFileSelected)
        self.fps = math.ceil(cap.get(cv2.CAP_PROP_FPS))
        self.totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.totalSeconds = round(self.totalFrames/self.fps)
        self.totalTime = strftime("%H:%M:%S", gmtime(self.totalSeconds))
        self.frameSelected = random.randint(0,self.totalFrames-1)
        self.frameSelectedTime = strftime("%H:%M:%S", gmtime(round(self.frameSelected/self.fps)))
        
        if ((self.frameSelected/self.fps) >= self.totalSeconds - config.GIF_Length): # TODO Fix this
            print("--------------GIF OUTSIDE LIMIT: ROUNDING--------------")
            self.frameSelected = self.frameSelected - round(config.GIF_Length * self.fps)
            
        #for (i, item) in enumerate(mediaList, start=1): # print all video files and their index
        #    print(i, item)
        
    def print_info(self):
        print("\nVideo file selected:",self.videoFileSelectedFileNameNoExtension)
        print("Duration in clock format", self.totalTime)
        print("Total amount of frames:",self.totalFrames)
        print("Random frame selected in clock format:",self.frameSelectedTime)
        print("Random frame selected:",self.frameSelected)
        print("Gif or no: ", self.gifOrNo)
        print("Frame rate:", self.fps)
        print("Amount of time in seconds: ", self.totalSeconds)
        
        
    def ffmpeg_work(self):

        # Output the subtitle streams
        if os.name == 'nt': # Windows
            x = 'ffprobe -i "{}" -show_streams -select_streams s 2>&1| findstr /r "Stream.*#0:.*:.*Subtitle:"'.format(self.videoFileSelected) 
        else: # Linux
            x = 'ffprobe -i "{}" -show_streams -select_streams s 2>&1| grep ".*Stream.*#0:.*:.*Subtitle:.*"'.format(self.videoFileSelected)
        subError = False
        
        secondToStart = self.frameSelected/self.fps
        firstSubtitleStreamNumber = ""
        
        # Checks if the video file has subtitles

        try:
            subCheck = subprocess.check_output(x,shell=True).decode(sys.stdout.encoding)
            print("Sub check", subCheck)
            subLangCheck = subCheck.splitlines()
            #firstSubtitleStreamNumber = self.stream_number(subLangCheck)
        except Exception as e:
            print("Error: ", e)
            print("No subtitles found")
            subError = True
            self.no_subtitles(secondToStart, config.GIF_Length)
            if self.gifOrNo and config.GIF_Resize: self.resize_gif(False, secondToStart, None, config.GIF_Length)
            print("No subtitles found")
            
        if (subError == False): # Checks for English subtitles
            firstSubtitleStreamNumber = self.stream_number(subLangCheck)
            r = re.compile(".*[(]eng[)].*")
            subLangEng = list(filter(r.match, subLangCheck))
            if (not subLangEng):
                r = re.compile(".*Stream.*#0:.\:.*") # Search for streams with no language tags
                subLangEng = list(filter(r.match, subLangCheck))
                if (not subLangEng): 
                    r = re.compile(".*Subtitle.*") # On failure of finding English subtitles, creates a list with the rest
                    subLangEng = list(filter(r.match, subLangCheck))
            
            assR = re.compile(".*Subtitle:.*ass.*")
            assSearch = list(filter(assR.match, subLangEng))
            hdmvR = re.compile(".*Subtitle:.*hdmv.*")
            hdmvSearch = list(filter(hdmvR.match, subLangEng))
            assStream = self.stream_adjust(self.stream_number(assSearch), firstSubtitleStreamNumber[0])
            hdmvStream = self.stream_adjust(self.stream_number(hdmvSearch), firstSubtitleStreamNumber[0]) # hdmv_PGS subtitles aren't currently working, may use this later when I've figured it out
            print("sub lang eng", subLangEng, "\nass stream", assStream)
            if assStream:
                print("ass")
                print(self.videoFileSelected)
                index = 0
                if "Wing." in self.videoFileSelectedFileNameNoExtension:
                    index = 1
                indexToSend = assStream[index]
                self.ass_subtitles(secondToStart, indexToSend, config.GIF_Length)
                if self.gifOrNo and config.GIF_Resize: self.resize_gif(True, secondToStart, indexToSend, config.GIF_Length)
                
            else:
                print("hdmv")
                print(hdmvStream[0])
                self.hdmv_pgs_subtitles(secondToStart, hdmvStream[0], config.GIF_Length)
                if self.gifOrNo and config.GIF_Resize: self.resize_gif(False, secondToStart, None, config.GIF_Length)
                
        print(self.videoFileSelectedFileNameNoExtension)
        print(self.frameSelectedTime)

        print ("FFMPEG work done")

    def resize_gif(self, subtitles, secondToStart, indexToSend, gifEnd):
        originalGifEnd = gifEnd
        while (os.path.getsize("{}".format(self.odest + "output.gif")) >= 15728640 and self.gifOrNo == True):
            gifEnd -= 1
            if subtitles:
                self.ass_subtitles(secondToStart, indexToSend, gifEnd)
            else:
                self.no_subtitles(secondToStart, gifEnd)
        if gifEnd != originalGifEnd: print("gif resized\nResized gif length: ", gifEnd)

    def no_subtitles(self, secondToStart, gifEnd):
        video = self.windows_check(self.videoFileSelected)
        if self.gifOrNo:
            o = 'ffmpeg -hide_banner -loglevel error -y -ss {} -t {} -i "{}"  -filter_complex "scale=500:-1:flags=lanczos,split [a][b]; [a] palettegen [p]; [b][p] paletteuse" "{}output.gif"'.format(
                    secondToStart, gifEnd, video, self.odest)
        else:
            o = 'ffmpeg -hide_banner -loglevel error -y -ss {} -copyts -i "{}" -vframes 1 "{}output.jpg"'.format(
                    secondToStart, video, self.odest)
        subprocess.check_output(o, shell=True)
        print("\n", o, "\n")
        self.runCommand = o

    def ass_subtitles(self, secondToStart, index, gifEnd):
        print("v file: ", self.videoFileSelected)
        video = self.windows_check(self.videoFileSelected)
        if self.gifOrNo:
            assCompile = 'ffmpeg -hide_banner -loglevel error -y -ss {} -t {} -itsoffset {} -i "{}" -vf "subtitles={},fps={},scale=500:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=255:reserve_transparent=0[p];[s1][p]paletteuse" {}output.gif'.format(
                secondToStart, gifEnd, secondToStart, video, video, self.fps, self.odest)
        else:
            assCompile = 'ffmpeg -hide_banner -loglevel error -y -ss {} -copyts -i "{}" -vf subtitles="{}":stream_index={} -frames:v 1 "{}output.jpg"'.format(
                secondToStart, video, video, index, self.odest)
        self.runCommand = assCompile
        subprocess.check_output(assCompile, shell=True)

    def hdmv_pgs_subtitles(self, secondToStart, index, gifEnd):
        print("v file: ", self.videoFileSelected)
        video = self.windows_check(self.videoFileSelected)
        if self.gifOrNo:
            hdmvCompile = 'ffmpeg -hide_banner -loglevel error -ss {} -t {} -i "{}" -filter_complex "[0:v][0:s:{}] overlay[a];[a] fps={},scale=w=500:h=-2,split [b][c]; [b] palettegen=stats_mode=single [p];[c][p] paletteuse=new=1" "{}output.gif"'.format(
                secondToStart, gifEnd, video, index, self.fps, self.odest)
        else:
            hdmvCompile = 'ffmpeg -hide_banner -loglevel error -y -ss {} -copyts -i "{}" -filter_complex "[0:v][0:s:{}]overlay" -vframes 1 "{}output.jpg"'.format(
                secondToStart, video, index, self.odest)

        print(hdmvCompile)
        self.runCommand = hdmvCompile
        subprocess.call(hdmvCompile,shell=True)

    def windows_check(self, video):
        if os.name == 'nt':
            return video.replace("\\", "/")
        else:
            return video

    def stream_number(self, x):
        array = []
        for i in range(len(x)):
            m = re.search('Stream #0:\d*', x[i])
            n = re.search('\d*$', m.group(0))
            array.append(n.group(0))
        return array

    def stream_adjust(self, x, base):
        for i in range(len(x)):
            x[i] = abs(int(base) - int(x[i]))
        return x

    def db_append(self, tweetLink):
        file_type = "output."
        if self.gifOrNo:
            file_type += "gif"
        else:
            file_type += "jpg"
        try:
            md5_hash = hashlib.md5()
            a_file = open(config.Generated_Media_Location + file_type, "rb")
            content = a_file.read()
            md5_hash.update(content)
            hash = md5_hash.hexdigest()

            if os.path.isfile(config.Text_Location + 'history.db'):
                print("True  -------------- DB Detected")
            else:
                print("False -------------- No DB Detected")
            
            conn = sqlite3.connect(config.Text_Location + 'history.db')
            cursor = conn.cursor()
            table = """CREATE TABLE IF NOT EXISTS HISTORY(DATE, TEXTPOST, RUNCOMMAND, LINK, HASHVALUE);"""
            cursor.execute(table)

            '''
            sql = """SELECT count(*) as tot FROM HISTORY"""
            cursor.execute(sql)
            data = cursor.fetchone()[0]
            if (data != 0):
                    last_hash = str(cursor.execute('select HASHVALUE from HISTORY').fetchall()[-1][0])
                    if(last_hash == hash):
                            #logging.error("Duplicate hash")
                            #sys.exit("Duplicate hash: Exiting")
                            print("Duplicate hash: Exiting")
                            return False
            '''
            cursor.execute("insert into HISTORY values(?, ?, ?, ?, ?)",
                            (str(datetime.datetime.now()), 
                            "From " + self.videoFileSelectedFileNameNoExtension + " at " + self.frameSelectedTime,
                            self.runCommand,
                            tweetLink,
                            hash)
                            )
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            return ("db_append error: " + str(e))
