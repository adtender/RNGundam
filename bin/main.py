import os
import sys
import screenshot
import tweetMedia
import config

# TODO: 
# Fix error 413 on linux (fixed?)
# Fix gif outside time limit
# remake code to no longer use itsoffset (done on hdmv)
# make videos with subtitles generate faster
# add select certain video and time within video
# add day checker for special posts
# add top four posts of the month (will require imagemagick)
        
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
        tweetLink = tweet.set(media, arg)
        print(tweetLink)
        media.db_append(tweetLink)

if __name__ == "__main__":
    main(sys.argv)