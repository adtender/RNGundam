import os
import sys
import screenshot
import tweetMedia
import config

# TODO: 
# Fix error 413 on linux (fixed?)
# Fix gif outside time limit
# remake code to no longer use itsoffset (done on hdmv)
# frame selection is not accuracte, rounds down to nearest second
# hdmv subtitles are not centered for zeta gundam (form factor problem?)
# make videos with subtitles generate faster
# add day checker for special posts
# add top four posts of the month (will require imagemagick)
# Find a way to resize gif without rerendering (cutting frames?)
# Index 395 and 396 are generating gifs twice, once with no subs then another with ass AND on not shown index
        
def main(arg):

    for _ in range(6):
        if (len(arg) <= 6):
            arg.append("")

    if(os.path.isdir(config.Media_Location) == False):
        print("Directory undetected")
        
    else:
        tweet = tweetMedia.TWEET()
        media = screenshot.SCREENSHOT()

        media.delete_files()
        media.select_video(arg)
        media.print_info()
        media.ffmpeg_work(arg)
        tweetLink = tweet.set(media, arg)
        print(tweetLink)
        media.db_append(tweetLink)

        print(arg)
    
def link(arg):
    # . 'main.py', 
    # 0 addtional text, 
    # 1 index, 
    # 2 frame, 
    # 3 imageOrGif, 
    # 4  gifLength, 
    # 5  subtitleTrack

    arg.insert(0, 'main.py')
    main(arg)

if __name__ == "__main__":
    main(sys.argv)