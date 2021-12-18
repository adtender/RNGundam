import os
import sys
import screenshot
import tweetMedia
import config
        
def main(arg):
    if(os.path.isdir(config.Media_Location) == False):
        print("Directory undetected")
        
    else:
        tweet = tweetMedia.TWEET()
        media = screenshot.SCREENSHOT()
        
        media.delete_files()
        media.select_video()
        media.print_info()
        media.ffmpeg_work()
        print(tweet.set(media, arg))

if __name__ == "__main__":
    main(sys.argv)