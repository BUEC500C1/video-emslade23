import tweepy
import PIL
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import subprocess
import time
import globalProcesses 
import os
import shutil

class userTweets:
    
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, twitterHandle, numberOfTweets, directory):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.twitterHandle = twitterHandle
        self.numberOfTweets = numberOfTweets
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.directory = directory
        self.textOfTweets = []
        self.imagesOfTweets = []
    
    def makeDirectory(self):
        if os.path.exists(self.directory):
            self.deletePhotosFolder()
            os.mkdir(self.directory)
        else:
            os.mkdir(self.directory)

    def getTweetDataAndCreateVideo(self):
        self.makeDirectory()
        self.getTweetData()
        self.createImagesofTweets()
        self.convertImagestoVideo()
        globalProcesses.twitterQueue.task_done()
        print("\n A thread for " + self.twitterHandle + " has completed. Path to video: " + os.getcwd() + "/" + self.directory + "\n")
        
    def getTweetData(self):
        # post is the entire element from api, tweet is the plain text tweet with links
        for post in tweepy.Cursor(self.api.user_timeline, screen_name=self.twitterHandle, tweet_mode="extended", include_entities=True).items(self.numberOfTweets):
            if( hasattr(post,'extended_entities')):
                for element in post.extended_entities['media']:
                    if(element['type'] == 'photo'):
                        self.imagesOfTweets.append(element['media_url_https'])
            else:
                self.imagesOfTweets.append('0')
            self.textOfTweets.append(post.full_text)
        print("Tweets: ", self.textOfTweets)
    
    def insertNewLines(self, tweet):
        if len(tweet) < 60:
            return tweet
        revisedTweet = ""
        
        for i in range(60, len(tweet), 60):
            revisedTweet = revisedTweet + tweet[i-60:i] + '\n' 
            if len(tweet)-i < 60:
                revisedTweet = revisedTweet + tweet[i:len(tweet)]
        return revisedTweet
    
    def createImagesofTweets(self):
        counter = 0
        indexArray = 0
        font = ImageFont.truetype("arial.ttf", 15)
        path = os.getcwd()
        for tweet in self.textOfTweets:
            revisedTweet = self.insertNewLines(tweet)
            
            img = Image.new('RGB', (500, 500), color = (0, 0, 0))
            d = ImageDraw.Draw(img)
            d.text((20,10), self.twitterHandle+":\n\n"+ revisedTweet, fill=(255,255,255), font=font)

            
            img.save(path+'/'+self.directory+'/frame'+str(counter)+'.png')
            counter += 1
            
            if self.imagesOfTweets[indexArray] != '0':
                response = requests.get(self.imagesOfTweets[indexArray])
                img = Image.open(BytesIO(response.content))
                img.save(path+'/'+self.directory+'/frame'+str(counter)+'.png')
                counter += 1
                indexArray += 1
        globalProcesses.twitterCompletedTasks[self.twitterHandle] = "50% Complete"
        print("**********************************")
        print("Current Status of all Threads:")
        for x in globalProcesses.twitterCompletedTasks:
            print(x+ ": "+ globalProcesses.twitterCompletedTasks[x])
        print("**********************************")
    
    def convertImagestoVideo(self):
        path = os.getcwd()
        result = subprocess.run('ffmpeg -r .3 -f image2 -s 1920x1080 -i frame%d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p test2.mp4', cwd=path+'/'+self.directory+'/')
        globalProcesses.twitterCompletedTasks[self.twitterHandle] = "100% Complete"
        print("**********************************")
        print("Current Status of all Processes:")
        for x in globalProcesses.twitterCompletedTasks:
            print(x+ ": "+ globalProcesses.twitterCompletedTasks[x])
        print("**********************************")
        return result.stdout
    
    def deletePhotosFolder(self):
        path = os.getcwd()
        shutil.rmtree(path+'/'+self.directory+'/')
        