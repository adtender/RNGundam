import os
import re
import sys
import math
import random
import time
import subprocess
import glob
import config
import devTestsMethods
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
        self.videoNumberSelected = 0
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
        self.subType = ""
    
    def delete_files(self):

        print("Delete files")
        [f.unlink() for f in Path(self.odest).glob("output*") if f.is_file()]
        time.sleep(1)
        ("dest: ", self.odest)
        
    def select_video(self, arg):
        
        print("Select video")
        if not arg[4]:
            if random.randint(1,100) <= config.Chance_Of_GIF:
                self.gifOrNo = True
            else:
                self.gifOrNo = False
        elif arg[4] == "gif":
            self.gifOrNo = True
        elif arg[4] == "image":
            self.gifOrNo = False
        
        mediaList = generateFileList.generate_file_list()
        
        if not arg[2]:
            self.videoNumberSelected = random.randint(0,len(mediaList)-1)
        else:
            self.videoNumberSelected = int(arg[2])
        #self.videoNumberSelected = 500
        self.videoFileSelected = mediaList[self.videoNumberSelected]
        self.videoFileSelectedPath, self.videoFileSelectedFileName = os.path.split(self.videoFileSelected)
        self.videoFileSelectedFileNameNoExtension = os.path.splitext(self.videoFileSelectedFileName)[0]
        cap = cv2.VideoCapture(self.videoFileSelected)
        self.fps = math.ceil(cap.get(cv2.CAP_PROP_FPS))
        self.totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.totalSeconds = round(self.totalFrames/self.fps)
        self.totalTime = strftime("%H:%M:%S", gmtime(self.totalSeconds))
        if not arg[3]:
            self.frameSelected = random.randint(0,self.totalFrames-1)
        else:
            self.frameSelected = int(arg[3])
        self.frameSelectedTime = strftime("%H:%M:%S", gmtime(round(self.frameSelected/self.fps)))
        
        if ((self.frameSelected/self.fps) >= self.totalSeconds - config.GIF_Length): # TODO Fix this
            print("--------------GIF OUTSIDE LIMIT: ROUNDING--------------")
            self.frameSelected = self.frameSelected - round(config.GIF_Length * self.fps)
        
    def print_info(self):
        print("\nVideo file selected:",self.videoFileSelectedFileNameNoExtension)
        print("Duration in clock format", self.totalTime)
        print("Total amount of frames:",self.totalFrames)
        print("Random frame selected in clock format:",self.frameSelectedTime)
        print("Random frame selected:",self.frameSelected)
        print("Gif or no: ", self.gifOrNo)
        print("Frame rate:", self.fps)
        print("Amount of time in seconds: ", self.totalSeconds)
        print("Video index: ", self.videoNumberSelected)
           
    def ffmpeg_work(self, arg):

        if arg[5]:
            config.GIF_Length = int(arg[5])/int(self.fps)

        def no_subs():
            self.no_subtitles(secondToStart, config.GIF_Length)
            if self.gifOrNo and config.GIF_Resize: 
                self.resize_gif(False, secondToStart, None, config.GIF_Length, "")
        
        secondToStart = self.frameSelected/self.fps
        outputList = devTestsMethods.video_file_subtitle_list([self.videoNumberSelected])

        if (arg[2] and not arg[6]):
            print("No subtitles found")
            no_subs()
        elif not (outputList[0]):
            print("No subtitles found")
            no_subs()
        else:
            assEng = []
            hdmvEng = []
            for i in range(len(outputList[0])):
                if outputList[0][i][1].find('ass') != -1 and outputList[0][i][1].find('eng') != -1:
                    assEng.append(outputList[0][i][0])
                elif outputList[0][i][1].find('hdmv') != -1 and outputList[0][i][1].find('eng') != -1:
                    hdmvEng.append(outputList[0][i][0])
            print("assEng " + str(assEng))
            print("hdmvEng " + str(hdmvEng))

            index = -1
            subOverwrite = False

            for i in config.Switch_Subtitle_Track:
                if self.videoNumberSelected in range(i[0], i[1]):
                    index = i[2]
                    subOverwrite = True
            if assEng:
                if subOverwrite == False:
                    index = assEng[0]
                
            elif hdmvEng:
                if subOverwrite == False:
                    index = hdmvEng[0]
            #if index == -1:
            #    no_subs()
            if arg[6]:
                index = int(arg[6])
            if outputList[0][index][1].find('ass') != -1:
                self.ass_subtitles(secondToStart, index, config.GIF_Length)
                if self.gifOrNo and config.GIF_Resize: 
                    self.resize_gif(True, secondToStart, index, config.GIF_Length, "ass")
            if outputList[0][index][1].find('hdmv') != -1:
                self.hdmv_pgs_subtitles(secondToStart, index, config.GIF_Length)
                if self.gifOrNo and config.GIF_Resize: 
                    self.resize_gif(True, secondToStart, index, config.GIF_Length, "hdmv")
                
        print(self.videoFileSelectedFileNameNoExtension)
        print(self.frameSelectedTime)

        print ("FFMPEG work done")

    def resize_gif(self, subtitles, secondToStart, indexToSend, gifEnd, subType):
        originalGifEnd = gifEnd
        while (os.path.getsize("{}".format(self.odest + "output.gif")) >= 15728640 and self.gifOrNo == True):
            gifEnd -= 1
            print("Resizing, new time is ", gifEnd, " seconds")
            if subtitles:
                if subType == "ass":
                    self.ass_subtitles(secondToStart, indexToSend, gifEnd)
                elif subType == "hdmv":
                    self.hdmv_pgs_subtitles(secondToStart, indexToSend, gifEnd)
            else:
                self.no_subtitles(secondToStart, gifEnd)
        if gifEnd != originalGifEnd: print("gif resized\nResized gif length: ", gifEnd)

    def no_subtitles(self, secondToStart, gifEnd):
        print("\nNo subtitle gif generation")
        print("v file: ", self.videoFileSelected)
        video = self.windows_check(self.videoFileSelected)
        if self.gifOrNo:
            o = 'ffmpeg -hide_banner -y -ss {} -t {} -i "{}"  -filter_complex "scale=500:-1:flags=lanczos,split [a][b]; [a] palettegen [p]; [b][p] paletteuse" "{}output.gif"'.format(
                    secondToStart, gifEnd, video, self.odest)
        else:
            o = 'ffmpeg -hide_banner -y -ss {} -copyts -i "{}" -vframes 1 "{}output.jpg"'.format(
                    secondToStart, video, self.odest)
        subprocess.check_output(o, shell=True)
        print("\n", o, "\n")
        self.runCommand = o

    def ass_subtitles(self, secondToStart, index, gifEnd):
        print("\nAss subtitle gif generation")
        print("v file: ", self.videoFileSelected)
        video = self.windows_check(self.videoFileSelected)
        if self.gifOrNo:
            assCompile = 'ffmpeg -hide_banner -y -ss {} -t {} -itsoffset {} -i "{}" -vf "subtitles={}:stream_index={},fps={},scale=500:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=255:reserve_transparent=0[p];[s1][p]paletteuse" {}output.gif'.format(
                secondToStart, gifEnd, secondToStart, video, video, index, self.fps, self.odest)
        else:
            assCompile = 'ffmpeg -hide_banner -y -ss {} -copyts -i "{}" -vf subtitles="{}":stream_index={} -frames:v 1 "{}output.jpg"'.format(
                secondToStart, video, video, index, self.odest)
        self.runCommand = assCompile
        subprocess.check_output(assCompile, shell=True)
        print("\n", self.runCommand, "\n")

    def hdmv_pgs_subtitles(self, secondToStart, index, gifEnd):
        print("\nHdmv subtitle gif generation")
        print("v file: ", self.videoFileSelected)
        video = self.windows_check(self.videoFileSelected)
        if self.gifOrNo:
            hdmvCompile = 'ffmpeg -hide_banner -ss {} -t {} -i "{}" -filter_complex "[0:v][0:s:{}] overlay[a];[a] fps={},scale=w=500:h=-2,split [b][c]; [b] palettegen=stats_mode=single [p];[c][p] paletteuse=new=1" "{}output.gif"'.format(
                secondToStart, gifEnd, video, index, self.fps, self.odest)
        else:
            hdmvCompile = 'ffmpeg -hide_banner -y -ss {} -copyts -i "{}" -filter_complex "[0:v][0:s:{}]overlay" -vframes 1 "{}output.jpg"'.format(
                secondToStart, video, index, self.odest)
        self.runCommand = hdmvCompile
        subprocess.call(hdmvCompile,shell=True)
        print("\n", self.runCommand, "\n")

    def windows_check(self, video):
        if os.name == 'nt':
            return video.replace("\\", "/")
        else:
            return video

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
            devTestsMethods.db_to_xlsx()
            return True
            
        except Exception as e:
            return ("db_append error: " + str(e))