import os
import sys
import screenshot
import tweetMedia
import config

def main(arg):
    
    test_1(arg)
        
def test_1(arg):
    tweet = tweetMedia.TWEET()
    media = screenshot.SCREENSHOT()
    
    media.delete_files()
    media.select_video()
    media.print_info()
    media.ffmpeg_work()
    print(tweet.set(media, arg))
    
def test_2():
    dStatus = ""
    
    tweet = tweetMedia.TWEET()
    media = screenshot.SCREENSHOT()
    #print("Media drive status: ", tweet.media_drive_status())
    
    if(os.path.isdir(config.Media_Location) == False):
        print("Directory undetected")
        
    else:
        print("Directory detected")
        media.delete_files()
        print("test 1")
        media.select_video()
        print("test 2")
        #media.print_info()
        print("test 3")
        media.ffmpeg_work()
        print("test 4")
        dStatus = "Media True"
        sendBack = tweet.overall_checks(media)
        print(sendBack)

if __name__ == "__main__":
    main(sys.argv)