# References: https://code-maven.com/create-images-with-python-pil-pillow

import PIL
from PIL import Image, ImageDraw, ImageFont
import datetime
import time
import tweepy
import queue
import subprocess
import threading
import requests
import shutil
from io import BytesIO

shutil.copy('keys', 'keys.py')
from keys import *

q = queue.Queue()

auth = tweepy.OAuthHandler(consumerKey, consumerSecretKey)
auth.set_access_token(accessToken, accessSecretToken)
api = tweepy.API(auth)

# twitter api
def getTweetText(twitterHandle, numberOfTweets):
    textOfTweets = list()
    imgsOfTweets = list()

    # post is the entire element from api, tweet is the plain text tweet with links
    for post in tweepy.Cursor(api.user_timeline, screen_name=twitterHandle, tweet_mode="extended", include_entities=True).items(numberOfTweets):
        if( hasattr(post,'extended_entities')):
            for element in post.extended_entities['media']:
                if(element['type'] == 'photo'):
                    imgsOfTweets.append(element['media_url_https'])
        else:
            imgsOfTweets.append('0')
        print(post.full_text)
        textOfTweets.append(post.full_text)
    return [textOfTweets, imgsOfTweets]

# queue
def callback(foo):
    print("A thread for " + str(foo) + " has finished")


def get_feed(twitterFeed, callback): # for each twitter handle, we must add the task of getting their tweets to the queue
    while True:
        twitterFeedList = q.get()
        #print(" feed: ", twitterFeedList)
        createImagesOfTweets(twitterFeedList)
        time.sleep(0.5)
        q.task_done()
        callback(twitterFeedList)


def queue_module(twitterHandle, textOfTweets, imagesOfTweets):
    print("q module")
    twitterFeedList = twitterHandle, textOfTweets, imagesOfTweets
    print(twitterFeedList)
    q.put(twitterFeedList)
    worker = threading.Thread(target=get_feed, args=(1, callback))
    worker.setDaemon(True)
    worker.start()


def addFeedToQueue(twitterHandle, textOfTweets):
    print("adding feed to q")
    imagesOfTweets =  ['images', 'hello']
    queue_module(twitterHandle, textOfTweets, imagesOfTweets)


def insertNewLines(tweet):
    if len(tweet) < 60:
        return tweet
    revisedTweet = ""
    
    for i in range(60, len(tweet), 60):
        revisedTweet = revisedTweet + tweet[i-60:i] + '\n' 
        if len(tweet)-i < 60:
            revisedTweet = revisedTweet + tweet[i:len(tweet)]

    #print("REVISED: "+ revisedTweet)
    return revisedTweet

def createImagesOfTweets(twitterHandle, textOfTweets, imgsOfTweets):
    counter = 0
    indexArray = 0
    font = ImageFont.truetype("arial.ttf", 15)
    for tweet in textOfTweets:
        revisedTweet = insertNewLines(tweet)
        
        img = Image.new('RGB', (500, 500), color = (0, 0, 0))
        d = ImageDraw.Draw(img)
        d.text((20,10), twitterHandle+":\n\n"+revisedTweet, fill=(255,255,255), font=font)

        img.save('/Users/elizabeth./Documents/code/ec500/video-emslade23/photos/frame'+str(counter)+'.png')
        counter += 1
        if imgsOfTweets[indexArray] != '0':
            #print('yoooo')
            response = requests.get(imgsOfTweets[indexArray])
            img = Image.open(BytesIO(response.content))
            img.save('/Users/elizabeth./Documents/code/ec500/video-emslade23/photos/frame'+str(counter)+'.png')
            counter += 1
        indexArray += 1

def convertImagestoVideo():
    #print(subprocess.run('ls').stdout)
    result = subprocess.run('ffmpeg -r .3 -f image2 -s 1920x1080 -i frame%d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p test2.mp4', cwd="/Users/elizabeth./Documents/code/ec500/video-emslade23/photos")
    return result.stdout

def cleanPhotos():
    result = subprocess.run('rm *', cwd="/Users/elizabeth./Documents/code/ec500/video-emslade23/photos")

def main():
    twitterHandle = '@realDonaldTrump'
    textOfTweets, imgsOfTweets = getTweetText(twitterHandle, 7) # eventually returns 2 things tweet text and image tweets
    #print(textOfTweets)
    #print(imgsOfTweets)
    createImagesOfTweets(twitterHandle, textOfTweets, imgsOfTweets)

    stdout = convertImagestoVideo()

main()
