# References: https://code-maven.com/create-images-with-python-pil-pillow

import PIL
from PIL import Image, ImageDraw, ImageFont
import datetime
import time
import tweepy
import config
import subprocess


auth = tweepy.OAuthHandler(config.consumerKey, config.consumerSecretKey)
auth.set_access_token(config.accessToken, config.accessSecretToken)
api = tweepy.API(auth)

def getTweetText(twitterHandle, numberOfTweets):
    tweetList = list()

    # post is the entire element from api, tweet is the plain text tweet with links
    for post in tweepy.Cursor(api.user_timeline, screen_name=twitterHandle, tweet_mode="extended").items(numberOfTweets):
        print(post.full_text)
        tweetList.append(post.full_text)
    #print("\n\n\n\n\n\n\n")
    return tweetList


def insertNewLines(tweet):
    if len(tweet) < 60:
        return tweet
    revisedTweet = ""
    
    for i in range(60, len(tweet), 60):
        #print("I: ",i)
        revisedTweet = revisedTweet + tweet[i-60:i] + '\n' 
        if len(tweet)-i < 60:
            revisedTweet = revisedTweet + tweet[i:len(tweet)]

    #print("REVISED: "+ revisedTweet)
    return revisedTweet


def createImagesOfTweets(twitterHandle, tweetList):
    counter = 0
    font = ImageFont.truetype("arial.ttf", 15)
    for tweet in tweetList:
        revisedTweet = insertNewLines(tweet)
        
        img = Image.new('RGB', (500, 500), color = (0, 0, 0))
        d = ImageDraw.Draw(img)
        d.text((20,10), twitterHandle+":\n\n"+revisedTweet, fill=(255,255,255), font=font)

        img.save('/Users/elizabeth./Documents/code/ec500/video-emslade23/photos/frame'+str(counter)+'.png')
        counter += 1

def convertImagestoVideo():
    subprocess.run('ffmpeg -r .3 -f image2 -s 1920x1080 -i frame%d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4')

def main():
    twitterHandle = '@elonmusk'
    results = getTweetText(twitterHandle, 1)
    time.sleep(2)
    createImagesOfTweets(twitterHandle, results)
   # convertImagestoVideo()
    print(subprocess.run('cd photos').stdout)

main()

# ffmpeg -r 1 -f image2 -s 1920x1080 -i frame%d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4