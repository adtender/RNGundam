import devTestsMethods
import sys
# Uncomment line with no space, save and run to run commands

# Output every video file and it's corresponding index to /RNGundam/bin/data/text/videoFileList.txt
#print(devTestsMethods.list_video_files())

# Print video file and it's subtitle tracks + titles
# input the starting index of the first video and ending index of the last
# These are found in videoFileList.txt (generated above)
#devTestsMethods.video_file_subtitle_list(sys.argv)

# Deletes database
#devTestsMethods.drop_table()

# View history database in excel format, output to /RNGundam/bin/data/text/history.xlsx
#devTestsMethods.db_to_xlsx()