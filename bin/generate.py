import sys
import math
import cv2
from main import link
import devTestsMethods
import generateFileList

def main(arg):

    def get_seconds(time_str):
        hh, mm, ss = time_str.split(':')
        return int(hh) * 3600 + int(mm) * 60 + int(ss)


    videoIndex = input(
        "\n\tVideo file [index]\n" + 
        "(generated in devTests.py and output in\n"+
        "/RNGundam/bin/data/text/videoFileList.txt): \t")
    
    mediaList = generateFileList.generate_file_list()
    cap = cv2.VideoCapture(mediaList[int(videoIndex)])
    fps = math.ceil(cap.get(cv2.CAP_PROP_FPS))

    framesOrSeconds = input(
        "\n[Seconds] or [frame] format: \t\t\t").lower()
    timestamp = ""
    
    if (framesOrSeconds == "seconds"):
        timestamp = get_seconds(input(
            "\n[Timestamp] (00:00:00 format): \t\t\t")) * fps
    elif (framesOrSeconds == "frame"):
        timestamp = input(
            "\n[Timestamp]: \t\t\t\t\t")

    imageOrGif = input(
        "\n[Image] or [gif]: \t\t\t\t").lower()
    if (imageOrGif == "gif"):
        framesOrSecondsGif = input(
            "\ngif in [seconds] or [frame] format: \t\t").lower()
        if (framesOrSecondsGif == "seconds"):
            gifLength = int(input(
                "\n[Length] of gif: \t\t\t\t")) * fps
        elif (framesOrSecondsGif == "frame"): 
            gifLength = input(
                "\n[Length] of gif: \t\t\t\t")
    else:
        gifLength = 0

    print("Generating subtitle tracks: ")
    devTestsMethods.video_file_subtitle_list(["", videoIndex, videoIndex])
    subtitleTrack = input(
        "\nSubtitle [track]"+
        "\n(Enter for no subtitles): \t\t\t")

    postText = input(
        "\nAdd [additional text] to post\n" +
        "(Enter if undesired):\t\t\t\t")

    postNow = input(
        "\nPost to twitter now (y/n): \t\t\t").lower()
    if postNow == 'n':
        postNext = input(
            "\nPost to twitter in next interval (y/n): \t").lower()
    
    link([postText, videoIndex, timestamp, imageOrGif, gifLength, subtitleTrack])

    # . 'main.py', 
    # 0 addtional text, 
    # 1 index, 
    # 2 frame, 
    # 3 imageOrGif, 
    # 4  ^(gifLength), 
    # 5  ^(subtitleTrack)

if __name__ == "__main__":
    main(sys.argv)