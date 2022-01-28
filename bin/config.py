import os
import apiKeys

# Create a new file called apiKeys.py and copy the 4 variables below into it, replacing the values with your API key as a string
# ie within ""
# If you need help with this step, read https://realpython.com/twitter-bot-python-tweepy/#creating-twitter-api-authentication-credentials
API_Key = apiKeys.API_Key
API_Key_Secret = apiKeys.API_Key_Secret
Access_Token = apiKeys.Access_Token
Access_Token_Secret = apiKeys.Access_Token_Secret

# How many folders down should it look
# For example, RNGundam has a parent folder called Gundam with two child folders within, TV and Movies.
#   Within TV and Movies are subfolders named the TV show or the movie corresponding.
#   The video files are within that folder, ie: 2 subfolders
Subfolders = 2

# How many folders deeper should it search from the Subfolders designation.
# Many folders within my collection have "Extras" folders within which I'd like to ignore thus Subfolders_Deep = 0
# If I wanted to include those "Extras" folders, I'd change Subfolders_Deep to 1
Subfolders_Deep = 0

# Location of your videos you will be pulling from
#Media_Location = './videos' # Windows Test from within the RNGundam parent folder
#Media_Location = '\\\\raspberrypi\\RaspberryPi NAS\\media\\plex\\gundam' # Networked Raspberry Pi example
Media_Location = os.path.expanduser('~/usb1/media/plex/gundam')

# Leave these alone
Generated_Media_Location = './data/output/'
Text_Location = './data/text/'
Regeneration_Location = './data/regenerate/'

# Chance for a gif to appear in percentage. RNGundam uses 33, or a 1 in 3 chance approximately for a gif to appear
Chance_Of_GIF = 33

# If a video has a subtitle track that you want to use that is not the default 0
# enter the starting index, the ending index and the track you want to use.
# All this information can be found by generating videoFileList.txt in devTests.py and
# video_file_subtitle_list also in devTests.py
# Shown below is two different shows with indicies from 298-347 and 198-246 which I want to use the subtitle track of 1 for
# If you want to do it for a single video, say subtitle track 3 on index 51, you would enter (51, 52, 3) within the []
# Example:
Switch_Subtitle_Track = [
                            (197, 245, 1),  # Gundam Wing
                            (297, 346, 1),  # Zeta Gundam
                            (543, 591, 0),
                            (592, 616, 0)   # Gundam Build Fighters
                        ]

# How long in seconds to make gifs
# Remember that twitter has a 15mb limit for gifs so a small number is recommended
# I've found that 99.9% of gifs that are 5 seconds long post for me but going up to 7 still works well
GIF_Length = 7

# Tool to regenerate the gif IF it is greater than 15mb. 
# Recommend that you keep this True otherwise nothing will post when it's above the file size cap
GIF_Resize = True

# Change this to the handle of your twitter bot account
Twitter_Account = "RNGundamTest"