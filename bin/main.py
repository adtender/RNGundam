import os
import sys
import screenshot
import tweetMedia
import config
import sqlite3

# TODO: 
# Fix error 413 on linux (fixed?)
# Fix gif outside time limit
# remake code to no longer use itsoffset (done on hdmv)
# frame selection is accurate on no_subtitles and hdmv, ass is off by nearly 4 seconds on index 297
#   ffprobe -show_entries stream=codec_type,start_time -v 0 -of compact=p=1:nk=0 input.mkv (may help)
#   itsoffset adding delay to ass based subtitles, find way to retime ass subtitles
# hdmv subtitles are not centered for zeta gundam (form factor problem?)
# make videos with subtitles generate faster
# add day checker for special posts
# add check to make sure image being posted lines up with db entry
# add top four posts of the month (will require imagemagick)
# Find a way to resize gif without rerendering (cutting frames?)
# Index 395 and 396 are generating gifs twice, once with no subs then another with ass AND on not shown index

def generate_or_post():
    conn = sqlite3.connect(config.Text_Location + 'history.db')
    cursor = conn.cursor()
    output = ""
    try:
        lastEntry = str(cursor.execute('select LINK from HISTORY').fetchall()[-1][0])
        
        if lastEntry:
            output = False
        else:
            output = True
    except:
        output = False

    conn.close()
    return output
        
def main(arg):

    for _ in range(6):
        if (len(arg) <= 6):
            arg.append("")

    if(os.path.isdir(config.Media_Location) == False):
        print("Directory undetected")
        
    else:
        tweet = tweetMedia.TWEET()
        media = screenshot.SCREENSHOT()

        print(generate_or_post)

        if generate_or_post() == False:
            media.delete_files()
            media.select_video(arg)
            media.print_info()
            media.ffmpeg_work(arg)
            media.db_append("", True)
        else:
            tweetLink = tweet.set(arg)
            print(tweetLink)
            media.db_append(tweetLink, False)

        #print(arg)
    
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