import os
import sys
import screenshot
import tweetMedia
import config

# TODO: 
# Fix error 413 on linux
# Fix selecting no subtitle when PGS before ass, use zeta gundam as test
# Add database
# regenerate gifs and images from database
# remake code to no longer use itsoffset (done on hdmv)
# make videos with subtitles generate faster
        
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