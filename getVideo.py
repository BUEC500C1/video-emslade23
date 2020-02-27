# References: https://code-maven.com/create-images-with-python-pil-pillow

import datetime
import time
import threading
import shutil
import subprocess
import os

import globalProcesses 
from getTweets import userTweets

#if no keys, then import default *****
shutil.copy('keys', 'keys.py')
from keys import *


def callback(userTweets):
    print("\n \n \n A thread for " + userTweets.twitterHandle + " has finished")

      
def threads(userTweets):
    globalProcesses.twitterQueue.put(userTweets)
    worker = threading.Thread(target=userTweets.getTweetDataAndCreateVideo())
    worker.setDaemon(True)
    worker.start()
    return worker   


def cleanPhotosFolder():
    result = subprocess.run('rm *', cwd="/Users/elizabeth./Documents/code/ec500/video-emslade23/photos")
    return result.stdout        


def main():
    # twitterHandles = []
    # numberOfTweetsArray = []
    # directoryNameArray = []
    # userInput = [""]
    
    # print("Hello, welcome to Lizzy's Twitter Video API!")
    # print("Directions: when you are done inputting Twitter Handles, type q")
    # while True:
    #     userInput = input("Please Input @twitterhandle, NumberOfTweets, folderName to create in current directory: \n (For Example: @elonmusk,10, muskVideo): ").split(',')
    #     if len(userInput) == 3:
    #         if userInput[0][0] != "@":
    #             print("Invalid Twitter Handle Structure. Try Again. \n \n")
    #         else:
    #             print("Your Input: "+ str(userInput))
    #             twitterHandles.append(userInput[0])
    #             numberOfTweetsArray.append(int(userInput[1]))
    #             directoryNameArray.append(userInput[2])
               
    #     elif userInput[0] == "q":
    #         break
    #     elif len(userInput) != 3:
    #         print("Your Input: "+ str(userInput))
    #         print("Incorrect, input exactly three arguments.\n \n \n")  
     
    globalProcesses.init()
    twitterHandle = '@elonmusk'
    directory = "photos4"
    userTweetsObj = userTweets(consumer_key, consumer_secret, access_token, access_token_secret, twitterHandle, 5, directory)
    worker = threads(userTweetsObj)
    
    twitterHandle = '@elizabeth'
    directory = "photos5"
    userTweetsObj = userTweets(consumer_key, consumer_secret, access_token, access_token_secret, twitterHandle, 5, directory)
    worker = threads(userTweetsObj)
    
    
    
    # stdout = userTweetsObj.cleanPhotosFolder() # this shit doesnt work

main()
