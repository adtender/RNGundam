import tweepy
#from TwitterAPI import TwitterAPI
import sqlite3
import hashlib
import logging
import sys
import os

#from tweepy.models import Place
import config
from datetime import datetime

class TWEET:

        def __init__(self):
                self.api_key = config.API_Key
                self.api_key_secret = config.API_Key_Secret
                self.access_token = config.Access_Token
                self.access_token_secret = config.Access_Token_Secret
                self.auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
                self.auth.set_access_token(self.access_token, self.access_token_secret)
                self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
                #self.api = TwitterAPI(self.api_key, self.api_key_secret, self.access_token, self.access_token_secret)
                self.media_location = os.path.expanduser(config.Media_Location)
                self.generated_media_location = os.path.expanduser(config.Generated_Media_Location)

        def tweet_media(self, media, output):
                
            try:

                if len(sys.argv) > 1:
                        #self.api.update_status(status = sys.argv[1] + "\n" + media.videoFileSelectedFileNameNoExtension + " at " + media.frameSelectedTime, media_ids = [pic.media_id_string])
                        #return "Tweet sent. Check Twitter for new content"
                        return "Hello :)"
                else:
                        #self.api.update_with_media(self.generated_media_location + output, media.videoFileSelectedFileNameNoExtension + " at " + media.frameSelectedTime, place_id = "Side 7")
                        #print("Got here")

                        if "gif" in output:
                            print("Attempt to upload gif")
                            upload = self.api.media_upload(filename = self.generated_media_location + output, 
                                chunked = True, 
                                media_category = "tweet_gif")
                            #self.api.update_status("From " + media.videoFileSelectedFileNameNoExtension + " at " + media.frameSelectedTime, 
                            #    media_ids=[upload.media_id_string])
                            print("Gif sent")
                        else:
                            print("Attempting to upload jpg")
                            upload = self.api.media_upload(filename = self.generated_media_location + output)
                            #self.api.update_status("From " + media.videoFileSelectedFileNameNoExtension + " at " + media.frameSelectedTime, 
                            #    media_ids=[upload.media_id_string])
                            print("JPG sent")

                        #self.api.chunked_upload(filename = self.generated_media_location + output, media_category = "tweet_gif")
                        #self.api.update_status(status="Hello :)")
                        return "Tweet sent. Check Twitter for new content"
            except Exception as e:
                return ("Error:  tweet not sent: ", str(e))

        def set(self, media):

            output = "output."
            if media.gifOrNo:
                output += "gif"
            else:
                output += "jpg"

            sendBack = self.tweet_media(media, output)
            return sendBack
