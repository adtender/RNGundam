import tweepy
import os
import config


class TWEET:

        def __init__(self):
                self.api_key = config.API_Key
                self.api_key_secret = config.API_Key_Secret
                self.access_token = config.Access_Token
                self.access_token_secret = config.Access_Token_Secret
                self.auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
                self.auth.set_access_token(self.access_token, self.access_token_secret)
                self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
                self.media_location = os.path.expanduser(config.Media_Location)
                self.generated_media_location = os.path.expanduser(config.Generated_Media_Location)

        def tweet_media(self, media, output, arg):
            
            if len(arg) > 1:
                arg = str(arg[1])
            else:
                arg = ""
            
            def send_gif(arg):
                print("Attempt to upload gif")
                upload = self.api.media_upload(filename = self.generated_media_location + output, 
                    chunked = True, 
                    media_category = "tweet_gif")
                self.api.update_status(arg + "\nFrom " + media.videoFileSelectedFileNameNoExtension + " at " + media.frameSelectedTime, 
                    media_ids=[upload.media_id_string])
                print("Gif sent")
            def send_jpg(arg):
                print("Attempting to upload jpg")
                upload = self.api.media_upload(filename = self.generated_media_location + output)
                self.api.update_status(arg + "\nFrom " + media.videoFileSelectedFileNameNoExtension + " at " + media.frameSelectedTime, 
                    media_ids=[upload.media_id_string])
                print("JPG sent")
                
            try:
                if "gif" in output:
                    send_gif(arg)
                else:
                    send_jpg(arg)
                            
                return "Tweet sent. Check Twitter for new content"
            except Exception as e:
                return ("Error:  tweet not sent: ", str(e))
            
            

        def set(self, media, arg):

            output = "output."
            if media.gifOrNo:
                output += "gif"
            else:
                output += "jpg"

            sendBack = self.tweet_media(media, output, arg)
            return sendBack
